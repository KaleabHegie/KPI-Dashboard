from import_export import fields, resources

from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal, KeyResultArea, Year, AnnualPlan, NationalPlan, Indicator
from import_export.widgets import ForeignKeyWidget

class GoalResource(resources.ModelResource):
    responsible_ministries = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='responsible_ministry_eng'))
    class Meta:
        model = StrategicGoal



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