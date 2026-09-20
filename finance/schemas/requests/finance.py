from enum import Enum

from ninja import Schema

from finance.schemas.common import Money_Amount


class GatewayEnum(str, Enum):
    zibal = "zibal"


class DepositToWalletSchema(Schema):
    gateway: GatewayEnum
    amount: Money_Amount


class ZibalCallbackQuery(Schema):
    success: bool
    trackId: int
    orderId: str | None = None
    status: int
