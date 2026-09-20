from django.db.models import QuerySet

from finance.models import Wallet, WalletTransaction


class FinanceAdminSelector:
    @staticmethod
    def list_wallets() -> QuerySet:
        return Wallet.objects.all().select_related("business")

    @staticmethod
    def list_transactions() -> QuerySet:
        return WalletTransaction.objects.all().select_related("wallet__business")
