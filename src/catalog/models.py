from django.db import models
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["slug", "is_active"]),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    sku = models.CharField(
        max_length=20, unique=True, blank=True, null=True, db_index=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField(db_index=True)
    stock = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    is_available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["slug", "is_available"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")
    is_feature = models.BooleanField(default=False)

    class Meta:
        ordering = ("-is_feature",)
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_feature=True),
                name="unique_featured_image_per_product",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    key = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=100)

    class Meta:
        ordering = ("key",)

    def __str__(self):
        return self.key
