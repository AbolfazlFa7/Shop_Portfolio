from enum import IntEnum

from django.conf import settings
from pydantic import BaseModel, field_validator

from finance.schemas.common import Bank_Account_Number, Money_Amount


class ZibalStatus(IntEnum):
    PENDING = -1
    INTERNAL_ERROR = -2
    PAID_VERIFIED = 1
    PAID_UNVERIFIED = 2
    USER_CANCELED = 3
    INVALID_CARD_NUMBER = 4
    INSUFFICIENT_FUNDS = 5
    INCORRECT_PIN = 6
    EXCEEDED_REQUEST_LIMIT = 7
    EXCEEDED_DAILY_PAYMENT_COUNT = 8
    EXCEEDED_DAILY_PAYMENT_AMOUNT = 9
    INVALID_ISSUER = 10
    SWITCH_ERROR = 11
    CARD_NOT_ACCESSIBLE = 12
    REFUNDED = 15
    REFUNDING = 16
    REVERSED = 18
    INVALID_MERCHANT = 21

    @property
    def description(self) -> str:
        descriptions = {
            self.PENDING: "Waiting for payment",
            self.INTERNAL_ERROR: "Internal system error",
            self.PAID_VERIFIED: "Paid and verified successfully",
            self.PAID_UNVERIFIED: "Paid but not yet verified",
            self.USER_CANCELED: "Cancelled by user",
            self.INVALID_CARD_NUMBER: "Invalid card number",
            self.INSUFFICIENT_FUNDS: "Insufficient balance",
            self.INCORRECT_PIN: "Incorrect PIN entered",
            self.EXCEEDED_REQUEST_LIMIT: "Too many requests",
            self.EXCEEDED_DAILY_PAYMENT_COUNT: "Daily transaction count exceeded",
            self.EXCEEDED_DAILY_PAYMENT_AMOUNT: "Daily transaction amount exceeded",
            self.INVALID_ISSUER: "Invalid card issuer",
            self.SWITCH_ERROR: "Switch error",
            self.CARD_NOT_ACCESSIBLE: "Card not accessible",
            self.REFUNDED: "Transaction refunded",
            self.REFUNDING: "Transaction is being refunded",
            self.REVERSED: "Transaction reversed",
            self.INVALID_MERCHANT: "Invalid merchant",
        }
        return descriptions.get(self, "Unknown status")


class ZibalResult(IntEnum):
    SUCCESS = 100
    MERCHANT_NOT_FOUND = 102
    MERCHANT_INACTIVE = 103
    INVALID_MERCHANT = 104
    INVALID_AMOUNT = 105
    INVALID_CALLBACK_URL = 106
    INVALID_PERCENT_MODE = 107
    INVALID_MULTIPLEXING_INFOS = 108
    INACTIVE_MULTIPLEXING_INFOS = 109
    MISSING_SELF_MULTIPLEXING = 110
    AMOUNT_MISMATCH_MULTIPLEXING = 111
    INSUFFICIENT_WAGE_WALLET_BALANCE = 112
    AMOUNT_EXCEEDS_MAX = 113
    INVALID_NATIONAL_CODE = 114
    IP_NOT_REGISTERED = 115
    INVALID_FEE_MODE = 116
    ALREADY_VERIFIED = 201
    NOT_PAID_OR_FAILED = 202
    INVALID_TRACK_ID = 203

    @property
    def description(self) -> str:
        descriptions = {
            self.SUCCESS: "Request successful",
            self.MERCHANT_NOT_FOUND: "Merchant not found",
            self.MERCHANT_INACTIVE: "Merchant is inactive or contract not signed",
            self.INVALID_MERCHANT: "Invalid merchant",
            self.INVALID_AMOUNT: "Amount must be greater than 1,000 Rials",
            self.INVALID_CALLBACK_URL: "Callback URL must start with http or https",
            self.INVALID_PERCENT_MODE: "Percent mode must be 0 or 1",
            self.INVALID_MULTIPLEXING_INFOS: "One or more beneficiaries in multiplexingInfos are invalid",
            self.INACTIVE_MULTIPLEXING_INFOS: "One or more beneficiaries in multiplexingInfos are inactive",
            self.MISSING_SELF_MULTIPLEXING: "id = self is missing in multiplexingInfos",
            self.AMOUNT_MISMATCH_MULTIPLEXING: "Amount does not match sum of shares in multiplexingInfos",
            self.INSUFFICIENT_WAGE_WALLET_BALANCE: "Fee wallet balance is insufficient",
            self.AMOUNT_EXCEEDS_MAX: "Transaction amount exceeds the limit",
            self.INVALID_NATIONAL_CODE: "Invalid national code",
            self.IP_NOT_REGISTERED: "IP address is not registered in the panel",
            self.INVALID_FEE_MODE: "Fee mode must be an integer",
            self.ALREADY_VERIFIED: "Transaction already verified",
            self.NOT_PAID_OR_FAILED: "Payment not completed or unsuccessful",
            self.INVALID_TRACK_ID: "Invalid track ID",
        }
        return descriptions.get(self, "Unknown result")


class MultiplexingInfo(BaseModel):
    amount: Money_Amount | None = None
    bankAccount: Bank_Account_Number | None = None
    walletID: int | None = None
    wagePayer: bool | None = None
    subMerchantId: str | None = None


class ZibalPaymentRequest(BaseModel):
    amount: Money_Amount
    callbackUrl: str
    mobile: str | None = None
    description: str | None = None
    orderId: str | None = None
    feeMode: int | None = None
    multiplexingInfos: list[MultiplexingInfo] | None = None

    @field_validator("amount", mode="after")
    def convert_to_rial(cls, v: int) -> int:
        return v * 10

    @field_validator("callbackUrl")
    def validate_callback_url(cls, v: str) -> str:
        if not settings.DEBUG and not v.startswith("https://"):
            raise ValueError("callbackUrl must start with http:// or https://")
        return v
