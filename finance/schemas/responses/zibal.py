from datetime import datetime

from pydantic import BaseModel

from finance.schemas.common import Money_Amount
from finance.schemas.requests.zibal import MultiplexingInfo, ZibalResult, ZibalStatus


class ZibalPaymentResponse(BaseModel):
    trackId: int
    result: ZibalResult
    message: str

    @property
    def is_success(self) -> bool:
        return self.result == ZibalResult.SUCCESS


class ZibalVerifyResponse(BaseModel):
    paidAt: datetime | None = None
    cardNumber: str | None = None
    status: ZibalStatus
    amount: Money_Amount
    refNumber: int | None = None
    description: str | None = None
    orderId: str | None = None
    result: ZibalResult
    message: str
    multiplexingInfos: list[MultiplexingInfo] | None = None

    @property
    def is_success(self) -> bool:
        return (
            self.result == ZibalResult.SUCCESS
            and self.status == ZibalStatus.PAID_VERIFIED
        )

    @property
    def is_paid(self) -> bool:
        return self.status in [ZibalStatus.PAID_VERIFIED, ZibalStatus.PAID_UNVERIFIED]


class ZibalInquiryResponse(BaseModel):
    status: ZibalStatus
    amount: Money_Amount
    trackId: int
    paidAt: datetime | None = None
    cardNumber: str | None = None
    refNumber: int | None = None
    description: str | None = None
    orderId: str | None = None
    result: ZibalResult
    message: str

    @property
    def is_success(self) -> bool:
        return self.result == ZibalResult.SUCCESS

    @property
    def is_paid(self) -> bool:
        return self.status in [ZibalStatus.PAID_VERIFIED]
