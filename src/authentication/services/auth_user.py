import logging
from http import HTTPStatus

from ninja.errors import HttpError

from authentication.models import User
from authentication.selectors.user import UserService
from common.services.jwt import AsyncJWTService

logger = logging.getLogger(__name__)


class AuthUser:
    @staticmethod
    async def login(phone: str) -> dict:
        """Login a user."""
        logger.info(f"Login attempt for phone: {phone}")
        user = await UserService.get_user_by_id(phone)

        logger.info(f"User found: {user.pk}, login successful")
        jwt = AsyncJWTService()
        token = await jwt.create_pair(user)

        return token

    @staticmethod
    async def register(phone: str) -> dict:
        """Register a user."""
        logger.info(f"Registration attempt for phone: {phone}")
        user = await User.objects.filter(
            phone_number=phone,
        ).afirst()

        if user:
            logger.warning(f"Registration failed - User already exists: {phone}")
            raise HttpError(HTTPStatus.BAD_REQUEST, "User already exists")

        user = await User.objects.acreate_user(
            phone_number=phone,
        )
        logger.info(f"User registered successfully: {user.id}, phone: {phone}")

        jwt = AsyncJWTService()
        token = await jwt.create_pair(user)

        return token

    @staticmethod
    async def refresh_token(refresh_token: str) -> dict:
        """Refresh a user's token."""
        logger.info("Token refresh attempt")
        jwt = AsyncJWTService()
        token = await jwt.refresh(refresh_token)
        logger.info("Token refreshed successfully")

        return token

    @staticmethod
    async def logout(refresh_token: str, user_id: int) -> dict:
        """Logout a user."""
        logger.info(f"Logout attempt for user {user_id}")
        jwt = AsyncJWTService()
        await jwt.logout(refresh_token, user_id)
        logger.info(f"Logout successful for user {user_id}")

        return {"detail": "Successfully logged out"}
