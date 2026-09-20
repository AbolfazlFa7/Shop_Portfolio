import base64
import logging
import secrets

from django.conf import settings
from pyotp import TOTP as time_based_otp

logger = logging.getLogger(__name__)


class TimeBased_OTP:
    @staticmethod
    def generate_secret() -> str:
        logger.info("Generating TOTP secret")
        return base64.b32encode(secrets.token_bytes(20)).decode("utf-8")

    @staticmethod
    def create(secret: str) -> str:
        logger.info("Creating TOTP code")
        totp = time_based_otp(
            secret, digits=settings.TOTP_DIGITS, interval=settings.TOTP_PERIOD
        )
        return totp.now()

    @staticmethod
    def verify(secret: str, code: str) -> bool:
        logger.info("Verifying TOTP code")
        totp = time_based_otp(
            secret,
            digits=settings.TOTP_DIGITS,
            interval=settings.TOTP_PERIOD,
        )
        return totp.verify(code)
