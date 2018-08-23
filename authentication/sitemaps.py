from django.contrib import sitemaps
from django.urls import reverse

class AuthSiteMap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['authentication:auth']

    def location(self, item):
        return reverse(item)