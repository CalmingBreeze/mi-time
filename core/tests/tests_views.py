from django.test import Client, TestCase
from django.urls import reverse

from core.models import Page, Massage, Bundle, GiftCard

# Create your tests here.

class HTTPSClient(Client):
    def get(self, path, data=None, secure=True, **extra):
        # extra.setdefault("secure", True)
        return super().get(path, data=data, secure=secure, **extra)

    def post(self, path, data=None, content_type=None, secure=True, **extra):
        # extra.setdefault("secure", True)
        return super().post(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            **extra,
        )

class BaseViewTests(TestCase):
    fixtures = [
        "appointment_config.yaml",
        "pages_and_configs.yaml",
        "products_and_practices.yaml"
    ]

    client_class = HTTPSClient

    def test_homepage_is_accessible(self):
        """The homepage should return HTTP 200."""
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_all_pages_objects_are_accessible(self):
        """All the pages objects should be return http 200 or 302"""
        pages = Page.objects.all()
        for page in pages:
            if page.custom_viewname is not None:
                with self.subTest(page=page):
                    if page.custom_viewname == "privilege" :
                        #url removed.
                        pass
                    else:
                        url = reverse(page.custom_viewname)
                        response = self.client.get(reverse(page.custom_viewname))
                        if page.custom_viewname == "user-profile" :
                            #redirect to login as unlogged user.
                            self.assertEqual(response.status_code, 302)
                        else :    
                            self.assertEqual(response.status_code, 200)

class ProductViewTests(TestCase):
    fixtures = [
        "appointment_config.yaml",
        "pages_and_configs.yaml",
        "products_and_practices.yaml"
    ]

    client_class = HTTPSClient

    def test_massages_view(self):
        """The massages view should return HTTP 200."""
        response = self.client.get(reverse("massages"))

        self.assertEqual(response.status_code, 200)

    def test_all_massages_have_working_booking_button(self):
        """All massages should have a booking button to reservation"""
        massages = Massage.objects.all()

        for massage in massages:
            with self.subTest(massage=massage):
                response = self.client.get(reverse("massage", kwargs={"massage_slug": massage.slug}))
                self.assertEqual(response.status_code, 200)
                #we expect to have a button with this url
                expected_url = f"/appointment/request/{massage.service.id}/"
                self.assertContains(response,expected_url)
                #and response on click to be 200
                response = self.client.get(expected_url)
                self.assertEqual(response.status_code, 200)

    def test_bundles_view(self):
        """The bundles view should return HTTP 200."""
        response = self.client.get(reverse("bundles"))

        self.assertEqual(response.status_code, 200)

    def test_all_bundles_have_checkout_button(self):
        """All bundles should have a button to create a stripe checkout session"""
        bundles = Bundle.objects.all()

        for bundle in bundles:
            with self.subTest(bundle=bundle):
                response = self.client.get(reverse("bundle", kwargs={"bundle_slug": bundle.slug}))
                self.assertEqual(response.status_code, 200)
                #we expect to have a form with that action
                expected_url = reverse("stripe:create-checkout-session",args=["bundle", bundle.id])
                self.assertContains(response,expected_url)

    def test_giftcards_view(self):
        """The giftcards view should return HTTP 200."""
        response = self.client.get(reverse("giftcards"))

        self.assertEqual(response.status_code, 200)

    def test_all_giftcards_have_checkout_button(self):
        """All giftcards should have a button to create a stripe checkout session"""
        giftcards = GiftCard.objects.all()

        for giftcard in giftcards:
            with self.subTest(giftcard=giftcard):
                response = self.client.get(reverse("giftcard", kwargs={"giftcard_slug": giftcard.slug}))
                self.assertEqual(response.status_code, 200)
                #we expect to have a form with that action
                expected_url = reverse("stripe:create-checkout-session",args=["giftcard", giftcard.id])
                self.assertContains(response,expected_url)

class ErrorViewTests(TestCase):

    client_class = HTTPSClient

    def test_unknown_massage_returns_404(self):
        url = reverse("massage",kwargs={"massage_slug": "ce-massage-nexiste-pas"},)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)