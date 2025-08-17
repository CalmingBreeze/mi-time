from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Practice
from .models import Massage
from .models import Page


# Handle custom error views
def err500_view(request):
    print("err500_view")
    return render(request, "core/error.html", {"request" : request, "exception": "500", "error_msg": "Internal Server Error"})
def err404_view(request, exception):
    return render(request, "core/error.html", {"request" : request, "exception": "404", "error_msg": "Not Found"})
def err403_view(request, exception):
    return render(request, "core/error.html", {"request" : request, "exception": "403", "error_msg": "Forbidden"})
def err401_view(request, exception):
    return render(request, "core/error.html", {"request" : request, "exception": "401", "error_msg": "Unauthorized"})
def err400_view(request, exception):
    return render(request, "core/error.html", {"request" : request, "exception": "400", "error_msg": "Bad Request"})

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
