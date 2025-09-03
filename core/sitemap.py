from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Practice, Massage, Page

class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ["home","practices","massages"]

    def location(self, item):
        return reverse(item)


class PracticeSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Practice.objects.all()
      
    def lastmod(self, obj):
        return obj.edit_date

class MassageSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return Massage.objects.all()
      
    def lastmod(self, obj):
        return obj.edit_date
    
class PageSitemap(Sitemap):
    priority = 0.3
    changefreq = "monthly"

    def items(self):
        return Page.objects.exclude(custom_viewname__isnull = False)
          
    def lastmod(self, obj):
        return obj.edit_date