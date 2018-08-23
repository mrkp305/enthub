"""ehub URL Configuration

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
from .sitemaps import *
from artists.sitemaps import ArtistSiteMap
from events.sitemaps import EventSiteMap
from venues.sitemaps import VenueSiteMap
from authentication.sitemaps import AuthSiteMap
sitemaps = {
    'static': StaticViewSitemap,
    'authentication':AuthSiteMap,
    'artist':ArtistSiteMap,
    'events':EventSiteMap,
    'venues':VenueSiteMap,
    
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view() , name='site-home'),
    # path('', include('pwa.urls', namespace='pwa'),
    path('auth/', include('authentication.urls')),
    path('account/', include('account.urls')),
    path('artists/', include('artists.urls')),
    path('events/', include('events.urls')),
    path('venues/', include('venues.urls')),
    path('terms-of-services/', Tos.as_view(), name='tos'),
    path('copyright-policy/', CoPolicy.as_view(), name='co-policy'),
    path('privacy-policy/', PrPolicy.as_view(), name='pr-policy'),
    re_path(r'^sitemap\.xml/$', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()