from django.shortcuts import render
from .models import Openings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

class OListView(LoginRequiredMixin, ListView):
    model = Openings
    template_name = 'openings/index.html'
    login_url = '/accounts/login/'
    context_object_name = 'openings'

class OCreateView(CreateView):
    model = Openings
    fields = '__all__'
    template_name = 'openings/create.html'
    success_url = reverse_lazy('openings')

class OUpdateView(UpdateView):
    model = Openings
    fields = '__all__'
    template_name = 'openings/update.html'
    success_url = reverse_lazy('openings')

class ODeleteView(DeleteView):
    model = Openings
    template_name = 'openings/delete.html'
    success_url = reverse_lazy('openings')