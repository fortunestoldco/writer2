from typing import Any, Optional
from redis import asyncio as aioredis
from fastapi.encoders import jsonable_encoder
import json
import structlog

logger = structlog.get_logger(__name__)

class Cache:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error("cache_error", operation="get", error=str(e))
            return None
            
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: int = 3600
    ) -> bool:
        """Set value in cache"""
        try:
            value = json.dumps(jsonable_encoder(value))
            return await self.redis.set(key, value, ex=expire)
        except Exception as e:
            logger.error("cache_error", operation="set", error=str(e))
            return False