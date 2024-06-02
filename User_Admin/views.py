from django.shortcuts import render

# Create your views here.
def dashboard_setting(request):
    return render(request, 'user-admin/dashboard-setting.html')