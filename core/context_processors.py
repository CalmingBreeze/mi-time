from .models import Practice, SiteConfig
from django.conf import settings

def siteconfig_processor(request):
    siteconfig = SiteConfig.objects.first()
    return {'siteconfig': siteconfig}

def practices_processor(request):
    practices = Practice.objects.all()
    return {'practices': practices}

def gmap_api_key_processor(request):
    return {'gmap_api_key': settings.GMAP_API_KEY}