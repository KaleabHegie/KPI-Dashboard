import json
from typing import Sequence
from django.conf import settings

import requests


class Whatsapp:

    def __init__(self, whatsapp_setting) -> None:
        self.phone_number_id = whatsapp_setting['phone_id']
        self.access_token = whatsapp_setting['access_token']
        self.url = f"https://graph.facebook.com/v13.0/{self.phone_number_id}/messages"
        self.template_name = whatsapp_setting['template_name'] or 'hello_world' # default whatsapp template
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            'Content-Type': 'application/json'
        }

    def send_message(self, phone, template_name=None, msg_vars: Sequence[str]=[], lang='en_US'):
        message_body_params = [ {'type': "text", "text": f"{mv}"} for mv in msg_vars ]
        template = {
            'name': template_name or self.template_name,
            'language': {
                'code': lang,
            }
        }
        if message_body_params:
            template.update({
                'components': message_body_params,
            })
        data = {
            'messaging_product': 'whatsapp',
            'to': phone,
            'type': 'template',
            'template': template,
        }
        response = requests.post(
            self.url,
            headers=self.headers,
            data=json.dumps(data)
        )
        return response

whatsapp_api = Whatsapp(settings.WHATSAPP)