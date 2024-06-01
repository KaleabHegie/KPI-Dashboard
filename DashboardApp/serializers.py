from rest_framework import serializers
from userManagement.models import ResponsibleMinistry 
from .models import StrategicGoal

class MinistrySerializers(serializers.ModelSerializer):
    goal_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = ResponsibleMinistry
        fields =  '__all__'


class GoalSerializers(serializers.ModelSerializer):
    class Meta:
        model = StrategicGoal
        fields =  '__all__'        







