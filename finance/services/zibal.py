import httpx
from django.conf import settings
from ninja.errors import HttpError

from finance.schemas.requests.zibal import ZibalPaymentRequest, ZibalResult
from finance.schemas.responses.zibal import (
    ZibalInquiryResponse,
    ZibalPaymentResponse,
    ZibalVerifyResponse,
)


class Zibal:
    BASE_URL = "https://gateway.zibal.ir"
    REQUEST_PATH = "/v1/request"
    VERIFY_PATH = "/v1/verify"
    INQUIRY_PATH = "/v1/inquiry"
    LAZY_REQUEST_PATH = "/request/lazy"
    LAZY_VERIFY_PATH = "/verify"
    START_PATH = "/start"

    def __init__(self, merchant_id: str | None = None):
        self.merchant_id = merchant_id or getattr(settings, "ZIBAL_MERCHANT_ID", None)
        if not self.merchant_id:
            raise ValueError("ZIBAL_MERCHANT_ID is not set in settings")

    async def _apost(self, path: str, data: dict[str, object]) -> dict[str, object]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.BASE_URL}{path}",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    def _handle_result(
        self, result_code: object, message: object | None = None
    ) -> None:
        if not isinstance(result_code, int):
            raise HttpError(400, "Invalid result code type")

        if result_code == ZibalResult.SUCCESS:
            return

        if result_code == ZibalResult.ALREADY_VERIFIED:
            return

        try:
            error_msg = ZibalResult(result_code).description
        except ValueError:
            error_msg = str(message) if message is not None else "Unknown error"

        raise HttpError(400, f"Zibal error: {error_msg} (code: {result_code})")

    async def request_payment(
        self,
        data: ZibalPaymentRequest,
        lazy: bool = False,
    ) -> ZibalPaymentResponse:
        payload = data.model_dump(exclude_unset=True, exclude_none=True)
        payload["merchant"] = self.merchant_id

        path = self.LAZY_REQUEST_PATH if lazy else self.REQUEST_PATH
        result = await self._apost(path, payload)

        self._handle_result(result.get("result"), result.get("message"))

        return ZibalPaymentResponse.model_validate(result)

    async def verify_payment(
        self, track_id: int, lazy: bool = False
    ) -> ZibalVerifyResponse:
        payload = {
            "merchant": self.merchant_id,
            "trackId": track_id,
        }

        path = self.LAZY_VERIFY_PATH if lazy else self.VERIFY_PATH
        result = await self._apost(path, payload)

        self._handle_result(result.get("result"), result.get("message"))

        return ZibalVerifyResponse.model_validate(result)

    async def inquiry_payment(self, track_id: int) -> ZibalInquiryResponse:
        payload = {
            "merchant": self.merchant_id,
            "trackId": track_id,
        }

        result = await self._apost(self.INQUIRY_PATH, payload)

        self._handle_result(result.get("result"), result.get("message"))

        return ZibalInquiryResponse.model_validate(result)

    def get_start_url(self, track_id: int) -> str:
        return f"{self.BASE_URL}{self.START_PATH}/{track_id}"
