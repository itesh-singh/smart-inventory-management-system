from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from products.models import Product
from inventory.models import StockItem
from orders.models import Sale
from alerts.models import Alert
from django.db import models


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "frontend/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
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


@login_required
def products_view(request):
    products = Product.objects.all()
    return render(request, "frontend/products.html", {"products": products})


@login_required
def inventory_view(request):
    stock_items = StockItem.objects.select_related("product").all()
    return render(request, "frontend/inventory.html", {"stock_items": stock_items})


@login_required
def alerts_view(request):
    alerts = Alert.objects.select_related("product").order_by("-created_at")
    return render(request, "frontend/alerts.html", {"alerts": alerts})