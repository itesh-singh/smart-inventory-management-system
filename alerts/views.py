from rest_framework import generics
from .models import Alert
from .serializers import AlertSerializer


class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.all().order_by("-id")
    serializer_class = AlertSerializer


class AlertDetailView(generics.RetrieveAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer