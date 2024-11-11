
from import_export import fields, resources

from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal, KeyResultArea,IndicatorTempo,AnnualQuarter,Indicator,QuarterPlanTemp,Year, SDG, AgendaGoals
from import_export.widgets import ForeignKeyWidget


class SDGResource(resources.ModelResource):
    class Meta:
        model = SDG

class AgendaGoalsResource(resources.ModelResource):
    class Meta:
        model = AgendaGoals




class GoalResource(resources.ModelResource):
    author = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='id'))
    class Meta:
        model = StrategicGoal
        exclude = ('responsible_ministries')







class TempIndicatorResource(resources.ModelResource):
    responsible_ministries = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='id'),
        saves_null_values = True,
        )
    goal_name = fields.Field(
        column_name='goal',
        attribute='goal',
        widget=ForeignKeyWidget(StrategicGoal, field='id'),
        
        )
    class Meta:
          model = IndicatorTempo
          skip_unchanged = True
          report_skipped = True
          fields = ('id','kpi_name_eng', 'kpi_name_amh', 'kpi_weight', 'kpi_measurement_units','kpi_characteristics', 'responsible_ministries', 'goal_name')
          #import_id_fields = ('responsible_ministries', 'goal_name','kpi_name_eng', 'kpi_name_amh', 'kpi_weight', 'kpi_measurement_units','kpi_characteristics')


class AnnualQuarterResource(resources.ModelResource):
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field= 'id'))  # Assuming 'name' is the field you want to display for Indicator

    class Meta:
        model = AnnualQuarter
        skip_unchanged = True
        report_skipped = True
        fields = ('indicator__responsible_ministries','indicator', 'performance_2015', 'target_2016','target_2017','target_2018', 'plan_9month_2016', 'performance_9month_2016',)
        #import_id_fields = ('indicator',)  # Corrected to be a tuple



class QuarterPlanTempFormatResource1(resources.ModelResource):
    indicator_name = fields.Field(attribute='kpi_name_eng', column_name='indicator')
    # indicator_code = fields.Field(attribute='kpi_code', column_name='Indicator Code')
    # Placeholder fields for the QuarterPlanTemp fields
    year = fields.Field(column_name='year')
    quarter1_target = fields.Field(column_name='quarter1_target')
    quarter2_target = fields.Field(column_name='quarter2_target')
    quarter3_target = fields.Field(column_name='quarter3_target')
    quarter4_target = fields.Field(column_name='quarter4_target')

    class Meta:
        model = Indicator
        fields = (
            'indicator_name',
           
            'year',
            'quarter1_target',
            'quarter2_target',
            'quarter3_target',
            'quarter4_target',
        )
        export_order = (
            'indicator_name',
            
         
            'year',
            'quarter1_target',
            'quarter2_target',
            'quarter3_target',
            'quarter4_target',
        )

    def dehydrate_year(self, obj):
        return '2017'

    def dehydrate_quarter1_target(self, obj):
        return ''

    def dehydrate_quarter2_target(self, obj):
        return ''

    def dehydrate_quarter3_target(self, obj):
        return ''

    def dehydrate_quarter4_target(self, obj):
        return ''


class QuarterPlanTempResource(resources.ModelResource):
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field='id')
    )

    year = fields.Field(
        column_name='year',
        attribute='year',
        widget=ForeignKeyWidget(Year, field='id')
    )

    class Meta:
        model = QuarterPlanTemp
        skip_unchanged = True
        report_skipped = True
        
        fields = ('indicator', 'year', 'quarter1_target', 'quarter2_target', 'quarter3_target', 'quarter4_target')
        # Remove 'exclude' to ensure 'id' is included
        #import_id_fields = ('indicator', 'year')  # Ensure this matches the unique fields
