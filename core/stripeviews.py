import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.shortcuts import redirect
import datetime
from django.utils import timezone
from .addtext2pdf import AddTextToPDF
from django.core.mail import EmailMessage, EmailMultiAlternatives

import logging
logger = logging.getLogger('__name__')

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        #retrieve model, dynamically switch from subclasses
        print(self.kwargs["model_name"]) 
        product_model = apps.get_model('core', self.kwargs["model_name"])
        product = product_model.objects.get(id=self.kwargs["product_id"])
        product_metadata = {
            "model_name": self.kwargs["model_name"], 
            "product_id" : self.kwargs["product_id"]
        }
        if self.kwargs["model_name"] == "giftcard":
            product_metadata["gift_label"] = product.gift_label
            product_metadata["coupon_id"] = product.stripe_coupon_id

        domain = "https://www.mi-time.fr"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': product.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            # allow_promotion_codes=True,
            success_url=domain + '/confirmation/',
            cancel_url=domain + '/annulation/',
            metadata=product_metadata
        )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "core/stripe/success.html"

class CancelView(TemplateView):
    template_name = "core/stripe/cancel.html"

def generate_giftcard(text = ('Massage 1H', 'TESTCODE', datetime.datetime.now().strftime('%d/%m/%Y')), pdfbase_path = "./core/static/core/giftcard.pdf", dest_path = "./static/core/pdf/carte-cadeau-"):
    full_dest_path = dest_path+text[1]+".pdf"
    pdf_editor = AddTextToPDF(pdfbase_path, full_dest_path)
    pdf_editor.buildGiftcard(text[0],text[1],text[2])
    pdf_editor.save()
    return full_dest_path

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
        metadata = session["metadata"]

        #print(session, customer_email, payment_intent, metadata)
        #logger.info("Giftcard bought, payment intent %s", payment_intent)

        #Handle Promocode generated for gift card.
        if metadata and metadata["model_name"] == "giftcard":
            new_coupon_expires_at = timezone.now() + datetime.timedelta(days=365)

            # generate new promocode for related coupon with 1Y expiry
            try:
                event2 = promotion_code = stripe.PromotionCode.create(
                    coupon=metadata["coupon_id"],
                    max_redemptions=1,
                    expires_at=new_coupon_expires_at
                )
            except ValueError as e:
                # Invalid payload
                return HttpResponse(status=400)
            except stripe.error.SignatureVerificationError as e:
                # Invalid signature
                return HttpResponse(status=400)

            #email the gift card
            from_email = settings.DEFAULT_FROM_EMAIL
            to = customer_email
            subject = "Mi-Time.fr, votre carte cadeau en pdf",
            text_content = "Merci pour votre commande. Veuillez trouver ci-joint votre carte cadeau en format imprimable. Belle Journée."
            html_content = "Merci pour votre commande.<br>Veuillez trouver ci-joint votre carte cadeau en format imprimable.<br><br>Belle Journée."
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            #generate filled pdf with the data
            try:
                gift_filepath = generate_giftcard((metadata["gift_label"],event2["code"],new_coupon_expires_at.strftime('%d/%m/%Y')))
                msg.attach_file(gift_filepath, 'application/pdf')
                msg.send()
            except Exception as e:
                logger.error("Giftcard PDF GEN Error : %s", e)
            
    return HttpResponse(status=200)