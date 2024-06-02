from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import MinistrySerializers , GoalSerializers
from django.http import JsonResponse
from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal , Indicator , KeyResultArea
from django.db.models import Count
from django.core import serializers
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'dashboard-app/dashboard-index.html')



@api_view(['GET'])
def ministries_lists(request):

    if request.method == 'GET':
        ministries = ResponsibleMinistry.objects.annotate(goal_count=Count('ministry_goal')).select_related()
        # ministries = ministries.filter(~Q(category_count = 0)) #Only Display with category > 0
        serializer = MinistrySerializers(ministries, many=True)
        
        return JsonResponse({'ministries':serializer.data})

@api_view(['GET'])
def goal_list(request, id): 


    if request.method == 'GET':
        goal_list = StrategicGoal.objects.filter(responsible_ministries__id=id)
        # ministries = ministries.filter(~Q(category_count = 0)) #Only Display with category > 0
        serializer = GoalSerializers(goal_list, many=True)
        
        return JsonResponse({'goal_list':serializer.data})

from django.db.models import F

@api_view(['GET'])
def key_area_list(request, id): 
    goal_list_id = list(StrategicGoal.objects.filter(responsible_ministries__id=id).prefetch_related('kra_goal__set').all().values_list('kra_goal__id', flat=True))

    goal_list = list(StrategicGoal.objects.filter(responsible_ministries__id=id).prefetch_related("kra_goal__set").all().values('id','goal_name_eng'))
    KeyResultArea_list = list(KeyResultArea.objects.filter(Q(id__in=goal_list_id)).prefetch_related('indicator__set','goal_set').annotate(kpi_name_eng=F('indicator__kpi_name_eng'),goal_name_eng=F('goal__`goal_name_eng')).values('id', 'activity_name_eng', 'kpi_name_eng' , 'goal_id'))# value_filter = list(DataValue.objects.filter(Q(for_indicator__id__in=indicator_list_id) & ~Q(for_datapoint_id__year_EC=None)).select_related("for_datapoint", "for_indicator").order_by('for_datapoint_id__year_EC').values(
    return JsonResponse({
        "KeyResultArea_list" : KeyResultArea_list,
        "goal_list" :goal_list
    })



