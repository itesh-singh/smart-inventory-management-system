from django.urls import path
from .views import StockItemListView, StockItemDetailView

urlpatterns = [
    path("", StockItemListView.as_view(), name="stockitem-list"),
    path("<int:pk>/", StockItemDetailView.as_view(), name="stockitem-detail"),
]