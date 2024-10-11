from import_export import fields, resources

from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal, KeyResultArea, Year, PolicyArea ,Quarter,AnnualPlan, NationalPlan, Indicator
from import_export.widgets import ForeignKeyWidget

from .models import SDG, AgendaGoals



class SDGResource(resources.ModelResource):
    class Meta:
        model = SDG

class AgendaGoalsResource(resources.ModelResource):
    class Meta:
        model = AgendaGoals



class GoalResource(resources.ModelResource):
    national_plan = fields.Field(
        column_name='national_plan',
        attribute='national_plan',
        widget=ForeignKeyWidget(NationalPlan, field='np_name_eng'))
    policy_area = fields.Field(
        column_name='policy_area',
        attribute='policy_area',
        widget=ForeignKeyWidget(PolicyArea, field='policyAreaEng'))
    responsible_ministries = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='responsible_ministry_eng'))
    class Meta:
        model = StrategicGoal


class KeyResultAreaResource(resources.ModelResource):
    goal = fields.Field(
        column_name='goal',
        attribute='goal',
        widget=ForeignKeyWidget(StrategicGoal, field='goal_name_eng'))
    class Meta:
        model = KeyResultArea


class IndicatorResource(resources.ModelResource):
    responsible_ministries = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='responsible_ministry_eng'))
    keyResultArea = fields.Field(
        column_name='keyResultArea',
        attribute='keyResultArea',
        widget=ForeignKeyWidget(KeyResultArea, field='activity_name_eng'))
    goal = fields.Field(
        column_name='goal',
        attribute='goal',
        widget=ForeignKeyWidget(StrategicGoal, field='goal_name_eng'))
    class Meta:
        model = Indicator




class QuarterResource(resources.ModelResource):
    class Meta:
        model = Quarter


class NationalPlanResource(resources.ModelResource):
    class Meta:
        model = NationalPlan


class PolicyAreaResource(resources.ModelResource):
    class Meta:
        model = PolicyArea




class YearResource(resources.ModelResource):
    class Meta:
        model = Year


class AnnualPlanResource(resources.ModelResource):
    # year = fields.Field(
    #     column_name='year',
    #     attribute='year',
    #     widget=ForeignKeyWidget(Year, field='year_amh'))
    # national_plan = fields.Field(
    #     column_name='national_plan',
    #     attribute='national_plan',
    #     widget=ForeignKeyWidget(NationalPlan, field='np_name_eng'))
    # indicator = fields.Field(
    #     column_name='indicator',
    #     attribute='indicator',
    #     widget=ForeignKeyWidget(Indicator, field='kpi_name_eng'))
    class Meta:
        model = AnnualPlan