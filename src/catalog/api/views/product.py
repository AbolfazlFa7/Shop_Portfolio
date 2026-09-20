from ninja import Router
from catalog.selectors.product import fetch_products, fetch_categories
from catalog.schemas.product import ProductSchema, CategorySchema, ProductCreateSchema
from catalog.services.product import create_product_service

router = Router()

@router.get("/products", response=list[ProductSchema])
def list_products(request, category_slug: str | None = None):
    return list(fetch_products(category_slug))

@router.get("/categories", response=list[CategorySchema])
def list_categories(request):
    return list(fetch_categories())

@router.post("/products", response=ProductSchema)
def create_product(request, payload: ProductCreateSchema):
    return create_product_service(payload.dict())
