from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.contrib.sitemaps.views import sitemap
from core.sitemap import StaticViewSitemap, PracticeSitemap, MassageSitemap, PageSitemap
from core.admin import admin_site

from django.http import Http404

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots, name="robots"),
    path("<slug:page_slug>", views.pages, name="page"),
    path("salons/", views.practices, name="practices"),
    path("salon/<slug:practice_slug>/", views.practiceBySlug, name="practice"),
    #path("practice/<int:practice_id>/", views.practice, name="practice"),
    path("massages/", views.massages, name="massages"),
    path("massage/<slug:massage_slug>/", views.massageBySlug, name="massage"),
    #path("massage/<int:massage_id>/", views.massageById, name="massage"),
    path('miadmin/', admin_site.urls),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {'statics': StaticViewSitemap, 'massages' : MassageSitemap, 'practices' : PracticeSitemap,'pages' : PageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    )
]