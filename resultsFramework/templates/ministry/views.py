# Import your models
import random  # Import the random module
from comment.models import Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .utility import PlanEntryDate, QuarterPerformanceEntryDate, AnnualPerformanceEntryDate, QuarterPlanEntryDate
from .models import AnnualPlan2, Indicator, KpiAggregation, Post, AnnualPlan, NationalPlan, Quarter, QuarterProgress, ScoreCardRange, Year, StrategicGoal, KeyResultArea,PolicyArea
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from userManagement.models import ResponsibleMinistry, UserSector
from userManagement.decorators import *
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db import IntegrityError
import json
from collections import defaultdict
from django.db.models import Min,Prefetch
from django.core.cache import cache
from django.conf import settings
import datetime
from .admin import *
from django import forms
from django.contrib import messages 
from .resource import *
from datetime import date
class ImportFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control'
    }))




CACHE_TIMEOUT = 2 * 1 # 1 hour
def current_year():


    today = date.today()

    year = today.year - 1

    return year

    
    
@login_required
@sector_user_required
def ministry_dashboard(request):
    year = Year.objects.filter(visible = True)
    u_sector = UserSector.objects.get(user=request.user)


    indicator = Indicator.objects.filter(responsible_ministries_id=u_sector.user_sector.id)[0:8]
    
    
    random_indicators = random.sample(list(indicator), min(3, len(indicator)))

    # Use Prefetch to filter and annotate in a single query
    random_kpi  = AnnualPlan.objects.filter(
        indicator__in=random_indicators,
        annual_performance__isnull=False,
        year__year_eng=current_year()
    )

    

    # Use Prefetch to filter and annotate in a single query
    plans_with_performance = AnnualPlan.objects.filter(
        indicator__in=indicator,
        annual_performance__isnull=False,
        year__year_eng = current_year()
    )

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).count()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).count()



    context = {
         'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        'policy_area_count':policy_area_count,
        'ministry': u_sector.user_sector,
        'years':year, 
        'plans_with_performance':plans_with_performance,
        'random_kpi':random_kpi
    }

    return render(request, 'ministry/dashboard_ministry.html', context)

def kpi_count_for_goal(kra_id: int) -> int:
    """Retrieves KPI count for a given Key Result Area ID, optimized for performance."""
    return Indicator.objects.filter(keyResultArea__id=kra_id).count()

def bubble_chart(request):
    # Cache key based on user sector and strategic goals
    cache_key = f'bubble_chart_data_{request.user.pk}'

    # Check cache for existing data
    data = cache.get(cache_key)

    if data is None:
        # Efficiently fetch data using prefetch_related
        u_sector = UserSector.objects.get(user=request.user)
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal'  # Prefetch activities and KPIs
        ).filter(responsible_ministries=u_sector.user_sector)

        # Prepare data for Highcharts
        data = []
        for goal in strategic_goals:
            goal_data = {
                'name': goal.goal_name_eng,
                'data': []  # Placeholder for child bubbles
            }
            for activity in goal.kra_goal.all():
                goal_data['data'].append({
                    'name': activity.activity_name_eng,
                    'value': kpi_count_for_goal(activity.id)
                })
            data.append(goal_data)

        # Set cache with expiration if desired
        # cache.set(cache_key, data, timeout=settings.CACHE_TTL_BUBBLE_CHART)

    chart_data = {
        'chart_type': 'packedbubble',
        'title': 'Strategic Goals and Key Result Areas',
        'series': data
    }

    return JsonResponse(chart_data)
        
           
from django.http import JsonResponse
from .models import Indicator

def count_performed_kpis(request, target_year=None):
    u_sector = UserSector.objects.get(user=request.user)   
    data = {'poor': 0, 'average': 0, 'good': 0}
    total_kpis = 0  # Total number of KPIs, including those without performance or target
    total_performance = 0  # Total performance across all KPIs

    indicators = Indicator.objects.filter(responsible_ministries=u_sector.user_sector)

    for indicator in indicators:
        total_kpis += 1  # Increment total KPIs count

        annual_plans = indicator.annual_indicators.filter(year__year_eng=target_year)

        if not annual_plans.exists():
            # If there are no annual plans for the specified year, consider it as without performance or target
            data['poor'] += 1
            continue

        for annual_plan in annual_plans:
            if annual_plan.annual_performance:
                percentage = annual_plan.calculate_score_and_card()[0]

                if float(percentage) <= 30:
                    data['poor'] += 1
                elif 30 < float(percentage) <= 70:
                    data['average'] += 1
                elif float(percentage) > 70:
                    data['good'] += 1

                # Increment total performance
                total_performance += percentage

    # Calculate the percentage of KPIs without performance or target
    no_data_percentage = (total_kpis - len(indicators)) / total_kpis * 100

    # Calculate total performance percentage
    total_performance_percentage = (total_performance / total_kpis) if total_kpis > 0 else 0

    # Prepare data for Highcharts pie chart
    chart_data = {
        'chart': {
            'type': 'pie',
        },
        'title': {
            'text': f'Performance State for {target_year}',
        },
        'series': [{
            'name': 'KPIs',
            'colorByPoint': True,
            'data': [{
                'name': 'poor',
                'y': data.get('poor'),
                'percentage': round(data.get('poor') / total_kpis * 100, 2),
            }, {
                'name': 'average',
                'y': data.get('average'),
                'percentage': round(data.get('average') / total_kpis * 100, 2),
            }, {
                'name': 'good',
                'y': data.get('good'),
                'percentage': round(data.get('good') / total_kpis * 100, 2),
            }, {
                'name': 'No Data',
                'y': len(indicators) - total_kpis,
                'percentage': round(no_data_percentage, 2),
            }]
        }]
    }

    # Prepare data for Total Performance chart
    total_performance_data = {
        'total_performance': total_performance_percentage,
    }

    return JsonResponse({'chart_data': chart_data, 'total_performance_data': total_performance_data}, safe=False)



def get_random_color():
    import random
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# def get_treegraph_data(request):
#   strategic_goals = StrategicGoal.objects.all()
#   data = []

#   # Create a dictionary to map model objects to their IDs
#   obj_map = {}

#   for goal in strategic_goals:
#     goal_data = {
#       'parent': None,
#       'id': goal.goal_name_eng,
#       'level': 0
#     }

#     data.append(goal_data)
#     obj_map[goal.goal_name_eng] = goal


#     key_result_areas = KeyResultArea.objects.filter(goal=goal)
#     for kra in key_result_areas:
#       kra_data = {
#         'parent': goal.goal_name_eng if goal.goal_name_eng else None,
#         'id': kra.activity_name_eng,
#         'level': 1
#       }

#       data.append(kra_data)
#       obj_map[kra.activity_name_eng] = kra

#       indicators = Indicator.objects.filter(keyResultArea=kra)
#       for indicator in indicators:
#         indicator_data = {
#           'parent': kra.activity_name_eng if kra.activity_name_eng else None,
#           'id': indicator.kpi_name_eng,
#           'level': 2
#         }

#         data.append(indicator_data)
#         obj_map[indicator.kpi_name_eng] = indicator

# #   return JsonResponse({'data': data, 'obj_map': obj_map})
#   return JsonResponse(CircularReferenceSerializer().serialize(data), safe=False)

# class CircularReferenceSerializer(JSONSerializer):
#     def default(self, obj):
#         if isinstance(obj, (StrategicGoal, KeyResultArea, Indicator)):
#             return obj.id
#         else:
#             return super().default(obj)


def view_goals(request):
    # Get the ResponsibleMinistry object or return a 404 error if it doesn't exist

    u_sector = UserSector.objects.get(user=request.user)

    # Filter StrategicGoal objects based on the responsible ministry
    goal = StrategicGoal.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id)

    # Define any other context data you want to pass to the template
    context = {
        'goals': goal,

    }

    # Render the template with the context data
    return render(request, 'ministry/view_goals.html', context)


def view_key_result_areas(request):
    u_sector = UserSector.objects.get(user=request.user)

    # Get all StrategicGoals related to the responsible ministry
    goals = StrategicGoal.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).prefetch_related('kra_goal')

    # Define the context data
    context = {
        'goals': goals,
    }

    return render(request, 'ministry/view_kra.html', context)


@login_required
@sector_user_required
def kpi_ministry(request):

        u_sector = UserSector.objects.get(user=request.user)

        indicators = Indicator.objects.filter(
            responsible_ministries=u_sector.user_sector).prefetch_related('sub_kpi')
        entry = AnnualPerformanceEntryDate.objects.filter(active=True).first()
        annual_plans = AnnualPlan.objects.filter(
            Q(indicator__responsible_ministries=u_sector.user_sector) |
            Q(sub_indicator__kpi__responsible_ministries=u_sector.user_sector)
        ).select_related('indicator', 'sub_indicator', 'year').all()

        years = Year.objects.filter(visible = True)
        paginator = Paginator(indicators, 41)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'indicators': page_obj,
            'years': years,
            'annual_plans': annual_plans,
            'entry': entry
        }

        return render(request, 'dashboard_ministry.html', context)





from django.core.cache import cache

def get_strategic_goals_with_policies_cache(ministry_id, selected_policies):
    cache_key = f"strategic_goals_ministry_{ministry_id}_policies_{'_'.join(map(str, selected_policies))}"
    strategic_goals = cache.get(cache_key)

    if not strategic_goals:
        indicators_prefetch = Prefetch(
            'indicators',
            queryset=Indicator.objects.filter(responsible_ministries_id=ministry_id)
        )

        kras_prefetch = Prefetch(
            'kra_goal',
            queryset=KeyResultArea.objects.prefetch_related(indicators_prefetch)
        )

        strategic_goals = StrategicGoal.objects.prefetch_related(
            kras_prefetch
        ).filter(
            policy_area_id__in=selected_policies,
            kra_goal__indicators__responsible_ministries_id=ministry_id
        ).distinct()

        cache.set(cache_key, strategic_goals, CACHE_TIMEOUT)

    return strategic_goals

def get_strategic_goals_with_cache(ministry_id):
    cache_key = f"strategic_goals_with_ministry_{ministry_id}"
    cache_key2 = f"kra_with_ministry_{ministry_id}"
    strategic_goals = cache.get(cache_key)
    kra = cache.get(cache_key2)
    
    if strategic_goals is None or  kra is None:
        # Prefetch indicators related to the specific ministry
        indicators_prefetch = Prefetch(
            'indicators',
            queryset=Indicator.objects.filter(responsible_ministries_id=ministry_id)
        )
        kra = KeyResultArea.objects.filter(indicators__responsible_ministries_id=ministry_id).distinct()
        # Prefetch KRAs with the prefetched indicators
        kras_prefetch = Prefetch(
            'kra_goal',
            queryset=KeyResultArea.objects.prefetch_related(indicators_prefetch)
        )

        # Filter strategic goals by the selected ministry and prefetch related KRAs and indicators
        strategic_goals = StrategicGoal.objects.filter(
            kra_goal__indicators__responsible_ministries_id=ministry_id
        ).prefetch_related(kras_prefetch).distinct()

        # Cache the results
        cache.set(cache_key, strategic_goals, CACHE_TIMEOUT)
        cache.set(cache_key2, kra, CACHE_TIMEOUT)

    return [strategic_goals,kra]



def get_policy_areas_by_ministry(ministry_id):
    cache_key = f"policy_areas_{ministry_id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        # Querying with prefetch_related to minimize database queries
        indicators = Indicator.objects.filter(
            responsible_ministries__id=ministry_id
        )
        
        # Get all KeyResultArea IDs associated with these indicators
        kra_ids = indicators.values_list('keyResultArea__id', flat=True)
        
        # Filter distinct StrategicGoal IDs based on these KRA IDs
        goal = StrategicGoal.objects.filter(kra_goal__id__in=kra_ids)

        policy_ids = goal.values_list('policy_area__id', flat=True)
        # Filter PolicyArea objects based on these Goal IDs
        policy_areas = PolicyArea.objects.filter(id__in=policy_ids).distinct()

        # Cache the result for future requests
        cache.set(cache_key, policy_areas, CACHE_TIMEOUT)

        return policy_areas

    except Exception as e:
        # Handle exceptions as needed
        print(f"Error fetching policy areas: {e}")
        return PolicyArea.objects.none()  # Return an empty queryset or handle appropriately







def mdip_ministry(request):
    u_sector = UserSector.objects.get(user=request.user)

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).count()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).count()
    


    # Fetch all policies for the dropdown
    policies = get_policy_areas_by_ministry(u_sector.user_sector.id )
    # Fetch strategic goals with related KeyResultAreas and Indicators

    strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        ).filter(policy_area_id__in=policies)


    # Fetch all visible years for the annual plans
    years = Year.objects.filter(mdip=True)

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

   
    context = {
        
        'strategic_goals': strategic_goals,
        'years': years,
        'annual_plans_lookup': annual_plans_lookup,
      
        'policies': policies,    # Pass the policies to the context for the dropdown
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        
        'policy_area_count':policy_area_count,
        
    }


    return render(request, 'ministry/mdip_ministry.html', context)



@login_required
@sector_user_required
def kpi_ministry_plan(request):
    form_file = ImportFileForm()
    u_sector = UserSector.objects.get(user=request.user)
    ministry_id = u_sector.user_sector.id

    policy_area_count = get_policy_areas_by_ministry(ministry_id).count()
    goal_count, kra_count = get_strategic_goals_with_cache(ministry_id)
    goal_count = goal_count.count()
    kra_count = kra_count.count()
    indicator_count = Indicator.objects.filter(responsible_ministries_id=ministry_id).count()

    entry = PlanEntryDate.objects.filter(active=True).first()
    qentry = QuarterPlanEntryDate.objects.filter(active=True).first()

    selected_policies = request.GET.getlist('selected_policies[]')
    policies = get_policy_areas_by_ministry(ministry_id)

    if selected_policies:
        strategic_goals = get_strategic_goals_with_policies_cache(ministry_id, selected_policies)
    else:
        strategic_goals = get_strategic_goals_with_cache(ministry_id)[0]

    years = Year.objects.filter(visible=True)
    quarters = Quarter.objects.all()

    annual_plans = AnnualPlan.objects.select_related('indicator', 'sub_indicator', 'year').filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector)
    annual_plans_lookup = {plan.indicator_id: {plan.year_id: plan} for plan in annual_plans}

    quarter_progress = QuarterProgress.objects.select_related('indicator', 'quarter', 'year').filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector)
    quarter_progress_lookup = {progress.indicator_id: {progress.year_id: {progress.quarter_id: progress}} for progress in quarter_progress}
    global imported_data_global,success,result
    if request.method == "POST":
        if 'fileAnnualValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_quarter_plan1(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'ministry/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')
        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'quarterPlan')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    context = {
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        'policy_area_count': policy_area_count,
        'strategic_goals': strategic_goals,
        'years': years,
        'quarters': quarters,
        'entry': entry,
        'qentry': qentry,
        'formFile': form_file,
        'annual_plans_lookup': annual_plans_lookup,
        'quarter_progress_lookup': quarter_progress_lookup,
        'policies': policies,
        'selected_policies': selected_policies,
    }

    return render(request, 'ministry/kpi_ministry_insert_plan.html', context)





def mopd_policy_area(request):


    policy_area = PolicyArea.objects.all()

   

    policy_colors = {   
        1: 'bg-info',
        2: 'bg-secondary',
        3: 'bg-success',
        4: 'bg-info',
        5: 'bg-warning',
        6: 'bg-info',
        7: 'bg-dark',
        8: 'bg-warning',
        9: 'bg-info',
        10: 'bg-secondary',
        11: 'bg-info',
        12: 'bg-secondary',
        13: 'bg-success',
        14: 'bg-info',
        15: 'bg-warning',
        16: 'bg-info',
        17: 'bg-warning',
        18: 'bg-dark',
        19: 'bg-info',
        20: 'bg-success',
        21: 'bg-warning',
        22: 'bg-secondary',
        23: 'bg-success',
        24: 'bg-warning',
        # Add more policies and corresponding colors as needed
    }

    context = {
       
        'policy_area':policy_area,
        'policy_colors':policy_colors
    }

    return render(request, 'mopd/mopd_policy_area.html', context)










def policy_area_ministry(request):

    u_sector = UserSector.objects.get(user=request.user)
    policy_area = PolicyArea.objects.all()

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).count()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).count()

    policy_colors = {   
        1: 'bg-info',
        2: 'bg-secondary',
        3: 'bg-success',
        4: 'bg-info',
        5: 'bg-warning',
        6: 'bg-info',
        7: 'bg-dark',
        8: 'bg-warning',
        9: 'bg-info',
        10: 'bg-secondary',
        11: 'bg-info',
        12: 'bg-secondary',
        13: 'bg-success',
        14: 'bg-info',
        15: 'bg-warning',
        16: 'bg-info',
        17: 'bg-warning',
        18: 'bg-dark',
        19: 'bg-info',
        20: 'bg-success',
        21: 'bg-warning',
        22: 'bg-secondary',
        23: 'bg-success',
        24: 'bg-warning',
        # Add more policies and corresponding colors as needed
    }

    context = {
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        
        'policy_area_count':policy_area_count,
        'policy_area':policy_area,
        'policy_colors':policy_colors
    }

    return render(request, 'ministry/policy_area.html', context)






@login_required
@sector_user_required
def kpi_ministry_new(request):

    entry  = AnnualPerformanceEntryDate.objects.filter(active=True).first()
    qentry = QuarterPerformanceEntryDate.objects.filter(active=True).first()
    u_sector = UserSector.objects.get(user=request.user)
    ministry_id = u_sector.user_sector.id  # Assuming the ministry ID is linked to the user's sector


    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).count()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).count()
    

    selected_policies = request.GET.getlist('selected_policies[]')

    # Fetch all policies for the dropdown
    policies = get_policy_areas_by_ministry(ministry_id)
    print(policies)
    # Fetch strategic goals with related KeyResultAreas and Indicators
    if selected_policies:
        strategic_goals = get_strategic_goals_with_policies_cache(ministry_id, selected_policies)
    else:
        strategic_goals = get_strategic_goals_with_cache(ministry_id)[0]

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(visible=True)
    quarters = Quarter.objects.all()

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

    # Fetch quarter progress data for the specific years and indicators
    quarter_progress = QuarterProgress.objects.select_related(
        'indicator', 'quarter', 'year'
    ).filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector)

    # Create a nested dictionary for quarter progress data
    quarter_progress_lookup = {}
    for progress in quarter_progress:
        if progress.indicator_id not in quarter_progress_lookup:
            quarter_progress_lookup[progress.indicator_id] = {}
        if progress.year_id not in quarter_progress_lookup[progress.indicator_id]:
            quarter_progress_lookup[progress.indicator_id][progress.year_id] = {}
        quarter_progress_lookup[progress.indicator_id][progress.year_id][progress.quarter_id] = progress

    context = {
        
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        
        'policy_area_count':policy_area_count,
        'strategic_goals': strategic_goals,
        'years': years,
        'quarters':quarters,
        'entry':entry,
        'qentry':qentry,
        'annual_plans_lookup': annual_plans_lookup,
        'quarter_progress_lookup': quarter_progress_lookup,
        'policies': policies,    # Pass the policies to the context for the dropdown
        'selected_policies': selected_policies,  # Pass the selected policies to the context
    }

    return render(request, 'ministry/kpi_ministry_insert_perfromance.html', context)


@login_required
@sector_user_required
def quarter_ministry(request):
    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)
        entry = QuarterPerformanceEntryDate.objects.filter(active=True).first()
        indicators = Indicator.objects.filter(
            responsible_ministries=u_sector.user_sector).prefetch_related('sub_kpi')

        annual_plans = QuarterProgress.objects.filter(
            Q(indicator__responsible_ministries=u_sector.user_sector) |
            Q(sub_indicator__kpi__responsible_ministries=u_sector.user_sector)
        ).select_related('indicator', 'sub_indicator', 'year').all()

        quarters = Quarter.objects.prefetch_related('quarter_entry')
        paginator = Paginator(indicators, 41)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'indicators': page_obj,
            'quarters': quarters,
            'annual_plans': annual_plans,
            'entry': entry
        }

        return render(request, 'quarter_ministry.html', context)


@login_required
@sector_user_required
def batch_insert_ministry(request):
    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)

        indicators = Indicator.objects.filter(
            responsible_ministries=u_sector.user_sector).prefetch_related('sub_kpi')
        entry = AnnualPerformanceEntryDate.objects.filter(active=True).first()
        annual_plans = AnnualPlan.objects.filter(
            Q(indicator__responsible_ministries=u_sector.user_sector) |
            Q(sub_indicator__kpi__responsible_ministries=u_sector.user_sector)
        ).select_related('indicator', 'sub_indicator', 'year').all()

        years = Year.objects.filter(visible = True)
        paginator = Paginator(indicators, 41)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'indicators': page_obj,
            'years': years,
            'annual_plans': annual_plans,
            'entry': entry
        }

        return render(request, 'dashboard_ministry_batch.html', context)


@login_required
@sector_user_required
def quarter_batch_insert_ministry(request):
    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)
        entry = QuarterPerformanceEntryDate.objects.filter(active=True).first()
        indicators = Indicator.objects.filter(
            responsible_ministries=u_sector.user_sector).prefetch_related('sub_kpi')

        annual_plans = QuarterProgress.objects.filter(
            Q(indicator__responsible_ministries=u_sector.user_sector) |
            Q(sub_indicator__kpi__responsible_ministries=u_sector.user_sector)
        ).select_related('indicator', 'sub_indicator', 'quarter').all()

        quarters = Quarter.objects.all()
        paginator = Paginator(indicators, 41)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'indicators': page_obj,
            'quarters': quarters,
            'annual_plans': annual_plans,
            'entry': entry
        }

        return render(request, 'quarter_ministry_batch.html', context)


@csrf_exempt  # Use csrf_exempt for simplicity; implement CSRF protection in production
def quarter_save_batch_performance_data(request):
    if request.method == 'POST':
        try:
            performance_data = request.POST.dict()

            # Create a dictionary to store updated performance values
            updated_performance_data = {}

            # Loop through the data and create/update AnnualPlan objects
            for quarter_plan_id, performance in performance_data.items():
                print(quarter_plan_id)
                try:

                    quarter_plan = QuarterProgress.objects.get(
                        pk=int(quarter_plan_id))
                    quarter_plan.quarter_performance = Decimal(
                        performance)  # Use Decimal for float precision
                    quarter_plan.save()
                except QuarterProgress.DoesNotExist:
                    # Handle the ObjectDoesNotExist exception here
                    print('error')
                else:
                    print('error')

                # Store the updated performance value in the response dictionary
                updated_performance_data[quarter_plan_id] = str(
                    quarter_plan.quarter_performance)

            response_data = {'success': True, 'data': updated_performance_data}
            return JsonResponse(response_data)
        except Exception as e:
            response_data = {'error': str(e)}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=405)


@csrf_exempt  # Use csrf_exempt for simplicity; implement CSRF protection in production
def save_batch_performance_data(request):
    if request.method == 'POST':
        try:
            performance_data = request.POST.dict()

            # Create a dictionary to store updated performance values
            updated_performance_data = {}

            # Loop through the data and create/update AnnualPlan objects
            for annual_plan_id, performance in performance_data.items():
                try:
                    annual_plan = AnnualPlan.objects.get(
                        pk=int(annual_plan_id))
                    annual_plan.annual_performance = Decimal(
                        performance)  # Use Decimal for float precision
                    annual_plan.save()
                except AnnualPlan.DoesNotExist:
                    # Handle the ObjectDoesNotExist exception here
                    pass
                else:
                    pass

                # Store the updated performance value in the response dictionary
                updated_performance_data[annual_plan_id] = str(
                    annual_plan.annual_performance)

            response_data = {'success': True, 'data': updated_performance_data}
            return JsonResponse(response_data)
        except Exception as e:
            response_data = {'error': str(e)}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=405)


# Import your Indicator and AnnualPlan models here
@login_required
@sector_user_required
def update_quarter_plan_performance(request):

    # Retrieve data from the AJAX request
    quarter_plan_id = request.POST.get('quarter_plan_id')
    new_performance = request.POST.get('performance')

    # Check if the annual_plan_id is valid
    try:
        quarter_plan = QuarterProgress.objects.get(id=int(quarter_plan_id))

    except QuarterProgress.DoesNotExist:
        response_data = {'success': False,
                         'error_message': 'Failed to update performance.'}

    # Try to update the annual performance, handle IntegrityError
    try:
        quarter_plan.quarter_performance = Decimal(new_performance)
        quarter_plan.save()
        response_data = {'success': True}
    except IntegrityError:
        response_data = {'success': False,
                         'error_message': 'Failed to update performance.'}

    # Return a JSON response indicating success or failure
    return JsonResponse(response_data)

# This decorator allows for POST requests without CSRF token

from django.views.decorators.http import require_POST

@login_required
@sector_user_required
@require_POST
def update_quarter_plan(request):
    try:
        # Retrieve data from the AJAX request
        quarter_plan_id = request.POST.get('quarter_plan_id')
        target = request.POST.get('target')
        quarter = request.POST.get('quarter')
        year = request.POST.get('year')
        kpi_id = request.POST.get('kpi_id')
        kpi_status = request.POST.get('kpi_status')
        
        # Validate the required fields
        print(quarter_plan_id)
        print('zzzzzzzzzzzzzzzzzzzzzzzzz')
        if not (quarter_plan_id and target and quarter and year and kpi_id and kpi_status):
            
            return JsonResponse({'success': True, 'error_message': 'Missing required parameters.'})

        target = float(target)  # Ensure target is a float
        kpi_id = int(kpi_id)  # Ensure kpi_id is an integer
        quarter_plan_id = int(quarter_plan_id)
        print(target)
  
        
        if kpi_status == 'no':
            
            response_data = create_new_quarter_plan(kpi_id, year, quarter, target)
        else:
            response_data = update_existing_quarter_plan(quarter_plan_id, target)

    except Exception as e:
        
        response_data = {'success': False, 'error_message': f'An unexpected error occurred: {e}'}
    
    return JsonResponse(response_data)

def create_new_quarter_plan(kpi_id, year, quarter, target):
    try:
        kpi = Indicator.objects.get(id=kpi_id)
        year_obj = Year.objects.get(year_amh=int(year))
        quarter_obj = Quarter.objects.get(quarter_eng=str(quarter))
        np = NationalPlan.objects.first()

        # Create a new QuarterProgress instance
        obj1 = QuarterProgress.objects.create(
            indicator=kpi,
            quarter=quarter_obj,
            year=year_obj,
            quarter_target=target,
            national_plan=np
        )
        return {'success': True, 'message': 'New data created successfully.','id':obj1.id}
    except Indicator.DoesNotExist:
        return {'success': False, 'error_message': 'KPI not found.'}
    except Year.DoesNotExist:
        return {'success': False, 'error_message': 'Year not found.'}
    except Quarter.DoesNotExist:
        return {'success': False, 'error_message': 'Quarter not found.'}
    except Exception as e:
        # logger.error(f"Error creating new quarter plan: {e}")
        return {'success': False, 'error_message': f'Failed to create new data: {e}'}

def update_existing_quarter_plan(quarter_plan_id, target):
    try:
        quarter_plan = QuarterProgress.objects.get(id=int(quarter_plan_id))
        quarter_plan.quarter_target = target
        quarter_plan.save()
        return {'success': True, 'message': 'Data updated successfully.'}
    except QuarterProgress.DoesNotExist:
        return {'success': False, 'error_message': 'Quarter plan not found.'}
    except Exception as e:
        # logger.error(f"Error updating quarter plan: {e}")
        return {'success': False, 'error_message': f'Failed to update data: {e}'}
    










@login_required
@sector_user_required
def update_annual_plan_performance(request):
    # Retrieve data from the AJAX request
    annual_plan_id = request.POST.get('annual_plan_id')
    print(annual_plan_id)
    new_performance = request.POST.get('performance')

    # Check if the annual_plan_id is valid
    annual_plan = get_object_or_404(AnnualPlan, id=int(annual_plan_id))

    # Try to update the annual performance, handle IntegrityError
    try:
        annual_plan.annual_performance = Decimal(new_performance)
        annual_plan.save()
        response_data = {'success': True}
    except IntegrityError:
        response_data = {'success': False,
                         'error_message': 'Failed to update performance.'}

    # Return a JSON response indicating success or failure
    return JsonResponse(response_data)


@login_required
@sector_user_required
def ajax_search_indicators(request):
    if request.user.is_sector:
        years = Year.objects.filter(visible = True)
        u_sector = UserSector.objects.get(user=request.user)

        # Get the search query from the AJAX request
        search_query = request.GET.get('q', '')

        # Function to retrieve indicators and matching sub-KPIs
        def get_indicators_with_sub_kpis(query):
            matching_indicators = Indicator.objects.filter(
                Q(kpi_name_eng__icontains=query) |
                Q(kpi_name_amh__icontains=query),
                responsible_ministries=u_sector.user_sector
            ).prefetch_related('sub_kpi')

            matching_sub_kpis = KpiAggregation.objects.filter(
                Q(sub_kpi_name_eng__icontains=query) |
                Q(sub_kpi_name_amh__icontains=query),
                kpi__in=matching_indicators
            )

            return matching_indicators, matching_sub_kpis

        # Retrieve indicators and sub-KPIs with matching sub-KPIs
        matching_indicators, matching_sub_kpis = get_indicators_with_sub_kpis(
            search_query)

        # Serialize Indicator and KpiAggregation objects
        def serialize_indicator(indicator):
            plans = []

            for year in years:
                if isinstance(indicator, Indicator):
                    plan = AnnualPlan.objects.filter(
                        Q(indicator=indicator, year=year)
                    ).select_related('indicator', 'year').first()
                else:
                    plan = None

                plans.append({
                    'annual_target': plan.annual_target if plan else '',
                    'annual_performance': plan.annual_performance if plan else ''
                })

            serialized = {
                'kpi_name_eng': indicator.kpi_name_eng,
                'plans': plans,
                'sub_kpi': []
            }

            if isinstance(indicator, Indicator) and indicator.sub_kpi.all():
                serialized['sub_kpi'] = [serialize_indicator(
                    sub_kpi) for sub_kpi in indicator.sub_kpi.all()]

            return serialized

        # Serialize all matching indicators and sub-KPIs
        serialized_indicators = []

        for indicator in matching_indicators:
            serialized_indicators.append(serialize_indicator(indicator))

        for sub_kpi in matching_sub_kpis:
            serialized_indicators.append(serialize_indicator(sub_kpi))

        return JsonResponse({'indicators': serialized_indicators})


def is_ajax(request):
    """
    Returns True if the request is an AJAX request, False otherwise.
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
@mopd_user_required
def dashboard_mopd(request):

    policy_area = PolicyArea.objects.all()
    policy_area_count = PolicyArea.objects.count()
    goal_count = StrategicGoal.objects.count()
    kra_count = KeyResultArea.objects.count()
    indicator_count = Indicator.objects.count()
    ministry_count = ResponsibleMinistry.objects.count()
    policy_colors = {   
        1: 'bg-info',
        2: 'bg-secondary',
        3: 'bg-success',
        4: 'bg-info',
        5: 'bg-warning',
        6: 'bg-info',
        7: 'bg-dark',
        8: 'bg-warning',
        9: 'bg-info',
        10: 'bg-secondary',
        11: 'bg-info',
        12: 'bg-secondary',
        13: 'bg-success',
        14: 'bg-info',
        15: 'bg-warning',
        16: 'bg-info',
        17: 'bg-warning',
        18: 'bg-dark',
        19: 'bg-info',
        20: 'bg-success',
        21: 'bg-warning',
        22: 'bg-secondary',
        23: 'bg-success',
        24: 'bg-warning',
        # Add more policies and corresponding colors as needed
    }

    context = {
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        'ministry_count': ministry_count,
        'policy_area_count':policy_area_count,
        'policy_area':policy_area,
        'policy_colors':policy_colors
    }

    return render(request, 'dashboard_mopd.html', context)


def detail_dashboard(request):
    context = {
   
    }
    return render(request, 'dashboard_detail.html', context)






def view_kpi_ministry(request):
    if request.method == 'GET' and is_ajax(request):
        indicators = Indicator.objects.all().prefetch_related('sub_kpi')
        annual_plans = AnnualPlan.objects.all().select_related(
            'indicator', 'sub_indicator', 'year')

        # Create a paginator for indicators
        indicator_paginator = Paginator(indicators, 30)

        # Use request.GET to get the page parameter
        page_number = request.GET.get('page')

        try:
            page_obj = indicator_paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = indicator_paginator.page(1)
        except EmptyPage:
            # Return empty response when no more pages
            # Include page_obj in the response
            return JsonResponse({'data': '', 'page_obj': None})

        # Render the HTML for data
        data_html = render_to_string("table.html", {
            'indicators': page_obj,
            'annual_plans': annual_plans,
            'years': Year.objects.filter(visible = True),
        })

        # Return JSON response with page_obj
        return JsonResponse({'data': data_html, 'page_obj': {
            'number': page_obj.number,
            'paginator': {
                'num_pages': indicator_paginator.num_pages
            }
        }})

    # Handle other cases

    ministries = ResponsibleMinistry.objects.values_list(
        'id', 'responsible_ministry_eng')
    return render(request, 'view_kpi_ministry.html', {'ministries': ministries})





def table_ajax(request):

    if request.method == 'GET':
        queryset = Indicator.objects.all().prefetch_related('sub_kpi')
        annual_plans = AnnualPlan.objects.all().select_related(
            'indicator', 'sub_indicator', 'year')

    # Create a paginator for indicators
    paginator = Paginator(queryset, 40)

    # Use request.GET to get the page parameter
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        # Return empty response when no more pages
        return JsonResponse({'data': '', 'page_obj': {}})

    # Render the HTML for data
    data_html = render_to_string("table.html", {
        'indicators': page_obj,
        'annual_plans': annual_plans,
        'years': Year.objects.filter(visible = True),
    })

    # Return JSON response with page_obj (defaultdict)
    return JsonResponse({'data': data_html, 'page_obj': defaultdict(lambda: None, {
        'number': page_obj.number,
        'paginator': {
            'num_pages': paginator.num_pages
        }
    })})


def table_ajax2(request):
    if request.method == 'GET':
        selected_ministries = request.POST.getlist('selectedMinistries[]', [])
        queryset = Indicator.objects.filter(
            responsible_ministries__id__in=selected_ministries
        ).prefetch_related('sub_kpi')

        annual_plans = AnnualPlan.objects.filter(
            Q(indicator__responsible_ministries__id__in=selected_ministries) |
            Q(sub_indicator__kpi__responsible_ministries__id__in=selected_ministries)
        ).select_related('indicator', 'sub_indicator', 'year').all()

        # Create a paginator for indicators
    paginator = Paginator(queryset, 40)
    # Use request.GET to get the page parameter
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        # Return empty response when no more pages
        return JsonResponse({'data': '', 'page_obj': None})
    # Render the HTML for data
    data_html = render_to_string("table.html", {
        'indicators': page_obj,
        'annual_plans': annual_plans,
        'years': Year.objects.filter(visible = True),
    })
    # Return JSON response with page_obj (defaultdict)
    return JsonResponse({'data': data_html, 'page_obj': defaultdict(lambda: None, {
        'number': page_obj.number,
        'paginator': {
            'num_pages': paginator.num_pages
        }
    })})


def filter_kpi_ministry(request):
    if request.method == 'GET':
        # Get the selected ministry values from the AJAX request
        selected_ministries = request.POST.getlist('selectedMinistries[]', [])

        indicators = Indicator.objects.filter(
            responsible_ministries__id__in=selected_ministries
        ).prefetch_related('sub_kpi')

        annual_plans = AnnualPlan.objects.filter(
            Q(indicator__responsible_ministries__id__in=selected_ministries) |
            Q(sub_indicator__kpi__responsible_ministries__id__in=selected_ministries)
        ).select_related('indicator', 'sub_indicator', 'year').all()

        years = Year.objects.filter(visible = True)

        # Use Django's Paginator to paginate your data
        paginator = Paginator(indicators, 10)  # 10 indicators per page
        page_number = request.POST.get('page')
        try:
            indicators = paginator.page(page_number)
        except PageNotAnInteger:
            indicators = paginator.page(1)
        except EmptyPage:
            indicators = paginator.page(paginator.num_pages)

        data = {
            'indicators': indicators,
            'years': years,
            'annual_plans': annual_plans,
        }

    context = {}
    context['data'] = render_to_string("table.html", data)

    return HttpResponse(json.dumps(context), content_type="application/json")


def view_kpi_ministry3(request):
    np = NationalPlan.objects.first()
    if request.user.is_mopd:
        years_to_copy = ['2012', '2013', '2014',
                         '2015', '2016', '2017', '2018']

        for plan in AnnualPlan2.objects.all():
            for year in years_to_copy:
                # Get the corresponding Year object for the current year
                year_obj = Year.objects.get(year_amh=int(year))

                # Try to get an existing AnnualPlan object for the year, indicator, and sub_indicator
                annual_plan, created = AnnualPlan.objects.get_or_create(
                    national_plan=np,
                    indicator=plan.indicator,
                    sub_indicator=plan.sub_indicator,
                    year=year_obj,
                    defaults={
                        'annual_target': getattr(plan, f'plan_year_{year}', None),
                        'annual_performance': getattr(plan, f'performance_year_{year}', None),
                        'target_state': plan.target_state,
                    }
                )

                # If the AnnualPlan object was created or it already exists, save it
                annual_plan.save()

        print(
            f"{AnnualPlan2.objects.count()} records copied from AnnualPlan2 to AnnualPlan")

        return render(request, 'view_kpi_ministry.html')


def mopd_kpi_ministry(request):
    """
    Returns a list of KPIs and annual plans for the selected ministries.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template with the list of KPIs and annual plans.
    """

    # Get the selected ministries.
    selected_ministries = request.GET.getlist('selectedMinistries[]')

    # Get the search query.
    query = request.GET.get('query', '')

    # Get the filtered KPIs and annual plans for selected ministries.
    kpis, annual_plans = search_kpis(
        query, selected_ministries=selected_ministries)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Paginate the KPIs.
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Render the HTML template.
    context = {
        'indicators': page_obj,
        'years': Year.objects.filter(visible = True),
        'annual_plans': annual_plans,
        'ministries': ResponsibleMinistry.objects.values_list('id', 'responsible_ministry_eng'),
        'selected_ministries': selected_ministries,
        'query': query,
        'goals': goals,  # Pass the filtered goals to the template
    }

    return render(request, 'mopd/mopd_kpi_ministry.html', context)







from django.db.models import Q


def mopd_mdip(request):

    policy_area_count = PolicyArea.objects.count()
    goal_count = StrategicGoal.objects.count()
    kra_count = KeyResultArea.objects.count()
    indicator_count = Indicator.objects.count()
    # Get the policy IDs from the request (assuming it's passed as GET parameters)
    selected_policies = request.GET.getlist('selected_policies[]')
    # Fetch all policies for the dropdown
    policies = PolicyArea.objects.all()
    print(selected_policies)
    # Fetch strategic goals with related KeyResultAreas and Indicators
    if selected_policies:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        ).filter(policy_area_id__in=selected_policies)
    else:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        )

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(mdip=True)

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

  
    context = {
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        'policy_area_count':policy_area_count,
        'strategic_goals': strategic_goals,
        'years': years,
        'annual_plans_lookup': annual_plans_lookup,
        
        'policies': policies,    # Pass the policies to the context for the dropdown
        'selected_policies': selected_policies,  # Pass the selected policies to the context
    }

    return render(request, 'mopd/mopd_mdip.html', context)




def mopd_result_matrix(request):

    policy_area_count = PolicyArea.objects.count()
    goal_count = StrategicGoal.objects.count()
    kra_count = KeyResultArea.objects.count()
    indicator_count = Indicator.objects.count()
    # Get the policy IDs from the request (assuming it's passed as GET parameters)
    selected_policies = request.GET.getlist('selected_policies[]')
    # Fetch all policies for the dropdown
    policies = PolicyArea.objects.all()
    print(selected_policies)
    # Fetch strategic goals with related KeyResultAreas and Indicators
    if selected_policies:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        ).filter(policy_area_id__in=selected_policies)
    else:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        )

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(visible=True)

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

    # Fetch quarter progress data for the specific years and indicators
    quarter_progress = QuarterProgress.objects.select_related(
        'indicator', 'quarter', 'year'
    ).filter(Q(year__visible=True))

    # Create a nested dictionary for quarter progress data
    quarter_progress_lookup = {}
    for progress in quarter_progress:
        if progress.indicator_id not in quarter_progress_lookup:
            quarter_progress_lookup[progress.indicator_id] = {}
        if progress.year_id not in quarter_progress_lookup[progress.indicator_id]:
            quarter_progress_lookup[progress.indicator_id][progress.year_id] = {}
        quarter_progress_lookup[progress.indicator_id][progress.year_id][progress.quarter_id] = progress

    context = {
        'goal_count': goal_count,
        'kra_count': kra_count,
        'indicator_count': indicator_count,
        'policy_area_count':policy_area_count,
        'strategic_goals': strategic_goals,
        'years': years,
        'annual_plans_lookup': annual_plans_lookup,
        'quarter_progress_lookup': quarter_progress_lookup,
        'policies': policies,    # Pass the policies to the context for the dropdown
        'selected_policies': selected_policies,  # Pass the selected policies to the context
    }

    return render(request, 'mopd/mopd_kpi_ministry_3year.html', context)




def mopd_quarter_kpi_ministry(request):
    """
    Returns a list of KPIs and annual plans for the selected ministries.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template with the list of KPIs and annual plans.
    """

    # Get the selected ministries.
    selected_ministries = request.GET.getlist('selectedMinistries[]')
    selected_years = request.GET.getlist('selectedYears[]')

    # Get the search query.
    query = request.GET.get('query', '')

    # Get the filtered KPIs and annual plans for selected ministries.
    kpis, annual_plans = search_kpis(
        query, selected_ministries=selected_ministries,type='quarter', year=selected_years)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Paginate the KPIs.
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Render the HTML template.
    context = {
        'indicators': page_obj,
        'years': Quarter.objects.all(),
        'quarters':Year.objects.filter(visible = True),
        'annual_plans': annual_plans,
        'ministries': ResponsibleMinistry.objects.values_list('id', 'responsible_ministry_eng'),
        'selected_ministries': selected_ministries,
        'selected_years':selected_years,
        'query': query,
        'goals': goals,  # Pass the filtered goals to the template
    }

    return render(request, 'mopd/mopd_kpi_ministry_quarter.html', context)




def mopd_kpi_ministry_filter(request):
    if request.method == 'POST':
        selected_ministries = request.POST.getlist('selectedMinistries[]')
    else:
        selected_ministries = []

    ministries = ResponsibleMinistry.objects.values_list(
        'id', 'responsible_ministry_eng')

    # Get the search query from the request
    query = request.GET.get('query')
    years = Year.objects.filter(visible = True)
    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_ministries=selected_ministries)

    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'indicators': page_obj,
        'years': years,
        'annual_plans': annual_plans,
        'ministries': ministries,
        'selected_ministries': selected_ministries,
    }
    return render(request, 'mopd/mopd_kpi_ministry.html', context)


def mopd_kpi_kra(request):
    
    
    # Get the selected goals and KRAs from request parameters
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_ministries = request.GET.getlist('selectedMinistries[]')

    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_goals=selected_goals, selected_kra=selected_kra, selected_ministries=selected_ministries)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Get available areas for each selected goal and ministry.
    goal_areas = {}
    for goal in goals:
        areas = KeyResultArea.objects.filter(
            goal=goal).values('id', 'activity_name_eng')
        goal_areas[goal.id] = list(areas)

    ministries = ResponsibleMinistry.objects.values_list(
        'id', 'responsible_ministry_eng')

    years = Year.objects.filter(visible = True)

    # Convert goal_areas to a JSON string.
    goal_areas_json = json.dumps(goal_areas)

    # Paginate the indicators
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'indicators': page_obj,
        'years': years,
        'annual_plans': annual_plans,
        'selected_goals': selected_goals,
        'selected_kra': selected_kra,  # Capture selected KRAs
        'goals': goals,  # Pass the filtered goals to the template
        'ministries': ministries,
        'selected_ministries': selected_ministries,
        'goal_areas_json': goal_areas_json,
        'query': query,  # Pass the search query to the template
    }

    return render(request, 'mopd/mopd_kpi_kra.html', context)


def view_kpi_table(request):

    u_sector = UserSector.objects.get(user=request.user)           
    # Get the selected goals and KRAs from request parameters
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_ministries = [u_sector.user_sector.id]

    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_goals=selected_goals, selected_kra=selected_kra, selected_ministries=selected_ministries)

 

    years = Year.objects.filter(visible = True)


    context = {
        'indicators': kpis,
        'years': years,
        'annual_plans': annual_plans,
        'query': query,  # Pass the search query to the template
    }



    return render(request, 'ministry/view_kpi_table.html',context )
                  
                  
                  
def view_kpi_kra_ministry(request):
    


    u_sector = UserSector.objects.get(user=request.user)           
    # Get the selected goals and KRAs from request parameters
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_ministries = [u_sector.user_sector.id]

    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_goals=selected_goals, selected_kra=selected_kra, selected_ministries=selected_ministries)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Get available areas for each selected goal and ministry.
    goal_areas = {}
    for goal in goals:
        areas = KeyResultArea.objects.filter(
            goal=goal).values('id', 'activity_name_eng')
        goal_areas[goal.id] = list(areas)


    years = Year.objects.filter(visible = True)

    # Convert goal_areas to a JSON string.
    goal_areas_json = json.dumps(goal_areas)

    # Paginate the indicators
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'indicators': page_obj,
        'years': years,
        'annual_plans': annual_plans,
        'selected_goals': selected_goals,
        'selected_kra': selected_kra,  # Capture selected KRAs
        'goals': goals,  # Pass the filtered goals to the template
        'selected_ministries': selected_ministries,

        'goal_areas_json': goal_areas_json,
        'query': query,  # Pass the search query to the template
    }

    return render(request, 'ministry/ministry_kpi_kra.html', context)




def mopd_kpi_kra_quarter(request):
    
    
    
    # Get the selected goals and KRAs from request parameters
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_ministries = request.GET.getlist('selectedMinistries[]')
    selected_years = request.GET.getlist('selectedYears[]')
    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_goals=selected_goals, selected_kra=selected_kra, selected_ministries=selected_ministries, year=selected_years)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Get available areas for each selected goal and ministry.
    goal_areas = {}
    for goal in goals:
        areas = KeyResultArea.objects.filter(
            goal=goal).values('id', 'activity_name_eng')
        goal_areas[goal.id] = list(areas)

    ministries = ResponsibleMinistry.objects.values_list(
        'id', 'responsible_ministry_eng')

    years = Quarter.objects.all()

    # Convert goal_areas to a JSON string.
    goal_areas_json = json.dumps(goal_areas)

    # Paginate the indicators
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'indicators': page_obj,
        'years': years,
        'annual_plans': annual_plans,
        'selected_goals': selected_goals,
        'selected_kra': selected_kra,  # Capture selected KRAs
        'goals': goals,  # Pass the filtered goals to the template
        'ministries': ministries,
         'quarters':Year.objects.filter(visible = True),
        'selected_ministries': selected_ministries,
          'selected_years':selected_years,
        'goal_areas_json': goal_areas_json,
        'query': query,  # Pass the search query to the template
    }

    return render(request, 'mopd/mopd_kpi_kra_quarter.html', context)






def ministry_kpi_kra_quarter(request):
    

    # Get the selected goals and KRAs from request parameters
    u_sector = UserSector.objects.get(user=request.user)      
    selected_ministries = [u_sector.user_sector.id]
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_years = request.GET.getlist('selectedYears[]')
    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = search_kpis(
        query, selected_goals=selected_goals, selected_kra=selected_kra, selected_ministries=selected_ministries, year=selected_years)

    # Filter the list of goals based on the selected ministries.
    # We traverse the relationships from StrategicGoal to ResponsibleMinistry.
    goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Get available areas for each selected goal and ministry.
    goal_areas = {}
    for goal in goals:
        areas = KeyResultArea.objects.filter(
            goal=goal).values('id', 'activity_name_eng')
        goal_areas[goal.id] = list(areas)



    years = Quarter.objects.all()

    # Convert goal_areas to a JSON string.
    goal_areas_json = json.dumps(goal_areas)

    # Paginate the indicators
    paginator = Paginator(kpis, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'indicators': page_obj,
        'years': years,
        'annual_plans': annual_plans,
        'selected_goals': selected_goals,
        'selected_kra': selected_kra,  # Capture selected KRAs
        'goals': goals,  # Pass the filtered goals to the template
        'quarters':Year.objects.filter(visible = True),
        'selected_ministries': selected_ministries,
        'selected_years':selected_years,
        'goal_areas_json': goal_areas_json,
        'query': query,  # Pass the search query to the template
    }

    return render(request, 'ministry/ministry_kpi_kra_quarter.html', context)

def filter_goals_and_kras(request):

    selected_ministries = request.GET.getlist('selectedMinistries[]')

    # Filter goals based on selected ministries
    filtered_goals = StrategicGoal.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).distinct()

    # Get available areas for each selected goal and ministry
    goal_areas = {}
    for goal in filtered_goals:
        areas = KeyResultArea.objects.filter(
            goal=goal).values('id', 'activity_name_eng')
        goal_areas[goal.id] = list(areas)

    # Return JSON response with filtered goals and areas
    data = {
        'filtered_goals': [{'id': goal.id, 'goal_name_eng': goal.goal_name_eng} for goal in filtered_goals],
        'goal_areas': goal_areas,
    }

    return JsonResponse(data)


def filter_indicators(request):
    selected_ministries = request.GET.getlist('selected_ministries[]')

    page_number = request.GET.get('page', 1)

    # Filter indicators based on the selected ministries
    filtered_indicators = Indicator.objects.filter(
        responsible_ministries__id__in=selected_ministries
    ).prefetch_related('sub_kpi').order_by('kpi_name_eng')

    # Create a Paginator instance
    paginator = Paginator(filtered_indicators, 10)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Generate HTML for the paginated indicators
    indicators_html = render_to_string(
        'mopd/partial_indicators.html', {'indicators': page_obj})

    # Generate HTML for pagination controls
    pagination_html = render_to_string(
        'mopd/partial_pagination.html', {'page_obj': page_obj})

    # Prepare JSON response
    data = {
        'html_data': indicators_html,
        'pagination_html': pagination_html,
    }

    return JsonResponse(data)


def get_chart_data(request, id=0):
    kpi_data = Indicator.objects.filter(id=id).prefetch_related(
        'sub_kpi', 'annual_indicators__year')
    years = Year.objects.filter(visible = True)

    # Extract year_amh values from yearsfrom django.db.models import Q

    chart_categories = [str(year.year_amh) for year in years]
    measurement = kpi_data.first().kpi_measurement_units
    print(measurement)

    # Extract annual_target and annual_performance using a list comprehension
    chart_target_data = [
        annual.annual_target for annual in kpi_data.first().annual_indicators.all()]
    chart_performance_data = [
        annual.annual_performance for annual in kpi_data.first().annual_indicators.all()]

    # Calculate the average, considering None values
    chart_average_data = [(target + performance) / 2 if target is not None and performance is not None else None
                          for target, performance in zip(chart_target_data, chart_performance_data)]

    chart_data = {
        'categories': chart_categories,
        'target_data': chart_target_data,
        'performance_data': chart_performance_data,
        'average_data': chart_average_data,
        'measurement': measurement
    }

    data = {
        'line_chart_data': {
            'categories': chart_categories,
            'series': [{
                'name': kpi_data.first().kpi_name_eng,
                'data': chart_performance_data,
            }]
        },
        'bar_chart_data': {
            'categories': chart_categories,
            'series': [{
                'name': kpi_data.first().kpi_name_eng,
                'data': chart_performance_data,
            }]
        },
        'target_performance_data': chart_data,
    }

    return JsonResponse(data)


def indicator_detail(request, id=0):
 
    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)   
    
    try:
        post = Post.objects.get(indicator__id=id)
    except Post.DoesNotExist:
        post = Post(user=request.user, indicator=Indicator.objects.get(id=id))
        post.save()


    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)  
        kpi_data = Indicator.objects.filter(id=id, responsible_ministries = u_sector.user_sector).prefetch_related(
            'sub_kpi').prefetch_related('annual_indicators')
        if not kpi_data:
            return HttpResponse('You are not authorized to access this content.')
    elif request.user.is_mopd:
        kpi_data = Indicator.objects.filter(id=id).prefetch_related(
            'sub_kpi').prefetch_related('annual_indicators')
    
    years = Year.objects.filter(visible = True)
    # Prepare data for the line chart
    # Get comments related to this blog post
    comments = Comment.objects.filter(object_id=post.id)

    data = {
        'kpi_data': kpi_data,
        'years': years,
        'comments': comments,
        'post': post,

    }
    return render(request, 'mopd/mopd_indicator_detail.html', data)


# def search_kpis(query, selected_ministries=None, selected_goals=None, selected_kra=None):
#     # Create the base query for KPIs
#     kpi_query = Q()  # Initialize an empty query

#     if query and query != '':
#         kpi_query = Q(kpi_name_eng__icontains=query) | Q(
#             kpi_measurement_units__icontains=query)
#     if selected_ministries:
#         kpi_query &= Q(responsible_ministries__id__in=selected_ministries)
#     if selected_goals:
#         kpi_query &= Q(keyResultArea__goal__id__in=selected_goals)
#     if selected_kra:
#         kpi_query &= Q(keyResultArea__id__in=selected_kra)

#     # If no search query and no ministries selected, retrieve random 2 ministries
#     if not query and not selected_ministries:
#         selected_ministries = [1, 13]
#         kpi_query &= Q(responsible_ministries__id__in=selected_ministries)

#     # Execute the query and prefetch related data
#     kpis = Indicator.objects.filter(kpi_query).prefetch_related(
#         'sub_kpi').order_by('kpi_name_eng')

#     # Retrieve annual plans for the filtered KPIs
#     annual_plans = AnnualPlan.objects.filter(
#         Q(indicator__in=kpis) | Q(sub_indicator__kpi__in=kpis)
#     ).select_related('indicator', 'sub_indicator', 'year').all()

#     return kpis, annual_plans





def search_kpis(query, selected_ministries=None, selected_goals=None, selected_kra=None, type:str=None, year = 2013):
    # Create the base query for KPIs
    kpi_query = Q()  # Initialize an empty query

    if query and query != '':
        kpi_query = Q(kpi_name_eng__icontains=query) | Q(
            kpi_measurement_units__icontains=query)
    if selected_ministries:
        kpi_query &= Q(responsible_ministries__id__in=selected_ministries)
    if selected_goals:
        kpi_query &= Q(keyResultArea__goal__id__in=selected_goals)
    if selected_kra:
        kpi_query &= Q(keyResultArea__id__in=selected_kra)

    # If no search query and no ministries selected, retrieve random 2 ministries
    if not query and not selected_ministries:
        selected_ministries = [1, 13]
        kpi_query &= Q(responsible_ministries__id__in=selected_ministries)

    # Execute the query and prefetch related data
    kpis = Indicator.objects.filter(kpi_query).prefetch_related(
        'sub_kpi').order_by('kpi_name_eng')

    # Retrieve annual plans for the filtered KPIs
    if type is not None:
        annual_plans = QuarterProgress.objects.filter(
            Q(indicator__in=kpis) | Q(sub_indicator__kpi__in=kpis)
        ).select_related('indicator', 'sub_indicator', 'year').all()
        
        annual_plans.filter(year__year_amh__in = year).order_by('year')
    else:
        annual_plans = AnnualPlan.objects.filter(
            Q(indicator__in=kpis) | Q(sub_indicator__kpi__in=kpis)
        ).select_related('indicator', 'sub_indicator', 'year').all()

    return kpis, annual_plans

    

def ministry_list(request):

    ministries = ResponsibleMinistry.objects.all()
    years = Year.objects.filter(visible = True)

    ministry_data = []

    for ministry in ministries:
        ministry_count = {
            'ministry_name': ministry.responsible_ministry_eng,
            'indicator_count': Indicator.objects.filter(responsible_ministries=ministry).count(),
        }

        annual_plan_counts = {}
        for year in years:
            annual_plans = AnnualPlan.objects.filter(
                year=year, indicator__responsible_ministries=ministry)

            total_kpis = ministry_count['indicator_count']
            annual_plans_with_no_target = annual_plans.filter(
                annual_target__isnull=False).count()
            # if year.year_amh  in [2016,2017,2018]:
            annual_plans_with_no_performance = annual_plans.filter(
                    annual_performance__isnull=False).count()

            percentage_no_target = (
                annual_plans_with_no_target / total_kpis) * 100 if total_kpis > 0 else 0
            percentage_no_performance = (
                annual_plans_with_no_performance / total_kpis) * 100 if total_kpis > 0 else 0
            score = ScoreCardRange.objects.filter(
                starting__lte=percentage_no_target, ending__gte=percentage_no_target).first()
            score2 = ScoreCardRange.objects.filter(
                starting__lte=percentage_no_performance, ending__gte=percentage_no_performance).first()
            
            
            annual_plan_counts[year.year_amh] = {
                'percentage_no_target': percentage_no_target,
                'percentage_no_performance': percentage_no_performance,
                'color1':score.color,
                'color2':score2.color,
            }

        ministry_count['annual_plan_counts'] = annual_plan_counts

        ministry_data.append(ministry_count)

    context = {'ministry_data': ministry_data, 'years': years}

    return render(request, 'mopd/ministry_list.html', context)



def generate_ministry_kpi(request):
    
    return render(request,  'mopd/generate_ministry_kpi.html')




def export_quarter_plan_temp(request):
    if request.user.is_sector:
        u_sector = UserSector.objects.get(user=request.user)   
    # Get all instances of QuarterPlanTemp
    quarter_plan_temp = Indicator.objects.filter(responsible_ministries =u_sector.user_sector)

    # Create the resource instance
    resource = QuarterPlanTempFormatResource1()
    
    # Export the data
    dataset = resource.export(quarter_plan_temp)
    
    # Create the HTTP response
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="quarterPlanTemp.xlsx"'
    
    return response