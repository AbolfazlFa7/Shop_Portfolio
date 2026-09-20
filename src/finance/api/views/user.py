from ninja import Router
from ninja.pagination import paginate

from common.services.jwt import JWTAuth
from finance.schemas.responses.finance import (
    WalletResponseSchema,
    WalletTransactionResponseSchema,
)
from finance.selectors.finance import (
    get_wallet_by_id_for_owner,
    list_wallet_transactions_for_owner,
    list_wallets_for_owner,
)

router = Router()


@router.get(
    "/wallets/",
    auth=JWTAuth(),
    response=list[WalletResponseSchema],
)
@paginate
async def get_user_wallets(request):
    return list_wallets_for_owner(request.user.id)


@router.get(
    "/wallets/{wallet_id}/",
    auth=JWTAuth(),
    response=WalletResponseSchema,
)
async def get_user_wallet_detail(request, wallet_id: int):
    return await get_wallet_by_id_for_owner(request.user.id, wallet_id)


@router.get(
    "/wallets/{wallet_id}/transactions/",
    auth=JWTAuth(),
    response=list[WalletTransactionResponseSchema],
)
@paginate
async def get_wallet_transactions(request, wallet_id: int):
    wallet = await get_wallet_by_id_for_owner(request.user.id, wallet_id)
    return list_wallet_transactions_for_owner(request.user.id, wallet.business_id or 0)
