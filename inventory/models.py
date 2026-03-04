from django.db import models
from products.models import Product


class StockItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    reorder_qty = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.sku} - {self.quantity_on_hand}"