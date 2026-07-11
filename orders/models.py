from django.db import models
from django.conf import settings


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("CARD", "Card"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    address = models.TextField()

    phone = models.CharField(max_length=15)

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"