import pytest
from django.contrib.auth import get_user_model
from finance.models import Wallet


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="finance_user@example.com",
        phone_number="09111111111",
        password="password123",
    )


@pytest.fixture
def sample_wallet(db, user):
    return Wallet.objects.create(user=user, balance=5000)
