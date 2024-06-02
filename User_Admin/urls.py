from django.urls import path
from .views import (
    dashboard_setting,
)
urlpatterns = [
    path('', dashboard_setting, name="user-admin-dashboard-setting"),
]
