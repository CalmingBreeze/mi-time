from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

import logging
logger = logging.getLogger('__name__')

def send_html_and_plaintext_mail(mail_address, subject, template_name, template_context = None, attachments = None):

    if template_context is None:
        template_context = {}

    #default context for admin mails
    template_context.update({"site_url" : "www.mi-time.fr", "phone_number" : "0783390680", "email": settings.DEFAULT_FROM_EMAIL})

    convert_to_html_content =  render_to_string(
        template_name=template_name,
        context=template_context
    )

    plain_message = strip_tags(convert_to_html_content)

    from_email = settings.DEFAULT_FROM_EMAIL
    to = mail_address
    text_content = plain_message
    html_content = convert_to_html_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    if attachments:
        msg.attach_file(attachments["path"], attachments["mime_type"])

    try:
        msg.send()
    except Exception as e:
        logger.exception("send_html_and_plaintext_mail : Send Error")