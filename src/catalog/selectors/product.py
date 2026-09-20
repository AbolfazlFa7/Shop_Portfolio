from catalog.models import Category, Product


def fetch_categories():
    return Category.objects.filter(is_active=True)


def fetch_category(category_id: int):
    return Category.objects.get(id=category_id, is_active=True)


def fetch_products(category_slug: str | None = None):
    qs = Product.objects.filter(is_available=True)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    return qs


def fetch_product(product_id: int):
    return Product.objects.get(id=product_id, is_available=True)
