from catalog.models import Product

def create_product_service(payload: dict) -> Product:
    return Product.objects.create(**payload)

def update_product_service(product_id: int, payload: dict) -> Product:
    product = Product.objects.get(id=product_id)
    for attr, val in payload.items():
        setattr(product, attr, val)
    product.save()
    return product
