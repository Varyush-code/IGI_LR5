from django.shortcuts import render
from django.views.generic import (ListView, DeleteView, CreateView, UpdateView, DetailView)
from .models import Enclosure

class EncListView(ListView):
    model = Enclosure
    template_name = 'enclosures.html'
    context_object_name = 'enclosures'