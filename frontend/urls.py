from django.urls import path
from .views import dashboard_view, products_view, inventory_view, alerts_view, login_view, logout_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("products-page/", products_view, name="products_page"),
    path("inventory-page/", inventory_view, name="inventory_page"),
    path("alerts-page/", alerts_view, name="alerts_page"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]