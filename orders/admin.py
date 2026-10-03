from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "status", "city", "state", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "product__name", "full_name", "phone_number", "city", "state", "pincode")
