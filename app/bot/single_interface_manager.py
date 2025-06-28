import logging
import asyncio
from typing import Dict, List, Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from app.config import settings
from app.bot.handlers import BotHandlers

logger = logging.getLogger(__name__)


class SingleInterfaceBotManager:
    """
    Single Interface Bot Manager
    
    Architecture:
    - Users interact with ONE bot (@your_main_bot)
    - Behind the scenes, 17 tokens handle the responses
    - Load balancing distributes users across tokens
    - Users never know they're talking to different backend tokens
    """
    
    def __init__(self):
        self.main_application: Optional[Application] = None  # Main bot that receives webhooks
        self.response_bots: Dict[str, Bot] = {}  # Backend bots for sending responses
        self.handlers = None
        self.primary_token = settings.get_primary_token()
        self.all_tokens = settings.active_bot_tokens
    
    @property
    def active_bots(self) -> List[Bot]:
        """Compatibility property for handlers - returns main bot in a list"""
        if self.main_application and self.main_application.bot:
            return [self.main_application.bot]
        return []
        
    async def initialize(self) -> None:
        """Initialize the single interface bot system"""
        logger.info("🚀 Initializing SINGLE INTERFACE mode...")
        logger.info(f"📱 Main bot interface: {self.primary_token[:10]}...")
        logger.info(f"⚡ Backend response tokens: {len(self.all_tokens)} tokens")
        logger.info(f"🎯 Total capacity: {len(self.all_tokens) * 30} messages/second")
        
        # Initialize main bot that receives all webhooks
        await self._create_main_bot()
        
        # Initialize all response bots for load balancing
        await self._create_response_bots()
        
        logger.info("✅ Single Interface Bot Manager initialized successfully!")
    
    async def _create_main_bot(self) -> None:
        """Create the main bot that receives webhooks"""
        try:
            logger.info("🤖 Creating main bot interface...")
            
            # Create application for main bot
            self.main_application = Application.builder().token(self.primary_token).build()
            
            # Create handlers
            self.handlers = BotHandlers(0, bot_manager=self, application=self.main_application)  # Pass self for response routing
            
            # Add handlers to main application
            self.main_application.add_handler(CommandHandler("start", self.handlers.start_command))
            self.main_application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
            self.main_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.text_message))
            
            # Initialize application
            await self.main_application.initialize()
            
            logger.info(f"✅ Main bot interface created: {self.primary_token[:10]}...")
            
        except Exception as e:
            logger.error(f"❌ Failed to create main bot: {e}")
            raise
    
    async def _create_response_bots(self) -> None:
        """Create backend bots for sending responses"""
        try:
            logger.info("⚡ Creating backend response bots...")
            
            for i, token in enumerate(self.all_tokens):
                # Create bot instance (not full application, just bot)
                bot = Bot(token=token)
                self.response_bots[token] = bot
                
                logger.info(f"   Bot {i}: {token[:10]}... ✅")
            
            logger.info(f"✅ Created {len(self.response_bots)} backend response bots")
            
        except Exception as e:
            logger.error(f"❌ Failed to create response bots: {e}")
            raise
    
    async def get_response_bot(self, user_id: int) -> Bot:
        """Get the appropriate bot for responding to a user"""
        response_token = settings.get_response_token(user_id)
        return self.response_bots[response_token]
    
    async def send_message(self, chat_id: int, text: str, **kwargs) -> None:
        """Send message using load-balanced bot"""
        try:
            response_bot = await self.get_response_bot(chat_id)
            await response_bot.send_message(chat_id=chat_id, text=text, **kwargs)
            
            # Log which backend token was used
            token_index = chat_id % len(self.all_tokens)
            logger.debug(f"📤 Message sent via backend bot {token_index} to user {chat_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to {chat_id}: {e}")
            # Fallback to main bot
            try:
                await self.main_application.bot.send_message(chat_id=chat_id, text=text, **kwargs)
                logger.info(f"✅ Fallback: Message sent via main bot to user {chat_id}")
            except Exception as fallback_error:
                logger.error(f"❌ Fallback also failed for user {chat_id}: {fallback_error}")
                raise
    
    async def edit_message_text(self, chat_id: int, message_id: int, text: str, **kwargs) -> None:
        """Edit message using load-balanced bot"""
        try:
            response_bot = await self.get_response_bot(chat_id)
            await response_bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id, 
                text=text, 
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to edit message for {chat_id}: {e}")
            # Fallback to main bot
            try:
                await self.main_application.bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=message_id, 
                    text=text, 
                    **kwargs
                )
            except Exception as fallback_error:
                logger.error(f"❌ Edit message fallback failed for user {chat_id}: {fallback_error}")
                raise
    
    async def answer_callback_query(self, callback_query_id: str, text: str = None, **kwargs) -> None:
        """Answer callback query using main bot"""
        try:
            await self.main_application.bot.answer_callback_query(
                callback_query_id=callback_query_id,
                text=text,
                **kwargs
            )
        except Exception as e:
            logger.error(f"❌ Failed to answer callback query {callback_query_id}: {e}")
            raise
    
    async def process_update(self, update_data: dict) -> None:
        """Process incoming update through main bot"""
        try:
            if not self.main_application:
                logger.error("❌ Main application not initialized")
                return
            
            # Parse update using main bot
            update = Update.de_json(update_data, self.main_application.bot)
            
            if update:
                # Process through main application
                await self.main_application.process_update(update)
                
                # Log user info for monitoring
                user_id = None
                if update.message:
                    user_id = update.message.from_user.id
                elif update.callback_query:
                    user_id = update.callback_query.from_user.id
                
                if user_id:
                    backend_index = user_id % len(self.all_tokens)
                    logger.debug(f"📥 Update from user {user_id} (backend: {backend_index})")
            
        except Exception as e:
            logger.error(f"❌ Error processing update: {e}")
    
    async def get_stats(self) -> dict:
        """Get bot statistics"""
        return {
            "mode": "single_interface",
            "main_bot_token": self.primary_token[:10] + "...",
            "backend_bots": len(self.response_bots),
            "total_capacity_per_second": len(self.all_tokens) * 30,
            "load_balancing": "user_id % tokens",
            "webhook_endpoint": "single (/webhook)",
            "user_experience": "single_bot_interface",
            "backend_distribution": f"{len(self.all_tokens)} tokens"
        }
    
    async def health_check(self) -> dict:
        """Check health of all bots"""
        health = {
            "main_bot": "unknown",
            "backend_bots": {},
            "total_healthy": 0
        }
        
        # Check main bot
        try:
            me = await self.main_application.bot.get_me()
            health["main_bot"] = "healthy"
            health["main_bot_info"] = {
                "username": me.username,
                "first_name": me.first_name,
                "id": me.id
            }
        except Exception as e:
            health["main_bot"] = f"error: {str(e)}"
        
        # Check backend bots
        healthy_count = 0
        for i, (token, bot) in enumerate(self.response_bots.items()):
            try:
                await bot.get_me()
                health["backend_bots"][f"bot_{i}"] = "healthy"
                healthy_count += 1
            except Exception as e:
                health["backend_bots"][f"bot_{i}"] = f"error: {str(e)}"
        
        health["total_healthy"] = healthy_count
        health["health_percentage"] = (healthy_count / len(self.response_bots)) * 100
        
        return health
    
    async def shutdown(self) -> None:
        """Shutdown the bot manager"""
        logger.info("🔄 Shutting down Single Interface Bot Manager...")
        
        # Shutdown main application
        if self.main_application:
            try:
                await self.main_application.shutdown()
                logger.info("✅ Main bot application shut down")
            except Exception as e:
                logger.error(f"❌ Error shutting down main application: {e}")
        
        # Clear response bots
        self.response_bots.clear()
        
        logger.info("✅ Single Interface Bot Manager shut down complete")