from django.urls import path
from .views import dashboard_view, products_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("products-page/", products_view, name="products_page"),
]