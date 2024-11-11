from celery import shared_task

from interactions.models import BroadcastMessage

from .utils import handle_broadcast_message


@shared_task(name='handle_broadcast_message_task')
def handle_broadcast_message_task(message: BroadcastMessage):
    handle_broadcast_message(message)
