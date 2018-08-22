from django.contrib.sitemaps import Sitemap
from .models import Artist


class ArtistSiteMap(Sitemap):    
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Artist.objects.all()

    def lastmod(self, obj):
        return obj.last_updated