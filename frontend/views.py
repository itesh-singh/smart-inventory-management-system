from django.shortcuts import render
from products.models import Product
from inventory.models import StockItem
from orders.models import Sale
from alerts.models import Alert
from django.db import models

def dashboard_view(request):

    total_products = Product.objects.count()
    low_stock = StockItem.objects.filter(
        quantity_on_hand__lte=models.F("reorder_level")
    ).count()

    total_sales = Sale.objects.count()
    active_alerts = Alert.objects.filter(is_resolved=False).count()

    context = {
        "total_products": total_products,
        "low_stock": low_stock,
        "total_sales": total_sales,
        "active_alerts": active_alerts,
    }

    return render(request, "frontend/dashboard.html", context)

def products_view(request):

    products = Product.objects.all()

    context = {
        "products": products
    }

    return render(request, "frontend/products.html", context)

def inventory_view(request):
    stock_items = StockItem.objects.select_related("product").all()

    context = {
        "stock_items": stock_items
    }

    return render(request, "frontend/inventory.html", context)

def alerts_view(request):

    alerts = Alert.objects.select_related("product").order_by("-created_at")

    context = {
        "alerts": alerts
    }

    return render(request, "frontend/alerts.html", context)