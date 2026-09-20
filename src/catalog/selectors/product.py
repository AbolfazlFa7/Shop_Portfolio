from catalog.models import Product, Category

def fetch_categories():
    return Category.objects.filter(is_active=True)

def fetch_products(category_slug: str | None = None):
    qs = Product.objects.filter(is_available=True)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    return qs
