from django.shortcuts import render
from products.models import Product
from inventory.models import StockItem
from orders.models import Sale

def dashboard_view(request):

    total_products = Product.objects.count()
    low_stock = StockItem.objects.filter(quantity_on_hand__lte=5).count()
    total_sales = Sale.objects.count()

    context = {
        "total_products": total_products,
        "low_stock": low_stock,
        "total_sales": total_sales,
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