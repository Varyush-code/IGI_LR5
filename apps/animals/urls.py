from django.urls import path, re_path
from .views import (AnimalListView, AnimalDetailView, AnimalCreateView, AnimalUpdateView, AnimalDeleteView)

app_name = 'animals'

urlpatterns = [
    path('', AnimalListView.as_view(), name='list'),  
    re_path(r'^(?P<pk>\d+)/$', AnimalDetailView.as_view(), name="detail"),
    path('create/', AnimalCreateView.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/update/', AnimalUpdateView.as_view(), name='update'),
    re_path(r'^(?P<pk>\d+)/delete/', AnimalDeleteView.as_view(), name='delete'),
]