from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, UnReadMessage

channel_layer = get_channel_layer()

@receiver(post_save, sender=Message)
def update_unread_message(sender, instance: Message, created: bool, **kwargs):
    if created:
        UnReadMessage.objects.create(message=instance)
        async_to_sync(channel_layer.group_send)(
            f'inbox_of_{instance.receiver.id}',
            {
                'type': 'inbox_update',
                'from': instance.sender.id,
            }
        )


@receiver(post_save, sender=Message)
def send_socket_message(sender, instance: Message, created: bool, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)(
            f'chat_of_{instance.receiver.id}_{instance.sender.id}', # group name `receiver_sender`
            {
                'type': 'chat_message',
                'message_id': instance.id,
                'message': instance.content,
                'from': instance.sender.id,
                'date': instance.created_at.strftime("%b %d %Y %H:%M:%S"),
            }
        )
