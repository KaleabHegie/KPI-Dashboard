from django.urls import path

from .views import (
    index , 
    ministries_lists,
    ministry_goal,
    indicator_lists
) 
urlpatterns = [
    path('', index, name='dashboard-api'),
    path('ministries_lists/',ministries_lists, name="dashboard-ministries_lists"),
    path('ministry-goal/<str:id>/',ministry_goal, name="dashboard-ministries_lists"),
    path('indicator_lists/<str:id>/',indicator_lists, name="dashboard-indicator_lists"),
]
