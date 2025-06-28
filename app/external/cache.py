import json
import logging
from typing import Optional, Dict, Any
import aioredis
from app.config import settings

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
            await self.redis.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data"""
        if not self.redis:
            return None
        
        try:
            cached_data = await self.redis.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Dict[str, Any], ttl: int = None) -> bool:
        """Set cached data with TTL"""
        if not self.redis:
            return False
        
        try:
            ttl = ttl or settings.cache_ttl_seconds
            await self.redis.setex(key, ttl, json.dumps(value, ensure_ascii=False))
            return True
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete cached data"""
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            return False
        
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache existence for key {key}: {e}")
            return False
    
    async def get_rate_limit_count(self, user_id: int) -> int:
        """Get current rate limit count for user"""
        if not self.redis:
            return 0
        
        try:
            key = f"rate_limit:{user_id}"
            count = await self.redis.get(key)
            return int(count) if count else 0
        except Exception as e:
            logger.error(f"Error getting rate limit for user {user_id}: {e}")
            return 0
    
    async def increment_rate_limit(self, user_id: int) -> int:
        """Increment rate limit counter for user"""
        if not self.redis:
            return 1
        
        try:
            key = f"rate_limit:{user_id}"
            pipeline = self.redis.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, 60)  # 1 minute window
            results = await pipeline.execute()
            return results[0] if results else 1
        except Exception as e:
            logger.error(f"Error incrementing rate limit for user {user_id}: {e}")
            return 1
    
    async def reset_rate_limit(self, user_id: int) -> bool:
        """Reset rate limit for user"""
        if not self.redis:
            return False
        
        try:
            key = f"rate_limit:{user_id}"
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error resetting rate limit for user {user_id}: {e}")
            return False
    
    def get_cache_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key"""
        return f"{prefix}:{identifier}"


# Global cache instance
redis_cache = RedisCache()