import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Primary bot token (handles all users)
    bot_token_main: str = os.getenv("BOT_TOKEN_MAIN", "")
    
    # Backup tokens (for fallback only)
    backup_bot_tokens: List[str] = [
        os.getenv("BOT_TOKEN_1", ""),
        os.getenv("BOT_TOKEN_2", ""),
        os.getenv("BOT_TOKEN_3", ""),
        os.getenv("BOT_TOKEN_4", ""),
        os.getenv("BOT_TOKEN_5", ""),
        os.getenv("BOT_TOKEN_6", ""),
        os.getenv("BOT_TOKEN_7", ""),
        os.getenv("BOT_TOKEN_8", ""),
        os.getenv("BOT_TOKEN_9", ""),
        os.getenv("BOT_TOKEN_10", ""),
        os.getenv("BOT_TOKEN_11", ""),
        os.getenv("BOT_TOKEN_12", ""),
        os.getenv("BOT_TOKEN_13", ""),
        os.getenv("BOT_TOKEN_14", ""),
        os.getenv("BOT_TOKEN_15", ""),
        os.getenv("BOT_TOKEN_16", ""),
    ]
    
    # Bot mode: single_interface = one bot face with multiple tokens, multi_bot = separate bots
    bot_mode: str = os.getenv("BOT_MODE", "single_interface")  # single_interface, multi_bot, single_token
    
    webhook_url: str = os.getenv("WEBHOOK_URL", "")
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # External API
    najah_api_base_url: str = os.getenv("NAJAH_API_BASE_URL", "https://serapi3.najah.iq")
    
    # Rate Limiting
    max_requests_per_minute: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "3"))
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def active_bot_tokens(self) -> List[str]:
        """Return active bot tokens based on mode"""
        all_tokens = [self.bot_token_main] + self.backup_bot_tokens
        return [token for token in all_tokens if token.strip()]

    @property
    def backup_tokens(self) -> List[str]:
        """Get backup tokens for internal use"""
        return [token for token in self.backup_bot_tokens if token.strip()]

    def get_primary_token(self) -> str:
        """Get the primary bot token (main interface)"""
        if not self.bot_token_main.strip():
            raise ValueError("Primary bot token not configured")
        return self.bot_token_main

    def get_response_token(self, user_id: int) -> str:
        """Get token to use for responding to user (load balancing)"""
        if self.bot_mode == "single_token":
            # Only use main token
            return self.get_primary_token()
        elif self.bot_mode == "single_interface":
            # One bot interface, multiple tokens for responses (load balancing)
            all_tokens = self.active_bot_tokens
            if not all_tokens:
                raise ValueError("No bot tokens configured")
            
            # Use different tokens for different users to distribute load
            token_index = user_id % len(all_tokens)
            return all_tokens[token_index]
        else:  # multi_bot mode
            # Traditional sharding
            all_tokens = self.active_bot_tokens
            if not all_tokens:
                raise ValueError("No bot tokens configured")
            
            shard_index = user_id % len(all_tokens)
            return all_tokens[shard_index]

    def get_webhook_token(self, shard_id: int) -> str:
        """Get token for webhook processing"""
        if self.bot_mode == "single_interface":
            # All webhooks go to main bot, but responses use different tokens
            return self.get_primary_token()
        else:
            # Traditional multi-bot or single token mode
            all_tokens = self.active_bot_tokens
            if shard_id < len(all_tokens):
                return all_tokens[shard_id]
            return self.get_primary_token()


settings = Settings()