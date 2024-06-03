from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import MinistrySerializers , GoalSerializers
from django.http import JsonResponse
from userManagement.models import ResponsibleMinistry
from .models import (
    StrategicGoal , 
    Indicator , 
    KeyResultArea,
    DashboardSetting,
    AnnualPlan,
    MonthProgress,
    QuarterProgress,
    Year
)
from django.db.models import Count
import time
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
def ministry_goal(request, id):
    if request.method == 'GET':
        ministry_goal = list(StrategicGoal.objects.filter(responsible_ministries__id = id).values(
            'id',
            'goal_name_eng',
            'goal_weight',
        ))

        context = {
            'ministry_goal' : ministry_goal
        }
        return JsonResponse(context)


@api_view(['GET'])
def indicator_lists(request, id):
    if request.method == 'GET':
        kra = KeyResultArea.objects.filter(goal__id = id)
        indicators = Indicator.objects.filter(keyResultArea__in = kra)



        value_annual = list(AnnualPlan.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator").values(
            'annual_target',
            'annual_performance',
            'indicator__id',
            'year__year_eng',
            'year__year_amh'
        ))

        value_quarter = list(QuarterProgress.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator").values(
            'quarter_target',
            'quarter_performance',
            'indicator__id',
            'year__year_eng',
            'year__year_amh'
        ))

        value_month = list(MonthProgress.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator").values(
            'month_target',
            'month_performance',
            'indicator__id',
            'year__year_eng',
            'year__year_amh'
        ))


        dashboardSetting = []
        for setting in DashboardSetting.objects.select_related():
            dashboardSetting.append({
                'id' : setting.id,
                'performance' : setting.performance,
                'target' : setting.target,
                'year__year_eng' : setting.year.year_eng,
                'year__year_amh' : setting.year.year_amh,
                'month_id' : setting.month.id if setting.month else None,
                'quarter_id' : setting.quarter.id if setting.quarter else None,
                'indicator_id' : list(setting.indicator.filter(id__in=indicators).values_list('id', flat=True))
            })


        kra = kra.values(
            'id',
            'activity_name_eng',
            'activity_weight',
        )


        indicators = indicators.values(
            'id',
            'keyResultArea_id',
            'kpi_name_eng',
            'kpi_weight',
            )



       

        context = {
            'kra' : list(kra),
            'indicators' : list(indicators),
            'dashboardSetting' : dashboardSetting,
            'value_annual' : value_annual,
            'value_quarter' : value_quarter,
            'value_month' : value_month,

        }
        #time.sleep(1)
        return JsonResponse(context)




