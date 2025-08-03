from .models import Practice

def practices_processor(request):
    practices = Practice.objects.all()
    return {'practices': practices}