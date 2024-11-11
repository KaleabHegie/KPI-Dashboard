from html.parser import HTMLParser
from typing import Sequence

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from interactions.models import BroadcastMessage

from .sms import sms_gw
from .whatsapp import whatsapp_api


class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data


def broadcast_mail(message: BroadcastMessage):
    tbe = get_template("interactions/mail_template.html")
    _html = tbe.template.source.format(
        title=message.subject,
        content=message.content,
    )
    email = EmailMultiAlternatives(
        message.subject,
        _html,
        settings.EMAIL_HOST_USER,
        [x.email for x in message.receivers.all() ]
    )
    email.attach_alternative(_html, 'text/html')
    email.send(fail_silently=True)

def broadcast_sms(message: BroadcastMessage):
    try:
        phone_list = [x.phone_number for x in message.receivers.all()]
        for phone in phone_list:
            hf = HTMLFilter()
            hf.feed(message.content)
            sms_gw.send(phone, hf.text)
    except Exception as e:
        print('Error sending SMS: ', e)

def broadcast_whatsapp(message: BroadcastMessage):
    phone_list:Sequence[str] = [x.phone_number for x in message.receivers.all()]
    for phone in phone_list:
        try:
            whatsapp_api.send_message(phone.strip('+'), msg_vars=[message.subject, message.content])
        except Exception as e:
            print('Error sending whatsapp message: ', e)

def handle_broadcast_message(message: BroadcastMessage):
    m_list = message.medium.all()
    if not m_list:
        # send via all
        broadcast_sms(message)
        broadcast_mail(message)
        broadcast_whatsapp(message)
    else:
        for m in m_list:
            if m.code == 'email':
                broadcast_mail(message)
            elif m.code == 'sms':
                broadcast_sms(message)
            elif m.code == 'whatsapp':
                broadcast_whatsapp(message)    