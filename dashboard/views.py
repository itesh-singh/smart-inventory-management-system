from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from inventory.models import StockItem
from orders.models import Sale, PurchaseOrder
from django.db.models import Sum
from django.db import models


class DashboardSummaryView(APIView):

    def get(self, request):

        total_products = Product.objects.count()

        total_stock = StockItem.objects.aggregate(
            total=Sum("quantity_on_hand")
        )["total"] or 0

        low_stock = StockItem.objects.filter(
            quantity_on_hand__lte=models.F("reorder_level")
        ).count()

        total_sales = Sale.objects.count()

        total_purchase_orders = PurchaseOrder.objects.count()

        data = {
            "total_products": total_products,
            "total_stock": total_stock,
            "low_stock_items": low_stock,
            "total_sales": total_sales,
            "total_purchase_orders": total_purchase_orders
        }

        return Response(data)