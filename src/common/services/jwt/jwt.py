import uuid
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.errors import HttpError

User = get_user_model()

class JWTService:
    def __init__(self):
        jwt_settings = getattr(settings, "JWT_SETTINGS", {})
        self.secret = jwt_settings.get("JWT_SECRET_KEY", settings.SECRET_KEY)
        self.algorithm = jwt_settings.get("ALGORITHM", "HS256")
        self.access_lifetime = jwt_settings.get("ACCESS_LIFETIME", timedelta(minutes=15))
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
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Token expired")
        except jwt.InvalidTokenError:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token")

    def create_pair(self, user) -> dict:
        return {
            "access_token": self._encode(str(user.id), "access", self.access_lifetime),
            "refresh_token": self._encode(str(user.id), "refresh", self.refresh_lifetime),
        }

    def refresh(self, refresh_token: str) -> dict:
        payload = self._decode(refresh_token)
        if payload.get("type") != "refresh":
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Invalid token type")
        user_id = payload.get("sub")
        return {
            "access_token": self._encode(user_id, "access", self.access_lifetime),
        }
