from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dashboard-app/dashboard-index.html')