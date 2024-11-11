from django.contrib import admin
from .models import Message, UnReadMessage, BroadcastMessage, BroadcastMedium


admin.site.register([Message, UnReadMessage, BroadcastMessage, BroadcastMedium])
