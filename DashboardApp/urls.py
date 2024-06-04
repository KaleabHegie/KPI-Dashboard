from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserPasswordConfirmForm

from .views import (
    index , 
    ministries_lists,
    ministry_goal,
    indicator_lists,
    indicator_details_json,
    ministry_goal_front,
    filter_indicators_by_kra,
    auto_complete_search_indicator,
    dashboard_login , 
    dashboard_logout
) 
urlpatterns = [
    path('login/',dashboard_login, name="dashboard-login"),
    path('logout/',dashboard_logout, name="dashboard-logout"),




    path('', index, name='dashboard-api'),
    path('ministries_lists/',ministries_lists, name="dashboard-ministries_lists"),
    path('ministry-goal/<str:id>/',ministry_goal, name="dashboard-ministries_lists"),
    path('ministry_goal_front/<str:id>/',ministry_goal_front, name="ministry_goal_front"),
    path('indicator_lists/<str:id>/',indicator_lists, name="dashboard-indicator_lists"),
    path('indicator-details/<int:indicator_id>/', indicator_details_json, name='indicator_details_json'),
    path('kra/<int:kra_id>/', filter_indicators_by_kra, name='filter_indicators_by_kra'),
    path('search_autocomplete_indicator_list/', auto_complete_search_indicator, name='dashboard-indicator-lists-auto-complete'),


     #### RESET PASSWORD
    #dashboard-pages/authentication/
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='dashboard-app/authentication/reset_password.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='dashboard-app/authentication/password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="dashboard-app/authentication/password_reset_confirm.html",form_class=UserPasswordConfirmForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="dashboard-app/authentication/password_reset_complete.html"), name='password_reset_complete'),

]
