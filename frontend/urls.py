from django.urls import path
from .views import dashboard_view, products_view, inventory_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("products-page/", products_view, name="products_page"),
    path("inventory-page/", inventory_view, name="inventory_page"),
]