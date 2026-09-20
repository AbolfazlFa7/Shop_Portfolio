import pytest

from finance.models import Wallet, WalletTransaction


@pytest.mark.django_db(transaction=True)
class TestFinanceAdminSelector:
    async def test_list_wallets_empty(self):
        """list_wallets returns empty queryset when no wallets exist."""
        from finance.selectors.admin import FinanceAdminSelector

        qs = FinanceAdminSelector.list_wallets()
        assert await qs.acount() == 0

    async def test_list_wallets_returns_all(self, sample_business):
        """list_wallets returns all wallets with business select_related."""
        wallet = await Wallet.objects.acreate(
            user=sample_business.owner,
            business=sample_business,
            type=Wallet.WalletType.BUSINESS,
            card_number="1234-5678-9012-3456",
            shaba_number="IR123456789012345678901234",
            account_number="ACC-001",
        )
        from finance.selectors.admin import FinanceAdminSelector

        qs = FinanceAdminSelector.list_wallets()
        assert await qs.acount() == 1
        w = await qs.afirst()
        assert w.pk == wallet.pk
        # Verify select_related worked
        assert w.business.pk == sample_business.pk

    async def test_list_transactions_empty(self):
        """list_transactions returns empty queryset when no transactions exist."""
        from finance.selectors.admin import FinanceAdminSelector

        qs = FinanceAdminSelector.list_transactions()
        assert await qs.acount() == 0

    async def test_list_transactions_returns_all(self, sample_business):
        """list_transactions returns all transactions with wallet__business select_related."""
        wallet = await Wallet.objects.acreate(
            user=sample_business.owner,
            business=sample_business,
            type=Wallet.WalletType.BUSINESS,
            card_number="1111-1111-1111-1111",
            shaba_number="IR111111111111111111111111",
            account_number="ACC-002",
        )
        txn = await WalletTransaction.objects.acreate(
            wallet=wallet,
            amount=50000,
            type=WalletTransaction.Type.DEPOSIT,
            status=WalletTransaction.Status.SUCCESSFUL,
        )
        from finance.selectors.admin import FinanceAdminSelector

        qs = FinanceAdminSelector.list_transactions()
        assert await qs.acount() == 1
        t = await qs.afirst()
        assert t.pk == txn.pk
        # Verify select_related chain
        assert t.wallet.business.pk == sample_business.pk

    async def test_list_transactions_multiple_wallets(self, sample_business):
        """list_transactions returns transactions from all wallets."""
        wallet1 = await Wallet.objects.acreate(
            user=sample_business.owner,
            business=sample_business,
            type=Wallet.WalletType.BUSINESS,
            card_number="2222-2222-2222-2222",
            shaba_number="IR222222222222222222222222",
            account_number="ACC-003",
        )
        wallet2 = await Wallet.objects.acreate(
            user=sample_business.owner,
            business=sample_business,
            type=Wallet.WalletType.BUSINESS,
            card_number="3333-3333-3333-3333",
            shaba_number="IR333333333333333333333333",
            account_number="ACC-004",
        )
        for w in (wallet1, wallet2):
            await WalletTransaction.objects.acreate(
                wallet=w,
                amount=10000,
                type=WalletTransaction.Type.DEPOSIT,
                status=WalletTransaction.Status.SUCCESSFUL,
            )

        from finance.selectors.admin import FinanceAdminSelector

        qs = FinanceAdminSelector.list_transactions()
        assert await qs.acount() == 2
