# Import your models
import random  # Import the random module
from comment.models import Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .utility import *
from .models import *
from django.http import HttpResponse, JsonResponse
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
from django.db.models import F
from celery import shared_task
from userManagement.admin import ResponsibleMinistryResource
from .forms import ImportFileForm
from userManagement.admin import handle_uploaded_responsible_ministry_file, confirm_file
from rest_framework.decorators import api_view
from .serializers import *
from .resource import *
from .admin import (
    YearResource,
    NationalPlanResource,
    StrategicGoalResource,
    KeyResultAreaResource,
    IndicatorResource,
    KpiAggregationResource,
    AnnualPlanResource,
    handle_uploaded_quarter_plan1
)


from .admin import (
    handle_uploaded_year_file, 
    confirm_file as admin_confirm_file, 
    handle_uploaded_national_plan_file, 
    handle_uploaded_strategical_goal_file, 
    handle_uploaded_key_result_area_file,
    handle_uploaded_indicator_file,
    handle_uploaded_kpiAggregation_file,
    handle_uploaded_annual_plan
    )
from .forms import (
    MinistriesForm,
    YearForm,
    NationalPlanForm,
    StrategicGoalForm,
    KeyResultAreaForm,
    IndicatorForm,
    SubIndicatorForm,
    )
from django.contrib import messages 
from .forms import ImportFileForm
from userManagement.admin import handle_uploaded_responsible_ministry_file, confirm_file
from .admin import (
    handle_uploaded_year_file, 
    confirm_file as admin_confirm_file, 
    handle_uploaded_national_plan_file, 
    handle_uploaded_strategical_goal_file, 
    handle_uploaded_key_result_area_file,
    handle_uploaded_indicator_file,
    handle_uploaded_kpiAggregation_file,
    handle_uploaded_annual_plan
    )
from .forms import (
    MinistriesForm,
    YearForm,
    NationalPlanForm,
    StrategicGoalForm,
    KeyResultAreaForm,
    IndicatorForm,
    SubIndicatorForm,
    ImportFileForm,
    )
from django.contrib import messages 

from django.db.models import Count
import time
from django.db.models import Q

CACHE_TIMEOUT = 2 * 1 # 1 hour








def current_year():


    today = datetime.date.today()

    year = today.year - 1

    return year

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
        ).distinct().order_by('id')  # Order by id in increasing order

        cache.set(cache_key, strategic_goals, CACHE_TIMEOUT)

    return strategic_goals

def get_strategic_goals_with_cache(ministry_id):
    cache_key = f"strategic_goals_with_ministry_{ministry_id}"
    cache_key2 = f"kra_with_ministry_{ministry_id}"
    strategic_goals = cache.get(cache_key)
    kra = cache.get(cache_key2)
    
    if strategic_goals is None or kra is None:
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
        ).prefetch_related(kras_prefetch).distinct().order_by('id')  # Order by id in increasing order

        # Cache the results
        cache.set(cache_key, strategic_goals, CACHE_TIMEOUT)
        cache.set(cache_key2, kra, CACHE_TIMEOUT)

    return [strategic_goals, kra]


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

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id)
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






def policy_area_ministry(request):

    u_sector = UserSector.objects.get(user=request.user)
    policy_area = PolicyArea.objects.all()

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).first()
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
def export_ministry1(request):
    u_sector = UserSector.objects.get(user=request.user)

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).first()
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


    return render(request, 'ministry/export_ministry.html', context)





@login_required
@sector_user_required
def mdip_ministry(request):
    u_sector = UserSector.objects.get(user=request.user)

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).first()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id).count()
    
    # Fetch all policies for the dropdown
    policies = get_policy_areas_by_ministry(u_sector.user_sector.id)

    # Fetch strategic goals with related KeyResultAreas and Indicators, ordered by 'id'
    strategic_goals = get_strategic_goals_with_cache(u_sector.user_sector.id)[0]
    

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(mdip=True)

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True, indicator__responsible_ministries__id = u_sector.user_sector.id)

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
        'policy_area_count': policy_area_count,
    }

    return render(request, 'ministry/mdip_ministry.html', context)


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



@login_required
@sector_user_required
def kpi_ministry_new(request):

    entry = AnnualPerformanceEntryDate.objects.filter(active=True).first()
    qentry = QuarterPerformanceEntryDate.objects.filter(active=True).first()
    u_sector = UserSector.objects.get(user=request.user)
    ministry_id = u_sector.user_sector.id  # Assuming the ministry ID is linked to the user's sector

    policy_area_count = get_policy_areas_by_ministry(u_sector.user_sector.id).first()
    goal_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[0].count()
    kra_count = get_strategic_goals_with_cache(u_sector.user_sector.id)[1].count()
    indicator_count = Indicator.objects.filter(
        responsible_ministries_id=u_sector.user_sector.id
    ).count()

    selected_policies = request.GET.getlist('selected_policies[]')

    # Fetch all policies for the dropdown, ordered by 'id'
    policies = get_policy_areas_by_ministry(ministry_id).order_by('id')
    
    # Fetch strategic goals with related KeyResultAreas and Indicators, ordered by 'id'
    if selected_policies:
        strategic_goals = get_strategic_goals_with_policies_cache(ministry_id, selected_policies).order_by('id')
    else:
        strategic_goals = get_strategic_goals_with_cache(ministry_id)[0].order_by('id')

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(quarter_view=True).order_by('id')
    
    # Fetch all quarters, ordered by 'id'
    quarters = Quarter.objects.all().order_by('id')

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector).order_by('id')

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

    # Fetch quarter progress data for the specific years and indicators
    quarter_progress = QuarterProgress.objects.select_related(
        'indicator', 'quarter', 'year'
    ).filter(year__visible=True, indicator__responsible_ministries=u_sector.user_sector).order_by('id')

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
        'policy_area_count': policy_area_count,
        'strategic_goals': strategic_goals,
        'years': years,
        'quarters': quarters,
        'entry': entry,
        'qentry': qentry,
        'annual_plans_lookup': annual_plans_lookup,
        'quarter_progress_lookup': quarter_progress_lookup,
        'policies': policies,  # Pass the policies to the context for the dropdown
        'selected_policies': selected_policies,  # Pass the selected policies to the context
    }

    return render(request, 'ministry/kpi_ministry_insert_perfromance.html', context)




from django.http import JsonResponse
from django.contrib import messages
import json
# Global variables should be defined outside of the function
from tablib import Dataset


@login_required
@sector_user_required
def kpi_ministry_plan(request):
    form_file = ImportFileForm()
    u_sector = UserSector.objects.get(user=request.user)
    ministry_id = u_sector.user_sector.id

    policy_area_count = get_policy_areas_by_ministry(ministry_id).first()
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

    years = Year.objects.filter(quarter_view=True)
    quarters = Quarter.objects.all().order_by('id')  # Corrected order_by usage

    annual_plans = AnnualPlan.objects.select_related('indicator', 'sub_indicator', 'year').filter(year__quarter_view=True, indicator__responsible_ministries=u_sector.user_sector)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

    quarter_progress = QuarterProgress.objects.select_related('indicator', 'quarter', 'year').filter(year__quarter_view=True, indicator__responsible_ministries=u_sector.user_sector)

    quarter_progress_lookup = {}
    for progress in quarter_progress:
        if progress.indicator_id not in quarter_progress_lookup:
            quarter_progress_lookup[progress.indicator_id] = {}
        if progress.year_id not in quarter_progress_lookup[progress.indicator_id]:
            quarter_progress_lookup[progress.indicator_id][progress.year_id] = {}
        quarter_progress_lookup[progress.indicator_id][progress.year_id][progress.quarter_id] = progress

    result = None  # Initialize result to a default value
    if request.method == "POST":
        if 'fileAnnualValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_quarter_plan1(file)

                # Convert Dataset to a list of dictionaries
                imported_data_serializable = [dict(row) for row in imported_data.dict]

                request.session['imported_data'] = json.dumps(imported_data_serializable)  # Store data in session
                context = {'result': result}
                return render(request, 'ministry/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

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
        'result': result,  # Add result to the context to avoid referencing it before assignment
    }

    return render(request, 'ministry/kpi_ministry_insert_plan.html', context)


@login_required
@sector_user_required
def confirm_kpi_ministry_plan(request):
    if request.method == "POST" and 'confirm_data_form' in request.POST:
        imported_data_json = request.session.get('imported_data')
        if imported_data_json:
            imported_data_list = json.loads(imported_data_json)  # Convert JSON back to list of dictionaries

            # Reconstruct Dataset from list of dictionaries
            imported_data = Dataset()
            headers = imported_data_list[0].keys()
            imported_data.headers = headers
            for row_dict in imported_data_list:
                row = [row_dict[header] for header in headers]
                imported_data.append(row)

            success, message = admin_confirm_file(imported_data, 'quarterPlan')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
        else:
            messages.error(request, 'No data to confirm')
        return redirect('kpi_ministry_plan')

    return redirect('kpi_ministry_plan')
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
        # Fetch related objects
        kpi = Indicator.objects.get(id=kpi_id)
        year_obj = Year.objects.get(year_amh=int(year))
        quarter_obj = Quarter.objects.get(quarter_eng=str(quarter))

        # Create or get QuarterProgress instance
        obj1, created = QuarterProgress.objects.get_or_create(
            indicator=kpi,
            quarter=quarter_obj,
            year=year_obj,
            defaults={'quarter_target': target}
        )

        if not created:
            obj1.quarter_target = target
            obj1.save()

        # Map quarter to target field
        quarter_name_to_field = {
            "3month": "quarter1_target",
            "6month": "quarter2_target",
            "9month": "quarter3_target",
            "12month": "quarter4_target",
        }
        quarter_field = quarter_name_to_field.get(quarter)

        if not quarter_field:
            return {'success': False, 'error_message': f'Invalid quarter name: {quarter}'}

        # Create or get QuarterPlanTemp instance and set target field
        quarter_plan_temp, _ = QuarterPlanTemp.objects.get_or_create(
            indicator=obj1.indicator,
            year=year_obj,
        )
        setattr(quarter_plan_temp, quarter_field, target)
        quarter_plan_temp.save()

        return {'success': True, 'message': 'New data created successfully.', 'id': obj1.id}
    except Indicator.DoesNotExist:
        return {'success': False, 'error_message': 'KPI not found.'}
    except Year.DoesNotExist:
        return {'success': False, 'error_message': 'Year not found.'}
    except Quarter.DoesNotExist:
        return {'success': False, 'error_message': 'Quarter not found.'}
    except Exception as e:
        return {'success': False, 'error_message': f'Failed to create new data: {e}'}




def update_existing_quarter_plan(quarter_plan_id, target):
    try:
        quarter_plan = QuarterProgress.objects.get(id=int(quarter_plan_id))
        quarter_plan.quarter_target = target
        quarter_plan.save()

        quarter_name_to_field = {
            "3month": "quarter1_target",
            "6month": "quarter2_target",
            "9month": "quarter3_target",
            "12month": "quarter4_target",
        }
        quarter_field = quarter_name_to_field.get(quarter_plan.quarter.quarter_eng)

        if not quarter_field:
            print(f"Invalid quarter name: {quarter_plan.quarter.quarter_eng}")
            return
        
        
        quarter_plan_temp, _ = QuarterPlanTemp.objects.get_or_create(
        indicator=quarter_plan.indicator,
        year=quarter_plan.year,

        )

        setattr(quarter_plan_temp, quarter_field, target)
        quarter_plan_temp.save()
        return {'success': True, 'message': 'Data updated successfully.', 'data':quarter_plan.quarter.quarter_eng}
    except QuarterProgress.DoesNotExist:
        return {'success': False, 'error_message': 'Quarter plan not found.'}
    except Exception as e:
        # logger.error(f"Error updating quarter plan: {e}")
        return {'success': False, 'error_message': f'Failed to update data: {e}'}
    



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

        quarters = Quarter.objects.all().order_by('id')
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





from django.db.models import Q


def mopd_mdip(request):

    policy_area_count = PolicyArea.objects.count()
    goal_count = StrategicGoal.objects.count()
    kra_count = KeyResultArea.objects.count()
    indicator_count = Indicator.objects.count()
    # Get the policy IDs from the request (assuming it's passed as GET parameters)
    selected_policies = request.GET.getlist('selected_policies[]')
    # Fetch all policies for the dropdown
    policies = PolicyArea.objects.all().order_by('id')
    # Fetch strategic goals with related KeyResultAreas and Indicators
    if selected_policies:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        ).filter(policy_area_id__in=selected_policies).order_by('id')
    else:
        strategic_goals = StrategicGoal.objects.prefetch_related(
            'kra_goal__indicators'
        ).order_by('id')

    # Fetch all visible years for the annual plans
    years = Year.objects.filter(mdip=True).order_by('id')

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__visible=True).order_by('id')

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
    years = Year.objects.filter(quarter_view=True)

    # Fetch all annual plans with related indicators and sub-indicators
    annual_plans = AnnualPlan.objects.select_related(
        'indicator', 'sub_indicator', 'year'
    ).filter(year__quarter_view=True)

    # Create a lookup dictionary for annual plans
    annual_plans_lookup = {}
    for plan in annual_plans:
        if plan.indicator_id not in annual_plans_lookup:
            annual_plans_lookup[plan.indicator_id] = {}
        annual_plans_lookup[plan.indicator_id][plan.year_id] = plan

    # Fetch quarter progress data for the specific years and indicators
    quarter_progress = QuarterProgress.objects.select_related(
        'indicator', 'quarter', 'year'
    ).filter(Q(year__quarter_view=True))

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



from django.core.exceptions import ObjectDoesNotExist  # For handling potential missing objects

@shared_task
def filter_kpis(query, selected_ministries=None, selected_goals=None, selected_kra=None, type=None, year=2013):
    try:
        # Create the base query for KPIs
        kpi_query = Q()

        # Filter KPIs based on search query (if provided)
        if query and query != '':
            kpi_query = Q(kpi_name_eng__icontains=query) | Q(
                kpi_measurement_units__icontains=query
            )

        # Filter KPIs based on selected ministries (if provided)
        if selected_ministries:
            kpi_query &= Q(responsible_ministries__id__in=selected_ministries)

        # Filter KPIs based on selected goals (if provided)
        if selected_goals:
            kpi_query &= Q(keyResultArea__goal__id__in=selected_goals)

        # Filter KPIs based on selected KRAs (if provided)
        if selected_kra:
            kpi_query &= Q(keyResultArea__id__in=selected_kra)

        # Handle the case where no search query or ministries are selected
        if not query and not selected_ministries:
            # Consider using pre-defined default ministries or a mechanism to choose them
            # For simplicity, we'll just skip filtering by ministries in this case
            kpi_query &= Q(responsible_ministries__id__in=[1, 13])  # Example of default ministries

        # Execute the query and prefetch related data
        kpis = Indicator.objects.filter(kpi_query).prefetch_related(
            'sub_kpi'
        ).order_by('kpi_name_eng')  # Order by KPI name

        # Retrieve annual plans for the filtered KPIs
        if type is not None:  # Filter for QuarterProgress data
            annual_plans = QuarterProgress.objects.filter(
                Q(indicator__in=kpis) | Q(sub_indicator__kpi__in=kpis)
            ).select_related('indicator', 'sub_indicator', 'year').all()
            annual_plans = annual_plans.filter(year__year_amh__in=year).order_by('year')
        else:  # Filter for AnnualPlan data
            annual_plans = AnnualPlan.objects.filter(
                Q(indicator__in=kpis) | Q(sub_indicator__kpi__in=kpis)
            ).select_related('indicator', 'sub_indicator', 'year').all()

        # Return the filtered KPIs and annual plans
        return kpis, annual_plans

    except (ObjectDoesNotExist, Exception) as e:
        # Handle potential object not found errors or other exceptions
        print(f"Error filtering KPIs: {e}")
        return None, e  # Return None for KPIs, and the exception for error handling



def view_kpi_table(request):

    u_sector = UserSector.objects.get(user=request.user)           
    # Get the selected goals and KRAs from request parameters
    selected_goals = request.GET.getlist('selectedGoals[]')
    selected_kra = request.GET.getlist('selectedAreas[]')
    selected_ministries = [u_sector.user_sector.id]

    # Get the search query from the request
    query = request.GET.get('query', '')

    # Use the search_kpis function to get filtered KPIs and annual plans
    kpis, annual_plans = filter_kpis(
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
    selected_goals = []
    selected_kra =[]
    selected_ministries = []
    selected_years = ['2016']
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



    years = Quarter.objects.all().order_by('id')

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
    years = Year.objects.all()

    # Extract year_amh values from yearsfrom django.db.models import Q

    chart_categories = [2015, 2016, 2017, 2018]
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



def search_kpis(query, selected_ministries=None, selected_goals=None, selected_kra=None, type:str=None, year = 2015):
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


def ministry_list_quarter(request):
    ministries = ResponsibleMinistry.objects.filter(ministry_is_visable=True)
    year_2017 = Year.objects.filter(year_amh=2017, visible=True).first()  # Only for 2017

    ministry_data = []
    quarters = ["3month", "6month", "9month", "12month"]  # Updated quarter labels

    if year_2017:
        for ministry in ministries:
            # Get the total number of indicators per ministry
            indicators = Indicator.objects.filter(responsible_ministries=ministry)
            total_kpis = indicators.count()

            # Initialize data structure for ministry
            ministry_count = {
                'ministry_name': ministry.responsible_ministry_eng,
                'indicator_count': total_kpis,
                'quarter_data': []  # List to store quarter info
            }

            # Iterate through each indicator and quarter
            for quarter in quarters:
                no_target = 0
                no_performance = 0

                for indicator in indicators:
                    # Fetch the QuarterProgress data for the indicator and quarter
                    quarter_data = QuarterProgress.objects.filter(
                        year=year_2017, 
                        quarter__quarter_eng=quarter, 
                        indicator=indicator
                    ).first()

                    if quarter_data:
                        # Increment no target or no performance based on quarter data
                        if quarter_data.quarter_target is not None:
                            no_target += 1
                        if quarter_data.quarter_performance is not None:
                            no_performance += 1

                # Calculate the percentages for this quarter
                percentage_no_target = (no_target / total_kpis * 100) if total_kpis > 0 else 0
                percentage_no_performance = (no_performance / total_kpis * 100) if total_kpis > 0 else 0

                # Get scorecard color based on percentage
                score = ScoreCardRange.objects.filter(
                    starting__lte=percentage_no_target, ending__gte=percentage_no_target
                ).first()
                score2 = ScoreCardRange.objects.filter(
                    starting__lte=percentage_no_performance, ending__gte=percentage_no_performance
                ).first()

                color1 = score.color if score else '#FFFFFF'  # Default to white if no score range found
                color2 = score2.color if score2 else '#FFFFFF'

                # Add the quarter data to the list
                ministry_count['quarter_data'].append({
                    'quarter': quarter,
                    'percentage_no_target': percentage_no_target,
                    'percentage_no_performance': percentage_no_performance,
                    'color1': color1,
                    'color2': color2
                })

            ministry_data.append(ministry_count)

    context = {
        'ministry_data': ministry_data,
        'year_2017': year_2017,
        'quarters': quarters  # Pass quarters to the template
    }
    return render(request, 'mopd/ministry_list_quarter.html', context)


def ministry_list(request):

    ministries = ResponsibleMinistry.objects.filter(ministry_is_visable = True)
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
            percentage_no_target = min(percentage_no_target, 100)
            percentage_no_performance = (
                annual_plans_with_no_performance / total_kpis) * 100 if total_kpis > 0 else 0
            percentage_no_performance = min(percentage_no_performance, 100)
            score = ScoreCardRange.objects.filter(
                starting__lte=percentage_no_target, ending__gte=percentage_no_target).first()
            score2 = ScoreCardRange.objects.filter(
                starting__lte=percentage_no_performance, ending__gte=percentage_no_performance).first()

            color1 = score.color if score else '#ffffff'  # Replace 'default_color1' with a suitable default value
            color2 = score2.color if score2 else '#ffffff'  # Replace 'default_color2' with a suitable default value
            annual_plan_counts[year.year_amh] = {
                'percentage_no_target': percentage_no_target,
                'percentage_no_performance': percentage_no_performance,
                'color1':color1,
                'color2':color2,
            }

        ministry_count['annual_plan_counts'] = annual_plan_counts
        ministry_data.append(ministry_count)
    context = {'ministry_data': ministry_data, 'years': years}

    return render(request, 'mopd/ministry_list.html', context)



def generate_ministry_kpi(request):
    
    return render(request,  'mopd/generate_ministry_kpi.html')







def sample_data(request):
    form_file = ImportFileForm()# to accept file for import export
    indicators = Indicator.objects.filter().prefetch_related("responsible_ministries", "sub_kpi" )[0:100]
    annual_plan= AnnualPlan.objects.filter().select_related("national_plan", "indicator", "sub_indicator", "year")[0:100]
    year = Year.objects.filter(visible = True).order_by('year_amh')
    count = 30
    paginator = Paginator(indicators, 30) 
    page_number = request.GET.get('page')

    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30
    if request.method == "POST":
        if 'fileAnnualValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_annual_plan(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')
        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'annualPlan')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    context = {
        'indicators': page,
        'annual_plans' : annual_plan,
        'years' : year,
        'count' : count,
        'formFile' : form_file,        
    }

    
    return render(request, 'data/sampleData.html', context=context)




def responsible_ministries(request):
    form = MinistriesForm()

    ministries  = ResponsibleMinistry.objects.all()
    paginator = Paginator(ministries, 30)
    page_number = request.GET.get('page')
    count = 30


    form_file = ImportFileForm()# to accept file for import export
    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addMinistryForm' in request.POST:
            form = MinistriesForm(request.POST)
            if form.is_valid():
                form.save()
                form = MinistriesForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileResponsibleMinistriesValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_responsible_ministry_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = confirm_file(imported_data_global, 'responsible_ministries')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

            return redirect('responsible-ministries')


    context = {
        'ministries' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form,
    }
    return render(request, 'data/responsible_ministries.html', context=context)



def year(request):
    form = YearForm()
    years  = Year.objects.all()
    paginator = Paginator(years, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export
    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addYearForm' in request.POST:
            form = YearForm(request.POST)
            if form.is_valid():
                form.save()
                form = YearForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileYearsValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_year_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'year')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('year')


    context = {
        'years' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form, 
    }
    return render(request, 'data/year.html', context=context)

def national_plan(request):
    form = NationalPlanForm()
    national_plan  = NationalPlan.objects.all()
    paginator = Paginator(national_plan, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export
    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addPlanForm' in request.POST:
            form = NationalPlanForm(request.POST)
            if form.is_valid():
                form.save()
                form = NationalPlanForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileNationalPlanValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_national_plan_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'national_plan')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('national_plan')

    context = {
        'nationalPlan' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form
    }
    return render(request, 'data/national_plan.html', context=context)

def strategic_goal(request):
    form = StrategicGoalForm()
    strategic_goals  = StrategicGoal.objects.filter()
    paginator = Paginator(strategic_goals, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export

    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addStrategicGoalForm' in request.POST:
            form = StrategicGoalForm(request.POST)
            if form.is_valid():
                form.save()
                form = StrategicGoalForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileNationalPlanValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_strategical_goal_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'strategical_goal')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('strategic_goal')

    context = {
        'strategicGoals' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form
    }
    return render(request, 'data/strategic_goal.html', context=context)

def key_result_area(request):
    form = KeyResultAreaForm()
    key_result_areas  = KeyResultArea.objects.filter().select_related()
    paginator = Paginator(key_result_areas, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export

    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addkeyResultAreaForm' in request.POST:
            form = KeyResultAreaForm(request.POST)
            if form.is_valid():
                form.save()
                form = KeyResultAreaForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileKeyResultAreasValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_key_result_area_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'key_result_area')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

            return redirect('key_result_area')

    context = {
        'keyResultAreas' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form
    }
    return render(request, 'data/key_result-area.html', context=context)

def indicator(request):
    form  = IndicatorForm()
    indicators  = Indicator.objects.filter().select_related()
    paginator = Paginator(indicators, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export

    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30


    if request.method == 'POST':
        if 'addIndicatorForm' in request.POST:
            form = IndicatorForm(request.POST)
            if form.is_valid():
                form.save()
                form = IndicatorForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileIndicatorsValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_indicator_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'indicator')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('indicator')

    context = {
        'indicators' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form
    }
    return render(request, 'data/indicator.html', context=context)

def kpiAggrigation(request):
    form  = IndicatorForm()
    form_sub = SubIndicatorForm()
    form_sub_sub = SubIndicatorForm()
    indicators = Indicator.objects.filter()
    paginator = Paginator(indicators, 30)
    page_number = request.GET.get('page')
    count = 30
    form_file = ImportFileForm()# to accept file for import export

    global imported_data_global
    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30
    

    if request.method == 'POST':
        if 'addIndicatorForm' in request.POST:
            form = IndicatorForm(request.POST)
            if form.is_valid():
                form.save()
                form = IndicatorForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'addSubIndicatorForm' in request.POST:
            form_sub = SubIndicatorForm(request.POST)
            if form_sub.is_valid():
                kpi_id = request.POST['indicatorSubIndicatorName']
                sub_kpi_id = request.POST['indicatorSubOfSubIndicatorName']

                try: last_id = KpiAggregation.objects.latest('id').id
                except: last_id = 0
                
                kpi = Indicator.objects.get(pk = kpi_id)
                sub_kpi = KpiAggregation.objects.get(pk = sub_kpi_id) if sub_kpi_id else None


                sub_indicator = form_sub.save(commit=False)
                sub_indicator.kpi = kpi
                sub_indicator.id = last_id + 1
                sub_indicator.parent = sub_kpi
                sub_indicator.save()

                form_sub = SubIndicatorForm()
                messages.success(request, 'Successfully added')
                return redirect(request.META['HTTP_REFERER'])
        if 'fileSubIndicatorsValue' in request.POST:
            form_file = ImportFileForm(request.POST, request.FILES)
            if form_file.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_kpiAggregation_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'data/import_preview.html', context=context)
            else:
                messages.error(request, 'File not recognized')

        elif 'confirm_data_form' in request.POST:
            success, message = admin_confirm_file(imported_data_global, 'subIndicator')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('kpi-aggregation')
    context = {
        'indicators' : page,
        'count' : count,  
        'formFile' : form_file,
        'form' : form,
        'form_sub': form_sub,
        'form_sub_sub' : form_sub_sub,
    }
    return render(request, 'data/kpi_aggregation.html', context=context)

def category(request):

    return render(request, 'data/category.html')

def annual_plan(request):
    return render(request, 'annual_plan')




########### Save Data
def update_performance(request):
    performance = request.POST['performance']
    kpi_name = request.POST['kpi_name']
    annual_plan_id = request.POST['annual_plan_id']

    try:
        annual_plan = AnnualPlan.objects.get(pk= annual_plan_id)
        annual_plan.annual_performance = performance
        annual_plan.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)


def update_ministry(request):
    ministry_name_eng = request.POST['ministry_name_eng']
    ministry_name_amh = request.POST['ministry_name_amh']
    ministry_code = request.POST['ministry_code']
    ministry_id = request.POST['ministry_id']

    try:
        ministry = ResponsibleMinistry.objects.get(pk = ministry_id)
        ministry.responsible_ministry_eng = ministry_name_eng
        ministry.responsible_ministry_amh = ministry_name_amh
        ministry.code = ministry_code
        ministry.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)


def delete_ministry(request, pk):
    try:
        ResponsibleMinistry.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting responsible ministry')
    
    return redirect(request.META['HTTP_REFERER'])

def update_year(request):
    year_eng = request.POST['yearEng']
    year_amh = request.POST['yearAmh']
    year_visible = request.POST['yearVisible']
    year_id = request.POST['yearId']

    try:
        year = Year.objects.get(pk = year_id)
        year.year_eng = year_eng
        year.year_amh = year_amh
        year.visible = True if year_visible == 'true' else False
        year.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)


def delete_year(request, pk):
    try:
        Year.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting Year')
    
    return redirect(request.META['HTTP_REFERER'])


def update_national_plan(request):
    nameEng = request.POST['nameEng']
    nameAmh = request.POST['nameAmh']
    decsEng = request.POST['decsEng']
    decsAmh = request.POST['decsAmh']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    plan_id = request.POST['id']

    try:
        plan = NationalPlan.objects.get(pk = plan_id)
        plan.np_name_eng = nameEng
        plan.np_name_amh = nameAmh
        plan.description_eng = decsEng
        plan.description_amh = decsAmh
        plan.starting_date = str(startDate)+":00+00:00"
        plan.ending_date = endDate
        plan.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)

def delete_national_plan(request, pk):
    try:
        NationalPlan.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting Year')
    
    return redirect(request.META['HTTP_REFERER'])

def update_strategic_goal(request):
    goal_name_eng = request.POST['goal_name_eng']
    goal_name_amh = request.POST['goal_name_amh']
    goal_weight = request.POST['goal_weight']
    goal_is_shared = request.POST['goal_is_shared']
    national_plan = request.POST['national_plan']
    responsible_ministries = request.POST['responsible_ministries']
    id = request.POST['id']

    try:
        goal = StrategicGoal.objects.get(pk = id)
        plan = NationalPlan.objects.get(pk = national_plan )
        ministry = ResponsibleMinistry.objects.get(pk = responsible_ministries)
    
    
        goal.goal_name_eng = goal_name_eng
        goal.goal_name_amh = goal_name_amh
        goal.goal_weight = goal_weight
        goal.goal_is_shared = True if goal_is_shared == "true" else  False
        goal.national_plan = plan
        goal.responsible_ministries = ministry
        goal.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    
    return JsonResponse(response)
 

def delete_strategic_goal(request, pk):
    try:
        StrategicGoal.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting Year')
    
    return redirect(request.META['HTTP_REFERER'])


def update_key_result_area(request):
    activity_name_eng = request.POST['activity_name_eng']
    activity_name_amh = request.POST['activity_name_amh']
    activity_weight = request.POST['activity_weight']
    activity_is_shared = request.POST['activity_is_shared']
    goal_id = request.POST['goal']
    id = request.POST['id']

    try:
        activity = KeyResultArea.objects.get(pk = id)
        goal = StrategicGoal.objects.get(pk = goal_id)
        activity.activity_name_eng = activity_name_eng
        activity.activity_name_amh = activity_name_amh
        activity.activity_weight = activity_weight
        activity.activity_is_shared = True if activity_is_shared == "true" else  False
        activity.goal = goal
        activity.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)

def delete_key_result_area(request, pk):
    try:
        KeyResultArea.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting Year')
    
    return redirect(request.META['HTTP_REFERER'])

def update_indicator(request):
    kpi_name_eng = request.POST['kpi_name_eng']
    kpi_name_amh = request.POST['kpi_name_amh']
    kpi_weight = request.POST['kpi_weight']
    kpi_measurement_units = request.POST['kpi_measurement_units']
    kpi_characteristics = request.POST['kpi_characteristics']
    ministries_id = request.POST['responsible_ministries']
    area_id = request.POST['keyResultArea']
    indicator_id = request.POST['indicator_id']


    try:
        responsible_ministries = ResponsibleMinistry.objects.get(pk = ministries_id)
        area = KeyResultArea.objects.get(pk = area_id)
        kpi = Indicator.objects.get(pk = indicator_id)

        kpi.kpi_name_eng = kpi_name_eng
        kpi.kpi_name_amh = kpi_name_amh
        kpi.kpi_weight = kpi_weight if kpi_weight else None
        kpi.kpi_measurement_units = kpi_measurement_units
        kpi.kpi_characteristics = kpi_characteristics
        kpi.responsible_ministries = responsible_ministries
        kpi.keyResultArea = area
        kpi.save()

        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)

def delete_indicator(request, pk):
    try:
        Indicator.objects.get(pk=pk).delete()
        messages.success(request, 'Successfully Deleted!')
    except:
        messages.error(request, 'An error occurred while deleting Year')
    
    return redirect(request.META['HTTP_REFERER'])

def update_kpi_aggregation(request):
    kpi_name_eng = request.POST['kpi_name_eng']
    kpi_name_amh = request.POST['kpi_name_amh']
    kpi_category = request.POST['kpi_category']
    id = request.POST['indicator_id']

    try:
        kpi = KpiAggregation.objects.get(pk = id)
        category = Category.objects.get(pk = kpi_category)
        kpi.sub_kpi_name_eng = kpi_name_eng
        kpi.sub_kpi_name_amh = kpi_name_amh
        kpi.category = category
        kpi.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)




@login_required
def index(request):
    return render(request, 'dashboard-app/dashboard-index.html')



@login_required(login_url='dashboard-login')
@api_view(['GET'])
def ministries_lists(request):
    if request.method == 'GET':
        ministries = ResponsibleMinistry.objects.filter(ministry_is_visable = True).annotate(goal_count=Count('ministry_goal')).select_related()
   
        serializer = MinistrySerializers(ministries, many=True,context={'year': 2016, 'quarter':'9 month'})
        return JsonResponse({'ministries':serializer.data})



def policy_area_lists(request):
    if request.method == 'GET':
        policyArea = PolicyArea.objects.annotate(goal_count=Count('policy_area_goal')).select_related().order_by('id')

        serializer = PolicyAreaSerializers(policyArea,many=True,context={'year': 2016, 'quarter':'9 month'})

        return JsonResponse({'policy':serializer.data})




@login_required(login_url='dashboard-login')
@api_view(['GET'])
def ministries_lists(request):
    if request.method == 'GET':
        ministries = ResponsibleMinistry.objects.filter(ministry_is_visable = True).annotate(goal_count=Count('ministry_goal')).select_related()
        # ministries = ministries.filter(~Q(category_count = 0)) #Only Display with category > 0
        serializer = MinistrySerializers(ministries, many=True,context={'year': 2016, 'quarter':'9 month'})
        return JsonResponse({'ministries':serializer.data})

        


@login_required(login_url='dashboard-login')
@api_view(['GET'])
def ministry_goal(request, id):
    if request.method == 'GET':
        ministry_goal = list(StrategicGoal.objects.filter(policy_area__id = id).values(
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
     
        krax = KeyResultAreaSerializer1(kra, many=True, context={'year': 2016, 'quarter':'9 month'})
  
        print(krax.data)
        ministries = ResponsibleMinistry.objects.filter(ministry_is_visable = True).annotate(goal_count=Count('ministry_goal')).select_related()
   
        serializer = MinistrySerializers(ministries, many=True,context={'year': 2016, 'quarter':'9 month'})

        if 'q' in request.GET:
            q = request.GET['q']
            indicators = Indicator.objects.filter(Q(kpi_name_eng__contains=q)  )
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
             'ministries':serializer.data,
             'kraz':krax.data
        }
        #time.sleep(1)
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



@login_required(login_url='/login/')
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

    time.sleep(3)
    return JsonResponse(data)



@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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









def export_ministry(request):
    ministries = ResponsibleMinistryResource()
    dataset = ministries.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ministries.xlsx"'
    return response


def export_year(request):
    year = YearResource()
    dataset = year.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="year.xlsx"'
    return response

def export_national_plan(request):
    national = NationalPlanResource()
    dataset = national.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="national_plan.xlsx"'
    return response

def export_strategic_goal(request):
    goal = StrategicGoalResource()
    dataset = goal.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="strategic_goal.xlsx"'
    return response


def export_key_result_area(request):
    key = KeyResultAreaResource()
    dataset = key.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="key_result_area.xlsx"'
    return response


def export_indicator(request):
    indicator = IndicatorResource()
    dataset = indicator.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="indicators.xlsx"'
    return response

def export_kpi_sub_indicator(request):
    kpi = KpiAggregationResource()
    dataset = kpi.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="kpi_Aggregate.xlsx"'
    return response

def export_annual_plan(request):
    active_year = AnnualPlan.objects.filter(year__visible = True)
    annual = AnnualPlanResource()
    dataset = annual.export(active_year)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="annualPlan.xlsx"'
    return response







@login_required
@is_pm_required
def policy_area3(request):
    return render(request, 'PolicyAndMinistries/index.html')


@login_required
@is_pm_required
def info3(request): 
    return render(request, 'PolicyAndMinistries/info.html')


@login_required
@is_pm_required
def search3(request):
    return render(request, 'PolicyAndMinistries/search.html')


@login_required
@is_pm_required
def ministry_index3(request):
    return render(request, 'PolicyAndMinistries/ministries_index.html')
