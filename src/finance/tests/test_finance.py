import pytest
from finance.models import Wallet, WalletTransaction


@pytest.mark.django_db
def test_wallet_creation(user):
    wallet = Wallet.objects.create(
        user=user,
        type=Wallet.WalletType.PERSONAL,
        balance=1000,
    )
    assert wallet.balance == 1000
    assert wallet.user == user
    assert wallet.type == Wallet.WalletType.PERSONAL


@pytest.mark.django_db
def test_wallet_unique_constraint(user):
    Wallet.objects.create(user=user, type=Wallet.WalletType.PERSONAL, balance=500)
    constraints_names = [c.name for c in Wallet._meta.constraints]
    assert "unique_user_wallet_type" in constraints_names


@pytest.mark.django_db
def test_wallet_transaction_creation(user):
    wallet = Wallet.objects.create(user=user, balance=2000)
    tx = WalletTransaction.objects.create(
        wallet=wallet,
        amount=500,
        balance_before=2000,
        balance_after=2500,
        type=WalletTransaction.Type.DEPOSIT,
        status=WalletTransaction.Status.SUCCESSFUL,
    )
    assert tx.amount == 500
    assert tx.status == WalletTransaction.Status.SUCCESSFUL
    assert wallet.transactions.count() == 1


@pytest.mark.django_db
def test_wallet_find_by_card_number(user):
    wallet = Wallet.objects.create(
        user=user,
        card_number_hmac="abc123hash",
    )
    found = Wallet.find_by_card_number("somecardnumber")
    assert found.count() == 0
