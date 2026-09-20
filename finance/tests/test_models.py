import uuid

import pytest
from django.db import IntegrityError

from finance.models import Wallet, WalletTransaction


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_creation(sample_business):
    wallet = await Wallet.objects.acreate(
        user=sample_business.owner,
        business=sample_business,
        type=Wallet.WalletType.BUSINESS,
        card_number="1234567890123456",
        shaba_number="IR123456789012345678901234",
        account_number="ACC-001",
    )
    assert wallet.balance == 0
    assert wallet.is_active is True
    assert wallet.business == sample_business
    assert wallet.type == Wallet.WalletType.BUSINESS


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_balance_non_negative(sample_business):
    with pytest.raises(IntegrityError):
        await Wallet.objects.acreate(
            user=sample_business.owner,
            business=sample_business,
            type=Wallet.WalletType.BUSINESS,
            balance=-1000,
        )


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_transaction_creation(sample_business):
    wallet = await Wallet.objects.acreate(
        user=sample_business.owner,
        business=sample_business,
        type=Wallet.WalletType.BUSINESS,
    )
    group_id = uuid.uuid4()
    txn = await WalletTransaction.objects.acreate(
        wallet=wallet,
        amount=50000,
        type=WalletTransaction.Type.DEPOSIT,
        status=WalletTransaction.Status.SUCCESSFUL,
        transaction_group_id=group_id,
        balance_before=0,
        balance_after=50000,
    )
    assert txn.amount == 50000
    assert txn.type == WalletTransaction.Type.DEPOSIT
    assert txn.status == WalletTransaction.Status.SUCCESSFUL
    assert txn.wallet == wallet
    assert txn.transaction_group_id == group_id


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_transaction_types(sample_business):
    wallet = await Wallet.objects.acreate(
        user=sample_business.owner,
        business=sample_business,
        type=Wallet.WalletType.BUSINESS,
    )
    txn = await WalletTransaction.objects.acreate(
        wallet=wallet,
        amount=20000,
        type=WalletTransaction.Type.SYSTEM_PAYMENT,
        status=WalletTransaction.Status.PENDING,
        balance_before=20000,
        balance_after=0,
    )
    assert txn.type == WalletTransaction.Type.SYSTEM_PAYMENT
    assert txn.status == WalletTransaction.Status.PENDING


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_transaction_with_reference(sample_business):
    wallet = await Wallet.objects.acreate(
        user=sample_business.owner,
        business=sample_business,
        type=Wallet.WalletType.BUSINESS,
    )
    txn = await WalletTransaction.objects.acreate(
        wallet=wallet,
        amount=100000,
        type=WalletTransaction.Type.REFUND,
        status=WalletTransaction.Status.SUCCESSFUL,
        reference_id="REF-001",
        balance_before=0,
        balance_after=100000,
    )
    assert txn.reference_id == "REF-001"


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_wallet_transaction_status_choices(sample_business):
    wallet = await Wallet.objects.acreate(
        user=sample_business.owner,
        business=sample_business,
        type=Wallet.WalletType.BUSINESS,
    )
    txn = await WalletTransaction.objects.acreate(
        wallet=wallet,
        amount=0,
        type=WalletTransaction.Type.SYSTEM_PAYMENT,
        status=WalletTransaction.Status.FAILED,
        balance_before=0,
        balance_after=0,
    )
    assert txn.status == WalletTransaction.Status.FAILED
