

from django.urls import path
from .views import *
from . import views
from .views import *
from .api_policy_area import views as policyAreaDashboard 
from .api_ministry import views as MinistryDashboard
urlpatterns = [
    # quarter_ministry,
    path('mopd/', index, name='dashboard-api'),
    path('home/', index, name='mopd_url'),
    path('',dashboard_mopd, name='dashboard_mopd_url'),
    path('mopd_policy_area/', mopd_policy_area, name='mopd_policy_area_url'),
    path('mopd_public_bodies/', mopd_public_bodies, name='mopd_public_bodies_url'),
    path('mopd_mdip/', mopd_mdip, name='mopd_mdip_url'),
    path('annual-quarter/', mopd_result_matrix, name='mopd_result_matrix'),
    path('view-goals/', view_goals, name='view_goals'),
    path('view_key_result_areas/', view_key_result_areas, name='view_kra'),


    # Profile
    path('ministry_profile/', ministry_profile, name='ministry_profile'),


    # affiliated
    path('year_quarter_list/' , year_quarter_list  ),
    path('affiliated_ministries/', affiliated_ministries, name='affiliated_ministries'),
    path('affiliated_ministries_list/', affiliated_ministries_list, name='affiliated_ministries_list'),
    path('above_threshold/' , above_threshold , name='above_threshold'),

    path('dashboard/', ministry_dashboard, name="ministry"),
    path('policy_area_ministry/', policy_area_ministry, name='policy_area_ministry_url'),
    path('mdip_ministry/', mdip_ministry, name='mdip_ministry_url'),
    path('export_ministry/', export_ministry1, name='export_ministry_url'),
    path('ministry1/', kpi_ministry_new, name='kpi_ministry_new_url'),
    path('plan_ministry/', kpi_ministry_plan, name='kpi_ministry_plan'),
    path('confirm_kpi_ministry_plan/', confirm_kpi_ministry_plan, name='confirm_kpi_ministry_plan'),
    path('update_quarter_plan/',update_quarter_plan,name="update_quarter_plan"),
    path('export-quarter-plan-temp/', export_quarter_plan_temp, name='export_quarter_plan_temp'),

    path('count_performed_kpis/<int:target_year>/', count_performed_kpis, name="count_performed_kpis"),
    path('bubble_chart/', bubble_chart, name="bubble_chart"),

    path('ministry/', kpi_ministry, name='ministry_url'),
    path('ministryBatch/', batch_insert_ministry, name='ministryBatch'),
    path('batch-data/', save_batch_performance_data, name='save_batch'),
    path('ajax_search_indicators/', ajax_search_indicators,
         name='ajax_search_indicators'),
    path('update_performance/', update_annual_plan_performance,
         name='update_performance'),



    path('quarter_ministry/', quarter_ministry, name='quarter_ministry'),
    path('update_quarter_ministry/', update_quarter_plan_performance,
         name='quarter_plan_performance'),

    path('bulk_update_quarter_ministry/', quarter_batch_insert_ministry,
         name='quarter_batch_insert_ministry'),
    path('bulk_quarter_ministry/', quarter_save_batch_performance_data,
         name='bulk_quarter_ministry'),

    #    ____________________________________________________________________________________________________________

    path('mopd_kpi_ministry/', mopd_kpi_ministry, name='mopd_kpi_ministry'),
    path('mopd_kpi_kra/', mopd_kpi_kra, name='mopd_kpi_kra'),
    path('mopd_kpi_ministry_filter/', mopd_kpi_ministry_filter,
         name='mopd_kpi_ministry_filter'),

    path('filter_indicators/', filter_indicators, name='filter_indicators'),

    path('view_kpi_kra_ministry/', view_kpi_kra_ministry, name='view_kpi_kra_ministry'),
    path('view_kpi_table/', view_kpi_table, name='view_kpi_table'),
    
    path('view_kpi_ministry/', view_kpi_ministry, name='view_kpi_ministry'),
    path('filter_kpi_ministry/', filter_kpi_ministry, name='filter_kpi_ministry'),
    path('table_ajax/', table_ajax, name='table_ajax'),
    path('table_ajax2/', table_ajax2, name='table_ajax2'),
    #     path('view_kpi_ministry1/', filter_kpi_ministry1,
    #          name='filter_kpi_ministry1')
    path('filter-goals-and-kras/', filter_goals_and_kras,
         name='filter_goals_and_kras'),
    path('indicator_detail/<int:id>/', indicator_detail, name='indicator_detail'),
    path('get_chart_data/<int:id>/', get_chart_data, name='get_chart_data'),
    path('ministry_lists/',ministry_list, name='ministry_list'),
    path('ministry_list_quarter/',ministry_list_quarter, name='ministry_list_quarter'),
    
    path('generate_ministry_kpi/',generate_ministry_kpi, name='generate_ministry_kpi'), 
       
    path('mopd_quarter_kpi_ministry/', mopd_quarter_kpi_ministry, name='mopd_quarter_kpi_ministry'),
    path('mopd_kpi_kra_quarter/', mopd_kpi_kra_quarter, name='mopd_kpi_kra_quarter'),
    path('ministry_kpi_kra_quarter/', ministry_kpi_kra_quarter, name='ministry_kpi_kra_quarter'),    


 #    ____________________________________________________________________________________________________________

    path('dataManagement/', views.index, name='home1_url'),
    path('sample_data/', views.sample_data, name='sample_data' ),
    path('ministries/', views.responsible_ministries, name="responsible-ministries"),
    path('year/', views.year, name="year"),
    path('national_plan/', views.national_plan, name="national_plan"),
    path('strategic_goal/', views.strategic_goal, name="strategic_goal"),
    path('key_result-area/', views.key_result_area, name="key_result_area"),
    path('indicator/', views.indicator, name="indicator"),
    path('kpi_aggregation/', views.kpiAggrigation, name="kpi-aggregation"), 


    ###
    path('save-performance/', views.update_performance, name='update-performance'),
    path('update_ministry/', views.update_ministry, name='update_ministry'),
    path('update_year/', views.update_year, name='update_year'),
    path('update_national_plan/', views.update_national_plan, name='update_national_plan'),
    path('update_strategic_goal/', views.update_strategic_goal, name='update_strategic_goal'),
    path('update_key_result_area/', views.update_key_result_area, name='update_key_result_area'),
    path('update_indicator/', views.update_indicator, name='update_indicator'),
    path('update_kpi_aggregation/', views.update_kpi_aggregation, name='update_kpi_aggregation'),
    

    ###
    path('delete_ministry/<str:pk>', views.delete_ministry, name="delete_ministry"),
    path('delete_year/<str:pk>', views.delete_year, name="delete_year"),
    path('delete_national_plan/<str:pk>', views.delete_national_plan, name="delete_national_plan"),
    path('delete_strategic_goal/<str:pk>', views.delete_strategic_goal, name="delete_strategic_goal"),
    path('delete_key_result_area/<str:pk>', views.delete_key_result_area, name="delete_key_result_area"),
    path('delete_indicator/<str:pk>', views.delete_indicator, name="delete_indicator"),




    ##
    path('export_ministry/', views.export_ministry, name="export_ministry"),
    path('export_year/', views.export_year, name="export_year"),
    path('export_national_plan/', views.export_national_plan, name="export_national_plan"),
    path('export_strategic_goal/', views.export_strategic_goal, name="export_strategic_goal"),
    path('export_key_result_area/', views.export_key_result_area, name="export_key_result_area"),
    path('export_indicator/', views.export_indicator, name="export_indicator"),
    path('export_kpi_sub_indicator/', views.export_kpi_sub_indicator, name="export_kpi_sub_indicator"),
    path('export_annual_plan/', views.export_annual_plan, name="export_annual_plan"),




    path('home/', index, name='dashboard-api'),
    path('ministries_lists/',ministries_lists, name="dashboard-ministries_lists"),
    path('policy_area_lists/',policy_area_lists, name="policy_area_lists"),
    path('ministry-goal/<str:id>/',ministry_goal, name="dashboard-ministries_lists"),
    path('ministry_goal_front/<str:id>/',ministry_goal_front, name="ministry_goal_front"),
    path('indicator_lists/<str:id>/',indicator_lists, name="dashboard-indicator_lists"),
    path('indicator-details/<int:indicator_id>/', indicator_details_json, name='indicator_details_json'),
    path('kra/<int:kra_id>/', filter_indicators_by_kra, name='filter_indicators_by_kra'),
    path('search_autocomplete_indicator_list/', auto_complete_search_indicator, name='dashboard-indicator-lists-auto-complete'),


     #######################################################################################################

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
    path('api/ministry/ministries/',MinistryDashboard.ministries),
    path('api/ministry/goal_with_kra/<str:id>/',MinistryDashboard.goal_with_kra),
    path('api/ministry/indicator/<str:id>/',MinistryDashboard.indicator),
    path('api/ministry/time_series_year/',MinistryDashboard.time_series_year),
    path('api/ministry/dashboard/' ,MinistryDashboard.dashboard),
    path('api/ministry/dashboard_ministries/<str:ministry_id>/',MinistryDashboard.dashboard_ministries),
    path('api/ministry/indicatorsInGoal/<str:id>/',MinistryDashboard.indicatorsInGoal),
    path('api/ministry/ministry_kra_serializer/<str:ministry_id>/',MinistryDashboard.ministry_kra_serializer),
    path('api/ministry/ministry_indicator_performance/<str:ministry_id>/',MinistryDashboard.ministry_indicator_performance),

    path('min/', ministry_index3, name='ministry_index'),
    path('pm/', policy_area3, name='policy_area'),
    path('info/',info3, name="info"),
    path('search/', search3, name='search'),

   ##AUDIT 
   path('audit/', audit_log_list, name="audit"),


]
