from rest_framework import serializers
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity", "unit_price"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ["id", "customer_name", "sale_date", "items"]


class CreateSaleItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CreateSaleSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    items = CreateSaleItemSerializer(many=True)