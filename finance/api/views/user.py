from ninja import Router
from ninja.pagination import paginate

from common.services.jwt import JWTAuth
from finance.schemas.responses.finance import (
    WalletResponseSchema,
)
from finance.selectors.finance import (
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
