from ninja import Router
from product.api.views import product

router = Router(tags=["Product"])
router.add_router("/products", product.router)
