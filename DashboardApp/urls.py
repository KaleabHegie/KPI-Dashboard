from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserPasswordConfirmForm

from .api_policy_area import views as policyAreaDashboard 
from .api_ministry import views as MinistryDashboard

from .views import *
urlpatterns = [
    path('login/',dashboard_login, name="dashboard-login"),
    path('logout/',dashboard_logout, name="dashboard-logout"),




    path('', policy_area, name='policy_area'),
    path('info/',info, name="info"),
    path('search/', search, name='search'),



    path('ministry_index/', ministry_index, name='ministry_index'),
    path('ministries_lists/',ministries_lists, name="dashboard-ministries_lists"),
    path('ministry-goal/<str:id>/',ministry_goal, name="dashboard-ministries_lists"),
    path('ministry_goal_front/<str:id>/',ministry_goal_front, name="ministry_goal_front"),
    path('indicator_lists/<str:id>/',indicator_lists, name="dashboard-indicator_lists"),
    path('indicator-details/<int:indicator_id>/', indicator_details_json, name='indicator_details_json'),
    path('kra/<int:kra_id>/', filter_indicators_by_kra, name='filter_indicators_by_kra'),
    path('search_autocomplete_indicator_list/', auto_complete_search_indicator, name='dashboard-indicator-lists-auto-complete'),

    ####policy-area dashboard
    path('api/dashboard/',policyAreaDashboard.dashboard),
    path('api/policy-area/',policyAreaDashboard.policy_areas),
    path('api/policy-area/<str:id>/',policyAreaDashboard.policy_area),
    path('api/goal_with_kra/<str:id>/',policyAreaDashboard.goal_with_kra),
    path('api/indicator/<str:id>/',policyAreaDashboard.indicator),
    path('api/time_series_year/',policyAreaDashboard.time_series_year),
    path('api/policy_area_SDG/',policyAreaDashboard.policy_area_SDG),
    path('api/search/',policyAreaDashboard.search_item),
    path('api/search/kra/<str:id>/',policyAreaDashboard.search_key_result_area_detail),
    path('api/search/goal/<str:id>/',policyAreaDashboard.search_goal_detail),
    path('api/search_auto_complete/',policyAreaDashboard.search_auto_complete),


    ###Ministry dashboard
    path('api/ministry/ministry_with_policy_area/<str:ministry_id>/',MinistryDashboard.ministry_with_policy_area),
    path('api/ministry/policy_area_with_goal/<str:id>/',MinistryDashboard.policy_area_with_goal),
    path('api/ministry/ministries/' ,MinistryDashboard.ministries),
    path('api/ministry/goal_with_kra/<str:id>/',MinistryDashboard. goal_with_kra),
    path('api/ministry/indicator/<str:id>/',MinistryDashboard. indicator),
    path('api/ministry/time_series_year/',MinistryDashboard. time_series_year),
    path('api/ministry/dashboard/' ,MinistryDashboard.dashboard),
    path('api/ministry/dashboard_ministries/<str:ministry_id>/',MinistryDashboard.dashboard_ministries),
    path('api/ministry/indicatorsInGoal/<str:id>/',MinistryDashboard.indicatorsInGoal),
    path('api/ministry/ministry_kra_serializer/<str:ministry_id>/',MinistryDashboard.ministry_kra_serializer),
   
     #### RESET PASSWORD
    #dashboard-pages/authentication/
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='dashboard-app/authentication/reset_password.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='dashboard-app/authentication/password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="dashboard-app/authentication/password_reset_confirm.html",form_class=UserPasswordConfirmForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="dashboard-app/authentication/password_reset_complete.html"), name='password_reset_complete'),

]
