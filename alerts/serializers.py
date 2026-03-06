from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "alert_type",
            "product",
            "product_name",
            "sku",
            "message",
            "is_resolved",
            "created_at",
        ]