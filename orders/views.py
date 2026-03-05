from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import StockItem
from suppliers.models import SupplierProduct
from django.db import models


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