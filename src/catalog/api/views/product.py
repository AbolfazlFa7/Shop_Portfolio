from ninja import Router, Status
from ninja.pagination import paginate

from catalog.schemas.product import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
)
from catalog.selectors.product import (
    fetch_categories,
    fetch_category,
    fetch_product,
    fetch_products,
)
from catalog.services.product import (
    create_category_service,
    create_product_service,
    delete_category_service,
    delete_product_service,
    update_category_service,
    update_product_service,
)
from common.schemas.responses import DetailResponse
from common.services.jwt import JWTAuth

router = Router()


@router.get("/products", auth=JWTAuth(), response=list[ProductSchema])
@paginate
async def list_products(request, category_slug: str | None = None):
    return fetch_products(category_slug)


@router.get("/products/{product_id}", auth=JWTAuth(), response=ProductSchema)
async def get_product(request, product_id: int):
    return fetch_product(product_id)


@router.post("/products", auth=JWTAuth(), response={201: ProductSchema})
async def create_product(request, payload: ProductCreateSchema):
    product = create_product_service(payload.dict())
    return Status(201, product)


@router.patch("/products/{product_id}", auth=JWTAuth(), response=ProductSchema)
async def update_product(request, product_id: int, payload: ProductUpdateSchema):
    return update_product_service(product_id, payload.dict(exclude_unset=True))


@router.delete("/products/{product_id}", auth=JWTAuth(), response=DetailResponse)
async def delete_product(request, product_id: int):
    delete_product_service(product_id)
    return Status(200, {"detail": "Product deleted successfully"})


@router.get("/categories", auth=JWTAuth(), response=list[CategorySchema])
@paginate
async def list_categories(request):
    return fetch_categories()


@router.get("/categories/{category_id}", auth=JWTAuth(), response=CategorySchema)
async def get_category(request, category_id: int):
    return fetch_category(category_id)


@router.post("/categories", auth=JWTAuth(), response={201: CategorySchema})
async def create_category(request, payload: CategoryCreateSchema):
    category = create_category_service(payload.dict())
    return Status(201, category)


@router.patch("/categories/{category_id}", auth=JWTAuth(), response=CategorySchema)
async def update_category(request, category_id: int, payload: CategoryUpdateSchema):
    return update_category_service(category_id, payload.dict(exclude_unset=True))


@router.delete("/categories/{category_id}", auth=JWTAuth(), response=DetailResponse)
async def delete_category(request, category_id: int):
    delete_category_service(category_id)
    return Status(200, {"detail": "Category deleted successfully"})
