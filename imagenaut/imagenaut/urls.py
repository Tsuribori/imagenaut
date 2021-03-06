"""imagenaut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from debug_toolbar import urls as debug_urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from imageboard import urls as imageboard_urls
from moderation import urls as moderation_urls
from rules import urls as rules_urls
from navigation import urls as navigation_urls
from navigation.views import Frontpage #Messy solution
from archives import urls as archives_urls
from api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('boards/', include(navigation_urls)),
    path('board/', include(imageboard_urls)),
    path('mod/', include((moderation_urls, 'mod'), namespace='dj-mod')),
    path('rules/', include(rules_urls)),
    path('archive/', include(archives_urls)),
    path('api/v1/', include(api_urls)),
    path('captcha/', include('captcha.urls')),
    path('', Frontpage.as_view(), name='navigation_frontpage'),
]

if settings.DEBUG:
    urlpatterns = [
        path('debug/', include(debug_urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

