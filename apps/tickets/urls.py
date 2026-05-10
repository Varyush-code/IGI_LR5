from django.urls import path
from .views import ticket_home
from .views import ticket_create
from .views import my_tickets

urlpatterns = [
    path('',ticket_home,name='tickets'),
    path('create/',ticket_create,name="ticket_create"),
    path('my/',my_tickets,name="my_tickets")
]