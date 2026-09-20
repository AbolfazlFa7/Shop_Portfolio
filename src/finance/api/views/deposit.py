from ninja import Query, Router, Status

from common.schemas.responses import DetailResponse
from finance.schemas.requests.finance import DepositToWalletSchema, ZibalCallbackQuery
from finance.schemas.responses.finance import DepositToWalletResponseSchema
from finance.services.callback import ZibalCallback
from finance.services.finance import WalletDeposit

router = Router()


@router.post(
    "/wallets/{wallet_id}/deposit",
    response=DepositToWalletResponseSchema,
)
async def deposit_to_wallet(request, wallet_id: int, payload: DepositToWalletSchema):
    service = WalletDeposit(
        request.user.id, wallet_id, payload, request.build_absolute_uri()
    )
    payment_url = await service.deposit_to_wallet()

    return Status(200, {"payment_url": payment_url})


@router.get("/zibal/callback", response=DetailResponse)
async def zibal_callback(request, query: Query[ZibalCallbackQuery]):
    service = ZibalCallback(query)
    response = await service.verify()

    return Status(200, response)
