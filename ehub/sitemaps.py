from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'events:index',
            'events:map', 
            'events:calendar',
            'events:post-event',
            'artists:index', 
            'venues:index',
            'tos', 
            'co-policy', 
            'pr-policy', 
            ]

    def location(self, item):
        return reverse(item)