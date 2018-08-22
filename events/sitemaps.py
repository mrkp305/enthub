from django.contrib.sitemaps import Sitemap
from .models import Event


class EventSiteMap(Sitemap):    
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.last_modified