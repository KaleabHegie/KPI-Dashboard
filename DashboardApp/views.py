from django.shortcuts import render , redirect


from rest_framework.decorators import api_view
from .serializers import *
from django.http import JsonResponse
from userManagement.models import ResponsibleMinistry
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib.auth import login,authenticate,logout
import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userManagement.forms import LoginFormDashboard
from .models import *
from django.db.models import Count
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@login_required(login_url='dashboard-login')
def index(request):
    return render(request, 'dashboard-app/dashboard-index.html')



@login_required(login_url='dashboard-login')
@api_view(['GET'])
def ministries_lists(request):
    if request.method == 'GET':
        ministries = ResponsibleMinistry.objects.annotate(goal_count=Count('ministry_goal')).select_related()
        # ministries = ministries.filter(~Q(category_count = 0)) #Only Display with category > 0
        serializer = MinistrySerializers(ministries, many=True)
        return JsonResponse({'ministries':serializer.data})


@login_required(login_url='dashboard-login')
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




@login_required(login_url='dashboard-login')
@api_view(['GET'])
def filter_indicators_by_kra(request, kra_id):
    try:
        kra = KeyResultArea.objects.prefetch_related('indicators').get(id=kra_id)
    except KeyResultArea.DoesNotExist:
        return JsonResponse({'error': 'Key Result Area not found'}, status=404)
    
    serializer = KeyResultAreaSerializer2(kra)
    return JsonResponse(serializer.data)



@login_required(login_url='dashboard-login')
@api_view(['GET'])
def indicator_lists(request, id):
    if request.method == 'GET':
        kra = KeyResultArea.objects.filter(goal__id = id)
        indicators = Indicator.objects.filter(keyResultArea__in = kra)

        if 'q' in request.GET:
            q = request.GET['q']
            indicators = Indicator.objects.filter(Q(kpi_name_eng__contains=q) | Q(kpi_name_amh__contains=q) | Q(responsible_ministries__responsible_ministry_eng__contains=q) | Q(responsible_ministries__code__contains=q) )
            kra_id = indicators.filter().values_list('keyResultArea__id', flat=True)
            kra = KeyResultArea.objects.filter(id__in = kra_id)


        value_annual = list(AnnualPlan.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator").values(
            'annual_target',
            'annual_performance',
            'indicator__id',
            'year__year_eng',
            'year__year_amh'
        ))

        value_quarter = list(QuarterProgress.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator", 'quarter').values(
            'quarter__quarter_eng',
            'quarter_target',
            'quarter_performance',
            'indicator__id',
            'year__year_eng',
            'year__year_amh'
        ))

        value_month = list(MonthProgress.objects.filter( Q(indicator__in=indicators)).select_related("year", "indicator", "month").values(
            'month__month_english',
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
                'is_score_card' : setting.is_score_card,
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
            'kpi_characteristics',
            )
        score_card =  list(ScoreCardRange.objects.all().values())



       

        context = {
            'kra' : list(kra),
            'indicators' : list(indicators),
            'dashboardSetting' : dashboardSetting,
            'value_annual' : value_annual,
            'value_quarter' : value_quarter,
            'value_month' : value_month,
             'score_card' : score_card,
        }
        return JsonResponse(context)




@login_required(login_url='dashboard-login')
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



@login_required(login_url='dashboard-login')
@api_view(['GET'])
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

    return JsonResponse(data)



@login_required(login_url='dashboard-login')
@api_view(['GET'])
def auto_complete_search_indicator(request):
    queryset = []
    if 'search' in request.GET:
            q = request.GET['search']
            queryset = Indicator.objects.filter(Q(kpi_name_eng__contains=q) | Q(kpi_name_amh__contains=q) | Q(responsible_ministries__responsible_ministry_eng__contains=q) | Q(responsible_ministries__code__contains=q) ).values(
                'kpi_name_eng',
            )[:15]
    return JsonResponse({'indicators': list(queryset)})




#============================================
#               Mine
#============================================
@login_required(login_url='dashboard-login')
def get_previous_year_performance(chrx, year,Previndicator,per, target,national_plan):
        # Calculate and return the change in performance compared to the previous year
        previous_year = year.year_amh - 1
        try:
            previous_year_plan = AnnualPlan.objects.get(
                year__year_amh=previous_year,
                national_plan= national_plan,
                indicator= Previndicator,
            )
            if previous_year_plan.annual_performance is not None and per is not None:
                performance_change = per - \
                    previous_year_plan.annual_performance


                performance_change_percent = (
                    (per - previous_year_plan.annual_performance)/previous_year_plan.annual_performance) * 100

                if Previndicator.kpi_characteristics == 'inc':
                    # For increasing KPIs, positive change is good, and negative change is bad
                    return [performance_change, performance_change_percent]
                elif Previndicator.kpi_characteristics == 'dec':
                    # For decreasing KPIs, negative change is good, and positive change is bad
                    return [-performance_change, -performance_change_percent]
                else:
                    # For constant KPIs, return the change without modifying its sign
                    return [performance_change, performance_change_percent]
            else:
                return None
        except AnnualPlan.DoesNotExist:
            return None


@login_required(login_url='dashboard-login')
def indicator_details_json(request, indicator_id):
    # Fetch the specific Indicator by ID using select_related
    indicator = get_object_or_404(Indicator.objects.select_related(
        'keyResultArea__goal', 'responsible_ministries'
    ), pk=indicator_id)

    # Access the related StrategicGoal
    goal_name_eng = None
    kra_activity_name_eng = None

    if indicator.keyResultArea:
        kra_activity_name_eng = indicator.keyResultArea.activity_name_eng
    if indicator.keyResultArea and indicator.keyResultArea.goal:
        goal_name_eng = indicator.keyResultArea.goal.goal_name_eng

    # Prepare data structure
    data = {
        "indicator_id": indicator.id,
        "kpi_name_eng": indicator.kpi_name_eng,
        "kpi_name_amh": indicator.kpi_name_amh,
        "kpi_weight": indicator.kpi_weight,
        "kpi_measurement_units": indicator.kpi_measurement_units,
        "kpi_characteristics": indicator.kpi_characteristics,
        "responsible_ministries__code": indicator.responsible_ministries.code,
        "kra_activity_name_eng": kra_activity_name_eng,
        "goal_name_eng": goal_name_eng,
        "quarter_progress": [],
        "month_progress": [],
        "annual_plans": [],
        "score_card_ranges": []
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
            "monthly_target": month.month_target,
            "month_performance": month.month_performance,
            "date": month.date
        })

    # Fetch annual plan data related to the indicator and order by year
    annual_plans = AnnualPlan.objects.filter(indicator=indicator).order_by('year')
    for plan in annual_plans:
        performance_per = get_previous_year_performance(plan.indicator.kpi_characteristics, plan.year, plan.indicator, plan.annual_performance, plan.annual_target, plan.national_plan)
        data["annual_plans"].append({
            "year": plan.year.year_amh,
            "annual_target": plan.annual_target,
            "annual_performance": plan.annual_performance,
            "target_state": plan.target_state,
            "annual_date": plan.annual_date,
            'perfomance_comp': performance_per
        })

    # Fetch score card range data
    score_card_ranges = ScoreCardRange.objects.all()
    for range_obj in score_card_ranges:
        data["score_card_ranges"].append({
            "name": range_obj.name,
            "color": range_obj.color,
            "starting": range_obj.starting,
            "ending": range_obj.ending
        })

    return JsonResponse(data)
#============================================




##### Login ######
def dashboard_login(request):
    form = LoginFormDashboard(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request,email=email,password=password)
        if user is not None and user.is_admin:
            login(request, user)
            return redirect('dashboard-api')
        else:
            messages.error(request, 'Invalid Password or Email')
        form = LoginFormDashboard()
    context = {
        'form' : form
    }
    return render(request, 'dashboard-app/authentication/login.html', context=context)


@login_required(login_url='dashboard-login')
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard-login')





def policy_area(request):
    import random

    for policy_area in PolicyArea.objects.all():
        goals = list(policy_area.policy_area_goal.all())
        num_goals = len(goals)
    
        if num_goals == 0:
            continue
    
        random_weights = [random.random() for _ in range(num_goals)]
        total = sum(random_weights)
    
        # Scale the weights to be in the range of 0 to 100
        scaled_weights = [(weight / total) * 100 for weight in random_weights]
    
        # Ensure no weight is negative (they should already be non-negative if using random.random())
        # But if you're using any other method, you can filter negative weights here.
        scaled_weights = [max(0.0, weight) for weight in scaled_weights]
    
        # Adjust weights to make sure they sum to 100
        total_scaled = sum(scaled_weights)
        diff = 100 - total_scaled
    
        if diff != 0:
            # Distributing the difference proportionally to each weight
            for i in range(num_goals):
                scaled_weights[i] += (scaled_weights[i] / total_scaled) * diff
    
        for goal, weight in zip(goals, scaled_weights):
            goal.goal_weight = weight  # Weights can be decimals
            goal.save()



    return render(request, 'PolicyAndMinistries/index.html')

def info(request): 
    return render(request, 'PolicyAndMinistries/info.html')

def search(request):
    return render(request, 'PolicyAndMinistries/search.html')


def ministry_index(request):
    return render(request, 'PolicyAndMinistries/ministries_index.html')



    
