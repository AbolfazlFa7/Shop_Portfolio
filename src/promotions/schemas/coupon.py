from datetime import datetime

from ninja import Schema


class CouponSchema(Schema):
    id: int
    code: str
    description: str
    discount_type: str
    discount_value: int
    start_date: datetime
    end_date: datetime | None = None
    is_active: bool
    min_order_amount: int
    max_usage: int | None = None
    usage_count: int


class CouponVerifySchema(Schema):
    code: str
    order_amount: int
