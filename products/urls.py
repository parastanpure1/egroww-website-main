from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductReviewCreateView,
    ProductUpdateView,
    WishlistListView,
    WishlistToggleView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("add/", ProductCreateView.as_view(), name="add"),
    path("wishlist/", WishlistListView.as_view(), name="wishlist"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/review/", ProductReviewCreateView.as_view(), name="review"),
    path("<int:pk>/wishlist/", WishlistToggleView.as_view(), name="wishlist_toggle"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]
