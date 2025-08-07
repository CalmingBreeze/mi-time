from .models import Practice
from django.conf import settings

def practices_processor(request):
    practices = Practice.objects.all()
    return {'practices': practices}

def gmap_api_key_processor(request):
    return {'gmap_api_key' : settings.GMAP_API_KEY}