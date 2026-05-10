"""
URL configuration for zoo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('animals/', include('apps.animals.urls')),
    path('news/', include('apps.news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('contacts/', include('apps.employees.urls')),
    path('feeding/', include('apps.feeding.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('openings/', include('apps.openings.urls')),
    path('enclosures/', include('apps.enclosures.urls')),
    path('statistic/', include('apps.statistic.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )