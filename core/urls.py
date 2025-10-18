from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from . import views
from .stripeviews import CreateCheckoutSessionView, SuccessView, CancelView, stripe_webhook

from django.contrib.sitemaps.views import sitemap
from core.sitemap import StaticViewSitemap, PracticeSitemap, MassageSitemap, GiftCardSitemap, PageSitemap
from core.admin import admin_site

from django.http import Http404

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots, name="robots"),

    # path("testgcmail", views.testgcmail, name="testgcmail"),

    #stripe related
    path('annulation/', CancelView.as_view(), name='cancel'),
    path('confirmation/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<model_name>/<int:product_id>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path("forfaits/", views.bundles, name="bundles"),
    path("forfaits/<slug:bundle_slug>/", views.bundleBySlug, name="bundle"),

    #pdf-gen
    # do not forget to import the view to test
    # path('generate-giftcard/', GenerateGifcard.as_view() , name='generate-giftcard'),

    path("cartes-cadeaux/", views.giftcards, name="giftcards"),
    path("carte-cadeau/<slug:giftcard_slug>/", views.giftcardBySlug, name="giftcard"),

    path("privilege/<slug:page_slug>", views.privilege, name="privilege"),
    #redirect to fix mismatch between two simple slug matches
    path("offre-privilege", lambda request: redirect('privilege/offre-privilege', permanent=True)),
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
        {"sitemaps": {'statics': StaticViewSitemap, 'massages' : MassageSitemap, 'practices' : PracticeSitemap, 'giftcards' : GiftCardSitemap, 'pages' : PageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    )
]