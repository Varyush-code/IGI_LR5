from django.shortcuts import render
import requests
import logging
from django.views.generic import TemplateView
from django.utils import timezone
from apps.news.models import News

logger = logging.getLogger(__name__)

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['latest_news'] = (
            News.objects
            .order_by('-created_at')
            .first()
        )
        context['current_date'] = timezone.localtime()
        context['utc_date'] = timezone.now()

        cat_fact = None
        try:
            response = requests.get( "https://catfact.ninja/fact",timeout=5)
            if response.status_code == 200:
                data = response.json()
                cat_fact = data.get("fact")
                logger.info("Загрузка прошла успешно")
        except requests.RequestException:
            logger.error("Ошибка API")
            cat_fact = "Не удалось загрузить факт о кошках"

        context['cat_fact'] = cat_fact

        joke = None
        try:
            response = requests.get( "https://official-joke-api.appspot.com/random_joke",timeout=5)
            if response.status_code == 200:
                data = response.json()
                joke = { 
                    "setup": data.get("setup"),
                    "punchline": data.get("punchline"),
                }
                logger.info("Загрузка прошла успешно")
        except requests.RequestException:
            logger.error("Ошибка API")
            joke = "Не удалось загрузить шутку"

        context['joke'] = joke

        return context
    
class AboutPageView(TemplateView):
    template_name = 'about.html'