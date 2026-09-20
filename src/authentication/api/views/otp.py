import logging

from ninja import Router, Status

from authentication.schemas.requests.otp import SendOTP_SMS_Schema
from authentication.services.otp import OTP
from common.permissions import IsAnonymous, permissions
from common.schemas.responses import DetailResponse

logger = logging.getLogger(__name__)

router = Router()


@router.post("/sms", response=DetailResponse)
@permissions(IsAnonymous)
async def send_otp_sms(request, payload: SendOTP_SMS_Schema):
    logger.info(f"OTP request for phone: {payload.phone_number}")
    data = await OTP.send_otp(payload.phone_number)
    return Status(200, data)
