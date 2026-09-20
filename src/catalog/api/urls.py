from ninja import Router
from catalog.api.views.product import router as product_router

router = Router(tags=["Catalog"])
router.add_router("/", product_router)
