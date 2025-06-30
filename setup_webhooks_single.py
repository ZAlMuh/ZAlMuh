#!/usr/bin/env python3
"""
Script to set up webhook for SINGLE BOT mode
Only the main bot token gets a webhook, others are backup
"""

import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your MAIN bot token (only this one will have webhook)
MAIN_BOT_TOKEN = "5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM"

# Your Render.com URL (replace with your actual URL)
RENDER_URL = "https://your-app-name.onrender.com"


async def set_webhook_single_bot(session: aiohttp.ClientSession, token: str, webhook_url: str) -> bool:
    """Set webhook for the main bot token"""
    telegram_url = f"https://api.telegram.org/bot{token}/setWebhook"
    
    payload = {
        "url": webhook_url,
        "max_connections": 100,
        "allowed_updates": ["message", "callback_query"]
    }
    
    try:
        async with session.post(telegram_url, json=payload) as response:
            result = await response.json()
            
            if result.get("ok"):
                logger.info(f"✅ Webhook set for main bot: {webhook_url}")
                return True
            else:
                logger.error(f"❌ Failed to set webhook for main bot: {result}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error setting webhook for main bot: {e}")
        return False


async def get_webhook_info(session: aiohttp.ClientSession, token: str) -> None:
    """Get webhook info for the bot token"""
    telegram_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        async with session.get(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                webhook_info = result.get("result", {})
                url = webhook_info.get("url", "Not set")
                pending_updates = webhook_info.get("pending_update_count", 0)
                last_error = webhook_info.get("last_error_message", "None")
                
                logger.info(f"📊 Main Bot Status:")
                logger.info(f"   URL: {url}")
                logger.info(f"   Pending: {pending_updates}")
                logger.info(f"   Last error: {last_error}")
            else:
                logger.error(f"❌ Failed to get webhook info: {result}")
                
    except Exception as e:
        logger.error(f"❌ Error getting webhook info: {e}")


async def delete_webhook(session: aiohttp.ClientSession, token: str) -> bool:
    """Delete webhook for the bot token"""
    telegram_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    try:
        async with session.post(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                logger.info(f"🗑️ Webhook deleted for main bot")
                return True
            else:
                logger.error(f"❌ Failed to delete webhook: {result}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error deleting webhook: {e}")
        return False


async def setup_single_bot_webhook(render_url: str = None) -> None:
    """Set up webhook for single bot mode"""
    global RENDER_URL
    
    if render_url:
        RENDER_URL = render_url
    
    if "your-app-name" in RENDER_URL:
        logger.error("❌ Please update RENDER_URL in the script with your actual Render.com URL!")
        return
    
    # Single webhook endpoint for single bot mode
    webhook_url = f"{RENDER_URL}/webhook"
    
    async with aiohttp.ClientSession() as session:
        logger.info("🚀 Setting up webhook for SINGLE BOT mode...")
        logger.info(f"📡 Main Bot Token: {MAIN_BOT_TOKEN[:10]}...")
        logger.info(f"📡 Webhook URL: {webhook_url}")
        
        success = await set_webhook_single_bot(session, MAIN_BOT_TOKEN, webhook_url)
        
        if success:
            logger.info("✅ Successfully set up single bot webhook!")
        else:
            logger.error("❌ Failed to set up webhook")
            return
        
        # Wait a bit then check webhook status
        logger.info("🔍 Checking webhook status...")
        await asyncio.sleep(2)
        await get_webhook_info(session, MAIN_BOT_TOKEN)
        
        logger.info("\n🎯 SINGLE BOT MODE SETUP:")
        logger.info("• All users will connect to the MAIN bot")
        logger.info("• Backup tokens are available for failover")
        logger.info("• Maximum capacity: ~30 messages/second")
        logger.info("• Recommended for up to 10,000-15,000 users")


async def delete_single_bot_webhook() -> None:
    """Delete webhook for single bot mode"""
    async with aiohttp.ClientSession() as session:
        logger.info("🗑️ Deleting webhook for main bot...")
        await delete_webhook(session, MAIN_BOT_TOKEN)


async def check_single_bot_status() -> None:
    """Check status of main bot webhook"""
    async with aiohttp.ClientSession() as session:
        logger.info("🔍 Checking main bot webhook status...")
        await get_webhook_info(session, MAIN_BOT_TOKEN)


async def get_bot_info(session: aiohttp.ClientSession, token: str) -> None:
    """Get bot information"""
    telegram_url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        async with session.get(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                bot_info = result.get("result", {})
                username = bot_info.get("username", "Unknown")
                first_name = bot_info.get("first_name", "Unknown")
                
                logger.info(f"🤖 Bot Info:")
                logger.info(f"   Name: {first_name}")
                logger.info(f"   Username: @{username}")
                logger.info(f"   ID: {bot_info.get('id', 'Unknown')}")
            else:
                logger.error(f"❌ Failed to get bot info: {result}")
                
    except Exception as e:
        logger.error(f"❌ Error getting bot info: {e}")


async def show_bot_info() -> None:
    """Show main bot information"""
    async with aiohttp.ClientSession() as session:
        logger.info("🤖 Getting main bot information...")
        await get_bot_info(session, MAIN_BOT_TOKEN)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            render_url = sys.argv[2] if len(sys.argv) > 2 else None
            asyncio.run(setup_single_bot_webhook(render_url))
        elif command == "delete":
            asyncio.run(delete_single_bot_webhook())
        elif command == "status":
            asyncio.run(check_single_bot_status())
        elif command == "info":
            asyncio.run(show_bot_info())
        else:
            print("Usage:")
            print("  python setup_webhooks_single.py setup [render_url]")
            print("  python setup_webhooks_single.py delete")
            print("  python setup_webhooks_single.py status")
            print("  python setup_webhooks_single.py info")
    else:
        print("📱 Single Bot Mode Webhook Setup")
        print("="*40)
        print("Usage:")
        print("  python setup_webhooks_single.py setup https://your-app.onrender.com")
        print("  python setup_webhooks_single.py delete")
        print("  python setup_webhooks_single.py status")
        print("  python setup_webhooks_single.py info")
        print("")
        print("🎯 Single Bot Mode:")
        print("• Only MAIN bot token receives webhook")
        print("• All 100K users connect to one bot")
        print("• Backup tokens available for failover")
        print("• Simpler architecture, easier management")