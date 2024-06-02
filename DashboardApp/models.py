from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Year(models.Model):
    year_eng = models.IntegerField(blank=True, null=True)
    year_amh = models.IntegerField(blank=True, null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year_amh)

    class Meta:
        ordering = ['year_amh']
        
class Quarter(models.Model):
    year = models.ForeignKey(
        Year, on_delete=models.SET_NULL, blank=True, null=True)
    quarter_eng = models.CharField(max_length=100, blank=True, null=True)
    quarter_amharic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.quarter_eng


class Month(models.Model):
    year = models.ForeignKey(
        Year, on_delete=models.SET_NULL, blank=True, null=True)
    month_amh = models.CharField(max_length=100 , blank=True, null=True)
    month_english = models.CharField(max_length=100, blank=True, null=True)
    month_ranked = models.IntegerField()

    def __str__(self):
        return self.month_english


class NationalPlan(models.Model):
    np_name_eng = models.CharField(max_length=150, blank=True)
    np_name_amh = models.CharField(max_length=150, blank=True)
    description_eng = models.TextField()
    description_amh = models.TextField()
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()

    def __str__(self):
        return self.np_name_eng



class StrategicGoal(models.Model):
    goal_name_eng = models.CharField(max_length=350, blank=True)
    goal_name_amh = models.CharField(max_length=350, blank=True, null=True)
    goal_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    goal_is_shared = models.BooleanField(default=False)
    national_plan = models.ForeignKey(
        NationalPlan, on_delete=models.SET_NULL, null=True)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", on_delete=models.SET_NULL, null=True, related_name="ministry_goal")


    def __str__(self):
        return self.goal_name_eng


class KeyResultArea(models.Model):
    activity_name_eng = models.CharField(max_length=350)
    activity_name_amh = models.CharField(max_length=350, blank=True)
    activity_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    activity_is_shared = models.BooleanField(default=False)
    goal = models.ForeignKey(StrategicGoal, related_name="kra_goal", verbose_name=(
        "Strategic Planning Goals"), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.activity_name_eng

    class Meta:
        indexes = [
            models.Index(fields=['goal']),
        ]


        
class Indicator(models.Model):
    KPI_CHARACTERISTIC_CHOICES = [
        ('inc', 'Increasing'),
        ('dec', 'Decreasing'),
        ('const', 'Constant'),
    ]

    kpi_name_eng = models.CharField(max_length=100)
    kpi_name_amh = models.CharField(max_length=100, blank=True)
    kpi_weight = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True)
    kpi_measurement_units = models.CharField(max_length=50)
    kpi_characteristics = models.CharField(
        max_length=10,
        choices=KPI_CHARACTERISTIC_CHOICES,
        default='inc',
    )

    # kpi_shared = models.BooleanField(default=False)
    # kpi_selected = models.BooleanField(default=False)
    # kpi_additive = models.BooleanField(default=False)
    # has_aggregation = models.BooleanField(default=False)
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", on_delete=models.SET_NULL, null=True)
    keyResultArea = models.ForeignKey(
        KeyResultArea, on_delete=models.SET_NULL, null=True)
    # kpi = models.ForeignKey("Indicator", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.kpi_name_eng

    class Meta:
        verbose_name = "Key Performance Indicator"



view_types  = [
    ('month', 'Month'),
    ('quarter', 'Quarter'),
    ('year','Year')
]
trend  = [
    ('performance', 'Performance'),
    ('both','Both')
]

class DashboardCategory(models.Model):
    name_eng = models.CharField(max_length=200)
    name_amh = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name_eng


class DashboardSetting(models.Model):
    year = models.ForeignKey(Year , on_delete=models.CASCADE)
    performance = models.BooleanField(default=False)
    target = models.BooleanField(default=False)
    indicator = models.ManyToManyField(Indicator)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    dashboard_category = models.ForeignKey(DashboardCategory , on_delete=models.CASCADE)
    
    def __str__(self):
        return self.indicator



class Category(models.Model):
    name_eng = models.CharField(max_length=200)
    name_amh = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name_eng

        
class KpiAggregation(MPTTModel):
    sub_kpi_name_eng = models.CharField(max_length=400)
    sub_kpi_name_amh = models.CharField(max_length=400)
    kpi = models.ForeignKey(
        "Indicator", on_delete=models.SET_NULL, null=True, related_name='sub_kpi')
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['sub_kpi_name_eng']

    def __str__(self):
        return self.sub_kpi_name_eng

class QuarterProgress(models.Model):
    national_plan = models.ForeignKey(NationalPlan, on_delete=models.CASCADE)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_indicators')

    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_sub_indicators')

    quarter_target = models.FloatField(blank=True)
    quarter = models.ForeignKey(
        Quarter, on_delete=models.CASCADE, related_name='quarters')
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    quarter_performance = models.FloatField(blank=True, null=True)
    quarter_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.kpi_name_eng
        else:
            return self.sub_indicator.sub_kpi_name_eng


class AnnualPlan(models.Model):
    national_plan = models.ForeignKey(
        NationalPlan, on_delete=models.SET_NULL, null=True)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='annual_indicators')

    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='annual_sub_indicators')
    annual_target = models.FloatField(blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    annual_performance = models.FloatField(blank=True, null=True)
    annual_date = models.DateTimeField(auto_now_add=True,  blank=True)
    target_state = models.CharField(max_length=20, choices=[
        ("cum", "Cumulative"),
        ("net", "Net"),

    ], null=True)

    def __str__(self):
        return str(self.year)


class MonthProgress(models.Model):
    national_plan = models.ForeignKey(NationalPlan, on_delete=models.CASCADE)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='month_indicators')

    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='month_sub_indicators')

    monthly_target = models.FloatField(blank=True)
    month = models.ForeignKey(
        Month, on_delete=models.CASCADE, related_name='months')
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    month_performance = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.kpi_name_eng
        else:
            return self.sub_indicator.sub_kpi_name_eng        


