from django.db import models
from products.models import Product
from django.core.exceptions import ValidationError
from alerts.models import Alert


class StockItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    reorder_qty = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.sku} - {self.quantity_on_hand}"


class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"

    MOVEMENT_TYPES = [
        (IN, "Stock In"),
        (OUT, "Stock Out"),
        (ADJUST, "Adjustment"),
    ]

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} for {self.stock_item.product.sku}"

    def clean(self):
        if self.pk is None and self.movement_type == self.OUT:
            stock = self.stock_item
            if self.quantity > stock.quantity_on_hand:
                raise ValidationError({"quantity": "Insufficient stock for OUT movement."})

    def save(self, *args, **kwargs):
        creating = self.pk is None

        self.full_clean()
        super().save(*args, **kwargs)

        if creating:
            stock = self.stock_item

            if self.movement_type == self.IN:
                stock.quantity_on_hand += self.quantity
            elif self.movement_type == self.OUT:
                stock.quantity_on_hand -= self.quantity
            else:
                stock.quantity_on_hand = self.quantity

            stock.save()

            # resolve all existing active alerts first
            Alert.objects.filter(
                product=stock.product,
                is_resolved=False
            ).update(is_resolved=True)

            # create the correct current alert only if needed
            if stock.quantity_on_hand == 0:
                Alert.objects.create(
                    alert_type=Alert.OUT_OF_STOCK,
                    product=stock.product,
                    message=f"{stock.product.name} is out of stock.",
                    is_resolved=False,
                )

            elif stock.quantity_on_hand <= stock.reorder_level:
                Alert.objects.create(
                    alert_type=Alert.LOW_STOCK,
                    product=stock.product,
                    message=f"{stock.product.name} is running low.",
                    is_resolved=False,
                )