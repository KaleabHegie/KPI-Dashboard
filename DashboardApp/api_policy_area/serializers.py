from rest_framework import serializers
from userManagement.models import ResponsibleMinistry 
from DashboardApp.models import *
from django.db.models import Count
from django.db.models import Q, F
from django.db.models.functions import Coalesce


class ResponsibleMinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleMinistry
        fields ='__all__'

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('year_amh',)

class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = ('quarter_eng',)

class AnnualSerializer(serializers.ModelSerializer):
    year = serializers.SlugRelatedField(read_only=True, slug_field='year_amh')
    class Meta:
        model = AnnualPlan
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    annual = serializers.SerializerMethodField()
    annual_indicators = AnnualSerializer(many=True, read_only=True)
    keyResultArea = serializers.SlugRelatedField(slug_field='activity_name_eng', read_only=True)
    responsible_ministries = ResponsibleMinistrySerializer()
    class Meta:
        model = Indicator
        fields = '__all__'

    def get_annual(self,obj):
        request = self.context.get('request')
        year = request.query_params.get('year')
        annual =  AnnualPlan.objects.filter(indicator=obj, year__year_amh=year)
        serializer = AnnualSerializer(annual, many=True)
        return serializer.data
    

class SearchIndicatorSerializer(serializers.ModelSerializer):
    responsible_ministries = serializers.SlugRelatedField(slug_field='responsible_ministry_eng', read_only=True)
    annual_indicators = AnnualSerializer(many=True, read_only=True)
    class Meta:
        model = Indicator
        fields = '__all__'


class AgendaSerializer(serializers.ModelSerializer):
    num_of_sdg = serializers.SerializerMethodField()
    class Meta:
        model = AgendaGoals
        fields = '__all__'

    def get_num_of_sdg(self, obj):
        return obj.sdg.all().count()


class PolicyAreaSDGSerializer(serializers.ModelSerializer):
    num_of_goals = serializers.SerializerMethodField()    
    class Meta:
        model = PolicyArea
        fields = '__all__'
    
    def get_num_of_goals(self, obj):
        return obj.policy_area_goal.all().count()
    

class SDGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDG
        fields = '__all__'

    

    
   

class PolicyAreaSerializer(serializers.ModelSerializer):
    count_goal = serializers.IntegerField(read_only=True)
    policy_area_score_card = serializers.SerializerMethodField()
    class Meta:
        model = PolicyArea
        fields = '__all__'
    
    def get_policy_area_score_card(self, obj):
        
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        # Call the policy_area_score_card method from the model
        return obj.policy_area_score_card(quarter=quarter, year=year)

class KeyResultAreaSerializer(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)
    kra_score_card = serializers.SerializerMethodField()

    class Meta:
        model = KeyResultArea
        fields = '__all__'
    
    def get_kra_score_card(self, obj):
        
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        # Call the policy_area_score_card method from the model
        return obj.key_result_area_score_card(quarter=quarter, year=year)
    

class SearchKeyResultAreaSerializer(serializers.ModelSerializer):
    goal = serializers.SlugRelatedField(slug_field='goal_name_eng', read_only=True)
    indicators = SearchIndicatorSerializer(many=True, read_only=True)
    class Meta:
        model = KeyResultArea
        fields = '__all__'
    


class GoalWithKraSerializers(serializers.ModelSerializer):
    kra_goal = KeyResultAreaSerializer(many=True, read_only=True)
    good_performance = serializers.SerializerMethodField()
    average_performance = serializers.SerializerMethodField()
    poor_performance = serializers.SerializerMethodField()
    no_performance = serializers.SerializerMethodField()
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        

    def get_good_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')


        if quarter and year:
            total_target = obj.kra_goal.filter(
                            Q(indicators__quarter_indicators__quarter_target__isnull=False),
                            Q(indicators__quarter_indicators__year__year_amh=year),
                            Q(indicators__quarter_indicators__quarter__quarter_eng=quarter)
                            ).aggregate(total = Count('indicators__quarter_indicators'))['total']
             
            performance = obj.kra_goal.filter(
                            indicators__quarter_indicators__quarter_target__isnull=False,
                            indicators__quarter_indicators__year__year_amh=year,
                            indicators__quarter_indicators__quarter__quarter_eng=quarter,
                            indicators__quarter_indicators__quarter_performance__gte=0.7 * F('indicators__quarter_indicators__quarter_target')
                            ).aggregate(
                            good_performance=Count('indicators__quarter_indicators')
                            )['good_performance']
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }


        else:
            total_target = obj.kra_goal.filter(
                            Q(indicators__annual_indicators__annual_target__isnull=False),
                            Q(indicators__annual_indicators__year__year_amh=year),
                            ).aggregate(total = Count('indicators__annual_indicators'))['total']
             
            performance = obj.kra_goal.filter(
                            indicators__annual_indicators__annual_target__isnull=False,
                            indicators__annual_indicators__year__year_amh=year,
                            indicators__annual_indicators__annual_performance__gte=0.7 * F('indicators__annual_indicators__annual_target')
                            ).aggregate(
                            good_performance=Count('indicators__annual_indicators')
                            )['good_performance']
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }

    def get_average_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')


        if quarter and year:
            total_target = obj.kra_goal.filter(
                            Q(indicators__quarter_indicators__quarter_target__isnull=False),
                            Q(indicators__quarter_indicators__year__year_amh=year),
                            Q(indicators__quarter_indicators__quarter__quarter_eng=quarter)
                            ).aggregate(total = Count('indicators__quarter_indicators'))['total']
            
            performance =  obj.kra_goal.filter(
                    indicators__quarter_indicators__quarter_target__isnull=False,
                    indicators__quarter_indicators__year__year_amh=year,
                    indicators__quarter_indicators__quarter__quarter_eng=quarter,
                    indicators__quarter_indicators__quarter_performance__gte=0.5 * F('indicators__quarter_indicators__quarter_target'),
                    indicators__quarter_indicators__quarter_performance__lt=0.7 * F('indicators__quarter_indicators__quarter_target')
                    ).aggregate(
                    avg_performance=Count('indicators__quarter_indicators')
                    )['avg_performance']
            
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }
        
    


        else:
            total_target = obj.kra_goal.filter(
                            Q(indicators__annual_indicators__annual_target__isnull=False),
                            Q(indicators__annual_indicators__year__year_amh=year),
                            ).aggregate(total = Count('indicators__annual_indicators'))['total']

            performance = obj.kra_goal.filter(
            indicators__annual_indicators__annual_target__isnull=False,
            indicators__annual_indicators__year__year_amh=year,
            indicators__annual_indicators__annual_performance__gte=0.5 * F('indicators__annual_indicators__annual_target'),
            indicators__annual_indicators__annual_performance__lt=0.7 * F('indicators__annual_indicators__annual_target')
            ).aggregate(
            avg_performance=Count('indicators__annual_indicators')
            )['avg_performance']

            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }

    def get_poor_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')


        if quarter and year:
            total_target = obj.kra_goal.filter(
                            Q(indicators__quarter_indicators__quarter_target__isnull=False),
                            Q(indicators__quarter_indicators__year__year_amh=year),
                            Q(indicators__quarter_indicators__quarter__quarter_eng=quarter)
                            ).aggregate(total = Count('indicators__quarter_indicators'))['total']



            performance =  obj.kra_goal.filter(
                            Q(indicators__quarter_indicators__quarter_target__isnull=False),
                            Q(indicators__quarter_indicators__year__year_amh=year),
                            Q(indicators__quarter_indicators__quarter__quarter_eng=quarter),
                            Q(indicators__quarter_indicators__quarter_performance__lt=0.5 * F('indicators__quarter_indicators__quarter_target')) | 
                            Q(indicators__quarter_indicators__quarter_performance__isnull=True)
                            ).aggregate(
                            low_performance=Count('indicators__quarter_indicators')
                            )['low_performance']

            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }
         

        else:
            total_target = obj.kra_goal.filter(
                            Q(indicators__annual_indicators__annual_target__isnull=False),
                            Q(indicators__annual_indicators__year__year_amh=year),
                            ).aggregate(total = Count('indicators__annual_indicators'))['total']


            performance = obj.kra_goal.filter(
                        Q(indicators__annual_indicators__annual_target__isnull=False),
                        Q(indicators__annual_indicators__annual_performance__isnull=False),
                        Q(indicators__annual_indicators__year__year_amh=year),
                        Q(indicators__annual_indicators__annual_performance__lt=0.5 * F('indicators__annual_indicators__annual_target')) | 
                        Q(indicators__annual_indicators__annual_performance__isnull=True)
                        ).aggregate(
                            low_performance=Coalesce(Count('indicators__annual_indicators'), 0)
                        )['low_performance']
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }
    
    def get_no_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')


        if quarter and year:
            total_target = obj.kra_goal.filter(
                            Q(indicators__quarter_indicators__quarter_target__isnull=False),
                            Q(indicators__quarter_indicators__year__year_amh=year),
                            Q(indicators__quarter_indicators__quarter__quarter_eng=quarter)
                            ).aggregate(total = Count('indicators__quarter_indicators'))['total']


            performance = obj.kra_goal.filter(
                        Q(indicators__quarter_indicators__quarter_target__isnull=False),
                        Q(indicators__quarter_indicators__year__year_amh=year),
                        Q(indicators__quarter_indicators__quarter__quarter_eng=quarter),
                        Q(indicators__quarter_indicators__quarter_performance__isnull=True)
                        ).aggregate(
                        no_performance=Count('indicators__quarter_indicators')
                        )['no_performance']
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }

        else:
            total_target = obj.kra_goal.filter(
                            Q(indicators__annual_indicators__annual_target__isnull=False),
                            Q(indicators__annual_indicators__year__year_amh=year),
                            ).aggregate(total = Count('indicators__annual_indicators'))['total']


            performance = obj.kra_goal.filter(
                        Q(indicators__annual_indicators__annual_target__isnull=False),
                        Q(indicators__annual_indicators__year__year_amh=year),
                        Q(indicators__annual_indicators__annual_performance__isnull=True)
                        ).aggregate(
                        no_performance=Coalesce(Count('indicators__annual_indicators'), 0)
                        )['no_performance']
            return  {
                'performance': performance,
                'percentage' : (performance/ total_target) * 100 if total_target > 0 else 0
            }
            


class ResponsibleMinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleMinistry
        fields ='__all__'


class GoalSerializers(serializers.ModelSerializer):
    goal_score_card = serializers.SerializerMethodField()
    responsible_ministries = ResponsibleMinistrySerializer()
    
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        

    def get_goal_score_card(self, obj):
        
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        # Call the policy_area_score_card method from the model
        return obj.strategic_goal_score_card(quarter=quarter, year=year)
    

class SearchStrategicGoalSerializer(serializers.ModelSerializer):
    policy_area = serializers.SlugRelatedField(slug_field='policyAreaEng', read_only=True)
    kra_goal = SearchKeyResultAreaSerializer(many=True, read_only=True)
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        




    
class PolicyAreaWithGoalSerializer(serializers.ModelSerializer):
    policy_area_goal = GoalSerializers(many=True, read_only=True)
    policy_area_score_card = serializers.SerializerMethodField()
    count_kra = serializers.SerializerMethodField()
    count_indicator = serializers.SerializerMethodField()
    count_goal = serializers.SerializerMethodField()
    count_indicator_target = serializers.SerializerMethodField()
    count_indicator_have_performance = serializers.SerializerMethodField()
    count_indicator_have_target_and_no_performance = serializers.SerializerMethodField()
    
    
    class Meta:
        model = PolicyArea
        fields = '__all__'

    def get_policy_area_score_card(self, obj):

        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        # Call the policy_area_score_card method from the model
        return obj.policy_area_score_card(quarter=quarter, year=year)
    

    def get_count_goal(self, obj):
        return obj.policy_area_goal.all().count()
    
    def get_count_indicator_target(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        return obj.policy_area_goal.aggregate(count_indicator_target=Count(
                'kra_goal__indicators',
                filter=Q(kra_goal__indicators__annual_indicators__annual_target__isnull=False) & 
                       Q(kra_goal__indicators__annual_indicators__year__year_amh=year)
            )
        )['count_indicator_target']
    
    def get_count_indicator_have_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        return obj.policy_area_goal.aggregate(count_indicator_have_performance=Count(
                'kra_goal__indicators',
                filter=Q(kra_goal__indicators__annual_indicators__annual_target__isnull=False) & 
                       Q(kra_goal__indicators__annual_indicators__annual_performance__isnull=False) &
                       Q(kra_goal__indicators__annual_indicators__year__year_amh=year)
            )
        )['count_indicator_have_performance']
    
    def get_count_indicator_have_target_and_no_performance(self, obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        return obj.policy_area_goal.aggregate(count_indicator_have_target_and_no_performance=Count(
                'kra_goal__indicators',
                filter=Q(kra_goal__indicators__annual_indicators__annual_target__isnull=False) & 
                       Q(kra_goal__indicators__annual_indicators__annual_performance__isnull=True) &
                       Q(kra_goal__indicators__annual_indicators__year__year_amh=year)
            )
        )['count_indicator_have_target_and_no_performance']


    def get_count_kra(self, obj):
        # Count the KRAs related to all the Goals under this PolicyArea
        return obj.policy_area_goal.aggregate(count_goal=Count('kra_goal'))['count_goal']
       
    
   
    def get_count_indicator(self, obj):
        # Count the Indicators related to all the KRAs under the Goals in this PolicyArea
        return obj.policy_area_goal.aggregate(count_indicator=Count('kra_goal__indicators'))['count_indicator']















class KeyResultAreaSerializer2(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = KeyResultArea
        fields = ['id', 'activity_name_eng', 'indicators']

class MinistrySerializers(serializers.ModelSerializer):
    goal_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = ResponsibleMinistry
        fields =  '__all__'


class StrategicGoalSerializer(serializers.ModelSerializer):
    kra_goals = KeyResultAreaSerializer(source='kra_goal', many=True, read_only=True)

    class Meta:
        model = StrategicGoal
        fields = ['id', 'goal_name_eng', 'goal_weight', 'kra_goals']


