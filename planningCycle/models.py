from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
import datetime
from mptt.models import MPTTModel, TreeForeignKey


class Plan_type(models.Model):
    name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name
    
class Planning_period(models.Model):
    plan_type = models.ForeignKey(Plan_type,on_delete = models.SET_NULL, null=True)
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date not exceed than end date && end date not less than start date")
    class Meta:
        verbose_name = "Planning Period"
    def __str__(self):
        return self.plan_name
    
 
class Status(models.Model):
    status_name = models.CharField(max_length=10,default=1)
    def __str__(self) -> str:
        return self.status_name
class Policy_Area(models.Model):
    policy_area_eng_name = models.CharField(max_length=255,null=True)
    policy_area_amh_name = models.CharField(max_length=255, null=True)
    rank_for_order = models.IntegerField()
    short_name = models.SlugField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.short_name


class DraftStrategicGoal(models.Model):
    parent_policy_area = models.ForeignKey(Policy_Area, on_delete=models.SET_NULL,null=True)
    goal_name_eng = models.CharField(max_length=105, null=True, blank=True,unique = True)
    goal_name_amh = models.CharField(max_length=105,null=True, blank=True)
    goal_weight = models.DecimalField(max_digits=10,null=True,decimal_places=2)
    goal_is_shared = models.BooleanField(default=False,)
    national_plan = models.ForeignKey(
        "resultsFramework.NationalPlan", on_delete=models.SET_NULL, null=True,default = 1)
    
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank = True, null=True,default=1)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", related_name="goal_ministry", on_delete=models.SET_NULL,blank =True, null=True)
    description = RichTextField(blank=True)
    def __str__(self):
        return self.goal_name_eng or ''
   
class Comment(models.Model):
    strategicgoal = models.ForeignKey(DraftStrategicGoal, on_delete=models.CASCADE,related_name="comments")
    commenter_name = models.ForeignKey("userManagement.ResponsibleMinistry", related_name="comment_ministry" ,on_delete=models.SET_NULL, null=True)
    body = RichTextField()
    # goalstatus = models.ForeignKey(GoalStatus,on_delete=models.CASCADE, null=True,default = 1)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.strategicgoal.goal_name_eng, self.date_added)

 ####################################################################### 
#  Key Result Area -KRA
######################################################################

class DraftKeyResultArea(models.Model):
    activity_name_eng = models.CharField(max_length=110,unique = True)
    activity_name_amh = models.CharField(max_length=110)
    activity_weight = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    activity_is_shared = models.BooleanField(default=False)
    goal = models.ForeignKey(DraftStrategicGoal, on_delete=models.SET_NULL, blank = True,null=True)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", related_name="kra_ministry", on_delete=models.SET_NULL, null=True,blank=True)
    krastatus = models.ForeignKey(Status, on_delete=models.CASCADE,blank=True, null=True, default=1)
    description = RichTextField(null = True, blank = True)
    def __str__(self):
        return self.activity_name_eng
    
class KRAComment(models.Model):
    strategickra = models.ForeignKey(DraftKeyResultArea, on_delete=models.CASCADE,related_name="kracomments")
    kra_commenter = models.ForeignKey("userManagement.ResponsibleMinistry", related_name="kra_comment_ministry" ,on_delete=models.SET_NULL, null=True)
    body = RichTextField()
    # goalstatus = models.ForeignKey(GoalStatus,on_delete=models.CASCADE, null=True,default = 1)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.strategickra.activity_name_eng, self.date_added)

class DraftKPI(models.Model):
    CHARACTERISTICS = (
        ("increasing","Increasing"),
        ("decreasing","Decreasing"),
        ("constant","Constant"),
        ("ratio","Ratio"),
    )
    kpi_name_eng = models.CharField(max_length=220,unique = True)
    kpi_name_amh = models.CharField(max_length=220)
    kpi_weight = models.DecimalField(max_digits=10, decimal_places=2,blank = True,null=True)
    kpi_measurement_units = models.CharField(max_length = 50)
    kpi_characteristics = models.CharField(max_length = 50,choices = CHARACTERISTICS,default = None)
    kpi_description = RichTextField(null = True)
    base_value = models.FloatField(null = True)
    target = models.FloatField(null=True)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", related_name="kPI_ministry", on_delete=models.SET_NULL, blank = True, null=True)
    draftkra = models.ForeignKey(DraftKeyResultArea, verbose_name=(
        "Key Result Area"), on_delete=models.SET_NULL, null=True)
    kpistatus = models.ForeignKey(Status, on_delete=models.SET_NULL,blank=True, null=True, default=1)
    year = models.ForeignKey("resultsFramework.Year",on_delete=models.CASCADE,null=True,default=datetime.datetime.now().year)

    class Meta:
        verbose_name = "Draft Key Performance Indicators"
        unique_together = (('kpi_name_eng', 'year'),)
    def __str__(self):
        return self.kpi_name_eng


class DraftMpttKPI(MPTTModel):
    CHARACTERISTICS = (
        ("increasing","Increasing"),
        ("decreasing","Decreasing"),
        ("constant","Constant"),
        ("ratio","Ratio"),
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    kpi_name_eng = models.CharField(max_length=220,unique = True)
    kpi_name_amh = models.CharField(max_length=220)
    kpi_weight = models.DecimalField(max_digits=10, decimal_places=2,blank = True,null=True)
    kpi_measurement_units = models.CharField(max_length = 50)
    kpi_characteristics = models.CharField(max_length = 50,choices = CHARACTERISTICS,default = None)
    kpi_description = RichTextField(null = True)
    base_value = models.FloatField(null = True)
    target = models.FloatField(null=True)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", related_name="mptt_kPI_ministry", on_delete=models.SET_NULL, blank = True, null=True)
    draftkra = models.ForeignKey(DraftKeyResultArea, verbose_name=(
        "Key Result Area"), on_delete=models.SET_NULL,blank=True, null=True)
    kpistatus = models.ForeignKey(Status, on_delete=models.SET_NULL,blank=True, null=True, default=1)
    year = models.ForeignKey("resultsFramework.Year",on_delete=models.CASCADE,null=True,default=datetime.datetime.now().year)

    class MPTTMeta:
        order_insertion_by =['kpi_name_eng']
    def __str__(self):
        return f"{self.kpi_name_eng}-{self.target}" or ''
    
class KPIComment(models.Model):
    strategickpi = models.ForeignKey(DraftMpttKPI, on_delete=models.CASCADE,related_name="kpicomments")
    kpi_commenter = models.ForeignKey("userManagement.ResponsibleMinistry", related_name="kpi_comment_ministry" ,on_delete=models.SET_NULL, null=True)
    body = RichTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.strategickpi.kpi_name_eng, self.date_added)

class Annual_Plan(models.Model):
    kpi = models.ForeignKey(DraftMpttKPI, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=150,null=True)
    quarter1_target = models.FloatField()
    quarter2_target = models.FloatField()
    quarter3_target = models.FloatField()
    quarter4_target = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name