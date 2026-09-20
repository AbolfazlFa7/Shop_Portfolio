from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Category, Product
from finance.models import Wallet, WalletTransaction
from promotions.models import Coupon

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with minimal realistic test data"

    def handle(self, *args, **options):
        WalletTransaction.objects.all().delete()
        Wallet.objects.all().delete()
        Coupon.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        user, _ = User.objects.get_or_create(
            phone_number="09123456789",
            defaults={"username": "shop_user", "is_active": True},
        )

        cat1 = Category.objects.create(name="Electronics", slug="electronics")
        cat2 = Category.objects.create(name="Clothing", slug="clothing")

        Product.objects.create(
            name="Smartphone",
            slug="smartphone",
            sku="EL-001",
            category=cat1,
            price=15000000,
            stock=10,
        )
        Product.objects.create(
            name="T-Shirt",
            slug="t-shirt",
            sku="CL-001",
            category=cat2,
            price=500000,
            stock=50,
        )

        Coupon.objects.create(
            code="OFF10",
            description="10% Discount",
            discount_type="percent",
            discount_value=10,
            start_date=timezone.now(),
            min_order_amount=100000,
        )

        wallet = Wallet.objects.create(
            user=user, type=Wallet.WalletType.PERSONAL, balance=1000000
        )

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=1000000,
            type=WalletTransaction.Type.DEPOSIT,
            status=WalletTransaction.Status.SUCCESSFUL,
            reference_id="ref_seed_001",
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
