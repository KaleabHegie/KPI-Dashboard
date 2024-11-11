from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserPasswordConfirmForm

    
urlpatterns = [
        path('login/', login_view, name='login_url'),
        path('logout/', logout_view, name='logout_url'),
        path('', dashboard_setting, name="user-admin-dashboard-setting"),
        path('addsetting/', addsetting, name='addsetting'),
        path('setting_delete/<int:id>/', setting_delete, name='setting_delete'),
        path('setting_edit/<int:id>/', edit_setting, name='edit_setting'),




        #### RESET PASSWORD
    #dashboard-pages/authentication/
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication-dashboard/reset_password.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication-dashboard/password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="authentication-dashboard/password_reset_confirm.html",form_class=UserPasswordConfirmForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication-dashboard/password_reset_complete.html"), name='password_reset_complete'),


]            