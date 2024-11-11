
from django.urls import path
from . import views

urlpatterns = [
    
    path('planninghome/', views.planninghome,name="home"),
# adding strategic goals
    path('strategic_gola/add', views.add_strategic_goal, name = "addstrategicgoal"),
# update strategic goals
    path('strategic_gola/update/<int:id>', views.update_strategic_goal, name = "updatestrategicgoal"),
# delete strategic goals
    path('strategic_gola/delete/<int:goal_id>', views.delete_goal, name = "deletestrategicgoal"),
# goal commet
    path('strategic_gola/comment/<int:goal_id>', views.goal_comment, name = "comment_goal"),
    
# KRA related 
    path('key_result_area/',views.add_key_result_area, name = "key_result_area"),
# update KRA
    path('key_result_area/update/<int:id>', views.update_kra, name = "updatekra"),
# delete KRA
    path('key_result_area/delete/<int:kra_id>', views.delete_KRA, name = "deletekra"),
# kRA comment
    path('key_result_area/comment/<int:kra_id>', views.kra_comment, name = "commentkra"),
# KPI related
    path('key_performance_indicator/',views.add_key_performance_indicator,name = "key_performance_indicator"),
# modified pre order tree traversal
    path('mptt_key_performance_indicator/<int:id>/',views.add_mptt_key_performance_indicator,name = "mptt_key_performance_indicator"),

# update KPI
    path('key_performance_indicator/update/<int:id>', views.update_kpi, name = "updatekpi"),

# delete KPI
    path('key_performance_indicator/delete/<int:kpi_id>', views.delete_kpi, name = "deletekpi"),
# comment KPI
    path('key_performance_indicator/comment/<int:kpi_id>', views.kpi_comment, name = "commentkpi"),
    
    path('delete/<int:id>/',views.delete_goal,name="goal_delete"),
    
    # path('goal/<int:id>/status', views.goal_status,name="change_status"),
    path('kpiplanning/<int:id>', views.kpiplanning, name="kpiplanning"),
    # quarter plan urls
    path('addquarterpla/<int:id>/', views.quarterplan, name="addquarterplan"),
    path('updatequarterpla/<int:id>/', views.update_Quarter_Plan, name="updatequarterplan")
]