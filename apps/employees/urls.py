from django.urls import path
from .views import EmployeesListView, EmployeesCreateView, EmployeesDeleteView, EmployeesUpdateView

app_name = 'employees' 

urlpatterns = [
    path('', EmployeesListView.as_view(), name='contacts'),
    path('create/', EmployeesCreateView.as_view(), name='create'),
    path('<int:pk>/update/', EmployeesUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', EmployeesDeleteView.as_view(), name='delete'),
]