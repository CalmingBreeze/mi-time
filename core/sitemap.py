from django.contrib.sitemaps import Sitemap
from .models import Practice, Massage, Page

class PracticeSitemap(Sitemap):
    def items(self):
        return Practice.objects.all()
      
    def lastmod(self, obj):
        return obj.edit_date

class MassageSitemap(Sitemap):
    def items(self):
        return Massage.objects.all()
      
    def lastmod(self, obj):
        return obj.edit_date
    
class PageSitemap(Sitemap):
    def items(self):
        return Page.objects.all()
      
    def lastmod(self, obj):
        return obj.edit_date