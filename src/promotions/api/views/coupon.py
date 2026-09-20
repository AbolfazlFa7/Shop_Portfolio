from ninja import Router
from promotions.schemas.coupon import CouponSchema, CouponVerifySchema
from promotions.services.coupon import apply_coupon_service
from promotions.models import Coupon

router = Router()

@router.get("/coupons", response=list[CouponSchema])
def list_coupons(request):
    return list(Coupon.objects.filter(is_active=True))

@router.post("/coupons/verify", response=dict)
def verify_coupon(request, payload: CouponVerifySchema):
    discount = apply_coupon_service(payload.code, payload.order_amount)
    return {"discount": discount}
