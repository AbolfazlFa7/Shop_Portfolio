from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import F
from ninja.errors import HttpError

from finance.models import Wallet, WalletTransaction
from finance.schemas.requests.finance import ZibalCallbackQuery
from finance.services.zibal import Zibal


class ZibalCallback:
    def __init__(self, data: ZibalCallbackQuery):
        self.success = data.success
        self.trackId = data.trackId
        self.status = data.status
        self.orderId = data.orderId

    async def _get_pending_transaction(self) -> WalletTransaction:
        tx = await WalletTransaction.objects.filter(
            reference_id=str(self.trackId)
        ).afirst()

        if tx is None:
            raise HttpError(404, "Transaction not found")

        return tx

    def _get_wallet(self, wallet_id: int) -> Wallet:
        qs = Wallet.objects.select_for_update().filter(id=wallet_id, is_active=True)

        wallet = qs.first()
        if wallet is None:
            raise HttpError(404, "Wallet not found")

        return wallet

    @transaction.atomic
    def _apply_success(self, tx_id: int) -> WalletTransaction:
        """
        Locks rows and applies balance charge atomically inside DB transaction.
        """
        tx = WalletTransaction.objects.select_for_update().get(id=tx_id)

        if tx.status != WalletTransaction.Status.PENDING:
            return tx

        wallet = self._get_wallet(tx.wallet_id)  # type: ignore

        balance_before = wallet.balance
        balance_after = balance_before + tx.amount

        Wallet.objects.filter(id=wallet.pk).update(balance=F("balance") + tx.amount)

        tx.status = WalletTransaction.Status.SUCCESSFUL
        tx.balance_before = balance_before
        tx.balance_after = balance_after
        tx.save(update_fields=["status", "balance_before", "balance_after"])

        return tx

    @transaction.atomic
    def _apply_failure(self, tx_id: int) -> None:
        WalletTransaction.objects.filter(
            id=tx_id, status=WalletTransaction.Status.PENDING
        ).update(status=WalletTransaction.Status.FAILED)

    async def verify(self):
        tx = await self._get_pending_transaction()

        if tx.status != WalletTransaction.Status.PENDING:
            return {"detail": "Already processed"}

        if not self.success:
            await sync_to_async(self._apply_failure)(tx.pk)
            return {"detail": "Payment canceled by user"}

        zibal = Zibal()
        response = await zibal.verify_payment(self.trackId, True)

        if response.is_success and response.is_paid:
            await sync_to_async(self._apply_success)(tx.pk)
            return {"detail": "Payment successful"}
        else:
            await sync_to_async(self._apply_failure)(tx.pk)
            raise HttpError(400, response.message)
