from rest_framework import generics
from .models import StockItem, StockMovement
from .serializers import StockItemSerializer, StockMovementSerializer


class StockItemListView(generics.ListAPIView):
    queryset = StockItem.objects.all().order_by("-id")
    serializer_class = StockItemSerializer


class StockItemDetailView(generics.RetrieveAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer


class StockMovementListView(generics.ListAPIView):
    queryset = StockMovement.objects.all().order_by("-id")
    serializer_class = StockMovementSerializer


class StockMovementDetailView(generics.RetrieveAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer