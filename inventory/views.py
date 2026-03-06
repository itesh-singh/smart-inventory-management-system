from rest_framework import generics
from .models import StockItem
from .serializers import StockItemSerializer


class StockItemListView(generics.ListAPIView):
    queryset = StockItem.objects.all().order_by("-id")
    serializer_class = StockItemSerializer


class StockItemDetailView(generics.RetrieveAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer