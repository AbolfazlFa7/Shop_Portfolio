import logging
import uuid
from asgiref.sync import sync_to_async
from django.db import transaction
from ninja.errors import HttpError
from finance.models import Wallet, WalletTransaction
from finance.schemas.requests.finance import DepositToWalletSchema
from finance.schemas.requests.zibal import ZibalPaymentRequest
from finance.services.zibal import Zibal

logger = logging.getLogger(__name__)


class WalletDeposit:
    def __init__(
        self,
        user_id: int,
        wallet_id: int,
        payload: DepositToWalletSchema,
        callback_url: str,
    ):
        self.user_id = user_id
        self.wallet_id = wallet_id
        self.amount = payload.amount
        self.callback_url = callback_url

    def _get_wallet(self) -> Wallet:
        wallet = Wallet.objects.filter(
            id=self.wallet_id, user_id=self.user_id, is_active=True
        ).first()
        if not wallet:
            logger.warning(
                f"Wallet {self.wallet_id} not found for user {self.user_id}"
            )
            raise HttpError(404, "Wallet not found")
        return wallet

    @transaction.atomic
    def _create_transaction(self, wallet_id: int, track_id: int) -> WalletTransaction:
        wallet = Wallet.objects.select_for_update().get(id=wallet_id)
        logger.info(
            f"Creating deposit transaction for wallet {wallet_id}, amount {self.amount}"
        )
        return WalletTransaction.objects.create(
            wallet=wallet,
            amount=self.amount,
            type=WalletTransaction.Type.DEPOSIT,
            status=WalletTransaction.Status.PENDING,
            reference_id=str(track_id),
            transaction_group_id=uuid.uuid4(),
        )

    async def deposit_to_wallet(self) -> str:
        wallet = await sync_to_async(self._get_wallet)()
        zibal = Zibal()
        payment_req = ZibalPaymentRequest(
            amount=self.amount,
            callbackUrl=self.callback_url,
            description=f"Deposit to wallet {wallet.id}",
            orderId=str(uuid.uuid4()),
        )
        zibal_res = await zibal.request_payment(payment_req, lazy=True)
        await sync_to_async(self._create_transaction)(wallet.id, zibal_res.trackId)
        return zibal.get_start_url(zibal_res.trackId)


class WalletTransfer:
    pass
