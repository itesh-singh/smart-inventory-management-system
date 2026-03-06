from django.urls import path
from .views import StockItemListView, StockItemDetailView, StockMovementListView, StockMovementDetailView

urlpatterns = [
    path("", StockItemListView.as_view(), name="stockitem-list"),
    path("<int:pk>/", StockItemDetailView.as_view(), name="stockitem-detail"),
    path("movements/", StockMovementListView.as_view(), name="stockmovement-list"),
    path("movements/<int:pk>/", StockMovementDetailView.as_view(), name="stockmovement-detail"),
]