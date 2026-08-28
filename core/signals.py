from django.db.models.signals import post_save
# from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from .models import MailUser

@receiver(post_save, sender=MailUser)
def send_activation_email(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance

    token = user.activation_token

    context = {
        "email": user.email,
        "domain": settings.DOMAIN,
        "site_name": settings.WEBSITE_NAME,
        "user": user,
        "token": token,
        "protocol": settings.PROTOCOL,
    }

    subject = render_to_string(
        "registration/activation_email_title.txt",
        context,
    ).strip()

    text_body = render_to_string(
        "registration/activation_email.txt",
        context,
    )

    html_body = render_to_string(
        "registration/activation_email.html",
        context,
    )

    email_message = EmailMultiAlternatives(
        subject,
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

    email_message.attach_alternative(
        html_body,
        "text/html",
    )

    email_message.send()


# due to DJA force login we cannot generate token on creation like above, but as we autolog on creation, the firstetime last_login shouldbe None.
# @receiver(user_logged_in)
# def first_login(sender, request, user, **kwargs):
#     if user.last_login is None:
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)

#         context = {
#             "email": user.email,
#             "domain": settings.DOMAIN,
#             "site_name": settings.WEBSITE_NAME,
#             "uid": uid,
#             "user": user,
#             "token": token,
#             "protocol": settings.PROTOCOL,
#         }

#         subject = render_to_string(
#             "registration/activation_email_title.txt",
#             context,
#         ).strip()

#         text_body = render_to_string(
#             "registration/activation_email.txt",
#             context,
#         )

#         html_body = render_to_string(
#             "registration/activation_email.html",
#             context,
#         )

#         email_message = EmailMultiAlternatives(
#             subject,
#             text_body,
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#         )

#         email_message.attach_alternative(
#             html_body,
#             "text/html",
#         )

#         email_message.send()