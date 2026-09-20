import logging
from http import HTTPStatus

from django.conf import settings
from django.core.cache import cache
from ninja.errors import HttpError

from common.services.otp import TimeBased_OTP as TOTP

logger = logging.getLogger(__name__)


class OTP:
    @staticmethod
    async def send_otp(phone_number: str) -> dict:
        logger.info(f"Sending OTP to {phone_number}")
        cache_key = f"auth_otp:{phone_number}:secret_key"

        if await cache.aget(cache_key):
            logger.warning(f"OTP already sent for {phone_number}")
            raise HttpError(HTTPStatus.BAD_REQUEST, "OTP has already been sent.")

        secret_key = TOTP.generate_secret()
        code = TOTP.create(secret=secret_key)

        message = f"کد یکبار مصرف شما: {code}"
        # stat = send_sms_task.send(phone_number, message)
        stat = (phone_number, message)
        print(stat)

        if stat:
            logger.info(f"OTP sent to {phone_number}")
            await cache.aset(cache_key, secret_key, settings.TOTP_PERIOD)
            data = {"detail": "The OTP has been sent."}
            return data

        else:
            logger.error(f"Failed to send OTP to {phone_number}")
            raise HttpError(HTTPStatus.BAD_REQUEST, "The OTP has not been sent.")

    @staticmethod
    async def verify_otp(phone_number: str, code: str) -> dict:
        logger.info(f"Verifying OTP for {phone_number}")
        cache_key = f"auth_otp:{phone_number}:secret_key"

        secret_key = await cache.aget(cache_key)
        if not secret_key:
            logger.warning(f"OTP expired or invalid for {phone_number}")
            raise HttpError(HTTPStatus.BAD_REQUEST, "The OTP is expired or invalid.")

        verified = TOTP.verify(secret_key, code)
        if verified:
            logger.info(f"OTP verified for {phone_number}")
            await cache.adelete_many([cache_key])
            data = {"detail": "The OTP is valid"}
            return data

        else:
            logger.warning(f"Invalid OTP attempt for {phone_number}")
            raise HttpError(HTTPStatus.BAD_REQUEST, "The OTP is expired or invalid.")
