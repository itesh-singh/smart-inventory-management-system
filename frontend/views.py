from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from products.models import Product
from inventory.models import StockItem
from orders.models import Sale
from alerts.models import Alert
from django.db import models
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            context["error"] = True

    return render(request, "frontend/login.html", context)


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

    last_7_days = timezone.now() - timedelta(days=7)

    sales_data = (
        Sale.objects.filter(created_at__gte=last_7_days)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    labels = [str(item["day"]) for item in sales_data]
    data = [item["count"] for item in sales_data]
    low_stock_items = (
        StockItem.objects.filter(quantity_on_hand__lte=models.F("reorder_level"))
        .select_related("product")
    )

    low_stock_labels = [item.product.name for item in low_stock_items]
    low_stock_data = [item.quantity_on_hand for item in low_stock_items]
    context = {
    "total_products": total_products,
    "low_stock": low_stock,
    "total_sales": total_sales,
    "active_alerts": active_alerts,
    "sales_labels": labels,
    "sales_data": data,
    "low_stock_labels": low_stock_labels,
    "low_stock_data": low_stock_data,
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