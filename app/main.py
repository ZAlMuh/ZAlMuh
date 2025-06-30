import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from app.config import settings
from app.bot.handlers import TelegramBotManager
from app.bot.single_interface_manager import SingleInterfaceBotManager
from app.external.cache import redis_cache
from app.database.supabase_client import supabase_client

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Arabic Telegram Bot application...")
    
    # Initialize Redis connection
    await redis_cache.connect()
    
    # Initialize bot manager based on mode
    if settings.bot_mode == "single_interface":
        logger.info("🚀 Starting in SINGLE INTERFACE mode")
        bot_manager = SingleInterfaceBotManager()
    else:
        logger.info("🚀 Starting in MULTI-BOT mode")
        bot_manager = TelegramBotManager()
    
    await bot_manager.initialize()
    
    # Store bot manager in app state
    app.state.bot_manager = bot_manager
    
    logger.info("Application startup complete")
    
    yield
    
    # Cleanup
    logger.info("Shutting down application...")
    await redis_cache.disconnect()
    await bot_manager.shutdown()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Arabic Telegram Bot",
    description="Scalable Arabic exam results bot for 100K users",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Arabic Telegram Bot is running",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    health_status = {
        "api": "healthy",
        "redis": "unknown",
        "database": "unknown",
        "bots": "unknown"
    }
    
    # Check Redis
    try:
        if redis_cache.redis:
            await redis_cache.redis.ping()
            health_status["redis"] = "healthy"
        else:
            health_status["redis"] = "disconnected"
    except Exception as e:
        health_status["redis"] = f"error: {str(e)}"
    
    # Check database
    try:
        # Simple query to test database connection
        result = supabase_client.client.table("students").select("count").limit(1).execute()
        health_status["database"] = "healthy"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
    
    # Check bot manager
    try:
        if hasattr(app.state, 'bot_manager'):
            bot_count = len(app.state.bot_manager.active_bots)
            health_status["bots"] = f"active: {bot_count}"
        else:
            health_status["bots"] = "not_initialized"
    except Exception as e:
        health_status["bots"] = f"error: {str(e)}"
    
    return health_status


@app.post("/webhook/{shard_id}")
async def webhook_handler(shard_id: int, request: Request):
    """Handle incoming webhook requests"""
    try:
        if not hasattr(app.state, 'bot_manager'):
            raise HTTPException(status_code=503, detail="Bot manager not initialized")
        
        # Get request body
        update_data = await request.json()
        
        # Process update through bot manager
        # In single bot mode, all webhooks route to the primary bot
        await app.state.bot_manager.process_update(shard_id, update_data)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook for shard {shard_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/webhook")
async def webhook_handler_single(request: Request):
    """Handle incoming webhook requests for single interface mode"""
    try:
        if not hasattr(app.state, 'bot_manager'):
            raise HTTPException(status_code=503, detail="Bot manager not initialized")
        
        # Get request body
        update_data = await request.json()
        
        # Check if we're in single interface mode
        if hasattr(app.state.bot_manager, 'process_update'):
            # Single interface mode - direct processing
            await app.state.bot_manager.process_update(update_data)
        else:
            # Fallback to traditional mode
            await app.state.bot_manager.process_update(0, update_data)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/stats")
async def get_stats():
    """Get bot statistics"""
    try:
        if not hasattr(app.state, 'bot_manager'):
            return {"error": "Bot manager not initialized"}
        
        stats = await app.state.bot_manager.get_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": str(e)}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
        reload=settings.environment == "development"
    )