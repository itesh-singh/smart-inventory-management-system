from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from suppliers.models import Supplier
from inventory.models import StockItem
from orders.models import PurchaseOrder
from alerts.models import Alert
from django.db import models


class DashboardStatsView(APIView):

    def get(self, request):

        total_products = Product.objects.count()
        total_suppliers = Supplier.objects.count()

        low_stock_items = StockItem.objects.filter(
            quantity_on_hand__lte=models.F("reorder_level"),
            quantity_on_hand__gt=0
        ).count()

        out_of_stock_items = StockItem.objects.filter(
            quantity_on_hand=0
        ).count()

        pending_purchase_orders = PurchaseOrder.objects.filter(
            status=PurchaseOrder.PENDING
        ).count()

        unresolved_alerts = Alert.objects.filter(
            is_resolved=False
        ).count()

        data = {
            "total_products": total_products,
            "total_suppliers": total_suppliers,
            "low_stock_items": low_stock_items,
            "out_of_stock_items": out_of_stock_items,
            "pending_purchase_orders": pending_purchase_orders,
            "unresolved_alerts": unresolved_alerts,
        }

        return Response(data)