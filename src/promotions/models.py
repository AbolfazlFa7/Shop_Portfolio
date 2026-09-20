from django.db import models
from catalog.models import Product


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, default=DiscountType.PERCENT)
    discount_value = models.PositiveBigIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    min_order_amount = models.PositiveBigIntegerField(default=0)
    max_usage = models.PositiveIntegerField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['code', 'is_active']),
        ]

    def __str__(self):
        return f"{self.code} - {self.discount_value}"


class ProductCoupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='coupons')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='products')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'coupon'], name='unique_product_coupon')
        ]
