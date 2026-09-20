from ninja import Router

from finance.api.views.business import router as finance_router
from finance.api.views.deposit import router as deposit_router
from finance.api.views.user import router as user_router

router = Router(tags=["Finance"])

router.add_router("", finance_router)
router.add_router("", deposit_router)
router.add_router("", user_router)
