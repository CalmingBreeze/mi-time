import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, timezone, timedelta
from django.utils import timezone
from .addtext2pdf import AddTextToPDF
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string
from django.utils.html import strip_tags

import logging
logger = logging.getLogger('__name__')

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def get_domain_url(self):
        return "http://127.0.0.1:8000" if settings.DEBUG else "https://www.mi-time.fr"

    def fetch_product_infos(self, app_origin, model_name, object_id):
        """
        Retrieve the correct product model (Massage, Giftcard, Bundle) depending on app origin

        Parameters:
        app_origin (str) : app who made the call to stripe API ('appointment' or 'core')
        model_name (str) : the name of the model to invoke (PaymentInfo for appointment, 
        """
        if (app_origin == 'appointment'):
            model = apps.get_model(app_origin, model_name)
            paymentinfo = model.objects.get(id=object_id)
            service = paymentinfo.appointment.appointment_request.service
            product = service.related_product
        elif (app_origin == 'core'):
            model = apps.get_model(app_origin, model_name)
            product = model.objects.get(id=object_id)
        else:
            logger.error("Invalid Product pairing")

        return product
    
    def apply_discount_event(self, product):
        """
        Handle a discount event on stripe

        Parameters:
        product (AbstractProduct)
        """
        #handle promotion discount events
        if product.promo_stripe_coupon_id and product.promo_start_date < timezone.now() and product.promo_end_date > timezone.now():
            #There is a valid discount event
            logger.debug(f"Discount event applied : {product.promo_stripe_coupon_id}")
            discount=[{
                'coupon': product.promo_stripe_coupon_id
            }]
        else:
            discount=[{}]
        return discount
    
    def generate_metadatas(self, product):
        model_name = product._meta.model_name

        #generate metadata for after purchase routing
        product_metadata = {
            "model_name": model_name, 
            "product_id" : product.id
        }
        logger.debug(f"Generate metadatas : model_name : {model_name}, product_id : {product.id}")

        if model_name == "giftcard":
            product_metadata["gift_label"] = product.gift_label
            product_metadata["coupon_id"] = product.stripe_coupon_id
            logger.debug(f"Additional metadatas : gift_label : {product.gift_label}, coupon_id : {product.stripe_coupon_id}")

        return product_metadata

    #Handle appointment redirects
    def get(self, request, *args, **kwargs):
        # int : object_id (service id)
        # str : id_request
        logger.debug(request)
        logger.debug(self.kwargs)

        product = self.fetch_product_infos('appointment', 'PaymentInfo', self.kwargs["object_id"])
        logger.debug("CreateCheckoutSessionView : GET : call")

        logger.debug(product.stripe_product_id)
        logger.debug(product.stripe_price_id)

        #handle domain in prod or debug
        domain = self.get_domain_url()

        #handle discount events
        discount_event = self.apply_discount_event(product)

        #generate metadata
        product_metadata = self.generate_metadatas(product)
        #add appointment to meta data to change status to paid when done
        product_metadata["paymentinfo_id"] = self.kwargs["object_id"]

        #create stripe checkout object
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card','paypal'],
            line_items=[
                {
                    'price': product.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            allow_promotion_codes=True,
            discounts = discount_event,
            success_url=domain + reverse("stripe:success"),
            cancel_url=domain + reverse("stripe:cancel"),
            metadata=product_metadata
        )
        return redirect(checkout_session.url)

    
    def post(self, request, *args, **kwargs):
        #we need to match related Product
        product = self.fetch_product_infos('core', self.kwargs["model_name"], self.kwargs["product_id"]) 
        logger.debug("CreateCheckoutSessionView : POST : call")

        #handle domain in prod or debug
        domain = self.get_domain_url()
        
        #handle discount events
        discount_event = self.apply_discount_event(product)

        #generate metadata
        product_metadata = self.generate_metadatas(product)

        #create stripe checkout object
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card','paypal'],
            line_items=[
                {
                    'price': product.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            # allow_promotion_codes=True,
            discounts = discount_event,
            success_url=domain + reverse("stripe:success"),
            cancel_url=domain + reverse("stripe:cancel"),
            metadata=product_metadata
        )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "core/stripe/success.html"

class CancelView(TemplateView):
    template_name = "core/stripe/cancel.html"

def generate_giftcard(text = ('Massage 1H', 'TESTCODE', datetime.now().strftime('%d/%m/%Y')), pdfbase_path = "./core/static/core/giftcard.pdf", dest_path = "./static/core/pdf/carte-cadeau-"):
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

def confirm_massage_paid(paymentinfo_id):
    """
    Update the payment status to paid after trigger stripe webhook from success checkout

    paymentinfo_id : int The PaymentInfo id of the purchase
    """
    model = apps.get_model("appointment", "PaymentInfo")
    paymentinfo = model.objects.get(id=paymentinfo_id)
    paymentinfo.set_paid_status(True)

    return paymentinfo

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
        logger.debug(f"ValueError (invalid payload) : {e}")
        return HttpResponse(status=400)
    except stripe.error.InvalidRequestError as e:
        logger.debug(f"InvalidRequestError : {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.debug(f"SignatureVerificationError : {e}")
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

        if metadata :
        # Update payment status
            if metadata["model_name"] == "massage":
                confirm_massage_paid(metadata["paymentinfo_id"])

            #Handle Giftcard generation workflow (new coupon, pdf generation, and email)
            if metadata["model_name"] == "giftcard":
                new_coupon_expires_at = timezone.now() + timedelta(days=365)

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

            if metadata["model_name"] == "bundle":
                # Order Confirmation
                send_neworder_confirmation(customer_email, customer_name, session["payment_intent"], metadata["model_name"])

        # Alert Mi-time manager by mail that a new order has been processed by Stripe
        send_neworder_selfmail(customer_email, customer_name, session["payment_intent"], metadata["model_name"])

            
    return HttpResponse(status=200)