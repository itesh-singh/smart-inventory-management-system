from django.urls import path
from .views import ReorderSuggestionView, SaleListView, CreateSaleView, SaleDetailView

urlpatterns = [
    path("reorder-suggestions/", ReorderSuggestionView.as_view(), name="reorder-suggestions"),
    path("sales/", SaleListView.as_view(), name="sales-list"),
    path("sales/<int:pk>/", SaleDetailView.as_view(), name="sale-detail"),
    path("sales/create/", CreateSaleView.as_view(), name="create-sale"),
]