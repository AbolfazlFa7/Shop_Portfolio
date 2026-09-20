from http import HTTPStatus

from ninja.errors import HttpError

from promotions.models import Coupon


def apply_coupon_service(code: str, order_amount: int):
    coupon = Coupon.objects.filter(code=code, is_active=True).first()
    if not coupon:
        raise HttpError(HTTPStatus.BAD_REQUEST, "Invalid coupon")
    if coupon.min_order_amount > order_amount:
        raise HttpError(
            HTTPStatus.BAD_REQUEST, "Order amount is less than minimum required"
        )
    if coupon.max_usage and coupon.usage_count >= coupon.max_usage:
        raise HttpError(HTTPStatus.BAD_REQUEST, "Coupon usage limit reached")
    coupon.usage_count += 1
    coupon.save(update_fields=["usage_count"])
    if coupon.discount_type == "percent":
        return int(order_amount * coupon.discount_value / 100)
    return min(coupon.discount_value, order_amount)
