"""ehub\venues URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import VenueSiteMap

sitemaps = {
    'venues': VenueSiteMap
}

app_name='venues'
urlpatterns = [
    
    path('', Index.as_view(), name='index'),
    path('post', Add.as_view(), name='post-venue'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[a-zA-Z0-9\-\'\w]+)/', ViewVenue.as_view(), name='view-venue'),
    re_path(r'^my/(\d+)/edit/([a-zA-Z0-9\-\'\w]+)/', EditVenue.as_view(), name='edit-venue'),
    re_path(r'^my/(\d+)/delete/([a-zA-Z0-9\-\'\w]+)/', Delete.as_view(), name='delete-venue'),
    re_path(r'^my/', My.as_view(), name='my'),
    re_path(r'^sitemap\.xml/$', sitemap, {'sitemaps' : sitemaps } , name='sitemap')
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()