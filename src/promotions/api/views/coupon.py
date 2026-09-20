from ninja import Router
from ninja.pagination import paginate

from common.services.jwt import JWTAuth
from promotions.models import Coupon
from promotions.schemas.coupon import CouponSchema, CouponVerifySchema
from promotions.services.coupon import apply_coupon_service

router = Router()


@router.get("/coupons", auth=JWTAuth(), response=list[CouponSchema])
@paginate
async def list_coupons(request):
    return Coupon.objects.filter(is_active=True)


@router.post("/coupons/verify", auth=JWTAuth(), response=dict)
async def verify_coupon(request, payload: CouponVerifySchema):
    return {"discount": apply_coupon_service(payload.code, payload.order_amount)}
