from datetime import datetime

from ninja import Schema


class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    parent_id: int | None = None
    is_active: bool


class CategoryCreateSchema(Schema):
    name: str
    slug: str
    parent_id: int | None = None
    is_active: bool = True


class CategoryUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    parent_id: int | None = None
    is_active: bool | None = None


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


class ProductUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    sku: str | None = None
    category_id: int | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    is_available: bool | None = None
