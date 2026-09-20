import logging
from catalog.models import Category, Product

logger = logging.getLogger(__name__)


def create_category_service(payload: dict) -> Category:
    logger.info(f"Creating category: {payload.get('name')}")
    return Category.objects.create(**payload)


def update_category_service(category_id: int, payload: dict) -> Category:
    logger.info(f"Updating category: {category_id}")
    category = Category.objects.get(id=category_id)
    for attr, val in payload.items():
        if val is not None:
            setattr(category, attr, val)
    category.save()
    return category


def delete_category_service(category_id: int) -> None:
    logger.info(f"Deleting category: {category_id}")
    category = Category.objects.get(id=category_id)
    category.delete()


def create_product_service(payload: dict) -> Product:
    logger.info(f"Creating product: {payload.get('name')}")
    return Product.objects.create(**payload)


def update_product_service(product_id: int, payload: dict) -> Product:
    logger.info(f"Updating product: {product_id}")
    product = Product.objects.get(id=product_id)
    for attr, val in payload.items():
        if val is not None:
            setattr(product, attr, val)
    product.save()
    return product


def delete_product_service(product_id: int) -> None:
    logger.info(f"Deleting product: {product_id}")
    product = Product.objects.get(id=product_id)
    product.delete()
