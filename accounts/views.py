from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import User
from orders.models import Order
from products.models import Product


def public_home(request):
    featured_products = Product.objects.select_related("vendor")[:3]
    return render(
        request,
        "home.html",
        {"featured_products": featured_products},
    )


def get_redirect_url_for_user(user):
    if user.is_superuser or user.role in {User.Role.ADMIN, User.Role.VENDOR}:
        return reverse("accounts:vendor_dashboard")
    return reverse("accounts:home")


@login_required
def home(request):
    return render(request, "accounts/home.html")


@login_required
@user_passes_test(
    lambda user: user.is_superuser or user.role in {User.Role.ADMIN, User.Role.VENDOR}
)
def vendor_dashboard(request):
    vendor_orders = (
        Order.objects.select_related("product", "user", "product__vendor")
        .filter(product__vendor=request.user)
        .exclude(status=Order.Status.DELIVERED)
        .order_by("-created_at")[:5]
    )
    if request.user.is_superuser or request.user.role == User.Role.ADMIN:
        vendor_orders = Order.objects.select_related(
            "product", "user", "product__vendor"
        ).exclude(status=Order.Status.DELIVERED).order_by("-created_at")[:5]
    return render(
        request,
        "accounts/vendor_dashboard.html",
        {"vendor_orders": vendor_orders},
    )


class RegisterView(FormView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(get_redirect_url_for_user(request.user))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(get_redirect_url_for_user(user))


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(get_redirect_url_for_user(request.user))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return get_redirect_url_for_user(self.request.user)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
