from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Practice
from .models import Massage

# Create your views here.

def index(request):
    practices = Practice.objects.order_by("pub_date")
    massages = Massage.objects.order_by("-duration")
    context = {"practices" : practices, "massages" : massages}
    return render(request, "core/index.html", context)

def legal(request):
    context = {}
    return render(request, "core/legal.html", context)

def practices(request):
    practices = Practice.objects.order_by("pub_date")
    context = {"practices" : practices}
    return render(request, "core/practice_list.html", context)    

def practiceBySlug(request, practice_slug):
    practice = get_object_or_404(Practice, slug=practice_slug)
    practices = Practice.objects.order_by("pub_date")

    #get related massages
    massages = practice.massages.all()

    context = {"practice" : practice, "practices" : practices, "massages" : massages}
    return render(request, "core/practice_full.html", context)   

def massages(request):
    massages = Massage.objects.order_by("duration")

    context = {"massages" : massages}
    return render(request, "core/massage_list.html", context)

def massageBySlug(request, massage_slug):
    massage = get_object_or_404(Massage, slug=massage_slug)

    #get related salon
    practices = massage.practice_set.all()

    context = {"massage" : massage, "practices" : practices}
    return render(request, "core/massage_full.html", context)
