########################
import time
from .serializers import *
from userManagement.models import ResponsibleMinistry
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from resultsFramework.models import *
from rest_framework import status
import random
from userManagement.decorators import *


@login_required
@is_pm_required
@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        num_policy_area = PolicyArea.objects.count()
        goal = StrategicGoal.objects.count()
        kra = KeyResultArea.objects.count()
        indicator = Indicator.objects.count()

        context = {
            'dashboard' : [
                {'title' : 'Policy Areas', 'value' : num_policy_area},
                {'title' : 'Strategic Goals', 'value' : goal},
                {'title' : 'Key Result Areas', 'value' : kra},
                {'title' : 'Key Performance Indcators', 'value' : indicator},
            ]
            }
        
        return Response(context)


@login_required
@is_pm_required
@api_view(['GET'])
def policy_areas(request):
    if request.method == 'GET':
        policy_areas = PolicyArea.objects.annotate(count_goal=Count('policy_area_goal')).order_by('rank')
        serializer = PolicyAreaSerializer(policy_areas, many=True, context={'request': request})
        return Response(serializer.data)


@login_required
@is_pm_required
@api_view(['GET'])
def policy_area(request,id):
    try:
        policy_area = PolicyArea.objects.get(id=id)
    except PolicyArea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PolicyAreaWithGoalSerializer(policy_area ,  context={'request': request})
        return Response(serializer.data)
    

@login_required
@is_pm_required
@api_view(['GET'])
def goal_with_kra(request,id):
    try:
        goal = StrategicGoal.objects.get(id=id)
    except StrategicGoal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = GoalWithKraSerializers(goal, context={'request': request})
        return Response(serializer.data)


@login_required
@is_pm_required
@api_view(['GET'])
def indicator(request,id):
    try:
        indicator = Indicator.objects.get(id=id)
    except Indicator.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = IndicatorSerializer(indicator, context={'request': request})
        return Response(serializer.data)


@login_required
@is_pm_required
@api_view(['GET'])
def time_series_year(request):
    if request.method == 'GET':
        current_year = Year.objects.filter(is_current_year = True).first().year_amh
        year = Year.objects.filter(Q(year_amh__lte = current_year))

        yearSerializer = YearSerializer(year, many=True, context={'request': request})
        quarter = Quarter.objects.all()
        quarterSerializer = QuarterSerializer(quarter, many=True, context={'request': request})
        context = {
            'years' : yearSerializer.data,
            'quarters' : quarterSerializer.data,
        }
        return Response(context)
    

@login_required
@is_pm_required
@api_view(['GET'])
def policy_area_SDG(request):
    if request.method == 'GET':
        policy_area = PolicyArea.objects.all()
        serializer = PolicyAreaSDGSerializer(policy_area, many=True)

        sdg = SDG.objects.all()
        serializerSDG = SDGSerializer(sdg, many=True)

        agenda = AgendaGoals.objects.all()
        serializerAgenda = AgendaSerializer(agenda, many=True)


        


        context = {
            'policy_areas' : serializer.data,
            'sdgs' : serializerSDG.data,
            'agendas' : serializerAgenda.data
        }
        return Response(context)


@login_required
@is_pm_required
@api_view(['GET'])
def search_auto_complete(request):
    if 'q' in request.GET: 
        q = request.GET['q']
        indicators = list(Indicator.objects.filter(Q(kpi_name_eng__contains=q) | Q(kpi_name_amh__contains=q) ).values_list('kpi_name_eng', flat=True))[:5]
        kra =list(KeyResultArea.objects.filter(Q(activity_name_eng__contains=q) |Q(activity_name_amh__contains=q)).values_list('activity_name_eng', flat=True))[:5]
        goal =list(StrategicGoal.objects.filter(Q(goal_name_eng__contains=q) | Q(goal_name_amh__contains=q)).values_list('goal_name_eng', flat=True))[:5]

        context = {
            'indicators' : indicators,
            'kras' : kra,
            'goals' : goal
        }
        return Response(context)

@login_required
@is_pm_required
@api_view(['GET'])
def search_item(request):
    if 'q' in request.GET: 
        q = request.GET['q']
        indicators = Indicator.objects.filter(Q(kpi_name_eng__contains=q) | Q(kpi_name_amh__contains=q) )
        indicator_serializer =  SearchIndicatorSerializer(indicators, many=True)

        kra = KeyResultArea.objects.filter(Q(activity_name_eng__contains=q) |Q(activity_name_amh__contains=q))
        kra_serializer = SearchKeyResultAreaSerializer(kra, many=True)

        goal = StrategicGoal.objects.filter(Q(goal_name_eng__contains=q) | Q(goal_name_amh__contains=q))
        goal_serializer = SearchStrategicGoalSerializer(goal, many=True)

        current_year = Year.objects.filter(is_current_year = True).first().year_amh
        year = Year.objects.filter(Q(year_amh__lte = current_year))
        yearSerializer = YearSerializer(year, many=True, context={'request': request})



        context = {
            'indicators' : indicator_serializer.data,
            'kras' : kra_serializer.data,
            'goals' : goal_serializer.data,
            'years' : yearSerializer.data,
        }
        return Response(context)
    

@login_required
@is_pm_required
@api_view(['GET'])
def search_key_result_area_detail(request, id):
    if request.method == 'GET':
        kra = get_object_or_404(KeyResultArea, pk=id)
        serializer = SearchKeyResultAreaSerializer(kra, context={'request': request})

        current_year = Year.objects.filter(is_current_year = True).first().year_amh
        year = Year.objects.filter(Q(year_amh__lte = current_year))
        yearSerializer = YearSerializer(year, many=True, context={'request': request})

        context = {
            'kra' : serializer.data,
            'years' : yearSerializer.data,
        }
        return Response(context)
    

@login_required
@is_pm_required
@api_view(['GET'])
def search_goal_detail(request, id):
    if request.method == 'GET':
        goal = get_object_or_404(StrategicGoal, pk=id)
        serializer = SearchStrategicGoalSerializer(goal, context={'request': request})

        current_year = Year.objects.filter(is_current_year = True).first().year_amh
        year = Year.objects.filter(Q(year_amh__lte = current_year))
        yearSerializer = YearSerializer(year, many=True, context={'request': request})

        context = {
            'goal' : serializer.data,
            'years' : yearSerializer.data,
        }
        return Response(context)