from ninja import Router

from promotions.api.views.coupon import router as coupon_router

router = Router(tags=["Promotions"])
router.add_router("/", coupon_router)
