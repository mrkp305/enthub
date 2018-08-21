"""ehub\events URL Configuration

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

app_name='events'
urlpatterns = [
    path('', Events.as_view(), name='index'),
    re_path(r'^(\d+)/([a-zA-Z\-\']*)', ViewEvent.as_view(), name='view-event'),
    path('post', Add.as_view(), name='post-event'),
    path('my', My.as_view(), name='my-events'),
    re_path('delete-event/(\d+)/', Delete.as_view(), name='delete'),
    re_path('edit-event/(\d+)/', Edit.as_view(), name='edit'),
    path('get-details/', Details.as_view(), name='get_details'),
    path('get-GeoSon-event-data/', GeoData.as_view(), name='geo-data'),
    path('calendar/', Calendar.as_view(), name='calendar'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()