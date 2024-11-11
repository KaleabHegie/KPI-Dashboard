from typing import Sequence
import threading

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from userManagement.models import Account

from .models import BroadcastMessage, Message, BroadcastMedium
from .models import UnReadMessage as NewMessage
from .utils import handle_broadcast_message


@login_required
def index(request):
    user:Account = request.user
    if any([user.is_hopr, user.is_mopd, user.is_dpg]):
        users_list = Account.objects.exclude(id=request.user.id)
    else:
        users_list = Account.objects.filter(Q(is_hopr=True) | Q(is_mopd=True) | Q(is_dpg=True)).exclude(id=request.user.id)
    return render(request, 'interactions/chat-new.html', {
        'users_list': users_list,
    })

message_in_template = """<div class="message received">{message_content}</div>"""
message_out_template= """<div class="message sent">{message_content}</div>"""

@csrf_exempt
def get_messages(request, user_id:int):
    html_text = ""
    messages: Sequence[Message] = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__id=user_id)) | (Q(sender__id=user_id) & Q(receiver=request.user))
    ).order_by('id')
    for message in messages:
        # t_str = message.created_at.strftime("%b %d %Y %H:%M")
        if message.sender.id == user_id:
            msg_temp = message_in_template.format(message_content=message.content)
        else:
            msg_temp = message_out_template.format(message_content=message.content)
        html_text += msg_temp
    return JsonResponse({
        'data': html_text
    })

@csrf_exempt
def count_new_messages(request, user_id):
    count = NewMessage.count_messages(user_id, request.user.id)
    return JsonResponse({
        'data': count
    })

@csrf_exempt
def mark_as_read(request, user_id):
    qs = NewMessage.objects.filter(Q(message__sender__id=user_id) & Q(message__receiver__id=request.user.id))
    qs.delete()
    return JsonResponse({
        'data': 0
    })

@csrf_exempt
@login_required
def send_message(request):
    print('post data')
    print(request.POST)
    message = request.POST.get('content')
    account_id = request.POST.get('user_id')
    receiver = get_object_or_404(Account, id=account_id)
    Message.objects.create(
        content=message,
        sender=request.user,
        receiver=receiver,
    )
    return JsonResponse({
        'data': True,
    })


# mopd decorator
@method_decorator(login_required, name='dispatch')
class ComposeNewMessage(View):

    def get(self, request):
        receivers = Account.objects.all().exclude(id=request.user.id)
        return render(request, 'interactions/compose_message1.html', {
            'account_list': receivers,
            'medium_list': BroadcastMedium.objects.all(),
        })

    def post(self, request):
        receivers_id = request.POST.getlist('compose_to')
        receivers = Account.objects.filter(id__in=receivers_id)
        subject = request.POST.get('compose_subject', '')
        content = request.POST.get('message_content')
        medium_ids = request.POST.getlist('medium')
        if not medium_ids:
            mediums = BroadcastMedium.objects.all()
        else:
            mediums = BroadcastMedium.objects.filter(id__in=medium_ids)
        bcast_message = BroadcastMessage.objects.create(
            sender=request.user,
            subject=subject,
            content=content,
        )
        bcast_message.receivers.set(receivers)
        bcast_message.medium.set(mediums)
        t = threading.Thread(target=handle_broadcast_message, args=[bcast_message, ])
        t.daemon = True
        t.start()
        return render(request, 'interactions/compose_message.html', {
            'account_list': receivers,
        })


class SentMessages(View):
    
    @method_decorator(login_required)
    def get(self, request):
        message_list = BroadcastMessage.objects.filter(Q(sender=request.user) & Q(is_active=True)).order_by('-id')
        return render(request, 'interactions/message_list.html', {
            'message_list': message_list,
        })


class MessageDetail(View):

    @method_decorator(login_required)
    def get(self, request, message_id):
        message = get_object_or_404(BroadcastMessage, id=message_id)
        prev_m = BroadcastMessage.objects.filter(Q(id__lt=message_id)).last()
        next_m =  BroadcastMessage.objects.filter(Q(id__gt=message_id)).first()
        return render(request, 'interactions/message_detail.html', {
            'message': message,
            'prev_id': prev_m.id if prev_m else 0,
            'next_id': next_m.id if next_m else 0,
        })


class DeleteMessages(View):
    
    @method_decorator(login_required)
    def post(self, request):
        message_id_list = request.POST.getlist('messageId')
        message_list = BroadcastMessage.objects.filter(id__in=message_id_list)
        for m in message_list:
            m.is_active = False
            m.save()
        return redirect('interactions:sent_messages')


class DeleteMessage(View):

    @method_decorator(login_required)
    def get(self, request, message_id):
        message = get_object_or_404(BroadcastMessage, id=message_id)
        if message.is_active:
            message.is_active = False
            message.save()
        else:
            message.delete()
        return redirect('interactions:sent_messages')


class DeletedMessageList(View):
    
    @method_decorator(login_required)
    def get(self, request):
        message_list = BroadcastMessage.objects.filter(Q(sender=request.user) & Q(is_active=False)).order_by('-id')
        return render(request, 'interactions/deleted_messages.html', {
            'message_list': message_list,
        })
