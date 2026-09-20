import pytest
from businesses.models import Business, BusinessCategory, City, Province
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
async def sample_business(db):
    cat, _ = await BusinessCategory.objects.aget_or_create(
        code="BEAUTY", defaults={"name": "Beauty"}
    )
    prov, _ = await Province.objects.aget_or_create(name="Tehran Province")
    city, _ = await City.objects.aget_or_create(province=prov, name="Tehran")
    return await Business.objects.acreate(
        city=city,
        name="Test Business",
        category=cat,
        owner=await User.objects.acreate_user(phone_number="09120000001"),
        address_text="Test Address",
        latitude=0,
        longitude=0,
    )
