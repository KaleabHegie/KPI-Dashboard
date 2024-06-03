from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import MinistrySerializers , GoalSerializers  ,  ResponsibleMinistrySerializer , KeyResultAreaSerializer2
from django.http import JsonResponse
from userManagement.models import ResponsibleMinistry
from django.shortcuts import get_object_or_404
from django.db.models import F
import time
from .models import (
    StrategicGoal , 
    Indicator , 
    KeyResultArea,
    DashboardSetting,
    AnnualPlan,
    MonthProgress,
    QuarterProgress,
    Year ,StrategicGoal, Indicator, AnnualPlan, QuarterProgress, MonthProgress
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
def filter_indicators_by_kra(request, kra_id):
    try:
        kra = KeyResultArea.objects.prefetch_related('indicators').get(id=kra_id)
    except KeyResultArea.DoesNotExist:
        return JsonResponse({'error': 'Key Result Area not found'}, status=404)
    
    serializer = KeyResultAreaSerializer2(kra)
    return JsonResponse(serializer.data)



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



@api_view(['GET'])
def ministry_goal_front(request, id):
    if request.method == 'GET':
        # Fetch the ministry with related goals and KRAs
        ministry = ResponsibleMinistry.objects.prefetch_related(
            'ministry_goal__kra_goal'
        ).get(id=id)

        # Serialize the data
        serializer = ResponsibleMinistrySerializer(ministry)

        # Structure the context
        context = serializer.data

        return JsonResponse(context)




def indicator_details_json(request, indicator_id):
    # Fetch the specific Indicator by ID using select_related
    indicator = get_object_or_404(Indicator.objects.select_related(
        'keyResultArea__goal', 'responsible_ministries'
    ), pk=indicator_id)

    # Prepare data structure
    data = {
        "indicator_id": indicator.id,
        "kpi_name_eng": indicator.kpi_name_eng,
        "kpi_name_amh": indicator.kpi_name_amh,
        "kpi_weight": indicator.kpi_weight,
        "kpi_measurement_units": indicator.kpi_measurement_units,
        "kpi_characteristics": indicator.kpi_characteristics,
        "responsible_ministries__code": indicator.responsible_ministries.code,
        "quarter_progress": [],
        "month_progress": [],
        "annual_plans": []
    }

    # Fetch quarter progress data related to the indicator and order by year and quarter
    quarter_progress = QuarterProgress.objects.filter(indicator=indicator).order_by('year', 'quarter__quarter_eng')
    for quarter in quarter_progress:
        data["quarter_progress"].append({
            "quarter": quarter.quarter.quarter_eng,
            "year": quarter.year.year_amh,
            "quarter_target": quarter.quarter_target,
            "quarter_performance": quarter.quarter_performance,
            "quarter_date": quarter.quarter_date
        })

    # Fetch month progress data related to the indicator
    month_progress = MonthProgress.objects.filter(indicator=indicator)
    for month in month_progress:
        data["month_progress"].append({
            "month": month.month.month_english,
            "year": month.year.year_amh,
            "monthly_target": month.monthly_target,
            "month_performance": month.month_performance,
            "date": month.date
        })

    # Fetch annual plan data related to the indicator and order by year
    annual_plans = AnnualPlan.objects.filter(indicator=indicator).order_by('year')
    for plan in annual_plans:
        data["annual_plans"].append({
            "year": plan.year.year_amh,
            "annual_target": plan.annual_target,
            "annual_performance": plan.annual_performance,
            "target_state": plan.target_state,
            "annual_date": plan.annual_date
        })

    time.sleep(3)
    return JsonResponse(data)

