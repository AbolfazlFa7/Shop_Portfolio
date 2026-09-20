import pytest
from catalog.models import Category


@pytest.fixture
def sample_category(db):
    return Category.objects.create(name="Sample Category", slug="sample-category")
