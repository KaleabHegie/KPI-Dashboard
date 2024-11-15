from rest_framework import serializers
from userManagement.models import ResponsibleMinistry 
from .models import StrategicGoal , KeyResultArea , Indicator,PolicyArea
from django.conf import settings
from django.core.cache import cache
# Create your models here.
CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 3600)
class MinistrySerializers(serializers.ModelSerializer):
    goal_count = serializers.IntegerField(read_only=True)

    score_card = serializers.SerializerMethodField()
    sum_score = serializers.SerializerMethodField()
    scorecard_color = serializers.SerializerMethodField()
    class Meta:
        model = ResponsibleMinistry
        fields =  '__all__'
    def get_score_card(self, obj):
        quarter = self.context.get('quarter')
        year = self.context.get('year')
        
        # Utilize a cached method to get score card details
        # cache_key = f'policy_area_{obj.id}_score_card_{year}_{quarter}'
        # score_card = cache.get(cache_key)
        score_card = None
        if score_card is None:
            score_card = obj.responsible_ministry_score_card(quarter=quarter, year=year)
            # cache.set(cache_key, score_card, CACHE_TIMEOUT)
        
        return score_card

    def get_sum_score(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('sum_score') if score_card else 0

    def get_scorecard_color(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('scorecard_color') if score_card else "#4680ff"


class PolicyAreaSerializers(serializers.ModelSerializer):
    goal_count = serializers.IntegerField(read_only=True)
    score_card = serializers.SerializerMethodField()
    sum_score = serializers.SerializerMethodField()
    scorecard_color = serializers.SerializerMethodField()

    class Meta:
        model = PolicyArea
        fields = '__all__'

    def get_score_card(self, obj):
        quarter = self.context.get('quarter')
        year = self.context.get('year')
        
        # Utilize a cached method to get score card details
        # cache_key = f'policy_area_{obj.id}_score_card_{year}_{quarter}'
        # score_card = cache.get(cache_key)
        score_card = None
        if score_card is None:
            score_card = obj.policy_area_score_card(quarter=quarter, year=year)
            # cache.set(cache_key, score_card, CACHE_TIMEOUT)
        
        return score_card

    def get_sum_score(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('sum_score') if score_card else 0

    def get_scorecard_color(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('scorecard_color') if score_card else "#4680ff"



class GoalSerializers(serializers.ModelSerializer):
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        


class ResponsibleMinistrySerializer4(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleMinistry
        fields = ['code', 'image']



from django.db.models import Prefetch
from rest_framework import serializers

class KeyResultAreaSerializer1(serializers.ModelSerializer):
    responsible_ministries = serializers.SerializerMethodField()
    sum_score = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    scorecard_color = serializers.SerializerMethodField()

    class Meta:
        model = KeyResultArea
        fields = ['id', 'activity_name_eng', 'responsible_ministries', 'sum_score', 'avg_score', 'scorecard_color']

    def get_responsible_ministries(self, obj):
        # Prefetch related ministries to minimize database hits
        indicators = Indicator.objects.filter(keyResultArea=obj)
        ministries = ResponsibleMinistry.objects.filter(id__in=indicators.values_list('responsible_ministries', flat=True).distinct())
        return ResponsibleMinistrySerializer4(ministries, many=True).data

    def get_score_card(self, obj):
        quarter = self.context.get('quarter', None)
        year = self.context.get('year', None)
        if year:
            # Utilize a cached method to get score card details
            cache_key = f'kra_{obj.id}_score_card_{year}_{quarter}'
            score_card = cache.get(cache_key)
            if score_card is None:
                score_card = obj.key_result_area_score_card(quarter=quarter, year=year)
                cache.set(cache_key, score_card, CACHE_TIMEOUT)
            return score_card
        return None

    def get_sum_score(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('sum_score') if score_card else None

    def get_avg_score(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('avg_score') if score_card else None

    def get_scorecard_color(self, obj):
        score_card = self.get_score_card(obj)
        return score_card.get('scorecard_color') if score_card else None





class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['id', 'kpi_name_eng', 'kpi_weight', 'kpi_measurement_units', 'kpi_characteristics']

class KeyResultAreaSerializer2(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = KeyResultArea
        fields = ['id', 'activity_name_eng', 'indicators']


class KeyResultAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResultArea
        fields = [ 'id' , 'activity_name_eng' ]

class StrategicGoalSerializer(serializers.ModelSerializer):
    kra_goals = KeyResultAreaSerializer(source='kra_goal', many=True, read_only=True)

    class Meta:
        model = StrategicGoal
        fields = ['id', 'goal_name_eng', 'goal_weight', 'kra_goals']

class ResponsibleMinistrySerializer(serializers.ModelSerializer):
    ministry_goal = StrategicGoalSerializer(many=True, read_only=True)

    class Meta:
        model = ResponsibleMinistry
        fields = ['responsible_ministry_eng', 'ministry_goal']



###################
class GoalSerializers(serializers.ModelSerializer):
    class Meta:
        model = StrategicGoal
        fields =  '__all__'    
