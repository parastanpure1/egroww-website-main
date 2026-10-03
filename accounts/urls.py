from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    home,
    vendor_dashboard,
)

app_name = "accounts"

urlpatterns = [
    path("", home, name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("vendor/dashboard/", vendor_dashboard, name="vendor_dashboard"),
]
