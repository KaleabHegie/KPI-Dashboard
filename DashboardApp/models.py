from audioop import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField
from django.db.models import Avg, Sum
from django.db.models import Q, F, ExpressionWrapper, FloatField, Avg, Value
from django.db.models.functions import Coalesce
from django.db.models import Case, When
from fontawesome_5.fields import IconField
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q, F, ExpressionWrapper, FloatField, Avg, Value
from django.db.models.functions import Coalesce
from django.db.models import Case, When
# Create your models here.
CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 300)

class ScoreCardRange(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')
    starting = models.DecimalField(max_digits=5, decimal_places=2)
    ending = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Year(models.Model):
    year_eng = models.IntegerField()
    year_amh = models.IntegerField()
    visible = models.BooleanField(default=True)
    mdip = models.BooleanField(default=True)
    quarter_view = models.BooleanField(default=False)
    is_current_year = models.BooleanField(default=False)  # New field

    def save(self, *args, **kwargs):
        # Check if the year_eng is the current year
        current_year = datetime.now().year
        self.is_current_year = (self.year_eng == current_year)
        super(Year, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.year_amh)

    class Meta:
        ordering = ['year_amh']
        
class Quarter(models.Model):
    quarter_eng = models.CharField(max_length=100, blank=True, null=True)
    quarter_amharic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.quarter_eng


class Month(models.Model):
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, blank=True, null=True)
    month_amh = models.CharField(max_length=100)
    month_english = models.CharField(max_length=100)
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

class SDG(models.Model):
    code = models.IntegerField( unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return 'SDG ' + str(self.code) + " - " + self.title
    
    class Meta:
        ordering = ['-code']


class AgendaGoals(models.Model):
    title = models.CharField(max_length=100)
    goal = models.CharField(max_length=100)
    sdg = models.ManyToManyField("SDG",  blank=True, related_name="agenda_goals")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']

class PolicyArea(models.Model):
    policyAreaEng = models.CharField(max_length=450, blank=True)
    policyAreaAmh = models.CharField(max_length=450, blank=True)
    icon = IconField()
    rank = models.IntegerField(default=400)
    sdg = models.ManyToManyField("SDG",  blank=True, related_name='sdgs')

    def __str__(self):
        return self.policyAreaEng 


    def policy_area_score_card(self, quarter=None, year=None):
        cache_key = f"policy_area_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            # Prefetch all goals for the policy area to avoid repeated DB queries
            goals = self.policy_area_goal.all().prefetch_related('kra_goal')
    
            total_score_sum = 0  # Initialize sum
            
            for goal in goals:
                goal_weight = goal.goal_weight  # Fetch goal weight
    
                # Use cached strategic_goal_score_card to avoid repeated scorecard calculation
                if quarter and year:
                    goal_score = goal.strategic_goal_score_card(quarter=quarter, year=year)['avg_score']
                else:
                    goal_score = goal.strategic_goal_score_card(year=year)['avg_score']
    
                # Calculate weighted goal score
                weighted_goal_score = float(goal_score) * float(goal_weight / 100)
                total_score_sum += weighted_goal_score
    
            # Final average score
            avg_score = total_score_sum
    
            # Cache score card ranges if not already cached
            score_card_ranges = cache.get_or_set('score_card_ranges', lambda: list(ScoreCardRange.objects.all()), CACHE_TIMEOUT)
    
            # Determine score card color based on average score
            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"
    
            # Store result
            result = {
                'sum_score': total_score_sum,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
    
            # Cache the final result
            cache.set(cache_key, result, CACHE_TIMEOUT)
    
        return result

    
    def ministry_policy_area_score_card(self, quarter=None, year=None , goal_ids = None , kra_id = None,indicator_id= None):
        cache_key = f"policy_area_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            # Perform calculations if not cached
            goals = self.policy_area_goal.filter(id__in = goal_ids)
            goal_avg_score = 0
            goal_total_wight = 0
            sum = 0
            for goal in goals:
                goal_weight = goal.goal_weight
                if quarter and year:
                    sum = sum + goal.ministry_strategic_goal_score_card(quarter=quarter, year=year , indicator_id = indicator_id , kras_ids = kra_id)['avg_score'] * float(goal_weight/100)
                else:
                    goal_percent = float(goal.ministry_strategic_goal_score_card(year=year , indicator_id = indicator_id , kras_ids = kra_id)['avg_score'])  * float(goal_weight/100)
                    sum = sum + goal_percent
                    goal_total_wight = goal_total_wight + goal_weight
            
            if goal_total_wight != 0:
              avg_score = float(sum * 100) / float(goal_total_wight) 
            else :
              avg_score = 0

            score_card_ranges = cache.get('score_card_ranges')
            

            if score_card_ranges is None:
                score_card_ranges = list(ScoreCardRange.objects.all())
                cache.set('score_card_ranges', score_card_ranges, CACHE_TIMEOUT)

            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"

            result = {
                'sum_score': sum,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
            cache.set(cache_key, result, CACHE_TIMEOUT)
        
        return result

    
class StrategicGoal(models.Model):
    goal_name_eng = models.CharField(max_length=350, blank=True)
    goal_name_amh = models.CharField(max_length=350, blank=True, null=True)
    goal_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    goal_is_shared = models.BooleanField(default=False)
    national_plan = models.ForeignKey(
        NationalPlan, on_delete=models.SET_NULL, null=True)
    policy_area = models.ForeignKey(
        "PolicyArea", on_delete=models.SET_NULL, related_name="policy_area_goal", blank=True,null=True, )

    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", on_delete=models.SET_NULL, null=True, related_name="ministry_goal", blank=True)
    
    goal_is_visable = models.BooleanField(default=False)
    def __str__(self):
        return self.goal_name_eng
    


    def strategic_goal_score_card(self, quarter=None, year=None):
        cache_key = f"strategic_goal_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            # Prefetch all KRAs and their weights to avoid repeated queries
            key_result_areas = self.kra_goal.all().prefetch_related('indicators')
    
            # Initialize sum to 0
            total_score_sum = 0
    
            for kra in key_result_areas:
                kra_weight = kra.activity_weight
                
                # Fetch the KRA score based on quarter and year
                kra_score = kra.key_result_area_score_card(year=year, quarter=quarter)['avg_score'] if quarter else kra.key_result_area_score_card(year=year)['avg_score']
                
                # Calculate weighted KRA score
                kra_weighted_score = float(kra_score) * float(kra_weight / 100)
                total_score_sum += kra_weighted_score
    
            # Calculate the strategic goal score and average score
            goal_score = total_score_sum * float(self.goal_weight / 100)
            avg_score = (goal_score * 100) / float(self.goal_weight) if self.goal_weight else 0
    
            # Cache score card ranges if not already cached
            score_card_ranges = cache.get_or_set('score_card_ranges', lambda: list(ScoreCardRange.objects.all()), CACHE_TIMEOUT)
    
            # Determine score card color
            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"
    
            # Final result dictionary
            result = {
                'sum_score': total_score_sum,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
    
            # Cache the final result
            cache.set(cache_key, result, CACHE_TIMEOUT)
    
        return result

    
    def ministry_strategic_goal_score_card(self, quarter=None, year=None , kras_ids=None , indicator_id=None):
        cache_key = f"ministry_strategic_goal_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            key_result_areas = self.kra_goal.filter(id__in=kras_ids).distinct()
            sum = 0
            kra_total_wight = 0
            for kra in key_result_areas:
                kra_weight =  kra.activity_weight
                if quarter and year:
                    sum = sum +kra.ministry_key_result_area_score_card(year=year, quarter=quarter , indicators_id = indicator_id)['avg_score']
                elif year:
                   kra_percent = float(kra.ministry_key_result_area_score_card(year=year , indicators_id=indicator_id)['avg_score']) * float(kra_weight/100)
                   sum = sum + kra_percent
            goals = StrategicGoal.objects.filter(kra_goal__id__in=kras_ids , policy_area = self.policy_area).distinct()
            total_goal_weight = 0
            for goal in goals:
                total_goal_weight = total_goal_weight + goal.goal_weight  
            

            
           
            
            calculated_weight = float((self.goal_weight)*100) / float(total_goal_weight)
          
            goal_score = float(float(sum) * float(calculated_weight)) / 100
            avg_score = goal_score

            print('-------===============',avg_score, total_goal_weight, sum, calculated_weight) 

            

            score_card_ranges = cache.get('score_card_ranges')

            if score_card_ranges is None:
                score_card_ranges = list(ScoreCardRange.objects.all())
                cache.set('score_card_ranges', score_card_ranges, CACHE_TIMEOUT)

            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"

            result = {
                'sum_score': sum,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
            cache.set(cache_key, result, CACHE_TIMEOUT)

     
        return result

class KeyResultArea(models.Model):
    activity_name_eng = models.CharField(max_length=350)
    activity_name_amh = models.CharField(max_length=350, blank=True)
    activity_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    activity_is_shared = models.BooleanField(default=False)
    goal = models.ForeignKey(StrategicGoal, related_name="kra_goal", verbose_name=(
        "Strategic Planning Goals"), on_delete=models.SET_NULL, null=True)
    kra_is_visable = models.BooleanField(default=False)
    def __str__(self):
        return self.activity_name_eng

    class Meta:
        indexes = [
            models.Index(fields=['goal']),
        ]

    def key_result_area_score_card(self, quarter=None, year=None):
        cache_key = f"key_result_area_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            indicators = self.indicators.values_list('id', flat=True)  # Faster, no need for 'all()'

            score_query = AnnualPlan.objects if not quarter else QuarterProgress.objects

            filter_params = {
                'indicator__in': indicators,
                'year__year_amh': year
            }
            if quarter:
                filter_params['quarter__quarter_eng'] = quarter
                filter_params['quarter_target__isnull'] = False
                performance_field = 'quarter_performance'
                target_field = 'quarter_target'
            else:
                filter_params['annual_target__isnull'] = False
                performance_field = 'annual_performance'
                target_field = 'annual_target'
                # Perform a single query with necessary annotations and aggregations
                scores = score_query.filter(**filter_params).annotate(
    
                performance_value=Coalesce(F(performance_field), Value(0)),
                raw_performance_percentage=ExpressionWrapper(
                    F('performance_value') * 100.0 / F(target_field), output_field=FloatField()
                ),
                performance_percentage=Case(
                    When(raw_performance_percentage__gt=100, then=Value(100.0)),
                    default=F('raw_performance_percentage'),
                    output_field=FloatField()
                ),
                weighted_performance=ExpressionWrapper(
                    F('performance_percentage') * F('indicator__kpi_weight') / 100.0, 
                    output_field=FloatField()
                )
            ).aggregate(
                total_score=Sum('weighted_performance'),
                total_indicator_weight=Sum('indicator__kpi_weight'),
            )


            try:
                avg_score = float(scores['total_score'] * 100 / float(scores['total_indicator_weight'])) if scores['total_indicator_weight'] else 0
            except:
                avg_score = 0

    
            # Cache ScoreCardRanges only if necessary
            score_card_ranges = cache.get_or_set('score_card_ranges', lambda: list(ScoreCardRange.objects.all()), CACHE_TIMEOUT)
    
            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"
    
            result = {
                'sum_score': avg_score,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
    
            cache.set(cache_key, result, CACHE_TIMEOUT)

        return result


    def ministry_key_result_area_score_card(self ,quarter=None, year=None , indicators_id=None):
        cache_key = f"ministry_key_result_area_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            indicators = self.indicators.filter(id__in=indicators_id).values_list('id', flat=True)

            if quarter:
                annual_scores = QuarterProgress.objects.filter(
                    Q(quarter_target__isnull=False),  
                    Q(indicator__in=indicators),
                    Q(year__year_amh=year),
                    Q(quarter__quarter_eng = quarter)
                ).annotate(
                    # Replace null performance values with 0 using Coalesce
                    performance_value=Coalesce('quarter_performance', Value(0)),
                    
                    # Calculate the percentage of performance over target for each row
                    raw_performance_percentage=ExpressionWrapper(
                        F('performance_value') * 100.0 / F('quarter_target'),
                        output_field=FloatField()
                    ),

                    
                    # Cap the performance percentage at 100 if it exceeds 100
                    performance_percentage=Case(
                        When(raw_performance_percentage__gt=100, then=Value(100.0)),
                        default=F('raw_performance_percentage'),
                        output_field=FloatField()
                    ),

                    kpi_weight_value=F('indicator__kpi_weight'),

                    weighted_performance=ExpressionWrapper(
                        F('performance_percentage') * (F('kpi_weight_value') / 100.0), 
                        output_field=FloatField()
                    )
                ).values('weighted_performance', 'kpi_weight_value'
                ).aggregate(
                    total_score=Sum('weighted_performance'),
                    total_indicator_weight=Sum('kpi_weight_value'),
                )

                sum_score = annual_scores['total_score'] or 0
                try: 
                    avg_score = float(annual_scores['total_score'] * 100) / float(annual_scores['total_indicator_weight']) 
                except: 
                    avg_score = 0
            else:
                annual_scores = AnnualPlan.objects.filter(
                    Q(annual_target__isnull=False),  
                    Q(indicator__in=indicators),
                    Q(year__year_amh=year)
                ).annotate(
                    # Replace null performance values with 0 using Coalesce
                    performance_value=Coalesce('annual_performance', Value(0)),
                    
                    # Calculate the percentage of performance over target for each row
                    raw_performance_percentage=ExpressionWrapper(
                        F('performance_value') * 100.0 / F('annual_target'),
                        output_field=FloatField()
                    ),

                    
                    # Cap the performance percentage at 100 if it exceeds 100
                    performance_percentage=Case(
                        When(raw_performance_percentage__gt=100, then=Value(100.0)),
                        default=F('raw_performance_percentage'),
                        output_field=FloatField()
                    ),

                    kpi_weight_value=F('indicator__kpi_weight'),

                    weighted_performance=ExpressionWrapper(
                        F('performance_percentage') * (F('kpi_weight_value') / 100.0), 
                        output_field=FloatField()
                    )
                ).values('weighted_performance', 'kpi_weight_value'
                ).aggregate(
                    total_score=Sum('weighted_performance'),
                    total_indicator_weight=Sum('kpi_weight_value'),
                )

                sum_score = annual_scores['total_score'] or 0
                try: 
                    avg_score = float(annual_scores['total_score'] * 100) / float(annual_scores['total_indicator_weight']) 
                except: 
                    avg_score = 0
                    


            score_card_ranges = cache.get('score_card_ranges')
            if score_card_ranges is None:
                score_card_ranges = list(ScoreCardRange.objects.all())
                cache.set('score_card_ranges', score_card_ranges, CACHE_TIMEOUT)

            card = next((range for range in score_card_ranges if range.starting <= avg_score <= range.ending), None)
            scorecard_color = card.color if card else "#4680ff"

            result = {
                'sum_score': sum_score,
                'avg_score': avg_score,
                'scorecard_color': scorecard_color,
            }
            cache.set(cache_key, result, CACHE_TIMEOUT)

        return result

class IndicatorTempo(models.Model):
    responsible_ministries = models.ForeignKey(
        "userManagement.ResponsibleMinistry", on_delete=models.SET_NULL, null=True, related_name="ministry_kpi3")
    goal = models.ForeignKey(StrategicGoal, related_name="kra_goal3", verbose_name=(
        "Strategic Planning Goals1"), on_delete=models.SET_NULL, null=True)
    KPI_CHARACTERISTIC_CHOICES = [
        ('inc', 'Increasing'),
        ('dec', 'Decreasing'),
        ('const', 'Constant'),
    ]

    kpi_name_eng = models.CharField(max_length=400)
    kpi_name_amh = models.CharField(max_length=400, blank=True)
    kpi_weight = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    kpi_measurement_units = models.CharField(max_length=50, null=True)
    kpi_characteristics = models.CharField(
        max_length=10,
        choices=KPI_CHARACTERISTIC_CHOICES,
        default='inc',
    )

class Indicator(models.Model):
    KPI_CHARACTERISTIC_CHOICES = [
        ('inc', 'Increasing'),
        ('dec', 'Decreasing'),
        ('const', 'Constant'),
    ]

    kpi_name_eng = models.CharField(max_length=400)
    kpi_code = models.CharField(max_length=400, blank=True, null=True)
    kpi_name_amh = models.CharField(max_length=400, blank=True)
    kpi_weight = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    kpi_measurement_units = models.CharField(max_length=50, null=True,blank=True)
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
        "userManagement.ResponsibleMinistry", on_delete=models.SET_NULL, null=True,blank=True, related_name="ministry_kpi")
    keyResultArea = models.ForeignKey(
        KeyResultArea, on_delete=models.SET_NULL, related_name="indicators", null=True, blank=True)
    # kpi = models.ForeignKey("Indicator", on_delete=models.SET_NULL, null=True)
    goal = models.ForeignKey(StrategicGoal, related_name="kra_goal_dashboard", verbose_name=(
        "goal dasboard"), on_delete=models.SET_NULL, null=True,blank=True)
    kpi_is_visable = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.kpi_name_eng

    class Meta:
        verbose_name = "Key Performance Indicator"
        indexes = [
            models.Index(fields=['kpi_name_eng', 'kpi_measurement_units']),
        ]
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


class IndicatorMetaData(models.Model):
    kpi = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    kpi_description_eng = models.TextField()
    kpi_description_amh = models.TextField()
    source = models.CharField(max_length=100)
    base_value = models.FloatField(blank=True, null=True)
    base_year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    calculation_method = models.TextField()
    interpretation = models.TextField()
    units_of_measurement = models.CharField(max_length=50)
    frequency_of_update = models.CharField(max_length=20, choices=[
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("biannual", "Biannual"),
        ("yearly", "Yearly")
    ])
    data_quality_and_validity = models.TextField()
    references = models.URLField(max_length=200)

    def __str__(self):
        return self.kpi_description

    class Meta:
        verbose_name = "Key Performance Indicator Meta Data"


class SharedIndicator(models.Model):

    responsible_ministry = models.ForeignKey(
        "userManagement.ResponsibleMinistry", on_delete=models.CASCADE)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.CASCADE, related_name='shared_indicator')

    kpi_weight = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True)

    def __str__(self):
        return self.responsible_ministry.responsible_ministry_name_eng

class QuarterPlanTemp(models.Model):
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_indicators_temp')

    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    quarter1_target = models.FloatField(blank=True,null=True)
    quarter2_target = models.FloatField(blank=True,null=True)
    quarter3_target = models.FloatField(blank=True,null=True)
    quarter4_target = models.FloatField(blank=True,null=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.kpi_name_eng
        else:
            return "sub-indicator or empty"

class QuarterProgress(models.Model):
    # national_plan = models.ForeignKey(NationalPlan, on_delete=models.CASCADE)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_indicators')

    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_sub_indicators')

    quarter_target = models.FloatField(blank=True,null=True)
    quarter = models.ForeignKey(
        Quarter, on_delete=models.CASCADE, related_name='quarters')
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    quarter_performance = models.FloatField(blank=True, null=True)
    quarter_date = models.DateTimeField(auto_now_add=True, null=True)

    score = models.FloatField(blank=True, null=True,)
    scorecard = ColorField(default='#FF0000',blank=True, null=True)
    def __str__(self):
        if self.indicator:
            return self.indicator.kpi_name_eng+" - "+str(self.year)
        else:
            return self.sub_indicator.sub_kpi_name_eng
    def calculate_score_and_card(self):
        performance = self.quarter_performance
        target = self.quarter_target

        if performance is None or target is None or target == 0:
            return [0, None]

        # Calculate the raw score based on KPI characteristics
        if self.indicator.kpi_characteristics == 'inc':
            score = (float(performance) / float(target)) * 100
        elif self.indicator.kpi_characteristics == 'dec':
            score = (float(target) / float(performance)) * 100
        else:
            score = (float(performance) / float(target)) * 100

        # Ensure score is between 0 and 100
        score = min(max(score, 0), 100)

        # Try to get score card ranges from the cache
        score_card_ranges = cache.get('score_card_ranges')

        if score_card_ranges is None:
            # If not in cache, retrieve from the database and store in cache
            score_card_ranges = list(ScoreCardRange.objects.all())
            cache.set('score_card_ranges', score_card_ranges, 23600)  # Cache for 1 hour

        # Find the corresponding score card range
        card = next((range for range in score_card_ranges if range.starting <= score <= range.ending), None)

        return [round(score), card.color] if card else [round(score), None]


    def save(self, *args, **kwargs):
        if self.indicator is None:
            raise ValueError("Indicator cannot be None")
        if not hasattr(self.indicator, 'kpi_characteristics'):
            raise ValueError("Indicator does not have the attribute 'kpi_characteristics'")

        self.score, self.scorecard = self.calculate_score_and_card()
        super().save(*args, **kwargs)

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

    score = models.FloatField(blank=True, null=True,)
    scorecard = ColorField(default='#FF0000',blank=True, null=True)

    def __str__(self):
        return str(self.year)
    @property
    def get_previous_year_performance(self):
        # Calculate and return the change in performance compared to the previous year
        previous_year = self.year.year_amh - 1
        try:
            previous_year_plan = AnnualPlan.objects.get(
                year__year_amh=previous_year,
                national_plan=self.national_plan,
                indicator=self.indicator,
                sub_indicator=self.sub_indicator,
            )
            if previous_year_plan.annual_performance is not None and self.annual_performance is not None:
                performance_change = self.annual_performance - \
                    previous_year_plan.annual_performance


                performance_change_percent = (
                    (self.annual_performance - previous_year_plan.annual_performance)/previous_year_plan.annual_performance) * 100

                if self.indicator.kpi_characteristics == 'inc':
                    # For increasing KPIs, positive change is good, and negative change is bad
                    return [performance_change, performance_change_percent]
                elif self.indicator.kpi_characteristics == 'dec':
                    # For decreasing KPIs, negative change is good, and positive change is bad
                    return [-performance_change, -performance_change_percent]
                else:
                    # For constant KPIs, return the change without modifying its sign
                    return [performance_change, performance_change_percent]
            else:
                return None
        except AnnualPlan.DoesNotExist:
            return None


    
    def calculate_score_and_card(self):
        performance = self.annual_performance
        target = self.annual_target

        if performance is None or target is None or target == 0:
            return [0, None]

        # Calculate the raw score based on KPI characteristics
        if self.indicator and  self.indicator.kpi_characteristics == 'inc':
            score = (float(performance) / float(target)) * 100
        elif self.indicator and self.indicator.kpi_characteristics == 'dec':
            score = (float(target) / float(performance)) * 100
        else:
            score = (float(performance) / float(target)) * 100

        # Ensure score is between 0 and 100
        score = min(max(score, 0), 100)

        # Try to get score card ranges from the cache
        score_card_ranges = cache.get('score_card_ranges')

        if score_card_ranges is None:
            # If not in cache, retrieve from the database and store in cache
            score_card_ranges = list(ScoreCardRange.objects.all())
            cache.set('score_card_ranges', score_card_ranges, 23600)  # Cache for 1 hour

        # Find the corresponding score card range
        card = next((range for range in score_card_ranges if range.starting <= score <= range.ending), None)

        return [round(score), card.color] if card else [round(score), None]

    def save(self, *args, **kwargs):
        self.score, self.scorecard = self.calculate_score_and_card()
        super().save(*args, **kwargs)

class MonthProgress(models.Model):
    national_plan = models.ForeignKey(NationalPlan, on_delete=models.CASCADE)
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='month_indicators')

    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='month_sub_indicators')

    month_target = models.FloatField(blank=True)
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

class AnnualQuarter(models.Model):
    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='annual_quarter_indicators_tempo')
    performance_2015 =models.FloatField(blank=True, null=True)
    target_2016 =models.FloatField(blank=True, null=True)
    target_2017 = models.FloatField(blank=True, null=True)
    target_2018  = models.FloatField(blank=True, null=True)
    # plan_9month_2016 =models.FloatField(blank=True, null=True)
    # performance_9month_2016 =models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.indicator}-'

class AnnualPlan2(models.Model):

    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='annual_indicators_tempo')

    kpi_name_eng = models.CharField(max_length=400, null=True)
    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='annual_sub_indicator_tempo')
    sub_kpi_name_eng = models.CharField(max_length=400, blank=True, null=True)
    target_state = models.CharField(max_length=20, choices=[
        ("cum", "Cumulative"),
        ("net", "Net"),

    ])

    plan_year_2012 = models.FloatField(
        blank=True, null=True)
    performance_year_2012 = models.FloatField(
        blank=True, null=True)
    plan_year_2013 = models.FloatField(
        blank=True, null=True)
    performance_year_2013 = models.FloatField(
        blank=True, null=True)
    plan_year_2014 = models.FloatField(
        blank=True, null=True)
    performance_year_2014 = models.FloatField(
        blank=True, null=True)
    plan_year_2015 = models.FloatField(
        blank=True, null=True)
    performance_year_2015 = models.FloatField(
        blank=True, null=True)
    plan_year_2016 = models.FloatField(
        blank=True, null=True)
    plan_year_2017 = models.FloatField(
        blank=True, null=True)

    plan_year_2018 = models.FloatField(
        blank=True, null=True)

    def __str__(self):
        return self.kpi_name_eng

class QuarterProgress2(models.Model):

    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_indicators_tempo')

    kpi_name_eng = models.CharField(max_length=400, null=True)
    sub_indicator = models.ForeignKey(
        KpiAggregation, on_delete=models.SET_NULL, blank=True, null=True, related_name='quarter_sub_indicator_tempo')
    sub_kpi_name_eng = models.CharField(max_length=400, blank=True, null=True)
    target_state = models.CharField(max_length=20, choices=[
        ("cum", "Cumulative"),
        ("net", "Net"),

    ])
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    plan_quarter1 = models.FloatField(
        blank=True, null=True)
    
    performance_quarter1 = models.FloatField(
        blank=True, null=True)

    plan_quarter2 = models.FloatField(
        blank=True, null=True)
    
    plan_quarter3 = models.FloatField(
        blank=True, null=True)
    
    plan_quarter4 = models.FloatField(
        blank=True, null=True)
    
    def __str__(self):
        return self.kpi_name_eng
      
class Post(models.Model):
    user = models.ForeignKey(
        "userManagement.Account", on_delete=models.SET_NULL, null=True, blank=True)

    indicator = models.ForeignKey(
        Indicator, on_delete=models.SET_NULL, blank=True, null=True, related_name='comment_indicators')
    body = models.TextField(null=True)
    # the field name should be comments


    def __str__(self) -> str:
        return str(self.id)

    def get_absolute_url(self):
        return reverse('indicator_detail', kwargs={'id': self.id})

class DashboardCategory(models.Model):
    name_eng = models.CharField(max_length=200)
    name_amh = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name_eng

class DashboardSetting(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    year = models.ForeignKey(Year , on_delete=models.CASCADE)
    performance = models.BooleanField( blank=True,null=True,default=False)
    target = models.BooleanField( blank=True,null=True, default=False)
    indicator = models.ManyToManyField(Indicator)
    month = models.ForeignKey(Month, on_delete=models.CASCADE , blank=True,null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, blank=True,null=True)
    rank = models.IntegerField(null=True, blank=True)
    is_score_card = models.BooleanField( blank=True,null=True, default=False)
    
    def __str__(self):
        return self.name

    
    class Meta:
      ordering = ['rank']
