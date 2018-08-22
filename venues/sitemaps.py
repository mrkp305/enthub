from django.contrib.sitemaps import Sitemap
from .models import Venue


class VenueSiteMap(Sitemap):    
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Venue.objects.all()

    def lastmod(self, obj):
        return obj.last_modified