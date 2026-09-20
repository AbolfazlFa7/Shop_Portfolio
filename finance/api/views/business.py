from ninja import Router
from ninja.pagination import paginate

from common.services.jwt import JWTAuth
from finance.schemas.responses.finance import (
    WalletTransactionResponseSchema,
)
from finance.selectors.finance import (
    list_wallet_transactions_for_owner,
)

router = Router()


@router.get(
    "/businesses/{business_id}/wallet/history",
    auth=JWTAuth(),
    response=list[WalletTransactionResponseSchema],
)
@paginate
async def wallet_history(request, business_id: int):
    qs = list_wallet_transactions_for_owner(request.user.id, business_id)
    return qs
