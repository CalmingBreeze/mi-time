from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Practice
from .models import Massage

# Create your views here.

def index(request):
    practices = Practice.objects.order_by("pub_date")
    massages = Massage.objects.order_by("-duration")
    template = loader.get_template("core/index.html")
    context = {"practices" : practices, "massages" : massages}
    return HttpResponse(template.render(context, request))

def practices(request):
    practices = Practice.objects.order_by("pub_date")
    template = loader.get_template("core/practice/list.html")
    context = {"practices" : practices}
    return HttpResponse(template.render(context, request))

def practiceById(request, practice_id):
    try:
        practice = Practice.objects.get(pk=practice_id)
    except Practice.DoesNotExist:
        raise Http404("This practice does not exist")
    
    #get related massages
    massages = practice.massages.all()

    template = loader.get_template("core/practice/full.html")
    context = {"practice" : practice, "massages" : massages}
    return HttpResponse(template.render(context, request))

def practiceBySlug(request, practice_slug):
    try:
        practice = Practice.objects.get(slug=practice_slug)
    except Practice.DoesNotExist:
        raise Http404("This practice does not exist")
    
    #get related massages
    massages = practice.massages.all()

    template = loader.get_template("core/practice/full.html")
    context = {"practice" : practice, "massages" : massages}
    return HttpResponse(template.render(context, request))

def massages(request):
    massages = Massage.objects.order_by("duration")
    template = loader.get_template("core/massage/list.html")
    context = {"massages" : massages}
    return HttpResponse(template.render(context, request))

def massageById(request, massage_id):
    try:
        massage = Massage.objects.get(pk=massage_id)
    except Massage.DoesNotExist:
        raise Http404("This massage does not exist")

    #get related salon
    #practices = {}

    template = loader.get_template("core/massage/full.html")
    context = {"massage" : massage}
    return HttpResponse(template.render(context, request))

def massageBySlug(request, massage_slug):
    try:
        massage = Massage.objects.get(slug=massage_slug)
    except Massage.DoesNotExist:
        raise Http404("This massage does not exist")

    #get related salon
    #practices = {}

    template = loader.get_template("core/massage/full.html")
    context = {"massage" : massage}
    return HttpResponse(template.render(context, request))