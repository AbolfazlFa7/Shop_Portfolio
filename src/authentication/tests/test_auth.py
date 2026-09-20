import pytest
from django.contrib.auth import get_user_model
from common.services.jwt.jwt import AsyncJWTService


@pytest.mark.django_db
def test_user_creation():
    User = get_user_model()
    user = User.objects.create_user(
        email="auth@example.com",
        phone_number="09987654321",
        password="password123",
    )
    assert user.email == "auth@example.com"
    assert user.check_password("password123")


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_jwt_service_token_creation(user):
    service = AsyncJWTService()
    tokens = await service.create_pair(user)
    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_jwt_service_refresh(user):
    service = AsyncJWTService()
    tokens = await service.create_pair(user)
    refresh_token = tokens["refresh_token"]
    new_tokens = await service.refresh(refresh_token)
    assert "access_token" in new_tokens
