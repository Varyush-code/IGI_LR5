from django.urls import path
from .views import review_list
from .views import review_create


urlpatterns = [
    path('',review_list,name='reviews'),
    path('create/',review_create,name='review_create'),
]