from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import StockItem
from suppliers.models import SupplierProduct
from django.db import models
from rest_framework import generics
from .models import Sale, Product, SaleItem
from rest_framework import status
from django.db import transaction
from .serializers import SaleSerializer, CreateSaleSerializer



class ReorderSuggestionView(APIView):

    def get(self, request):

        low_stock_items = StockItem.objects.filter(
            quantity_on_hand__lte=models.F("reorder_level")
        )

        suggestions = []

        for item in low_stock_items:

            supplier = SupplierProduct.objects.filter(
                product=item.product
            ).first()

            suggestions.append({
                "product": item.product.name,
                "sku": item.product.sku,
                "current_stock": item.quantity_on_hand,
                "reorder_level": item.reorder_level,
                "suggested_order_qty": item.reorder_qty,
                "supplier": supplier.supplier.name if supplier else None
            })

        return Response(suggestions)
    
class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all().order_by("-id")
    serializer_class = SaleSerializer

class SaleDetailView(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    
class CreateSaleView(APIView):

    def post(self, request):

        serializer = CreateSaleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        customer_name = data["customer_name"]
        items = data["items"]

        with transaction.atomic():
            sale = Sale.objects.create(customer_name=customer_name)

            for item in items:
                product = Product.objects.get(id=item["product_id"])

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=item["quantity"],
                    unit_price=item["unit_price"]
                )

        return Response(
            {"message": "Sale created successfully", "sale_id": sale.id},
            status=201
        )