from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ninja import NinjaAPI

from authentication.api.urls import router as auth_router
from product.api.urls import router as product_router

api = NinjaAPI(docs_url="/docs/")

api.add_router("/auth", auth_router)
api.add_router("/product", product_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
