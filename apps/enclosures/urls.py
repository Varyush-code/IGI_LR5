from django.urls import path
from .views import EncListView

urlpatterns = [
    path('', EncListView.as_view(), name='enclosures'),
]