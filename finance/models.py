from django.conf import settings
from django.db import models

from businesses.models import Business
from common.models import EncryptedCharField
from common.services.security.encryption import hmac_service


class Wallet(models.Model):
    class WalletType(models.TextChoices):
        PERSONAL = "PERSONAL", "Personal"  # ولت معمولی کلاینت
        BUSINESS = "BUSINESS", "Business"  # ولت اختصاصی بیزنس
        ESCROW = "ESCROW", "Escrow (System)"  # پول‌های امانی
        REVENUE = "REVENUE", "Platform Revenue"  # کارمزد و درآمد خالص پلتفرم

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets",
        db_index=True,
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="wallet",
        db_index=True,
    )
    type = models.CharField(
        max_length=20,
        choices=WalletType.choices,
        default=WalletType.PERSONAL,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    balance = models.PositiveBigIntegerField(default=0)
    card_number = EncryptedCharField(max_length=512, null=True, blank=True)
    card_number_hmac = models.CharField(
        max_length=64, null=True, blank=True, db_index=True
    )
    shaba_number = EncryptedCharField(max_length=512, null=True, blank=True)
    account_number = EncryptedCharField(max_length=512, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0), name="wallet_balance_non_negative"
            ),
            models.UniqueConstraint(
                fields=["user", "business", "type"],
                name="unique_user_business_wallet_type",
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(type="BUSINESS", business__isnull=False)
                    | models.Q(~models.Q(type="BUSINESS"), business__isnull=True)
                ),
                name="wallet_type_business_match",
            ),
        ]

    @classmethod
    def find_by_card_number(cls, card_number) -> models.QuerySet[Wallet]:
        h = hmac_service.compute(card_number)
        return cls.objects.filter(card_number_hmac=h)


class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
        BOOKING_PAYMENT = "BOOKING_PAYMENT", "Booking Payment"
        SYSTEM_PAYMENT = "SYSTEM_PAYMENT", "System Payment"
        REFUND = "REFUND", "Refund"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        FAILED = "FAILED", "Failed"

    wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, db_index=True, related_name="transactions"
    )
    amount = models.PositiveBigIntegerField()
    balance_before = models.PositiveBigIntegerField(null=True, blank=True)
    balance_after = models.PositiveBigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    transaction_group_id = models.UUIDField(null=True, blank=True, db_index=True)
    reference_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["transaction_group_id"]),
        ]
