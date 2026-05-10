from django.urls import path
from .views import feeding_list

urlpatterns = [
    path('',feeding_list,name='feeding_list'),
]