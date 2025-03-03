from fastapi import Request, HTTPException
from typing import Dict, Tuple
import time
import structlog
from cachetools import TTLCache

logger = structlog.get_logger(__name__)

class RateLimitMiddleware:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.cache = TTLCache(maxsize=10000, ttl=60)

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        key = f"{request.client.host}:{request.url.path}"
        
        # Check rate limit
        current_time = time.time()
        if key in self.cache:
            if self.cache[key] >= self.requests_per_minute:
                logger.warning("rate_limit_exceeded", client=request.client.host)
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests"
                )
            self.cache[key] += 1
        else:
            self.cache[key] = 1

        return await call_next(request)