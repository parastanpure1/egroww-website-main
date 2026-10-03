from django.urls import path

from .views import (
    CompletedOrdersView,
    OrderCreateView,
    OrderDetailView,
    OrderHistoryView,
    VendorOrderMarkDeliveredView,
    VendorOrderStatusUpdateView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderHistoryView.as_view(), name="history"),
    path("completed/", CompletedOrdersView.as_view(), name="completed"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("buy/<int:product_pk>/", OrderCreateView.as_view(), name="buy"),
    path("<int:pk>/delivered/", VendorOrderMarkDeliveredView.as_view(), name="mark_delivered"),
    path("<int:pk>/status/", VendorOrderStatusUpdateView.as_view(), name="status_update"),
]
