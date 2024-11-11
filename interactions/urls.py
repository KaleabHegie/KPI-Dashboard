from django.urls import path

from .views import (
    ComposeNewMessage,
    DeletedMessageList,
    DeleteMessage,
    DeleteMessages,
    MessageDetail,
    SentMessages,
    count_new_messages,
    get_messages,
    index,
    mark_as_read,
    send_message,
)

app_name = "interactions"
urlpatterns = [
    path('', index, name='index'),
    path('with-user/<int:user_id>', get_messages, name='get_messages'),
    path('new-message-count/<int:user_id>', count_new_messages, name='count_new_messages'),
    path('mark-as-read/<int:user_id>', mark_as_read, name='mark_as_read'),
    path('send-message', send_message),
    path('compose-message', ComposeNewMessage.as_view(), name='compose_new_message'),
    path('sent-messages', SentMessages.as_view(), name='sent_messages'),
    path('message/<message_id>', MessageDetail.as_view(), name='message_detail'),
    path('delete-message/<message_id>', DeleteMessage.as_view(), name='delete_message'),
    path('delete-messages', DeleteMessages.as_view(), name='delete_messages'),
    path('sent-messages/trash', DeletedMessageList.as_view(), name='deleted_message_list'),
]
