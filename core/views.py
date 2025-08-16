from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Practice
from .models import Massage
from .models import Page

# Create your views here.

def home(request):
    practices = Practice.objects.order_by("pub_date")
    massages = Massage.objects.order_by("-duration")
    page = Page.objects.filter(custom_viewname = "home").first()
    context = {"page": page, "practices" : practices, "massages" : massages}
    return render(request, "core/index.html", context)

def pages(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    context = {"page" : page}
    return render(request, "core/page.html", context)

def practices(request):
    practices = Practice.objects.order_by("pub_date")
    page = Page.objects.filter(custom_viewname = "practices").first()
    context = {"page" : page, "practices" : practices}
    return render(request, "core/practice_list.html", context)    

def practiceBySlug(request, practice_slug):
    practice = get_object_or_404(Practice, slug=practice_slug)
    practices = Practice.objects.order_by("pub_date")

    #get related massages
    massages = practice.massages.all()

    context = {"practice" : practice, "practices" : practices, "massages" : massages}
    return render(request, "core/practice_full.html", context)   

def massages(request):
    massages = Massage.objects.order_by("priority")
    page = Page.objects.filter(custom_viewname = "practices").first()
    context = {"page" : page, "massages" : massages}
    return render(request, "core/massage_list.html", context)

def massageBySlug(request, massage_slug):
    massage = get_object_or_404(Massage, slug=massage_slug)

    #get related salon
    practices = massage.practice_set.all()

    context = {"massage" : massage, "practices" : practices}
    return render(request, "core/massage_full.html", context)
