import requests
from django.conf import settings


class SMSGateway:
    def __init__(self, url, headers={}, params={}, method='GET', to_str='to'):
        self.url = url
        self.headers = headers
        self.params = params
        self.method = method
        self.to_str = to_str

    def send(self, to:str, message:str, timeout=5):
        # to = to.strip('+')
        self.params.update({
            self.to_str: to,
            'message': message,
        })
        try:
            if self.method == 'GET':
                result = requests.get(self.url, params=self.params, headers=self.headers, timeout=timeout)
            else:
                result = requests.post(self.url, params=self.params, headers=self.headers, timeout=timeout)
            if result.status_code == 200:
                return self.on_success(result)
            elif result.status_code in [400, 404, 500]:
                return self.on_error(result)
        except Exception as e:
            print('Error while sending sms: ', str(e))
            return 1

    def on_success(self, result):
        print('sms sent succesfully')
        print(result.json())
        return 0

    def on_error(self, result):
        print('error while sending sms')
        return 1


# sms gateway
sms_gw = SMSGateway(
    url='https://hahu.io/api/send/sms',
    method='POST',
    to_str='phone',
    params={
        'secret': settings.SMS_KEY,
        'mode':'devices',
        'device': settings.SMS_DEVICE_ID,
        'sim': 1,
    }
)