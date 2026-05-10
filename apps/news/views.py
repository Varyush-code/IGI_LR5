from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DeleteView, CreateView, UpdateView, DetailView)
from .models import News

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'news.html'
    login_url = '/accounts/login/'
    context_object_name = 'news_list'

class NewsDetailView(DeleteView):
    model = News
    template_name = 'home.html'
