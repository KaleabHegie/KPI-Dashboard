from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.html import mark_safe
from django.core.cache import cache
from django.conf import settings
from DashboardApp.models import AnnualPlan , QuarterProgress , Year , Quarter , ScoreCardRange
from django.db.models import Sum, Avg  , Value , F , FloatField , ExpressionWrapper , Case , When , Q
from django.db.models.functions import Coalesce

# Create your models here.
CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 300)


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be specified')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        extra_fields = {
            'is_staff': True,
            'is_superuser': True,
        }
        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    user_image = models.ImageField(
        upload_to='profile_image', blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_sector = models.BooleanField(default=False)
    is_mopd = models.BooleanField(default=False)
    is_hopr = models.BooleanField(default=False)
    is_dpg = models.BooleanField(default=False)
    is_ess = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email


class ResponsibleMinistry(models.Model):
    responsible_ministry_eng = models.CharField(max_length=350)
    responsible_ministry_amh = models.CharField(
        max_length=350, blank=True, null=True)
    code = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ministryImage' , blank=True , null = True)
    visible = models.BooleanField(default=True , blank=True , null = False)
    rank = models.IntegerField(null=True, blank=True )
    

    def __str__(self):
        return f"{self.responsible_ministry_eng}"
    # def ministry_score_card(self, quarter=None, year=None  , kra_id = None,indicator_id= None , goal_ids = None ,policy_area_ids = None):
    #     cache_key = f"ministry_score_card_{self.pk}_{quarter}_{year}"
    #     result = None
    #     if result is None:
    #         policy_area_avg_score = 0
    #         for policy_area in policy_area_ids:
    #             policy_area_score = policy_area.ministry_policy_area_score_card(quarter , year , goal_ids , kra_id ,indicator_id)
    #             policy_area_avg_score = policy_area_avg_score + int(policy_area_score['avg_score'])
    #         if policy_area_ids:
    #             policy_area_avg_score = int(policy_area_avg_score / len(policy_area_ids))
    #         score_card_ranges = list(ScoreCardRange.objects.all())

    #         card = next((range for range in score_card_ranges if range.starting <= policy_area_avg_score <= range.ending), None)
    #         scorecard_color = card.color if card else "#4680ff"

    #         result = {
    #             'avg_score': policy_area_avg_score,
    #             'scorecard_color': scorecard_color,
    #         }

    #     return result 
  
    def ministry_score_card(self, quarter=None, year=None, indicator_id=None):
        cache_key = f"ministry_score_card_{self.pk}_{quarter}_{year}"
        result = None
        if result is None:
            indicators = self.ministry_kpi.filter(id__in=indicator_id).values_list('id', flat=True)

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


class UserSector(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    user_sector = models.ForeignKey(
        ResponsibleMinistry, on_delete=models.CASCADE)
    
