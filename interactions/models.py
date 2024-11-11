from django.db import models
from django.db.models import Q
from django.utils import timezone
from userManagement.models import Account
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()

class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)


class UnReadMessage(models.Model):
    message = models.OneToOneField(to=Message, on_delete=models.CASCADE, related_name='new_message')

    @staticmethod
    def count_messages(sender_id, receiver_id) -> int:
        return UnReadMessage.objects.filter(Q(message__sender__id=sender_id) & Q(message__receiver__id=receiver_id)).count()

    @staticmethod
    def clean_unread_message(sender_id: int, receiver_id: int):
        pass


class BroadcastMedium(models.Model):
    CODE_CHOICES = [
        ('sms', 'sms'),
        ('email', 'email'),
        ('whatsapp', 'whatsapp'),
    ]
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, choices=CODE_CHOICES)

    def __str__(self):
        return self.name


class BroadcastMessage(models.Model):
    sender = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="sent_broadcast_messages")
    receivers = models.ManyToManyField(to=Account, related_name='received_broadcast_messages')
    subject = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    medium = models.ManyToManyField(to=BroadcastMedium)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.subject