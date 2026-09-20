from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ninja import NinjaAPI

from authentication.api.urls import router as auth_router
from catalog.api.urls import router as catalog_router
from promotions.api.urls import router as promotions_router
from finance.api.urls import router as finance_router

api = NinjaAPI(docs_url="/docs/")

if not settings.DEBUG:
    api.openapi_url = None

api.add_router("/auth", auth_router)
api.add_router("/catalog", catalog_router)
api.add_router("/promotions", promotions_router)
api.add_router("/", finance_router)

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
