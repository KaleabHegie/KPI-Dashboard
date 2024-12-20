from rest_framework import serializers
from userManagement.models import ResponsibleMinistry 
from resultsFramework.models import StrategicGoal , KeyResultArea , Indicator, PolicyArea ,QuarterProgress ,AnnualPlan , Year , Quarter
from django.db.models import Count , F


class ResponsibleMinistrySerializer(serializers.ModelSerializer):
    count_goals = serializers.IntegerField(read_only=True)

    class Meta:
        model = ResponsibleMinistry
        fields = '__all__'        

class AnnualSerializer(serializers.ModelSerializer):
    year = serializers.SlugRelatedField(read_only=True, slug_field='year_amh')
    previous_year_performance_data = serializers.SerializerMethodField()
    class Meta:
        model = AnnualPlan
        fields = '__all__'
    
    def get_previous_year_performance_data(self, obj):
        return obj.get_previous_year_performance

class QuarterDataSerializer(serializers.ModelSerializer):
    year = serializers.SlugRelatedField(read_only=True, slug_field='year_amh')
    quarter = serializers.SlugRelatedField(read_only=True, slug_field='quarter_eng')
    previous_year_performance_data = serializers.SerializerMethodField()
    class Meta:
        model = QuarterProgress
        fields = '__all__'
    
    def get_previous_year_performance_data(self, obj):
        return None

class IndicatorSerializer(serializers.ModelSerializer):
    annual = serializers.SerializerMethodField()
    annual_indicators = serializers.SerializerMethodField()
    keyResultArea = serializers.SlugRelatedField(slug_field='activity_name_eng', read_only=True)
    responsible_ministries = ResponsibleMinistrySerializer()
    class Meta:
        model = Indicator
        fields = '__all__'

    def get_annual(self,obj):
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')

        if quarter and year:
            quarters = QuarterProgress.objects.filter(indicator=obj, year__year_amh=year, quarter__quarter_eng = quarter)
            serializer = QuarterDataSerializer(quarters, many=True)
        else:
            annual =  AnnualPlan.objects.filter(indicator=obj, year__year_amh=year)
            serializer = AnnualSerializer(annual, many=True)
        return serializer.data
    
    def get_annual_indicators(self,obj):
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')

        if quarter and year:
            indicators = obj.quarter_indicators
            serializer = QuarterDataSerializer(indicators,many=True, read_only=True)
        else:
            indicators = obj.annual_indicators
            serializer = AnnualSerializer(indicators,many=True, read_only=True)
        
        return serializer.data
    

class KeyResultAreaWithIndictorSerializer(serializers.ModelSerializer):
    ministry_key_result_area_score_card = serializers.SerializerMethodField()
    indicators =  serializers.SerializerMethodField()

    class Meta:
        model = KeyResultArea
        fields =  '__all__' 
    def get_indicators(self, obj):
        ministry_id = self.context.get('ministry_id')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id , keyResultArea=obj).distinct()
        serializer = IndicatorSerializer(indicators, many=True , context=self.context)
        return serializer.data  
    def get_ministry_key_result_area_score_card(self, obj):
        request = self.context.get('request')
        ministry_id = self.context.get('ministry_id')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        indicators_id = Indicator.objects.filter(responsible_ministries__id=ministry_id, keyResultArea=obj).values_list('id', flat=True).distinct()
        return obj.ministry_key_result_area_score_card(quarter=quarter, year=year , indicators_id=indicators_id)

class GoalWithKraSerializers(serializers.ModelSerializer):
    kra_goal =  serializers.SerializerMethodField()

    class Meta:
        model = StrategicGoal
        fields =  '__all__' 
    def get_kra_goal(self, obj):
        # Filter the related StrategicGoal objects based on a condition
        request = self.context.get('request')
        ministry_id = self.context.get('ministry_id')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)
        kras = KeyResultArea.objects.filter(indicators__in=indicators , goal=obj).distinct()
        serializer = KeyResultAreaWithIndictorSerializer(kras, many=True , context=self.context)
        return serializer.data   
    
class GoalSerializers(serializers.ModelSerializer):
    ministry_strategic_goal_score_card = serializers.SerializerMethodField()
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        

    def get_ministry_strategic_goal_score_card(self, obj):
        m_id = self.context.get('m_id')
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        indicator_id = Indicator.objects.filter(responsible_ministries__id=m_id).values_list('id', flat=True).distinct()
        kras_ids = KeyResultArea.objects.filter(indicators__id__in=indicator_id , goal=obj).values_list('id', flat=True).distinct()
        return obj.ministry_strategic_goal_score_card(quarter=quarter, year=year , kras_ids=kras_ids , indicator_id=indicator_id)  

class PolicyAreaWithGoalSerializer(serializers.ModelSerializer):
    policy_area_goal = serializers.SerializerMethodField()
   
    class Meta:
        model = PolicyArea
        fields = '__all__'

    def get_policy_area_goal(self, obj):
        # Filter the related StrategicGoal objects based on a condition
        m_id = self.context.get('m_id')
        indicators = Indicator.objects.filter(responsible_ministries__id=m_id)
        kras = KeyResultArea.objects.filter(indicators__in=indicators).distinct()
        goals = StrategicGoal.objects.filter(kra_goal__in=kras , policy_area = obj).distinct()
        serializer = GoalSerializers(goals, many=True , context=self.context)
        return serializer.data    

class PolicyAreaSerializer(serializers.ModelSerializer):
    count_goal = serializers.IntegerField(read_only=True)
    ministry_policy_area_score_card = serializers.SerializerMethodField()
    count_has_performance = serializers.SerializerMethodField()
    count_has_no_performance = serializers.SerializerMethodField()
    count_has_no_target = serializers.SerializerMethodField()
    low_performance = serializers.SerializerMethodField()
    average_performance = serializers.SerializerMethodField()
    high_performance = serializers.SerializerMethodField()
    class Meta:
        model = PolicyArea
        fields = '__all__'
    
    def get_ministry_policy_area_score_card(self, obj):
        
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        ministry_id = self.context.get('ministry_id')
        indicator_id = Indicator.objects.filter(responsible_ministries__id=ministry_id).values_list('id', flat=True).distinct()
        kra_id = KeyResultArea.objects.filter(indicators__id__in=indicator_id).distinct().values_list('id', flat=True).distinct()
        goal_ids = StrategicGoal.objects.filter(kra_goal__id__in=kra_id , policy_area = obj).values_list('id', flat=True).distinct()
        return obj.ministry_policy_area_score_card(quarter=quarter, year=year , goal_ids=goal_ids , kra_id=kra_id , indicator_id=indicator_id)
    def get_count_has_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        if quarter and year:
            performance = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year, quarter__quarter_eng=quarter, quarter_target__isnull=False , quarter_performance__isnull=False ).count()
        else:
            performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False , annual_performance__isnull=False ).count()
        return performance    
    def get_count_has_no_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        if quarter and year:
            no_performance = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year, quarter__quarter_eng=quarter, quarter_target__isnull=False ,quarter_performance__isnull=True).count()
        else:
            no_performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False ,annual_performance__isnull=True).count()
        return  no_performance
    def get_count_has_no_target(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)
        
        if year and quarter:
            indicators_with_quarter = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year, quarter__quarter_eng=quarter)
            count_without_quarter_indicator = indicators.count() - indicators_with_quarter.count()
            no_target = QuarterProgress.objects.filter(indicator__in=indicators, year__year_amh=year, quarter__quarter_eng=quarter, quarter_target__isnull=True ).count()
            return no_target + count_without_quarter_indicator
        else:
            indicators_with_annual = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year)
            count_without_annual_indicator = indicators.count() - indicators_with_annual.count()
            no_target = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=True ).count()
            return no_target + count_without_annual_indicator           
    def get_average_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')

        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        if year and quarter:
            average_performance = QuarterProgress.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year, 
                quarter__quarter_eng=quarter ,
                quarter_target__isnull=False ,
                quarter_performance__gte = 0.5* F('quarter_target') ,  
                quarter_performance__lt = 0.7* F('quarter_target')).count()
        else:
            average_performance = AnnualPlan.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year, 
                annual_target__isnull=False ,
                annual_performance__gte = 0.5* F('annual_target') ,   
                annual_performance__lt = 0.7* F('annual_target')).count()
            
        return average_performance    
    def get_low_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        if year and quarter:
            low_performance = QuarterProgress.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year,
                quarter__quarter_eng=quarter ,  
                quarter_target__isnull=False , 
                quarter_performance__lt = 0.5* F('quarter_target')).count()
        else:
            low_performance = AnnualPlan.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year,  
                annual_target__isnull=False , 
                annual_performance__lt = 0.5* F('annual_target')).count()
        return low_performance    
    def get_high_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        if year and quarter:
            high_performance = QuarterProgress.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year, 
                quarter__quarter_eng=quarter ,  
                quarter_target__isnull=False, 
                quarter_performance__gte = 0.5* F('quarter_target')).count()
        else:
            high_performance = AnnualPlan.objects.filter(
                indicator__in=indicators, 
                year__year_amh=year, 
                annual_target__isnull=False, 
                annual_performance__gte = 0.5* F('annual_target')).count()
        return high_performance         

class MinistrySerializer(serializers.ModelSerializer):
    count_indicator = serializers.SerializerMethodField()
    ministry_score_card = serializers.SerializerMethodField()
    class Meta:
        model = ResponsibleMinistry
        fields = '__all__'

    def get_ministry_score_card(self , obj):
        request = self.context.get('request')
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        indicator_id = Indicator.objects.filter(responsible_ministries__id=obj.id).values_list('id', flat=True).distinct()
        return obj.ministry_score_card(quarter=quarter, year=year , indicator_id=indicator_id )    
    def get_count_indicator(self , obj):
        return obj.ministry_kpi.all().count()  
class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = '__all__'



class MinistryIndicatorPerformanceSerializer(serializers.ModelSerializer):
    average_performance = serializers.SerializerMethodField()
    low_performance = serializers.SerializerMethodField()
    high_performance = serializers.SerializerMethodField()

    class Meta:
        model = ResponsibleMinistry
        fields = '__all__'
    def get_average_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        average_performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False ,annual_performance__gte = 0.64* F('annual_target') ,   annual_performance__lt = 0.85* F('annual_target'))
        average_performance_serializer = AnnualSerializer(average_performance, many=True)
        return average_performance_serializer.data
    def get_low_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        low_performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year,  annual_target__isnull=False , annual_performance__lt = 0.65* F('annual_target'))
        low_performance_serializer = AnnualSerializer(low_performance, many=True)
        return low_performance_serializer.data
    def get_high_performance(self, obj):
        ministry_id = self.context.get('ministry_id')
        request = self.context.get('request')
        year = request.query_params.get('year')
        quarter = request.query_params.get('quarter')
        indicators = Indicator.objects.filter(responsible_ministries__id=ministry_id)

        high_performance = AnnualPlan.objects.filter(indicator__in=indicators, year__year_amh=year, annual_target__isnull=False, annual_performance__gte = 0.84* F('annual_target'))
        high_performance_serializer = AnnualSerializer(high_performance, many=True)
        return high_performance_serializer.data
