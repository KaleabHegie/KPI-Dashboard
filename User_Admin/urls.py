from django.urls import path
from .views import (
    dashboard_setting,setting_delete,edit_setting , addsetting
)
urlpatterns = [
    path('', dashboard_setting, name="user-admin-dashboard-setting"),
    path('addsetting/', addsetting, name='addsetting'),
    path('setting_delete/<int:id>/', setting_delete, name='setting_delete'),
    path('setting_edit/<int:id>/', edit_setting, name='edit_setting'),
]
