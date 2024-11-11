from django.shortcuts import render
from resultsFramework.models import DashboardSetting
from .forms import DashboardSettingForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from userManagement.models import ResponsibleMinistry 
from resultsFramework.models import Year , Month , Quarter 

# Create your views here.
def dashboard_setting(request):
    form = DashboardSettingForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Added')
            return redirect('user-admin-dashboard-setting')
        else:
            messages.error(request, 'An error occurred while Adding')
    context = {
         "kpi_settings" : DashboardSetting.objects.all(),
         "form" : form
    }
    
    return render(request, 'user-admin/dashboard-setting.html' , context)


def addsetting(request):
    form = DashboardSettingForm(request.POST or None, request.FILES or None)
    ministrys = ResponsibleMinistry.objects.all() 
    years = Year.objects.all() 
    quarters = Quarter.objects.all() 
    months = Month.objects.all() 
    if request.method == 'POST':
        name = request.POST.get('name')
        year = request.POST.get('year')
        month = request.POST.get('month')
        quarter = request.POST.get('quarter')
        indicators = request.POST.getlist('indicator')
        performance = bool(request.POST.get('performance'))
        target = bool(request.POST.get('target'))
        

        dashboard_setting = DashboardSetting.objects.create(
            name=name,
            year_id=year,
            month_id=month,
            quarter_id=quarter,
            performance=performance,
            target=target,
        )
        dashboard_setting.indicator.set(indicators)
        dashboard_setting.save()
        messages.success(request, 'Successfully Added')
        return redirect('user-admin-dashboard-setting')
    context = {
         "form" : form ,
         "ministrys" : ministrys,
         "years" : years,
         "quarters" : quarters,
         "months" : months
    }
    
    return render(request, 'user-admin/addsetting.html' , context)    





def setting_delete(request, id):
    try:
        setting = DashboardSetting.objects.get(pk = id)
        setting.delete()
        messages.success(request, 'Successfully Deleted')
        redirect('user-admin-dashboard-setting')
    except:
        messages.error(request, 'An error occurred while Deleting')
    
    return redirect('user-admin-dashboard-setting')     




def edit_setting(request , id):
    try:
        setting = DashboardSetting.objects.get(pk = id)
        setting.read = True
        setting.save()
    except:
        setting = None
    
    form = DashboardSettingForm(request.POST or None ,  instance=setting)
  

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('user-admin-dashboard-setting')
        else:
            messages.error(request, 'An error occurred while updating')
    context = {
        'form' : form
    }
    return render(request , "user-admin/edit_setting.html" , context)  

