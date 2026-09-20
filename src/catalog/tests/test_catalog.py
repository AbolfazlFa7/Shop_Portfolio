import pytest
from catalog.models import Category, Product


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Electronics", slug="electronics")
    assert category.name == "Electronics"
    assert str(category) == "Electronics"


@pytest.mark.django_db
def test_category_slug_unique():
    Category.objects.create(name="Books", slug="books")
    with pytest.raises(Exception):
        Category.objects.create(name="Books 2", slug="books")


@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(name="Clothing", slug="clothing")
    product = Product.objects.create(
        name="T-Shirt",
        slug="t-shirt",
        sku="TS123",
        category=category,
        price=1000,
        stock=50,
    )
    assert product.name == "T-Shirt"
    assert product.price == 1000
    assert str(product) == "T-Shirt (TS123)"


@pytest.mark.django_db
def test_product_availability():
    product = Product.objects.create(
        name="Laptop",
        slug="laptop",
        price=50000,
        is_available=False,
    )
    assert not product.is_available


@pytest.mark.django_db
def test_product_stock_default():
    product = Product.objects.create(
        name="Mouse",
        slug="mouse",
        price=500,
    )
    assert product.stock == 0


@pytest.mark.django_db
def test_category_parent():
    parent = Category.objects.create(name="Home", slug="home")
    child = Category.objects.create(name="Kitchen", slug="kitchen", parent=parent)
    assert child.parent == parent
    assert parent.children.first() == child
