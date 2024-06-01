from django.urls import path

from .views import (
    index , ministries_lists , goal_list , key_area_list
) 
urlpatterns = [
    path('', index, name='dashboard-api'),
    path('ministries_lists/',ministries_lists, name="ministries_lists"),
    path('goal_list/<int:id>',goal_list, name="goal_list"),
    path('key_area_list/<int:id>',key_area_list, name="key_area_list"),
]
