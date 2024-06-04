from django.urls import path

from .views import (
    index , 
    ministries_lists,
    ministry_goal,
    indicator_lists,
    indicator_details_json,
    ministry_goal_front,
    filter_indicators_by_kra,
    auto_complete_search_indicator
) 
urlpatterns = [
    path('', index, name='dashboard-api'),
    path('ministries_lists/',ministries_lists, name="dashboard-ministries_lists"),
    path('ministry-goal/<str:id>/',ministry_goal, name="dashboard-ministries_lists"),
    path('ministry_goal_front/<str:id>/',ministry_goal_front, name="ministry_goal_front"),
    path('indicator_lists/<str:id>/',indicator_lists, name="dashboard-indicator_lists"),
    path('indicator-details/<int:indicator_id>/', indicator_details_json, name='indicator_details_json'),
    path('kra/<int:kra_id>/', filter_indicators_by_kra, name='filter_indicators_by_kra'),
    path('search_autocomplete_indicator_list/', auto_complete_search_indicator, name='dashboard-indicator-lists-auto-complete'),
]
