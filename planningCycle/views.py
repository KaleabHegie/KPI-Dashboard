from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render,redirect,reverse,get_object_or_404
from . models import *
from datetime import datetime
from .forms import GoalForm,GoalCommentForm,KRAForm,KPIForm,KRACommentForm,KPICommentForm,MPTTKPIForm,QuarterForm
from userManagement.models import UserSector,ResponsibleMinistry
from django.contrib.auth.decorators import login_required
from userManagement.decorators import *
from django.core.paginator import Paginator
from django.contrib import messages
from .filters import KPIFilterbyMinistry,KRAFilter,GoalFilter
import logging

logger = logging.getLogger(__name__)




@login_required
def add_strategic_goal(request):
    form = GoalForm()

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if not request.user.is_mopd:
                sector_user = UserSector.objects.get(user=request.user)
                ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            else:
                ministry_id = form.cleaned_data.get('responsible_ministries').id
                ministry = ResponsibleMinistry.objects.get(id=ministry_id)
            post.responsible_ministries = ministry
            post.save()
            messages.success(request, "Strategic goal added successfully")
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, "addgoal.html", context)

def exclude_status_field(form_status):
    class ExcludedStatusForm(form_status):
        class Meta:
            model = form_status.Meta.model
            exclude = ['status','kpi_weight','responsible_ministries']
    return ExcludedStatusForm

@login_required
def update_strategic_goal(request, id):
   
    form_status = GoalForm
    if not request.user.is_mopd:
        form_status = exclude_status_field(form_status)
    goal_form = form_status()
    update_strategic_goal = get_object_or_404(DraftStrategicGoal, pk=id)
    if request.method=="POST":
        goal_form = GoalForm(request.POST , instance=update_strategic_goal)
        if goal_form.is_valid():
            if not request.user.is_mopd:
                sector_user = UserSector.objects.get(user=request.user)
                ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            else:
                ministry_id = goal_form.cleaned_data.get('responsible_ministries').id
                ministry = ResponsibleMinistry.objects.get(id=ministry_id)
            post = goal_form.save(commit=False)
            post.responsible_ministries = ministry
            post.save()
            messages.success(request,"Goal Updated")
            goal_page_number = request.GET.get('page', 1)
            return redirect(f"{reverse('home')}?page={goal_page_number}#goal-table")
    else:
        goal_form = GoalForm(instance=update_strategic_goal)
    context ={
        'form':goal_form,
    }
    return render(request,"addgoal.html",context)

@login_required 
def planninghome(request):
    current_year = datetime.now().year
    activegoalplan = Planning_period.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), plan_type__name="Goal" )
    activekraplan = Planning_period.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), plan_type__name="KRA" )
    activekpiplan = Planning_period.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), plan_type__name="KPI" )
    total_policy_area = Annual_Plan.objects.all().count()
    if request.user.is_sector:
        sector_user = UserSector.objects.get(user=request.user)
        ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
        draftgoals = DraftStrategicGoal.objects.filter(responsible_ministries = ministry)
       
        Goalfilter = GoalFilter(request.GET, queryset = draftgoals)
        goal_pagination = Goalfilter.qs

       
        goal_pagination = Paginator(goal_pagination,2)
        page = request.GET.get('page')
        goalPagination = goal_pagination.get_page(page)
        totaldraftgoals = DraftStrategicGoal.objects.filter(responsible_ministries = ministry).count()
        draftkra = DraftKeyResultArea.objects.filter(responsible_ministries = ministry)
        totaldraftkra = DraftKeyResultArea.objects.filter(responsible_ministries = ministry).count()
        
        KRAfilter = KRAFilter(request.GET, queryset = draftkra)
        kra_pagination = KRAfilter.qs

        kra_pagination = Paginator(kra_pagination,5)
        page = request.GET.get('page')
        kraPagination = kra_pagination.get_page(page)

        totaldraftkpi  = DraftKPI.objects.filter(responsible_ministries=ministry,year__year_eng=current_year).count()
        draftkpi  = DraftKPI.objects.filter(responsible_ministries=ministry, year__year_eng=current_year)
        # mptt 
        draftmpttkpi  = DraftMpttKPI.objects.filter(responsible_ministries=ministry, year__year_eng=current_year).order_by('tree_id', 'lft')
        
        KPIfilter = KPIFilterbyMinistry(request.GET, queryset = draftmpttkpi)
        kpi_pagination = KPIfilter.qs

        mptt_kpi_pagination = Paginator(kpi_pagination,10)
        page = request.GET.get('page')
        mpttkpi_pagination = mptt_kpi_pagination.get_page(page)
        kpi_pagination = Paginator(draftkpi,10)
        page = request.GET.get('page')
        kpiPagination = kpi_pagination.get_page(page)
        quarter_target = Annual_Plan.objects.filter(kpi__responsible_ministries=ministry, kpi__year__year_eng=current_year)
       
    elif request.user.is_mopd:
        draftgoals = DraftStrategicGoal.objects.all()
        totaldraftgoals = DraftStrategicGoal.objects.all().count()

        Goalfilter = GoalFilter(request.GET, queryset = draftgoals)
        goal_pagination = Goalfilter.qs

        goal_pagination = Paginator(goal_pagination,6)
        page = request.GET.get('page')
        goalPagination = goal_pagination.get_page(page)
        draftkra = DraftKeyResultArea.objects.all()
        totaldraftkra = DraftKeyResultArea.objects.all().count()

        KRAfilter = KRAFilter(request.GET, queryset = draftkra)
        kra_pagination = KRAfilter.qs

        kra_pagination = Paginator(kra_pagination,5)
        page = request.GET.get('page')
        kraPagination = kra_pagination.get_page(page)

       

        draftkpi  = DraftMpttKPI.objects.filter(year__year_eng=current_year).order_by('tree_id', 'lft')
        totaldraftkpi = DraftMpttKPI.objects.filter(year__year_eng=current_year).count()
        
        KPIfilter = KPIFilterbyMinistry(request.GET, queryset = draftkpi)
        kpi_pagination = KPIfilter.qs

        mptt_kpi_pagination = Paginator(kpi_pagination,10)
        page = request.GET.get('page')
        mpttkpi_pagination = mptt_kpi_pagination.get_page(page)

        kpi_pagination = Paginator(draftkpi,10)
        page = request.GET.get('page')
        kpiPagination = kpi_pagination.get_page(page)
        # quarter Plan
        quarter_target = Annual_Plan.objects.filter(kpi__year__year_eng=current_year)
        # filter by ministry
    else:
        return HttpResponseRedirect(' Not privilaged user')
    
    context = {
        
        'total_policy_area':total_policy_area,
        'totaldraftgoals':totaldraftgoals,
        'goals':draftgoals,
        'activegoalplan':activegoalplan,
        'activekraplan':activekraplan,
        'activekpiplan':activekpiplan,
        'draftkra':draftkra,
        'totaldraftkra':totaldraftkra,
        'draftkpi':draftkpi,
        'totaldraftkpi':totaldraftkpi,
        # goal pagination
        'goalPagination':goalPagination,
        # kra pagination
        'kraPagination':kraPagination,
        # kpi pagination
        'kpiPagination':kpiPagination,
        # mptt kpi
        'mpttkpi_pagination':mpttkpi_pagination,
        # year selection
        'current_year':current_year,
        # quarter pla
        'quarter_target':quarter_target,

        'KPIfilter':KPIfilter,

        'KRAfilter':KRAfilter,

        'Goalfilter':Goalfilter,

    }
    return render(request,"planninghome.html",context)

@login_required  
def delete_goal(request, goal_id):
    goal_delete = DraftStrategicGoal.objects.get(pk=goal_id)
    try:
        goal_delete.delete()
    except DraftKPI.DoesNotExist:
        raise Http404("Deletion could not performed")
    messages.success(request,"Goal is deleted ")
    goal_page_number = request.GET.get('page', 1)
    return redirect(f"{reverse('home')}?page={goal_page_number}#goal-table")

@login_required
def goal_comment(request,goal_id):
    eachgoal = DraftStrategicGoal.objects.get(pk=goal_id)
    num_comments = Comment.objects.filter(strategicgoal=eachgoal).count()
    comments = Comment.objects.filter(strategicgoal=eachgoal)
    # form = GoalCommentForm(instance=eachgoal)
    if request.method =='POST':
        form = GoalCommentForm(request.POST)
        if form.is_valid():
            user = UserSector.objects.get(user=request.user)
            ministry= ResponsibleMinistry.objects.get(id=user.user_sector.id)
            post = form.save(commit=False)
            post.commenter_name = ministry
            post.strategicgoal = eachgoal
            post.save()
            # selectedfrom = form.cleaned_data['goalstatus']
            # eachgoal.status=goalstatus.get(status_name=selectedfrom) 
            # eachgoal.save()
            return redirect("comment_goal",eachgoal.id)
    else:
        form = GoalCommentForm()
    context ={
        'eachgoal':eachgoal,
        'form':form,
        'num_comments':num_comments,
        'comments':comments,
        # 'goalstatus':goalstatus
    }
    return render(request,"comments.html",context)

@login_required
def kra_comment(request,kra_id):
    eachkra = DraftKeyResultArea.objects.get(pk=kra_id)
    num_comments = KRAComment.objects.filter(strategickra=eachkra).count()
    comments = KRAComment.objects.filter(strategickra=eachkra)
    # form = GoalCommentForm(instance=eachgoal)
    if request.method =='POST':
        form = KRACommentForm(request.POST)
        if form.is_valid():
            user = UserSector.objects.get(user=request.user)
            ministry= ResponsibleMinistry.objects.get(id=user.user_sector.id)
            post = form.save(commit=False)
            post.kra_commenter = ministry
            post.strategickra = eachkra
            post.save()
            # selectedfrom = form.cleaned_data['goalstatus']
            # eachgoal.status=goalstatus.get(status_name=selectedfrom) 
            # eachkra.save()
            return redirect("commentkra",eachkra.id)
    else:
        form = KRACommentForm()
    context ={
        'eachkra':eachkra,
        'form':form,
        'num_comments':num_comments,
        'comments':comments,
        # 'goalstatus':goalstatus
    }
    return render(request,"kracomments.html",context)
    


@login_required
# def goal_status(request, id):
#    eachgoalstatus = DraftStrategicGoal.objects.get(pk=id)
#    num_comments = Comment.objects.filter(strategicgoal=eachgoalstatus).count()
#    comments = Comment.objects.filter(strategicgoal=eachgoalstatus)
#    status_form = StatusForm()
#    if request.method =='POST':
#        if request.user.is_mopd:
#             status_form = StatusForm(request.POST or None, instance=eachgoalstatus)
#        else:
#            pass
#        if status_form.is_valid():
#             status_form.save()
#             return redirect("comment_goal",eachgoalstatus.id)
#    else:
#        if request.user.is_mopd:
#             status_form = StatusForm(request.POST or None, instance=eachgoalstatus)
#        else:
#            pass
#    return render(request,"statuschange.html",{'eachgoalstatus':eachgoalstatus,'status_form':status_form,'num_comments':num_comments,
#         'comments':comments,})

@login_required
def add_key_result_area(request):
    form = KRAForm(request.POST or None)
    if request.method =='POST':
        if form.is_valid():
            if not request.user.is_mopd:
                sector_user = UserSector.objects.get(user=request.user)
                ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            else:
                ministry_id = form.cleaned_data.get('responsible_ministries').id
                ministry = ResponsibleMinistry.objects.get(id=ministry_id)

            # sector_user = UserSector.objects.filter(user=request.user).first()
            # ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
                
            post = form.save(commit=False)
            post.responsible_ministries = ministry
            post.save()
            messages.success(request,"Key Result Area added")
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    context = {
        'form':form,
    }
    return render(request,"addkra.html",context)

@login_required
def update_kra(request,id):
    update_key_result_area = DraftKeyResultArea.objects.get(pk = id)
    kra_form = KRAForm(request.POST or None, instance=update_key_result_area)
    if kra_form.is_valid():
        if not request.user.is_mopd:
            sector_user = UserSector.objects.get(user=request.user)
            ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
        else:
            ministry_id = kra_form.cleaned_data.get('responsible_ministries').id
            ministry = ResponsibleMinistry.objects.get(id=ministry_id)
        post = kra_form.save(commit=False)
        post.responsible_ministries = ministry
        post.save()
        messages.success(request,"KRA Updated")
        kra_page_number = request.GET.get('page', 1)
        return redirect(f"{reverse('home')}?page={kra_page_number}#kra-table")
       
    context = {
        'form':kra_form,
    }
    return render(request,"addkra.html",context)

@login_required  
def delete_KRA(request, kra_id):
    try:
        kra_delete = DraftKeyResultArea.objects.get(pk=kra_id)
        kra_delete.delete()
        messages.success(request, "KRA is deleted ")
    except DraftKeyResultArea.DoesNotExist:
        raise Http404("Deletion could not be performed")
    kra_page_number = request.GET.get('page', 1)
    return redirect(f"{reverse('home')}?page={kra_page_number}#kra-table")
    
@login_required  
def delete_kpi(request, kpi_id):
    try:
        kpi_delete = DraftMpttKPI.objects.get(pk=kpi_id)
        page_number = request.GET.get('page', 1)
        kpi_delete.delete()
        messages.success(request, "KPI is deleted ")
    except DraftMpttKPI.DoesNotExist:
        raise Http404("Deletion could not be performed")
    return redirect(f"{reverse('home')}?page={page_number}#kpi-table")

@login_required
def kpiplanning(request,id):

    if request.user.is_sector:
        sector_user = UserSector.objects.get(user=request.user)
        ministry= ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
        draftkpi = DraftKPI.objects.filter(responsible_ministries = ministry,planning__id=id )
        context = {
        'draftkpi':draftkpi,
        }
    elif request.user.is_mopd:
        draftkpi = DraftKPI.objects.filter(planning__id=id)
        # kraplan = DraftKeyResultArea.objects.filter(planning__id =id)
        # goalstatus = GoalStatus.objects.all()
        context = {
            'draftkpi':draftkpi,
            # 'kraplan':kraplan,
        }
    else:
        return render(request,'kpiplanning.html')
    
    return render(request, "kpiplanning.html", context)

@login_required
def add_key_performance_indicator(request):
     
    form = KPIForm(request.POST or None)
    if request.method =='POST':
        if form.is_valid():
            if not request.user.is_mopd:
                sector_user = UserSector.objects.get(user=request.user)
                ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            else:
                ministry_id = form.cleaned_data.get('responsible_ministries').id
                ministry = ResponsibleMinistry.objects.get(id=ministry_id)
            # sector_user = UserSector.objects.filter(user=request.user).first()
            # ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            post = form.save(commit=False)
            post.responsible_ministries = ministry
            post.save()
            messages.success(request,"Key Performance Indicator added")
            return redirect('home',)
        else:
            return redirect('home')
    context = {
    'form':form,
    }
    return render(request,"addkpi.html",context)

@login_required
def add_mptt_key_performance_indicator(request, id):

    parent_kpi = get_object_or_404(DraftMpttKPI, pk=id)
    if request.method == 'POST':
        form = MPTTKPIForm(request.POST)
        if form.is_valid():
            mpttkpi = form.save(commit=False)
            mpttkpi.parent = parent_kpi  # Assign the parent KPI 
            if not request.user.is_mopd:
                sector_user = get_object_or_404(UserSector, user=request.user)
                ministry = get_object_or_404(ResponsibleMinistry, id=sector_user.user_sector.id)
            else:
                ministry_id = form.cleaned_data.get('responsible_ministries').id
                ministry = get_object_or_404(ResponsibleMinistry, id=ministry_id)
            mpttkpi.responsible_ministries = ministry
            mpttkpi.save()
            messages.success(request, "Sub Key Performance Indicator added")
            return redirect('home')
    else:
        form = MPTTKPIForm()

    context = {
        'form': form,
        'parent':parent_kpi,
    }
    return render(request, "addmpttkpi.html", context)


@login_required
def update_kpi(request, id):
    try:
        update_kpi = DraftMpttKPI.objects.get(pk=id)
    except DraftMpttKPI.DoesNotExist:
        raise Http404("DraftKPI does not exist")

    if request.method == 'POST':
        kpi_form = MPTTKPIForm(request.POST, instance=update_kpi)
        if kpi_form.is_valid():
            if not request.user.is_mopd:
                sector_user = UserSector.objects.get(user=request.user)
                ministry = ResponsibleMinistry.objects.get(id=sector_user.user_sector.id)
            else:
                ministry_id = kpi_form.cleaned_data.get('responsible_ministries').id
                ministry = get_object_or_404(ResponsibleMinistry, id=ministry_id)

            # Update fields with cleaned data
            update_kpi.kpi_name_eng = kpi_form.cleaned_data.get('kpi_name_eng')
            update_kpi.kpi_name_amh = kpi_form.cleaned_data.get('kpi_name_amh')
            update_kpi.kpi_weight = kpi_form.cleaned_data.get('kpi_weight')
            update_kpi.kpi_measurement_units = kpi_form.cleaned_data.get('kpi_measurement_units')
            update_kpi.kpi_characteristics = kpi_form.cleaned_data.get('kpi_characteristics')
            update_kpi.kpi_description = kpi_form.cleaned_data.get('kpi_description')
            update_kpi.base_value = kpi_form.cleaned_data.get('base_value')
            update_kpi.target = kpi_form.cleaned_data.get('target')
            update_kpi.responsible_ministries = ministry
            update_kpi.draftkra = kpi_form.cleaned_data.get('draftkra')
            update_kpi.kpistatus = kpi_form.cleaned_data.get('kpistatus')
            update_kpi.year = kpi_form.cleaned_data.get('year')

            # Save the KPI instance
            update_kpi.save()

            messages.success(request, "KPI Updated")
            page_number = request.GET.get('page', 1)
            return redirect(f"{reverse('home')}?page={page_number}#kpi-table")
    else:
        kpi_form = MPTTKPIForm(instance=update_kpi)

    # Get the parent KPI and hierarchy details
    hierarchy = []
    current_kpi = update_kpi
    while current_kpi:
        hierarchy.insert(0, current_kpi)
        current_kpi = current_kpi.parent

    context = {
        'form': kpi_form,
        'hierarchy': hierarchy,
    }
    return render(request, "addmpttkpi.html", context)


@login_required
def kpi_comment(request,kpi_id):
    eachkpi = DraftMpttKPI.objects.get(pk=kpi_id)
    num_comments = KPIComment.objects.filter(strategickpi=eachkpi).count()
    comments = KPIComment.objects.filter(strategickpi=eachkpi)
    # form = GoalCommentForm(instance=eachgoal)
    if request.method =='POST':
        form = KPICommentForm(request.POST)
        if form.is_valid():
            user = UserSector.objects.get(user=request.user)
            ministry= ResponsibleMinistry.objects.get(id=user.user_sector.id)
            post = form.save(commit=False)
            post.kpi_commenter = ministry
            post.strategickpi = eachkpi
            post.save()
            # selectedfrom = form.cleaned_data['goalstatus']
            # eachgoal.status=goalstatus.get(status_name=selectedfrom) 
            # eachkra.save()
            return redirect("commentkpi",eachkpi.id)
    else:
        form = KPICommentForm()
    context ={
        'eachkpi':eachkpi,
        'form':form,
        'num_comments':num_comments,
        'comments':comments,
        # 'goalstatus':goalstatus
    }
    return render(request,"kpicomments.html",context)


def error_404_view(request, exception):
    return render(request, 'page_not_found_404.html', status=404)

@login_required
def quarterplan(request,id):
    quarterdkpi = get_object_or_404(DraftMpttKPI, pk=id)
    if request.method == 'POST':
        quarterform = QuarterForm(request.POST)
        if quarterform.is_valid():
            quartertarget = quarterform.save(commit=False)
            quartertarget.kpi = quarterdkpi
            quartertarget.save()
            return redirect("home")
    else:
        quarterform = QuarterForm(initial={'kpi': quarterdkpi})    
    context ={
        'quarterdkpi':quarterdkpi,
        'quarterform':quarterform,
    }
    return render(request,"addquarterplan.html",context)

@login_required
def update_Quarter_Plan(request, id):
    update_quarter_plan = get_object_or_404(Annual_Plan, pk=id)

    if request.method == 'POST':
        quarter_form = QuarterForm(request.POST, instance=update_quarter_plan)

        if quarter_form.is_valid():
            # ministry_id = quarter_form.cleaned_data.get('responsible_ministries').id
            # ministry = get_object_or_404(ResponsibleMinistry, id=ministry_id)

            post = quarter_form.save(commit=False)
            # post.responsible_ministries = ministry
            post.save()
            messages.success(request, "Quarter Updated")
            return redirect("home")
    else:
        quarter_form = QuarterForm(instance=update_quarter_plan)

    context = {
        'quarterform': quarter_form,
    }
    return render(request, "addquarterplan.html", context)