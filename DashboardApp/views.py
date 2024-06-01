from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import MinistrySerializers , GoalSerializers
from django.http import JsonResponse
from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal
from django.db.models import Count
from django.core import serializers
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



@api_view(['GET'])
def key_area_list(request, id): 
    goal_list = list(StrategicGoal.objects.filter(responsible_ministries__id=id))
    KeyResultArea_list_id = list(StrategicGoal.objects.filter(responsible_ministries__id=id).prefetch_related('kra_goal__set').all().values_list('kra_goal__id', 'goal_name_eng' ))

    # value_filter = list(DataValue.objects.filter(Q(for_indicator__id__in=indicator_list_id) & ~Q(for_datapoint_id__year_EC=None)).select_related("for_datapoint", "for_indicator").order_by('for_datapoint_id__year_EC').values(
    #     'for_indicator__type_of',
    #     'value',
    #     'for_indicator_id',
    #     'for_datapoint_id__year_EC',
    #     'for_datapoint_id__year_GC',
    #     'for_quarter_id',
    #     'for_month_id__month_AMH',
    # ))

   


    # queryset = Category.objects.filter(dashboard_topic__id=id).prefetch_related('indicator__set').filter(indicator__is_dashboard_visible=True).values(
    #     'dashboard_topic__title_ENG',
    #     'id',
    #     'name_ENG',
    #     'name_AMH',
    #     'indicator__id',
    #     'indicator__title_ENG',
    #     'indicator__title_AMH',
    #     'indicator__is_dashboard_visible',
    #     'indicator__type_of'   
    # )

    # categories_lists = Category.objects.filter(dashboard_topic__id=id).annotate(count_indicators=Count('indicator')).filter(indicator__is_dashboard_visible=True).values(
    #     'id',
    #     'name_ENG',
    #     'name_AMH', 
    #     'count_indicators'
    # )
    # categories_lists = categories_lists.filter(~Q(count_indicators=0)).values(
    #     'id',
    #     'name_ENG',
    #     'name_AMH', 
    #     'count_indicators'
    # )

    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     dashboard_topic = DashboardTopic.objects.all()
    #     queryset = Category.objects.filter().prefetch_related('indicator__set').filter(Q(indicator__title_ENG__contains=q, dashboard_topic__in=dashboard_topic) | Q(indicator__for_category__name_ENG__contains=q, dashboard_topic__in=dashboard_topic)).order_by('for_datapoint_id__year_EC').values(
    #         'dashboard_topic__title_ENG',
    #         'id',
    #         'name_ENG',
    #         'name_AMH',
    #         'indicator__id',
    #         'indicator__title_ENG',
    #         'indicator__title_AMH',
    #         'indicator__is_dashboard_visible',
    #         'indicator__type_of'
    #     )
    #     indicator_list_id = queryset.values_list('indicator__id', flat=True)

    #     value_filter = list(DataValue.objects.filter(Q(for_indicator__id__in=indicator_list_id) & ~Q(for_datapoint_id__year_EC=None)).select_related("for_datapoint", "for_indicator").order_by('for_datapoint_id__year_EC').values(
    #         'for_indicator__type_of',
    #         'value',
    #         'for_indicator_id',
    #         'for_datapoint_id__year_EC',
    #         'for_datapoint_id__year_GC',
    #         'for_quarter_id',
    #         'for_month_id__month_AMH',
    #         'for_quarter_id__title_ENG',
    #     ))


    #     categories_lists_id = queryset.values_list('id', flat=True)
    #     categories_lists = Category.objects.filter(id__in=categories_lists_id).values(
    #         'id',
    #         'name_ENG',
    #         'name_AMH', 
    #     )

    # paginator = Paginator(queryset, 20) 
    # page_number = request.GET.get('page')
    # try:
    #     page_obj = paginator.page(page_number)
    # except PageNotAnInteger:
    #     # if page is not an integer, deliver the first page
    #     page_obj = paginator.page(1)
    # except EmptyPage:
    #     # if the page is out of range, deliver the last page
    #     page_obj = paginator.page(paginator.num_pages)

    return JsonResponse({
        # 'categories': list(queryset), 
        # 'has_previous': page_obj.has_previous(),
        # 'has_next': page_obj.has_next(),
        # 'previous_page_number': page_obj.has_previous() and page_obj.previous_page_number() or None,
        # 'next_page_number': page_obj.has_next() and page_obj.next_page_number() or None,
        # 'number': int(page_obj.number),
        # 'page_range': list(page_obj.paginator.page_range),
        # 'num_pages': page_obj.paginator.num_pages,
        # 'values': value_filter, 
        # 'categories_lists': list(categories_lists),
        "KeyResultArea_list_id" : KeyResultArea_list_id
    })