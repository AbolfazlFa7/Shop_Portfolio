import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class MeliPayamak:
    URL = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"

    @classmethod
    def send_sms(cls, mobile_number: str, message: str) -> bool:
        logger.info(f"Sending SMS to {mobile_number} via MeliPayamak")
        payload = {
            "username": settings.MELIPAYAMAK_USERNAME,
            "password": settings.MELIPAYAMAK_PASSWORD,
            "to": mobile_number,
            "from": settings.MELIPAYAMAK_PHONE_NUMBER,
            "text": message,
            "isFlash": False,
        }

        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                cls.URL,
                data=payload,
            )

        response.raise_for_status()
        success = response.status_code == 200
        if success:
            logger.info(f"SMS successfully sent to {mobile_number}")
        else:
            logger.error(
                f"Failed to send SMS to {mobile_number}, status code: {response.status_code}"
            )
        return success
