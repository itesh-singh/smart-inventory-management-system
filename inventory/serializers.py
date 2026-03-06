from rest_framework import serializers
from .models import StockItem


class StockItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = StockItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_sku",
            "quantity_on_hand",
            "reorder_level",
            "reorder_qty",
            "updated_at",
        ]