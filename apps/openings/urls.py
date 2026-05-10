from django.urls import path
from .views import (OListView, OCreateView, OUpdateView, ODeleteView)

urlpatterns = [
    path('', OListView.as_view(), name='openings'),
    path('create/', OCreateView.as_view(), name='create'),
    path('<int:pk>/update/', OUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ODeleteView.as_view(), name='delete'),
]