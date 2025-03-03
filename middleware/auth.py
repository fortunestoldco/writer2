from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)
security = HTTPBearer()

class AuthMiddleware:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        try:
            credentials: HTTPAuthorizationCredentials = await security(request)
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            request.state.user = payload
            return await call_next(request)
        except (JWTError, HTTPException) as e:
            logger.warning("auth_error", error=str(e))
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )