import threading
import  os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email_notifier(subject, message, email, stop_event):
    while not stop_event.is_set():
                
        subject, from_email, to = subject, 'mikiyasmebrate2656@gmail.com', email
        text_content = "Registration Successful"
        context = {
            'message': message,
        }

        html_content = render_to_string('email/notification_custom.html',context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        if msg.send():
            print('Email sent')


#preset Email lists
def email_public_bodies_overview(email,ministry,data_type, year, quarter=None):
    pass


def send_preset_email_notifier(request,email ,ministry, preset, data_type, year, quarter, language ,stop_event):
    while not stop_event.is_set():
        subject = body = None
        if preset == 'dashboard_overview':
            email_public_bodies_overview(email,ministry,data_type, year, quarter or None)
        elif preset == 'preset_performance':
            subject = 'Notification: Submission of Performance Reports'
            body = f'''Dear {ministry},

               We hope this email finds you well. As part of our ongoing commitment to monitoring and evaluating performance across all public bodies, we kindly remind you to submit your performance data for the reporting period {year if data_type == 'year' else quarter}.
               '''
        elif preset == 'preset_target':
            subject = 'Submission of Performance Targets'
            body = f'''Dear {ministry},

              We hope this message finds you well. This is a gentle reminder to submit your performance targets for the upcoming {year if data_type == 'year' else quarter}.
              '''
        elif preset == 'preset_document':
            subject = 'Reminder: Submission of Performance Documents'
            body = f'''Dear {ministry},

               We kindly remind you to submit your performance documentation for the {year if data_type == 'year' else quarter}.
               These documents are critical for assessing and evaluating your organization's progress towards its objectives.
               '''
        
        stop_event = threading.Event()
        background_thread = threading.Thread(target=send_email_notifier, args=(subject,body,email,stop_event), daemon=True)
        background_thread.start()
        stop_event.set()


            



