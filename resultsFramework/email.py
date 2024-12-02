import threading
import  os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_notifier(request, subject, message, email, stop_event):
    while not stop_event.is_set():
                
        subject, from_email, to = subject, 'mikiyasmebrate2656@gmail.com', f"{email}"
        text_content = "Registration Successful"
        context = {
            'message': message,
        }

        html_content = render_to_string('email/notification_custom.html',context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")

        if msg.send():
            print('Email sent')