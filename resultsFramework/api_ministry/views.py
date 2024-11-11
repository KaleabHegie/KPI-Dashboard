from userManagement.models import ResponsibleMinistry
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q 


import random

@api_view(['GET'])
def ministries(request):
    
    if request.method == 'GET':
        ministries = ResponsibleMinistry.objects.filter(ministry_is_visable=True)
        serializer = MinistrySerializer(ministries, many=True, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def ministry_with_policy_area(request, ministry_id=None):
    if ministry_id:
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)
        kras = KeyResultArea.objects.filter(indicators__in=indicators)
        goals = StrategicGoal.objects.filter(kra_goal__in=kras)
        policy_areas = PolicyArea.objects.filter(policy_area_goal__in=goals).annotate(count_goal=Count('policy_area_goal'))
    
    else:
        policy_areas = PolicyArea.objects.annotate(count_goal=Count('policy_area_goal'))
    serializer = PolicyAreaSerializer(policy_areas, many=True, context={'request': request , 'ministry_id' : ministry_id})
    return Response(serializer.data)

@api_view(['GET'])
def policy_area_with_goal(request, id):
    try:
        policy_area = PolicyArea.objects.get(id=id)
    except PolicyArea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if 'ministry_id' in request.GET:
            ministry_id = request.GET['ministry_id']
            serializer = PolicyAreaWithGoalSerializer(policy_area, context={'request': request , 'm_id' : ministry_id})
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def goal_with_kra(request, id):
    try:
        goal = StrategicGoal.objects.get(id=id)
    except StrategicGoal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if 'ministry_id' in request.GET:
            ministry_id = request.GET['ministry_id']
            serializer = GoalWithKraSerializers(goal, context={'request': request , 'ministry_id' : ministry_id})
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def indicator(request,id):
    try:
        indicator = Indicator.objects.get(id=id)
    except Indicator.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = IndicatorSerializer(indicator, context={'request': request})
        return Response(serializer.data)

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

@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        num_policy_area = PolicyArea.objects.count()
        goal = StrategicGoal.objects.count()
        kra = KeyResultArea.objects.count()
        indicator = Indicator.objects.count()
        ministries = ResponsibleMinistry.objects.count()

        context = {
            'dashboard' : [
                {'title' : 'Policy Areas', 'value' : num_policy_area},
                {'title' : 'Strategic Goals', 'value' : goal},
                {'title' : 'Key Result Areas', 'value' : kra},
                {'title' : 'Key Performance Indcators', 'value' : indicator},
                {'title' : 'Public Bodies', 'value' : ministries},
            ]
            }
        return Response(context)

@api_view(['GET'])
def dashboard_ministries(request , ministry_id):
    if request.method == 'GET':
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id).distinct()
        kras = KeyResultArea.objects.filter(indicators__in=indicators).distinct()
        goals = StrategicGoal.objects.filter(kra_goal__in=kras).distinct()
        num_policy_area = PolicyArea.objects.filter(policy_area_goal__in=goals).distinct()

        context = {
            'dashboard' : [
                {'title' : 'Policy Area', 'value' : num_policy_area.count()},
                {'title' : 'Strategic Goals', 'value' : goals.count()},
                {'title' : 'Key Result Areas', 'value' : kras.count()},
                {'title' : 'Public Bodies', 'value' : indicators.count()},
            ]
            }
        return Response(context)

@api_view(['GET'])
def ministryIndicatorPerformance(request , id):
    if request.method == 'GET':
        indicators = Indicator.objects.filter(responsible_ministries__id=id)
        for indicator in indicators:
           if indicator.annual_target:
            very_low = indicator.annual_target
            low = indicator.annual_target 
            high = indicator.annual_target 
            very_high = indicator.annual_target 
        context = {
            'status' : [
                {'title' : 'Very low', 'value' : very_low},
                {'title' : 'Low', 'value' : low},
                {'title' : 'Very high', 'value' : very_high},
                {'title' : 'High', 'value' : high},
            ]
            }
        return Response(context)

@api_view(['GET'])
def indicatorsInGoal(request , id):
    if request.method == 'GET':
        goal = StrategicGoal.objects.get(id=id).id
        kras = KeyResultArea.objects.filter(goal_id=goal)
        indicators = Indicator.objects.filter(keyResultArea__in=kras).distinct().count()
        context = {
            'status' : [
                {'title' : 'Total Indicators', 'value' : indicators},
            ]
            }
        return Response(context)



@api_view(['GET'])
def ministry_indicator_performance(request, ministry_id):
    if request.method == 'GET':
        ministry = ResponsibleMinistry.objects.get(id=ministry_id)
        serializer = MinistryIndicatorPerformanceSerializer(ministry, context={'request': request , 'ministry_id' : ministry_id})
        return Response(serializer.data)



@api_view(['GET'])
def ministry_kra_serializer(request , ministry_id):
    if request.method == 'GET':
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id).distinct()
        kras = KeyResultArea.objects.filter(indicators__in=indicators).distinct()
        serializer = KeyResultAreaWithIndictorSerializer(kras, many=True, context={'request': request , 'ministry_id' : ministry_id})
        return Response(serializer.data)
