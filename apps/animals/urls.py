from django.urls import path, re_path
from . import views

app_name = 'animals'

urlpatterns = [
    path('', views.index, name='list'),  
    path('create/', views.create, name='create'),
    re_path(r'^(?P<pk>\d+)/update/', views.update, name='update'),
    re_path(r'^(?P<pk>\d+)/delete/', views.delete, name='delete'),
]