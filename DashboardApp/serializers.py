from rest_framework import serializers
from userManagement.models import ResponsibleMinistry 
from .models import StrategicGoal , KeyResultArea , Indicator

class MinistrySerializers(serializers.ModelSerializer):
    goal_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = ResponsibleMinistry
        fields =  '__all__'


class GoalSerializers(serializers.ModelSerializer):
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        


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

