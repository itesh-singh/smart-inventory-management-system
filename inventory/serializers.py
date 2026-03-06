from rest_framework import serializers
from .models import StockItem, StockMovement


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

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="stock_item.product.name", read_only=True)
    sku = serializers.CharField(source="stock_item.product.sku", read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            "id",
            "product_name",
            "sku",
            "movement_type",
            "quantity",
            "reference",
            "created_at",
        ]