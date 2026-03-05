from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem
from inventory.models import StockItem, StockMovement


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderItemInline]
    list_display = ("id", "supplier", "status", "order_date", "expected_delivery")

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = PurchaseOrder.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # Only run when status changes to RECEIVED
        if previous_status != self.RECEIVED and self.status == self.RECEIVED:
            for item in self.items.all():
                stock_item, _ = StockItem.objects.get_or_create(
                    product=item.product,
                    defaults={"reorder_level": 0, "reorder_qty": 0},
                )
                StockMovement.objects.create(
                    stock_item=stock_item,
                    movement_type=StockMovement.IN,
                    quantity=item.quantity,
                    reference=f"PO-{self.id} received",
                )


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ("purchase_order", "product", "quantity", "unit_price")