import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Account, Message


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            self.close()
        else:
            self.room_name = f'inbox_of_{user.id}'
            print("Channel name is: ", self.channel_name)
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name,
            )
            self.accept()

    def receive(self, text_data, bytes_data=None):
        user = self.scope['user']
        text_data_json:dict = json.loads(text_data)
        print('Json data is: ')
        print(text_data_json)
        msg_type = text_data_json.get('type', None)
        if msg_type == 'chat_message':
            message = text_data_json['message']
            receiver = text_data_json['to']
            try:
                Message.objects.create(
                    content=message,
                    sender=user,
                    receiver=Account.objects.get(id=receiver)
                )
            except Exception as e:
                print(e)
        elif msg_type == 'active_chat':
            user_id = text_data_json['user_id']
            prev_user = text_data_json.get('prev_user', 0)
            print('Receive order to activate chat with user: ', user_id)
            c_room = f'chat_of_{user.id}_{user_id}'
            async_to_sync(self.channel_layer.group_add)(
                c_room,
                self.channel_name,
            )
            if prev_user != 0:
                p_room = f'chat_of_{user.id}_{prev_user}' # previous room; to be discarded
                async_to_sync(self.channel_layer.group_discard)(
                    p_room, 
                    self.channel_name
                ) # discard layer from prev group
        else:
            print('Unknow type of message received: ', text_data_json.get('type'))

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'from': event['from'],
            'date': event['date'],

        }))

    def inbox_update(self, event):
        self.send(text_data=json.dumps({
            'type': 'inbox_update',
            'from': event['from']
        }))
