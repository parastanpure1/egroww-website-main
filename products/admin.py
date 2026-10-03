from django.contrib import admin

from .models import Product, Review, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "price", "created_at")
    search_fields = ("name", "vendor__username", "vendor__email")
    list_filter = ("created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username", "user__email")
    list_filter = ("rating", "created_at")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("created_at",)
