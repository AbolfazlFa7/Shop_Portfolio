import logging

from django.db.models import QuerySet
from django.shortcuts import aget_object_or_404

from authentication.models import User

logger = logging.getLogger(__name__)


class User_Selector:
    @staticmethod
    def list_users() -> QuerySet:
        logger.info("Listing all users")
        return User.objects.all()

    @staticmethod
    async def get_user_by_id(id) -> User:
        logger.info(f"Fetching user by id: {id}")
        return await aget_object_or_404(User, id=id)
