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
from django.core.mail import EmailMessage

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

def generate_giftcard(text = ('Massage 1H', 'TESTCODE', datetime.datetime.now().strftime('%d/%m/%Y')), pdfbase_path = "./core/static/core/giftcard.pdf", dest_path = "./static/core/pdf/giftcard-"):
    full_dest_path = dest_path+text[1]+".pdf"
    pdf_editor = AddTextToPDF(pdfbase_path, full_dest_path)
    pdf_editor.buildGiftcard(text[0],text[1],text[2])
    pdf_editor.save()
    return full_dest_path

# class GenerateGifcard(View):
#     def get(self, request, *args, **kwargs):
#         generate_giftcard()

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
        # print('checkout.session.completed event captured !')
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
        metadata = session["metadata"]

        #print(session, customer_email, payment_intent, metadata)

        #Handle Promocode generated for gift card.
        if metadata and metadata["model_name"] == "giftcard":
            new_coupon_expires_at = timezone.now() + datetime.timedelta(days=365)

            # generate new promocode for related coupon
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

            #print(event2, event2["code"])

            try:
                gift_filepath = generate_giftcard((metadata["gift_label"],event2["code"],new_coupon_expires_at.strftime('%d/%m/%Y')))
                gift_email = EmailMessage(
                    subject = "Mi-Time.fr, votre carte cadeau en pdf",
                    body = "Merci pour votre commande. Veuillez trouver ci-joint votre carte cadeau en format imprimable./n/nBelle Journée.",
                    to = customer_email
                )
                gift_email.attach_file(gift_filepath, 'application/pdf')
                print("Email de la carte cadeau :", gift_email.send())
            except Exception as e:
                print('Email send error: ', e)
            
    return HttpResponse(status=200)