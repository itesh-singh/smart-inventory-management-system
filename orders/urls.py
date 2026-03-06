from django.urls import path
from .views import ReorderSuggestionView, SaleListView, CreateSaleView

urlpatterns = [
    path("reorder-suggestions/", ReorderSuggestionView.as_view(), name="reorder-suggestions"),
    path("sales/", SaleListView.as_view(), name="sales-list"),
    path("sales/create/", CreateSaleView.as_view(), name="create-sale"),
]