from .models import Practice, SiteConfig, Page
from django.conf import settings

def siteconfig_processor(request):
    siteconfig = SiteConfig.objects.first()
    return {'siteconfig': siteconfig}

def menu_processor(request):
    pages = Page.objects.all()
    menu_pages = Page.objects.exclude(menu_position__isnull = True).order_by("menu_position")
    return {'pages': pages, 'menu_pages': menu_pages}

def gmap_api_key_processor(request):
    return {'gmap_api_key': settings.GMAP_API_KEY}