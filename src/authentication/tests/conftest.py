import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="auth_user@example.com",
        phone_number="09222222222",
        password="password123",
    )
