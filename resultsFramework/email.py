import threading
import  os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from userManagement.models import ResponsibleMinistry
from .models import Indicator, AnnualPlan, QuarterProgress, Quarter
from django.db.models import Count , F

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


def calculate_quarter(quarter):
    quarter_number = quarter.split('-')[1].split('q')[1]
    return Quarter.objects.filter(rank = quarter_number).first()
    

#preset Email lists
def calculate_ministry_status(ministry, year, quarter, indicators, data_type):

    def get_good_performance():
        if quarter and year and data_type == 'quarter':
            quarter_number = calculate_quarter(quarter)
            year_amh = quarter.split('-')[0]

            high_performance = QuarterProgress.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year_amh, 
                quarter=quarter_number ,  
                quarter_target__isnull=False, 
                quarter_performance__gte = 0.5* F('quarter_target')).count()
        else:
            high_performance = AnnualPlan.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year, 
                annual_target__isnull=False, 
                annual_performance__gte = 0.5* F('annual_target')).count()
        return high_performance  
    
    def get_low_performance():
        if quarter and year and data_type == 'quarter':
            quarter_number = calculate_quarter(quarter)
            year_amh = quarter.split('-')[0]
            low_performance = QuarterProgress.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year_amh,
                quarter=quarter_number ,  
                quarter_target__isnull=False , 
                quarter_performance__lt = 0.5* F('quarter_target')).count()
        else:
            low_performance = AnnualPlan.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year,  
                annual_target__isnull=False , 
                annual_performance__lt = 0.5* F('annual_target')).count()
        return low_performance 

    def get_count_has_no_performance():
        if quarter and year and data_type == 'quarter':
            quarter_number = calculate_quarter(quarter)
            year_amh = quarter.split('-')[0]
            no_performance = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year_amh, quarter=quarter_number, quarter_target__isnull=False ,quarter_performance__isnull=True).count()
        else:
            no_performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False ,annual_performance__isnull=True).count()
        return  no_performance
    
    def get_count_has_performance():
        if quarter and year and data_type == 'quarter':
            quarter_number = calculate_quarter(quarter)
            year_amh = quarter.split('-')[0]
            performance = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year_amh, quarter=quarter_number, quarter_target__isnull=False,quarter_performance__isnull=False).count()
        else:
            performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False, annual_performance__isnull=False).count()
        return performance

    def calculate_percentage_target_performance():
        no_performance = get_count_has_no_performance()
        has_performance = get_count_has_performance()
        total = no_performance+has_performance

       

        no_performance_percentage = 0
        no_performance_percentage_75 = 0
        try:
            no_performance_percentage =round(((no_performance/(total))*100),2)
            no_performance_percentage_75 =round(((no_performance/(total))*75),2)
        except:
            no_performance_percentage = 0
            no_performance_percentage_75 = 0

        return {
            "no_performance_percentage" : no_performance_percentage,
            "no_performance_percentage_75" : no_performance_percentage_75,
            "no_performance_percentage_75_25" : round(75 - no_performance_percentage_75, 2),
        }



    def calculate_percentage_performance():
        good_performance = get_good_performance()
        low_performance = get_low_performance()
        total = good_performance + low_performance

        good_performance_percentage = 0
        good_performance_percentage_75 = 0
        low_performance_percentage_75 = 0
        try:
            good_performance_percentage =round(((good_performance/(total))*100),2)
            good_performance_percentage_75 =round(((good_performance/(total))*75),2)
        except:
            good_performance_percentage = 0
            good_performance_percentage_75 = 0

        low_performance_percentage = 0

        try:
            low_performance_percentage = round(((low_performance/(total))*100),2)
            low_performance_percentage_75 = round(((low_performance/(total))*75),2)
        except:
            low_performance_percentage = 0
            low_performance_percentage_75 = 0
        

        return {
            "good_performance_percentage" : good_performance_percentage,
            "good_performance_percentage_75" : good_performance_percentage_75,
            "good_performance_percentage_75_25" : round(75 - good_performance_percentage_75, 2),
            "low_performance_percentage" : low_performance_percentage,
            "low_performance_percentage_75" : low_performance_percentage_75,
            "low_performance_percentage_75_25" : round(75 - low_performance_percentage_75),
        }

    
    return {
        'no_performance' : get_count_has_no_performance(),
        'good_performance' : get_good_performance(),
        'low_performance' : get_low_performance(),
        'percentage' : calculate_percentage_performance(),
        'no_performance_percentage' : calculate_percentage_target_performance()
    }

def email_public_bodies_overview_notifier(subject, message,email,ministry,data_type, year, stop_event,quarter=None):
    while not stop_event.is_set():
        
        indicator = Indicator.objects.filter(responsible_ministries = ministry).values_list('id', flat=True)
        score_card = ministry.ministry_score_card(indicator_id=indicator, 
                                                  quarter=calculate_quarter(quarter).quarter_eng if quarter else None,
                                                  year=quarter.split('-')[0] if quarter else year
                                                  )
        ministry_analysis = calculate_ministry_status(ministry, year, quarter, indicator,data_type)
        
        subject, from_email, to = "DPMEs Analysis", 'mikiyasmebrate2656@gmail.com', email
        text_content = "DPMEs Analysis"
        context = {
            'score' : round(score_card['avg_score'],2),
            'score_color' : score_card['scorecard_color'],
            'no_performance' : ministry_analysis['no_performance'],
            'good_performance' : ministry_analysis['good_performance'],
            'low_performance' : ministry_analysis['low_performance'],
            'percentage' : ministry_analysis['percentage'],
            'no_performance_percentage' : ministry_analysis['no_performance_percentage'],
            'period' : quarter if  data_type == 'quarter' else year

        }



        html_content = render_to_string('email/notification.html',context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        if msg.send():
            print('Email sent')


def send_preset_email_notifier(request,email ,ministry, preset, data_type, year, quarter, language ,stop_event):
    while not stop_event.is_set():
        subject = body = None

        if preset == 'preset_performance':
            subject = 'Notification: Submission of Performance Reports'
            if language == 'english':
                body = f'''Dear {ministry.responsible_ministry_eng},
    
                   We hope this email finds you well. As part of our ongoing commitment to monitoring and evaluating performance across all public bodies, we kindly remind you to submit your performance data for the reporting period {year if data_type == 'year' else quarter}.
                   '''
            else:
                body = f'''እማረኛ ኢሚኤል'''

        elif preset == 'preset_target':
            subject = 'Submission of Performance Targets'
            if language == 'english':
                body = f'''Dear {ministry.responsible_ministry_eng},
    
                  We hope this message finds you well. This is a gentle reminder to submit your performance targets for the upcoming {year if data_type == 'year' else quarter}.
                  '''
            else:
                body = f'''እማረኛ ኢሚኤል'''

        elif preset == 'preset_document':
            subject = 'Reminder: Submission of Performance Documents'
            if language == 'english':
                body = f'''Dear {ministry.responsible_ministry_eng},
    
                   We kindly remind you to submit your performance documentation for the {year if data_type == 'year' else quarter}.
                   These documents are critical for assessing and evaluating your organization's progress towards its objectives.
                   '''
            else:
                body = f'''እማረኛ ኢሚኤል'''

        elif preset == 'dashboard_overview':
            stop_event = threading.Event()
            background_thread = threading.Thread(target=email_public_bodies_overview_notifier, args=(subject,body ,email,ministry,data_type, year, stop_event, quarter), daemon=True)
            background_thread.start()
            stop_event.set()
        
        if preset != 'dashboard_overview':
            stop_event = threading.Event()
            background_thread = threading.Thread(target=send_email_notifier, args=(subject,body,email,stop_event), daemon=True)
            background_thread.start()
            stop_event.set()


            



