from .models import Practice, SiteConfig, Page
from django.conf import settings

def siteconfig_processor(request):
    siteconfig = SiteConfig.objects.first()
    return {'siteconfig': siteconfig}

def menu_processor(request):
    pages = Page.objects.all()
    menu_pages = Page.objects.exclude(menu_position__isnull = True).order_by("menu_position")
    footer_links = Page.objects.exclude(footer_position__isnull = True).order_by("footer_position")
    legal_links = Page.objects.exclude(legal_page = False).order_by("name")
    practices_count = Practice.objects.count()
    first_practice = Practice.objects.first()
    return {'pages': pages, 'menu_pages': menu_pages, 'footer_links': footer_links, 'legal_links': legal_links, 'practices_count': practices_count, 'first_practice': first_practice}

def gmap_api_key_processor(request):
    return {'gmap_api_key': settings.GMAP_API_KEY}