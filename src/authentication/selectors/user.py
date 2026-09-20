import logging

from django.shortcuts import aget_object_or_404

from authentication.models import User

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    async def get_user_by_id(phone_number: str) -> User:
        logger.info(f"Fetching user by phone number: {phone_number}")
        user = await aget_object_or_404(
            User,
            phone_number=phone_number,
            is_active=True,
        )
        return user
