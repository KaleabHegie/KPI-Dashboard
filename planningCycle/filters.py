import django_filters
from .models import *
from userManagement.models import ResponsibleMinistry

class KPIFilterbyMinistry(django_filters.FilterSet):
    responsible_ministries = django_filters.ModelChoiceFilter(queryset=ResponsibleMinistry.objects.all(), label="Responsible Ministry")

    class Meta:
        model = DraftMpttKPI
        fields = ['responsible_ministries']

class KRAFilter(django_filters.FilterSet):
    goal = django_filters.ModelChoiceFilter(queryset=DraftStrategicGoal.objects.all(), label="Goal")

    class Meta:
        model = DraftKeyResultArea
        fields = ['goal']

class GoalFilter(django_filters.FilterSet):
    parent_policy_area = django_filters.ModelChoiceFilter(queryset=Policy_Area.objects.all(), label="Policy Area")

    class Meta:
        model = DraftStrategicGoal
        fields = ['parent_policy_area']