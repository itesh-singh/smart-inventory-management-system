from django.db import models
from suppliers.models import Supplier
from products.models import Product
from inventory.models import StockItem, StockMovement
from django.core.exceptions import ValidationError

class PurchaseOrder(models.Model):

    PENDING = "PENDING"
    ORDERED = "ORDERED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ORDERED, "Ordered"),
        (RECEIVED, "Received"),
        (CANCELLED, "Cancelled"),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchase_orders")
    order_date = models.DateField(auto_now_add=True)
    expected_delivery = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO-{self.id} - {self.supplier.name}"
    
    def clean(self):
        if self.pk:
            previous_status = PurchaseOrder.objects.get(pk=self.pk).status
            if previous_status == self.RECEIVED and self.status != self.RECEIVED:
                raise ValidationError({"status": "Received purchase orders cannot be modified."})   
    
    def save(self, *args, **kwargs):
        previous_status = None

        if self.pk:
            previous_status = PurchaseOrder.objects.get(pk=self.pk).status

        # block changes if already received
        self.full_clean()
        super().save(*args, **kwargs)

        if previous_status != self.RECEIVED and self.status == self.RECEIVED:
            for item in self.items.all():
                stock_item, _ = StockItem.objects.get_or_create(
                    product=item.product,
                    defaults={"quantity_on_hand": 0, "reorder_level": 0, "reorder_qty": 0},
                )

                StockMovement.objects.create(
                    stock_item=stock_item,
                    movement_type=StockMovement.IN,
                    quantity=item.quantity,
                    reference=f"PO-{self.id} received",
                )
    

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"PO-{self.purchase_order.id} - {self.product.sku} x {self.quantity}"
    
    def clean(self):
        if self.purchase_order.status == PurchaseOrder.RECEIVED:
            raise ValidationError("Cannot modify items of a received purchase order.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Sale(models.Model):
    customer_name = models.CharField(max_length=255)
    sale_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale-{self.id} - {self.customer_name}"
    

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale-{self.sale.id} - {self.product.sku} x {self.quantity}"
    
    def clean(self):
        stock_item = self.product.stock
        if self.quantity > stock_item.quantity_on_hand:
            raise ValidationError({"quantity": "Not enough stock available for this sale."})

    def save(self, *args, **kwargs):
        creating = self.pk is None

        self.full_clean()
        super().save(*args, **kwargs)

        if creating:
            stock_item = self.product.stock

            StockMovement.objects.create(
                stock_item=stock_item,
                movement_type=StockMovement.OUT,
                quantity=self.quantity,
                reference=f"Sale-{self.sale.id}",
            )