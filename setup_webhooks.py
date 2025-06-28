#!/usr/bin/env python3
"""
Script to set up webhooks for all bot tokens
Run this after deploying to Render.com
"""

import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot tokens
BOT_TOKENS = [
    "5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM",  # Main token
    "7199941836:AAGc4YhuG93HgSYWYNVUbdf3VsqkF2Nhl9U",
    "6895814597:AAHtDIi6GGMWN_G9hvg-QmIcB5iX_aNm8WA",
    "7005162458:AAHBRGZWdpscVzccmXGBkJCgjQ5xrDimS0Q",
    "6475702281:AAHIZIhiA4OY52WRBziRBrwrzRLRtl2OXzg",
    "7675746275:AAHu25CkfZP7KSE4SADObkm9-xrbYxflU48",
    "7435789657:AAHsrY-e6X9hmpRfDNhN1RJRREjYOz4xrq0",
    "7404095541:AAE9vfkvXxlxqmX21XgAs8Kz8ZG5d5j3Ujg",
    "6537125068:AAGvZgiVm1qRofumnwFnJ7_YIKd9AemehUs",
    "7645073760:AAEfGPb6VaCDDzHw6w7dPSpX5tu3FzgoT7M",
    "6636093163:AAFkebglqvrIOmZUfbqVqiKoBZc02sjW9a8",
    "6499811600:AAFzLLBG8tCxW2hXyoZCjsuHpL3Unh6VvGk",
    "7811073864:AAFHaqMyKR6y1q3B1cqJ7aMy-nzimDEdrnU",
    "6387793169:AAHX6e1QJWdMeizxRUOrBw-tcVSHGu4jzos",
    "7865730193:AAGfzgensrHnK9_NFnGYh-jEYtGihkNBJ9M",
    "7595720964:AAF4yBfn36wuyfbDjMVk54fTQvAOGvr_8MA",
    "7899892308:AAHUN4raPCRY_Sje9CfJw0cVloypNjoiIzQ"
]

# Your Render.com URL (replace with your actual URL)
RENDER_URL = "https://your-app-name.onrender.com"


async def set_webhook(session: aiohttp.ClientSession, token: str, shard_id: int) -> bool:
    """Set webhook for a single bot token"""
    webhook_url = f"{RENDER_URL}/webhook/{shard_id}"
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
                logger.info(f"✅ Webhook set for shard {shard_id}: {webhook_url}")
                return True
            else:
                logger.error(f"❌ Failed to set webhook for shard {shard_id}: {result}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error setting webhook for shard {shard_id}: {e}")
        return False


async def get_webhook_info(session: aiohttp.ClientSession, token: str, shard_id: int) -> None:
    """Get webhook info for a bot token"""
    telegram_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        async with session.get(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                webhook_info = result.get("result", {})
                url = webhook_info.get("url", "Not set")
                pending_updates = webhook_info.get("pending_update_count", 0)
                last_error = webhook_info.get("last_error_message", "None")
                
                logger.info(f"📊 Shard {shard_id}:")
                logger.info(f"   URL: {url}")
                logger.info(f"   Pending: {pending_updates}")
                logger.info(f"   Last error: {last_error}")
            else:
                logger.error(f"❌ Failed to get webhook info for shard {shard_id}: {result}")
                
    except Exception as e:
        logger.error(f"❌ Error getting webhook info for shard {shard_id}: {e}")


async def delete_webhook(session: aiohttp.ClientSession, token: str, shard_id: int) -> bool:
    """Delete webhook for a bot token"""
    telegram_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    
    try:
        async with session.post(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                logger.info(f"🗑️ Webhook deleted for shard {shard_id}")
                return True
            else:
                logger.error(f"❌ Failed to delete webhook for shard {shard_id}: {result}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error deleting webhook for shard {shard_id}: {e}")
        return False


async def setup_all_webhooks(render_url: str = None) -> None:
    """Set up webhooks for all bot tokens"""
    global RENDER_URL
    
    if render_url:
        RENDER_URL = render_url
    
    if "your-app-name" in RENDER_URL:
        logger.error("❌ Please update RENDER_URL in the script with your actual Render.com URL!")
        return
    
    async with aiohttp.ClientSession() as session:
        logger.info(f"🚀 Setting up webhooks for {len(BOT_TOKENS)} bot tokens...")
        logger.info(f"📡 Render URL: {RENDER_URL}")
        
        success_count = 0
        
        for i, token in enumerate(BOT_TOKENS):
            success = await set_webhook(session, token, i)
            if success:
                success_count += 1
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        logger.info(f"✅ Successfully set up {success_count}/{len(BOT_TOKENS)} webhooks")
        
        # Wait a bit then check webhook status
        logger.info("🔍 Checking webhook status...")
        await asyncio.sleep(2)
        
        for i, token in enumerate(BOT_TOKENS):
            await get_webhook_info(session, token, i)
            await asyncio.sleep(0.3)


async def delete_all_webhooks() -> None:
    """Delete all webhooks (useful for testing)"""
    async with aiohttp.ClientSession() as session:
        logger.info(f"🗑️ Deleting webhooks for {len(BOT_TOKENS)} bot tokens...")
        
        for i, token in enumerate(BOT_TOKENS):
            await delete_webhook(session, token, i)
            await asyncio.sleep(0.5)


async def check_webhook_status() -> None:
    """Check status of all webhooks"""
    async with aiohttp.ClientSession() as session:
        logger.info(f"🔍 Checking webhook status for {len(BOT_TOKENS)} bot tokens...")
        
        for i, token in enumerate(BOT_TOKENS):
            await get_webhook_info(session, token, i)
            await asyncio.sleep(0.3)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            render_url = sys.argv[2] if len(sys.argv) > 2 else None
            asyncio.run(setup_all_webhooks(render_url))
        elif command == "delete":
            asyncio.run(delete_all_webhooks())
        elif command == "status":
            asyncio.run(check_webhook_status())
        else:
            print("Usage:")
            print("  python setup_webhooks.py setup [render_url]")
            print("  python setup_webhooks.py delete")
            print("  python setup_webhooks.py status")
    else:
        print("Usage:")
        print("  python setup_webhooks.py setup https://your-app.onrender.com")
        print("  python setup_webhooks.py delete")
        print("  python setup_webhooks.py status")