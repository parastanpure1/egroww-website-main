"""
URL configuration for egroww project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import public_home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", public_home, name="public_home"),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
