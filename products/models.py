from django.conf import settings
from django.db import models
from django.db.models import Avg


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"]


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, "1 Star"
        TWO = 2, "2 Stars"
        THREE = 3, "3 Stars"
        FOUR = 4, "4 Stars"
        FIVE = 5, "5 Stars"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(choices=Rating.choices)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_product_review_per_user",
            )
        ]

    def __str__(self):
        return f"{self.product.name} review by {self.user.username}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_wishlist_item_per_user",
            )
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"
