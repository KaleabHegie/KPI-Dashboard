from django.shortcuts import render
from DashboardApp.models import DashboardSetting
from .forms import DashboardSettingForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

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
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Added')
            return redirect('user-admin-dashboard-setting')
        else:
            messages.error(request, 'An error occurred while Adding')
    context = {
         "form" : form
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

