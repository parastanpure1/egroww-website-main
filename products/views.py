from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.models import User

from .forms import ReviewForm
from .models import Product, Review, Wishlist


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.select_related("vendor")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("q", "").strip()
        context["search_query"] = search_query
        context["query_string"] = f"&q={search_query}" if search_query else ""
        if self.request.user.role == User.Role.FARMER:
            context["wishlist_product_ids"] = set(
                self.request.user.wishlist_items.values_list("product_id", flat=True)
            )
        else:
            context["wishlist_product_ids"] = set()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("vendor").prefetch_related(
            "reviews__user"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["reviews"] = product.reviews.select_related("user")
        context["average_rating"] = product.average_rating
        if self.request.user.role == User.Role.FARMER:
            existing_review = product.reviews.filter(user=self.request.user).first()
            context["review_form"] = ReviewForm(instance=existing_review)
            context["is_in_wishlist"] = Wishlist.objects.filter(
                user=self.request.user, product=product
            ).exists()
        return context


class FarmerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role == User.Role.FARMER


class ProductManagementPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def is_admin(self):
        user = self.request.user
        return user.is_superuser or user.role == User.Role.ADMIN

    def is_vendor(self):
        return self.request.user.role == User.Role.VENDOR

    def test_func(self):
        return self.is_admin() or self.is_vendor()


class ProductOwnerOrAdminMixin(ProductManagementPermissionMixin):
    def get_queryset(self):
        if self.is_admin():
            return Product.objects.all()
        return Product.objects.filter(vendor=self.request.user)


class ProductCreateView(ProductManagementPermissionMixin, CreateView):
    model = Product
    template_name = "products/product_form.html"

    def get_product_fields(self):
        if self.is_admin():
            return ["name", "description", "price", "image", "vendor"]
        return ["name", "description", "price", "image"]

    def get_form_class(self):
        return modelform_factory(Product, fields=self.get_product_fields())

    def form_valid(self, form):
        if not self.is_admin():
            form.instance.vendor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("products:detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(ProductOwnerOrAdminMixin, UpdateView):
    model = Product
    template_name = "products/product_form.html"

    def get_product_fields(self):
        if self.is_admin():
            return ["name", "description", "price", "image", "vendor"]
        return ["name", "description", "price", "image"]

    def get_form_class(self):
        return modelform_factory(Product, fields=self.get_product_fields())

    def get_success_url(self):
        return reverse_lazy("products:detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(ProductOwnerOrAdminMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:list")


class ProductReviewCreateView(FarmerRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs["pk"])
        existing_review = Review.objects.filter(
            product=product, user=request.user
        ).first()
        form = self.form_class(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been saved.")
        else:
            messages.error(request, "Please fix the review form and try again.")
        return redirect("products:detail", pk=product.pk)


class WishlistToggleView(FarmerRequiredMixin, CreateView):
    model = Wishlist

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs["pk"])
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if created:
            messages.success(request, "Product added to your wishlist.")
        else:
            wishlist_item.delete()
            messages.success(request, "Product removed from your wishlist.")

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("products:detail", pk=product.pk)


class WishlistListView(FarmerRequiredMixin, ListView):
    model = Wishlist
    template_name = "products/wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.select_related("product", "product__vendor").filter(
            user=self.request.user
        )
