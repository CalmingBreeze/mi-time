from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Practice, Massage, Page, GiftCard, Bundle

class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ["home","practices","massages","giftcards","bundles"]

    def location(self, item):
        return reverse(item)

class BundleSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return Bundle.objects.order_by("priority","name")
      
    def lastmod(self, obj):
        return obj.edit_date

class GiftCardSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return GiftCard.objects.order_by("priority","name")
      
    def lastmod(self, obj):
        return obj.edit_date

class PracticeSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Practice.objects.order_by("name")
      
    def lastmod(self, obj):
        return obj.edit_date

class MassageSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return Massage.objects.order_by("priority","name")
      
    def lastmod(self, obj):
        return obj.edit_date
    
class PageSitemap(Sitemap):
    priority = 0.3
    changefreq = "monthly"

    def items(self):
        return Page.objects.exclude(custom_viewname__isnull = False).order_by("name")
          
    def lastmod(self, obj):
        return obj.edit_date