from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework.exceptions import ValidationError

from_email = settings.EMAIL_HOST_USER

def send_template_mail(subject, to, context={}, template=None):    
    if template is not None:
        template_str = 'mail/'+ template+'.html'
        html_message = render_to_string(template_str, {'data': context})
        sent=send_mail(subject=subject, message=None, from_email=from_email, recipient_list=[to], html_message=html_message)
        return sent
    else:
        raise ValidationError(detail="Email template required!")

def send_content_mail(subject, to, message=None):
    if message is not None:
        sent=send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[to])
        return sent
    else:
        raise ValidationError(detail="Content is required!")
    
def send_template_content_mail(subject, to, context, message=None, template=None):
    if message is not None and template is not None:
        template_str = 'mail/'+ template+'.html'
        html_message = render_to_string(template_str, {'data': context})
        sent = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[to], html_message=html_message)
        return sent
    else:
        raise ValidationError(detail="Content and template are required!")

# def send_activation_mail(to):
#     send_content_mail()