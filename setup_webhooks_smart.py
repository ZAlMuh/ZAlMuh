#!/usr/bin/env python3
"""
Smart Webhook Setup for Single Interface Mode

This script sets up ONE webhook for the main bot interface,
while all 17 tokens work behind the scenes for load balancing.

Architecture:
- Users see: ONE bot interface (@your_main_bot)
- Backend: 17 tokens handle responses (load balanced)
- Webhook: Only main bot receives webhooks
- Capacity: 17 × 30 = 510 messages/second total
"""

import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your MAIN bot token (the face of your bot)
MAIN_BOT_TOKEN = "5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM"

# All tokens (main + 16 backup tokens for backend processing)
ALL_TOKENS = [
    "5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM",  # Main (interface)
    "7199941836:AAGc4YhuG93HgSYWYNVUbdf3VsqkF2Nhl9U",  # Backend 1
    "6895814597:AAHtDIi6GGMWN_G9hvg-QmIcB5iX_aNm8WA",  # Backend 2
    "7005162458:AAHBRGZWdpscVzccmXGBkJCgjQ5xrDimS0Q",  # Backend 3
    "6475702281:AAHIZIhiA4OY52WRBziRBrwrzRLRtl2OXzg",  # Backend 4
    "7675746275:AAHu25CkfZP7KSE4SADObkm9-xrbYxflU48",  # Backend 5
    "7435789657:AAHsrY-e6X9hmpRfDNhN1RJRREjYOz4xrq0",  # Backend 6
    "7404095541:AAE9vfkvXxlxqmX21XgAs8Kz8ZG5d5j3Ujg",  # Backend 7
    "6537125068:AAGvZgiVm1qRofumnwFnJ7_YIKd9AemehUs",  # Backend 8
    "7645073760:AAEfGPb6VaCDDzHw6w7dPSpX5tu3FzgoT7M",  # Backend 9
    "6636093163:AAFkebglqvrIOmZUfbqVqiKoBZc02sjW9a8",  # Backend 10
    "6499811600:AAFzLLBG8tCxW2hXyoZCjsuHpL3Unh6VvGk",  # Backend 11
    "7811073864:AAFHaqMyKR6y1q3B1cqJ7aMy-nzimDEdrnU",  # Backend 12
    "6387793169:AAHX6e1QJWdMeizxRUOrBw-tcVSHGu4jzos",  # Backend 13
    "7865730193:AAGfzgensrHnK9_NFnGYh-jEYtGihkNBJ9M",  # Backend 14
    "7595720964:AAF4yBfn36wuyfbDjMVk54fTQvAOGvr_8MA",  # Backend 15
    "7899892308:AAHUN4raPCRY_Sje9CfJw0cVloypNjoiIzQ"   # Backend 16
]

# Your Render.com URL
RENDER_URL = "https://your-app-name.onrender.com"


async def setup_single_interface_webhook(session: aiohttp.ClientSession, render_url: str) -> bool:
    """Set up webhook for single interface mode"""
    webhook_url = f"{render_url}/webhook"
    telegram_url = f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/setWebhook"
    
    payload = {
        "url": webhook_url,
        "max_connections": 100,
        "allowed_updates": ["message", "callback_query"]
    }
    
    try:
        async with session.post(telegram_url, json=payload) as response:
            result = await response.json()
            
            if result.get("ok"):
                logger.info(f"✅ Main bot webhook set: {webhook_url}")
                return True
            else:
                logger.error(f"❌ Failed to set main bot webhook: {result}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error setting main bot webhook: {e}")
        return False


async def clear_all_webhooks(session: aiohttp.ClientSession) -> None:
    """Clear webhooks from all tokens (cleanup)"""
    logger.info("🧹 Clearing webhooks from all tokens...")
    
    for i, token in enumerate(ALL_TOKENS):
        try:
            telegram_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
            async with session.post(telegram_url) as response:
                result = await response.json()
                
                if result.get("ok"):
                    logger.info(f"   Token {i}: Webhook cleared ✅")
                else:
                    logger.warning(f"   Token {i}: Clear failed - {result}")
                    
        except Exception as e:
            logger.error(f"   Token {i}: Error clearing webhook - {e}")
        
        await asyncio.sleep(0.2)  # Avoid rate limiting


async def get_all_bot_info(session: aiohttp.ClientSession) -> None:
    """Get information about all bots"""
    logger.info("🤖 Getting bot information...")
    
    for i, token in enumerate(ALL_TOKENS):
        try:
            telegram_url = f"https://api.telegram.org/bot{token}/getMe"
            async with session.get(telegram_url) as response:
                result = await response.json()
                
                if result.get("ok"):
                    bot_info = result["result"]
                    role = "MAIN INTERFACE" if i == 0 else f"BACKEND {i}"
                    logger.info(f"   {role}: @{bot_info.get('username', 'unknown')} - {bot_info.get('first_name', 'Unknown')}")
                else:
                    logger.error(f"   Token {i}: Failed to get info - {result}")
                    
        except Exception as e:
            logger.error(f"   Token {i}: Error getting info - {e}")
        
        await asyncio.sleep(0.2)


async def verify_single_interface_setup(session: aiohttp.ClientSession) -> None:
    """Verify the single interface setup"""
    logger.info("🔍 Verifying single interface setup...")
    
    # Check main bot webhook
    try:
        telegram_url = f"https://api.telegram.org/bot{MAIN_BOT_TOKEN}/getWebhookInfo"
        async with session.get(telegram_url) as response:
            result = await response.json()
            
            if result.get("ok"):
                webhook_info = result["result"]
                url = webhook_info.get("url", "Not set")
                pending = webhook_info.get("pending_update_count", 0)
                
                logger.info(f"📱 Main Bot Webhook:")
                logger.info(f"   URL: {url}")
                logger.info(f"   Pending Updates: {pending}")
                
                if url and "webhook" in url:
                    logger.info("   ✅ Webhook correctly configured")
                else:
                    logger.warning("   ⚠️ Webhook not properly set")
            else:
                logger.error(f"   ❌ Failed to get webhook info: {result}")
                
    except Exception as e:
        logger.error(f"❌ Error verifying setup: {e}")
    
    # Check that backend bots have no webhooks
    backend_with_webhooks = 0
    for i, token in enumerate(ALL_TOKENS[1:], 1):  # Skip main token
        try:
            telegram_url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
            async with session.get(telegram_url) as response:
                result = await response.json()
                
                if result.get("ok"):
                    webhook_info = result["result"]
                    url = webhook_info.get("url", "")
                    
                    if url:
                        backend_with_webhooks += 1
                        logger.warning(f"   ⚠️ Backend bot {i} has webhook: {url}")
                        
        except Exception:
            pass
        
        await asyncio.sleep(0.1)
    
    if backend_with_webhooks == 0:
        logger.info("   ✅ All backend bots correctly have no webhooks")
    else:
        logger.warning(f"   ⚠️ {backend_with_webhooks} backend bots have webhooks (should be cleared)")


async def main():
    """Main function for single interface setup"""
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 Single Interface Webhook Setup")
        print("="*50)
        print("This sets up ONE bot interface with 17 backend tokens")
        print("")
        print("Usage:")
        print("  python setup_webhooks_smart.py setup https://your-app.onrender.com")
        print("  python setup_webhooks_smart.py clear")
        print("  python setup_webhooks_smart.py info")
        print("  python setup_webhooks_smart.py verify")
        print("")
        print("🎯 Architecture:")
        print("• Users interact with: MAIN BOT (5036504214...)")
        print("• Backend processing: 17 tokens (load balanced)")
        print("• Webhook endpoint: /webhook (single)")
        print("• Total capacity: 510 messages/second")
        print("• User experience: Single bot interface")
        return
    
    command = sys.argv[1]
    render_url = sys.argv[2] if len(sys.argv) > 2 else RENDER_URL
    
    if "your-app-name" in render_url and command == "setup":
        logger.error("❌ Please provide your actual Render.com URL!")
        logger.error("   Example: python setup_webhooks_smart.py setup https://my-bot.onrender.com")
        return
    
    async with aiohttp.ClientSession() as session:
        if command == "setup":
            logger.info("🚀 Setting up Single Interface Bot...")
            logger.info(f"📡 Render URL: {render_url}")
            logger.info(f"🤖 Main Interface: {MAIN_BOT_TOKEN[:10]}...")
            logger.info(f"⚡ Backend Tokens: {len(ALL_TOKENS)} total")
            
            # Step 1: Clear all existing webhooks
            await clear_all_webhooks(session)
            await asyncio.sleep(2)
            
            # Step 2: Set up main bot webhook
            success = await setup_single_interface_webhook(session, render_url)
            
            if success:
                logger.info("✅ Single Interface setup completed!")
                await asyncio.sleep(2)
                await verify_single_interface_setup(session)
                
                print("\n🎯 SETUP COMPLETE!")
                print("="*30)
                print("• Users connect to: MAIN BOT")
                print("• Backend load balancing: 17 tokens")
                print("• Total capacity: 510 msg/sec")
                print("• Webhook: Single endpoint")
                print("• Ready for 100K users! 🚀")
            else:
                logger.error("❌ Setup failed!")
        
        elif command == "clear":
            await clear_all_webhooks(session)
            logger.info("✅ All webhooks cleared")
        
        elif command == "info":
            await get_all_bot_info(session)
        
        elif command == "verify":
            await verify_single_interface_setup(session)
        
        else:
            logger.error(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())