from ninja import Schema
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    parent_id: int | None = None
    is_active: bool

class ProductAttributeSchema(Schema):
    key: str
    value: str

class ProductImageSchema(Schema):
    image: str
    is_feature: bool

class ProductSchema(Schema):
    id: int
    name: str
    slug: str
    sku: str | None = None
    category_id: int | None = None
    description: str
    price: int
    stock: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

class ProductCreateSchema(Schema):
    name: str
    slug: str
    sku: str | None = None
    category_id: int | None = None
    description: str = ""
    price: int
    stock: int = 0
    is_available: bool = True
