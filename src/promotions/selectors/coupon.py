from django.db import models
from django.utils import timezone

from promotions.models import Coupon


def get_valid_coupon(code: str):
    return (
        Coupon.objects.filter(code=code, is_active=True, start_date__lte=timezone.now())
        .filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=timezone.now())
        )
        .first()
    )
