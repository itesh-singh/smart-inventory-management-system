from django.db import models
from products.models import Product


class Alert(models.Model):
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"

    ALERT_TYPES = [
        (LOW_STOCK, "Low Stock"),
        (OUT_OF_STOCK, "Out of Stock"),
    ]

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} - {self.product.sku}"