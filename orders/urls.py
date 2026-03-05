from django.urls import path
from .views import ReorderSuggestionView

urlpatterns = [
    path("reorder-suggestions/", ReorderSuggestionView.as_view(), name="reorder-suggestions"),
]