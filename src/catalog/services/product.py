from catalog.models import Category, Product


def create_category_service(payload: dict) -> Category:
    return Category.objects.create(**payload)


def update_category_service(category_id: int, payload: dict) -> Category:
    category = Category.objects.get(id=category_id)
    for attr, val in payload.items():
        if val is not None:
            setattr(category, attr, val)
    category.save()
    return category


def delete_category_service(category_id: int) -> None:
    category = Category.objects.get(id=category_id)
    category.delete()


def create_product_service(payload: dict) -> Product:
    return Product.objects.create(**payload)


def update_product_service(product_id: int, payload: dict) -> Product:
    product = Product.objects.get(id=product_id)
    for attr, val in payload.items():
        if val is not None:
            setattr(product, attr, val)
    product.save()
    return product


def delete_product_service(product_id: int) -> None:
    product = Product.objects.get(id=product_id)
    product.delete()
