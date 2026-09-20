import logging
import uuid
from datetime import UTC, datetime, timedelta
from http import HTTPStatus

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from ninja.security import HttpBearer

User = get_user_model()
logger = logging.getLogger(__name__)


class AsyncJWTService:
    def __init__(self):
        jwt_settings = getattr(settings, "JWT_SETTINGS", {})
        self.secret = jwt_settings.get("JWT_SECRET_KEY", settings.SECRET_KEY)
        self.algorithm = jwt_settings.get("ALGORITHM", "HS256")
        self.access_lifetime = jwt_settings.get(
            "ACCESS_LIFETIME", timedelta(minutes=15)
        )
        self.refresh_lifetime = jwt_settings.get("REFRESH_LIFETIME", timedelta(days=1))

    def _encode(self, user_id: str, token_type: str, lifetime: timedelta) -> str:
        now = datetime.now(UTC)
        exp = now + lifetime
        payload = {
            "sub": user_id,
            "type": token_type,
            "jti": str(uuid.uuid4()),
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def _decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired error")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Token expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid token error")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token")

    def _validate_type(self, payload: dict, expected: str) -> None:
        if payload.get("type") != expected:
            logger.warning(f"Invalid token type: expected {expected}, got {payload.get('type')}")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token type")

    def _create_access(self, user_id: str) -> str:
        return self._encode(user_id, "access", self.access_lifetime)

    def _create_refresh(self, user_id: str) -> str:
        return self._encode(user_id, "refresh", self.refresh_lifetime)

    async def _ensure_user_active(self, user_id: str) -> None:
        if not await User.objects.filter(id=user_id, is_active=True).aexists():
            logger.warning(f"User not found or inactive: {user_id}")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "User not found or inactive")

    async def create_pair(self, user) -> dict:
        user_id = str(user.id)
        await self._ensure_user_active(user_id)
        logger.info(f"Creating token pair for user: {user_id}")
        return {
            "access_token": self._create_access(user_id),
            "refresh_token": self._create_refresh(user_id),
        }

    async def refresh(self, refresh_token: str) -> dict:
        payload = self._decode(refresh_token)
        self._validate_type(payload, "refresh")
        user_id = payload["sub"]
        await self._ensure_user_active(user_id)
        logger.info(f"Refreshing token for user: {user_id}")
        return {
            "access_token": self._create_access(user_id),
            "refresh_token": self._create_refresh(user_id),
        }

    async def logout(self, refresh_token: str, user_id: int) -> None:
        payload = self._decode(refresh_token)
        self._validate_type(payload, "refresh")
        if str(payload.get("sub")) != str(user_id):
            logger.warning(f"Invalid token owner on logout for user: {user_id}")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token owner")
        logger.info(f"User logged out successfully: {user_id}")

    def verify_access(self, token: str) -> dict:
        payload = self._decode(token)
        self._validate_type(payload, "access")
        return payload


class JWTAuth(HttpBearer):
    async def authenticate(self, request, token: str):
        service = AsyncJWTService()
        payload = service.verify_access(token)
        user = await User.objects.filter(id=payload["sub"], is_active=True).afirst()
        if not user:
            logger.warning(f"Authenticated user not found or inactive: {payload['sub']}")
            raise HttpError(HTTPStatus.UNAUTHORIZED, "User not found or inactive")
        return user
