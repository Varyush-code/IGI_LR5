from django.shortcuts import render
from apps.employees.models import Employee
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)

class EmployeesListView(ListView):
    model = Employee
    template_name = 'employees/contacts.html'
    context_object_name = 'contacts'

class EmployeesCreateView(CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'employees/create.html'
    success_url = reverse_lazy('employees:contacts')

class EmployeesUpdateView(UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'employees/update.html'
    success_url = reverse_lazy('employees:contacts')

class EmployeesDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employees:contacts')