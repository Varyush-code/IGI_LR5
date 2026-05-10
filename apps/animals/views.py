from django.shortcuts import render
from apps.animals.models import Animal
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

class AnimalListView(ListView):
    model = Animal
    template_name = 'animals/index.html'
    context_object_name = 'animals'

class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/detail.html'

class AnimalCreateView(CreateView):
    model = Animal
    fields = '__all__'
    template_name = 'animals/create.html'
    success_url = reverse_lazy('animals:list')

class AnimalUpdateView(UpdateView):
    model = Animal
    fields = '__all__'
    template_name = 'animals/update.html'
    success_url = reverse_lazy('animals:list')

class AnimalDeleteView(DeleteView):
    model = Animal
    template_name = 'animals/delete.html'
    success_url = reverse_lazy('animals:list')