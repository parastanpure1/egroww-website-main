from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import User
from products.models import Product

from .forms import OrderCreateForm, OrderStatusForm
from .models import Order


class FarmerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.role == User.Role.FARMER


class VendorOrderRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.role in {User.Role.VENDOR, User.Role.ADMIN}

    def get_vendor_queryset(self):
        queryset = Order.objects.select_related("product", "user", "product__vendor")
        user = self.request.user
        if user.is_superuser or user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(product__vendor=user)


class OrderCreateView(FarmerRequiredMixin, CreateView):
    model = Order
    template_name = "orders/order_form.html"
    form_class = OrderCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs["product_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.product
        return context

    def get_initial(self):
        user = self.request.user
        return {
            "full_name": user.get_full_name(),
        }

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("orders:history")


class OrderHistoryView(FarmerRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.select_related("product", "product__vendor")
            .filter(user=self.request.user)
        )


class OrderDetailView(FarmerRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.select_related("product", "product__vendor").filter(
            user=self.request.user
        )


class VendorOrderStatusUpdateView(VendorOrderRequiredMixin, UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = "orders/order_status_form.html"

    def get_queryset(self):
        return self.get_vendor_queryset()

    def get_success_url(self):
        return reverse_lazy("accounts:vendor_dashboard")


class VendorOrderMarkDeliveredView(VendorOrderRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(self.get_vendor_queryset(), pk=kwargs["pk"])
        order.status = Order.Status.DELIVERED
        order.save(update_fields=["status"])
        messages.success(request, "Order marked as delivered.")
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("accounts:vendor_dashboard")


class CompletedOrdersView(VendorOrderRequiredMixin, ListView):
    model = Order
    template_name = "orders/completed_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return self.get_vendor_queryset().filter(status=Order.Status.DELIVERED)
