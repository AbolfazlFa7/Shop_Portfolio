import dramatiq

from common.providers.sms import MeliPayamak


@dramatiq.actor(
    max_retries=2,
    min_backoff=1000,
    max_backoff=9000,
    time_limit=6000,
)
def send_sms_task(
    mobile_number: str,
    message: str,
):
    return MeliPayamak.send_sms(
        mobile_number,
        message,
    )
