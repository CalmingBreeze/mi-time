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

from django.template.loader import render_to_string
from django.utils.html import strip_tags

import logging
logger = logging.getLogger('__name__')

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        #retrieve model, dynamically switch from subclasses
        # print(self.kwargs["model_name"]) 
        product_model = apps.get_model('core', self.kwargs["model_name"])
        product = product_model.objects.get(id=self.kwargs["product_id"])
        logger.debug("CreateCheckoutSessionView : call")
        logger.debug(f"STRIPE PRICE ID : {product.stripe_price_id}")
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
    """

    This function generate a PDF file with AddTextToPDF class and given infos

    text : list
        list of 3 str, first is the title of the gift certificate, then the stripe coupon code used, and the expiry date
    pdfbase_path : str
        Base pdf file used
    dest_path : str
        Where to store the filled pdf.
    """
    full_dest_path = dest_path+text[1]+".pdf"
    pdf_editor = AddTextToPDF(pdfbase_path, full_dest_path)
    pdf_editor.buildGiftcard(text[0],text[1],text[2])
    pdf_editor.save()
    return full_dest_path

def send_giftcardmail(customer_email, pdf_added_text):
    """

    This function generate an email with the pdf giftcard attachment

    customer_email : str
    pdf_added_text : list
        list of 3 str, first is the title of the gift certificate, then the stripe coupon code used, and the expiry date  
    """
    # Template
    template_name = "core/mail/giftcard.html"
    context = {"site_url" : "www.mi-time.fr", "phone_number" : "0783390680", "email": settings.DEFAULT_FROM_EMAIL}
    
    convert_to_html_content =  render_to_string(
        template_name=template_name,
        context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    # Email parameters
    from_email = settings.DEFAULT_FROM_EMAIL
    to = customer_email
    subject = "[Mi-time.fr] Votre carte cadeau en pdf"
    text_content = plain_message
    html_content = convert_to_html_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    # PDF Generation
    try:
        gift_filepath = generate_giftcard(pdf_added_text)
    except Exception as e:
        logger.error("Giftcard : PDF-GEN Error : %s", e)
    
    # Include the pdf.
    msg.attach_file(gift_filepath, 'application/pdf')

    try:
        logger.debug("Giftcard Send Tentative")
        msg.send()
    except Exception as e:
        logger.error("Giftcard : Send Error : %s", e)

def send_neworder_confirmation(customer_email, customer_name, stripe_payment_id, order_type):
    """
        Send an automated mail when a command is validated
    """
    template_name = f"core/mail/{order_type}.html"
    context = {"site_url" : "www.mi-time.fr", "phone_number" : "0783390680", "customer_email": customer_email,"customer_name" : customer_name, "stripe_payment_id" : stripe_payment_id}

    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    # Email parameters
    from_email = settings.DEFAULT_FROM_EMAIL
    to = customer_email
    subject = "[Mi-time.fr] Confirmation de votre commande"
    text_content = plain_message
    html_content = convert_to_html_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        logger.error("New Order Client Confirm Mail : Send Error : %s", e)

def send_neworder_selfmail(customer_email, customer_name, stripe_payment_id, order_type):
    """
        Send an automated mail when a command is validated to facilitate manual handling of appointments until automation is online.
    """

    template_name = "core/mail/new_order_validated.html"
    context = {"site_url" : "www.mi-time.fr", "customer_email": customer_email,"customer_name" : customer_name, "stripe_payment_id" : stripe_payment_id}

    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    # Email parameters
    from_email = settings.DEFAULT_FROM_EMAIL
    to = from_email
    subject = f" [à traiter] Nouvelle commande : {customer_name} - {customer_email} - {stripe_payment_id}"
    text_content = plain_message
    html_content = convert_to_html_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        logger.error("New Order Validated Mail : Send Error : %s", e)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    logger.debug("stripe_webhook triggered")

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
        customer_name = session["customer_details"]["name"]
        payment_intent = session["payment_intent"]
        metadata = session["metadata"]

        #print(session, customer_email, payment_intent, metadata)
        logger.debug(f"Giftcard bought : {customer_email}, {payment_intent}, {metadata}")

        #Handle Giftcard generation workflow (new coupon, pdf generation, and email)
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

            send_giftcardmail(customer_email, (metadata["gift_label"],event2["code"],new_coupon_expires_at.strftime('%d/%m/%Y')))

        if metadata and metadata["model_name"] == "bundle":
            # Order Confirmation
            send_neworder_confirmation(customer_email, customer_name, session["payment_intent"], metadata["model_name"])

        # Alert Mi-time manager by mail that a new order has been processed by Stripe
        send_neworder_selfmail(customer_email, customer_name, session["payment_intent"], metadata["model_name"])

            
    return HttpResponse(status=200)