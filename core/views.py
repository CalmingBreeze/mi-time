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

def practices(request):
    practices = Practice.objects.order_by("pub_date")
    context = {"practices" : practices}
    return render(request, "core/practice/list.html", context)    

def practiceById(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)
    
    #get related massages
    massages = practice.massages.all()

    template = loader.get_template("core/practice/full.html")
    context = {"practice" : practice, "massages" : massages}
    return HttpResponse(template.render(context, request))

def practiceBySlug(request, practice_slug):
    practice = get_object_or_404(Practice, slug=practice_slug)
    
    #get related massages
    massages = practice.massages.all()

    context = {"practice" : practice, "massages" : massages}
    return render(request, "core/practice/full.html", context)   

def massages(request):
    massages = Massage.objects.order_by("duration")

    context = {"massages" : massages}
    return render(request, "core/massage/list.html", context)

def massageById(request, massage_id):
    massage = get_object_or_404(Massage, pk=massage_id)

    #get related salon
    #practices = {}

    template = loader.get_template("core/massage/full.html")
    context = {"massage" : massage}
    return HttpResponse(template.render(context, request))

def massageBySlug(request, massage_slug):
    massage = get_object_or_404(Massage, slug=massage_slug)

    #get related salon
    practices = massage.practice_set.all()

    context = {"massage" : massage, "practices" : practices}
    return render(request, "core/massage/full.html", context)
