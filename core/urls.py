from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.contrib.sitemaps.views import sitemap
from django.contrib.auth.views import PasswordResetView, LoginView

from . import views
from .stripeviews import CreateCheckoutSessionView, SuccessView, CancelView, stripe_webhook
from .forms import MailPasswordResetForm, MailAuthenticationForm

from core.sitemap import StaticViewSitemap, PracticeSitemap, MassageSitemap, GiftCardSitemap, BundleSitemap, PageSitemap
from core.admin import admin_site

from django.http import Http404

#app_name = 'core'

stripe_patterns = (
    [
        path('annulation/', CancelView.as_view(), name='cancel'),
        path('confirmation/', SuccessView.as_view(), name='success'),
        path('create-checkout-session/<model_name>/<int:product_id>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
        path('create-appointment-checkout-session/<int:object_id>/<str:id_request>/', CreateCheckoutSessionView.as_view(), name='create-appointment-checkout-session'),
        path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    ],
    "stripe",
)

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots, name="robots"),

    # path("testgcmail", views.testgcmail, name="testgcmail"),

    #stripe urls
    path("stripe/", include(stripe_patterns)),

    path("privilege/<slug:page_slug>", views.privilege, name="privilege"),
    #redirect to fix mismatch between two simple slug matches
    path("offre-privilege", lambda request: redirect('privilege/offre-privilege', permanent=True)),
    path("<slug:page_slug>", views.pages, name="page"),

    path("reservation/", views.reservation, name="reservation"),

    path("massages/", views.massages, name="massages"),
    path("massage/<slug:massage_slug>/", views.massageBySlug, name="massage"),
    #path("massage/<int:massage_id>/", views.massageById, name="massage"),

    path("forfaits/", views.bundles, name="bundles"),
    path("forfaits/<slug:bundle_slug>/", views.bundleBySlug, name="bundle"),

    #pdf-gen
    # do not forget to import the view to test
    # path('generate-giftcard/', GenerateGifcard.as_view() , name='generate-giftcard'),
    path("cartes-cadeaux/", views.giftcards, name="giftcards"),
    path("carte-cadeau/<slug:giftcard_slug>/", views.giftcardBySlug, name="giftcard"),

    path("salons/", views.practices, name="practices"),
    path("salon/<slug:practice_slug>/", views.practiceBySlug, name="practice"),
    #path("practice/<int:practice_id>/", views.practice, name="practice"),

    path('miadmin/', admin_site.urls),

    path("accounts/activate/<str:token>", views.activate_account, name="activate-account"),
    #override (auth modules defaults) password_reset to allow html template and plain text fallback
    path("accounts/login/",LoginView.as_view(
        authentication_form=MailAuthenticationForm),
        name="login",
    ),
    path('accounts/password_reset/', PasswordResetView.as_view(
            form_class=MailPasswordResetForm,
            subject_template_name="registration/password_reset_email_title.txt",
            email_template_name="registration/password_reset_email.txt", #compatibility purpose
            html_email_template_name="registration/password_reset_email.html",
        ),name="password_reset"),
    path("accounts/", include("django.contrib.auth.urls")),

    path("accounts/profile/", views.profile, name="user-profile"),
]

urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {'statics': StaticViewSitemap, 'massages' : MassageSitemap, 'practices' : PracticeSitemap, 'giftcards' : GiftCardSitemap, 'bundles' : BundleSitemap, 'pages' : PageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    )
]