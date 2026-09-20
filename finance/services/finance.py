import uuid

from django.db import models, transaction
from ninja.errors import HttpError

from finance.models import Wallet, WalletTransaction
from finance.schemas.requests.finance import DepositToWalletSchema
from finance.schemas.requests.zibal import ZibalPaymentRequest
from finance.selectors.finance import (
    get_wallet_by_id_for_owner,
)
from finance.services.zibal import Zibal


class WalletDeposit:
    ZIBAL_URL_CALLBACK = "/zibal/callback"

    def __init__(
        self,
        user_id: int,
        wallet_id: int,
        data: DepositToWalletSchema,
        absolute_uri: str,
    ):
        self.user_id = user_id
        self.wallet_id = wallet_id
        self.amount = data.amount
        self.gateway = data.gateway
        self.base_url = absolute_uri.split("/wallets")[0]
        self.callback_url = self._make_callback_url(data.gateway)

    def _make_callback_url(self, gateway: str) -> str:
        if gateway == "zibal":
            return self.base_url + self.ZIBAL_URL_CALLBACK
        else:
            raise HttpError(400, "Gateway not supported")

    async def _create_transaction(
        self, wallet: Wallet, reference_id: str
    ) -> WalletTransaction:
        return await WalletTransaction.objects.acreate(
            wallet=wallet,
            amount=self.amount,
            type=WalletTransaction.Type.DEPOSIT,
            status=WalletTransaction.Status.PENDING,
            reference_id=reference_id,
        )

    async def _zibal_deposit(self, wallet: Wallet) -> str:
        zibal = Zibal()
        zibal_request = ZibalPaymentRequest(
            amount=self.amount, callbackUrl=self.callback_url
        )
        response = await zibal.request_payment(zibal_request, True)

        if response.is_success:
            await self._create_transaction(wallet, str(response.trackId))

            payment_url = zibal.get_start_url(response.trackId)
            return payment_url
        else:
            raise HttpError(400, response.message)

    async def deposit_to_wallet(self):
        wallet = await get_wallet_by_id_for_owner(
            owner_id=self.user_id, wallet_id=self.wallet_id
        )

        if self.gateway == "zibal":
            return await self._zibal_deposit(wallet)


class WalletTransfer:
    def __init__(
        self,
        source_wallet_id: int,
        destination_wallet_id: int,
        amount: int,
        tx_type: str = WalletTransaction.Type.SYSTEM_PAYMENT,
    ):
        self.src_wallet_id = source_wallet_id
        self.dst_wallet_id = destination_wallet_id
        self.amount = amount
        self.tx_type = tx_type

    def _pre_validations(self) -> None:
        if self.src_wallet_id == self.dst_wallet_id:
            raise HttpError(400, "Source and destination wallets cannot be identical.")

        if self.amount <= 0:
            raise HttpError(400, "Amount must be greater than zero.")

    def _get_wallets(self) -> tuple[Wallet, Wallet]:
        first_id, second_id = sorted([self.src_wallet_id, self.dst_wallet_id])
        wallets = (
            Wallet.objects.select_for_update()
            .filter(id__in=[first_id, second_id], is_active=True)
            .in_bulk()
        )

        src = wallets.get(self.src_wallet_id)
        dst = wallets.get(self.dst_wallet_id)

        if not src or not dst:
            raise HttpError(400, "One or both wallets were not found or are inactive.")

        if src.balance < self.amount:
            raise HttpError(400, "Insufficient balance.")

        return src, dst

    def _update_wallet_balances(self, src: Wallet, dst: Wallet) -> None:
        Wallet.objects.filter(id=src.pk).update(
            balance=models.F("balance") - self.amount
        )
        Wallet.objects.filter(id=dst.pk).update(
            balance=models.F("balance") + self.amount
        )

    def _create_transactions(
        self,
        src: Wallet,
        dst: Wallet,
        src_before: int,
        dst_before: int,
        src_after: int,
        dst_after: int,
    ) -> tuple[WalletTransaction, WalletTransaction]:
        group_id = uuid.uuid4()

        src_tx = WalletTransaction.objects.create(
            wallet=src,
            amount=self.amount,
            type=self.tx_type,
            status=WalletTransaction.Status.SUCCESSFUL,
            transaction_group_id=group_id,
            balance_before=src_before,
            balance_after=src_after,
        )

        dst_tx = WalletTransaction.objects.create(
            wallet=dst,
            amount=self.amount,
            type=WalletTransaction.Type.DEPOSIT,
            status=WalletTransaction.Status.SUCCESSFUL,
            transaction_group_id=group_id,
            balance_before=dst_before,
            balance_after=dst_after,
        )

        return src_tx, dst_tx

    @transaction.atomic
    def transfer(self) -> dict[str, WalletTransaction]:
        self._pre_validations()

        src_wallet, dst_wallet = self._get_wallets()

        src_before = src_wallet.balance
        dst_before = dst_wallet.balance

        src_after = src_before - self.amount
        dst_after = dst_before + self.amount

        self._update_wallet_balances(src_wallet, dst_wallet)
        src_wallet.balance -= self.amount
        dst_wallet.balance += self.amount

        src_tx, dst_tx = self._create_transactions(
            src_wallet, dst_wallet, src_before, dst_before, src_after, dst_after
        )

        return {"src": src_tx, "dst": dst_tx}
