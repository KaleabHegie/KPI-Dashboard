from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resource import *


admin.site.register(Month)
admin.site.register(DashboardCategory)
admin.site.register(Category)
admin.site.register(KpiAggregation)
admin.site.register(ScoreCardRange)
admin.site.register(SDG)
admin.site.register(AgendaGoals)

class KeyResultAreaAdmin(ImportExportModelAdmin):
    resource_classes = [KeyResultAreaResource]
    search_fields = (
        "activity_name_eng", "id",)
    list_display = ('activity_name_eng', 'activity_name_amh',
                    'activity_weight', 'activity_is_shared', 'goal')
    list_filter = ('goal',)
    

admin.site.register(KeyResultArea,KeyResultAreaAdmin)
   

class IndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [IndicatorResource]
    list_display = ('id', 'kpi_name_eng', 'kpi_weight', 'kpi_measurement_units',
                    'kpi_characteristics', 'responsible_ministries', 'keyResultArea')
    search_fields = (
        "kpi_name_eng",)

admin.site.register(Indicator,IndicatorAdmin)


class GoalAdmin(ImportExportModelAdmin):
    list_display = ('goal_name_eng', 'goal_name_amh',
                    'goal_weight', 'goal_is_shared', 'national_plan')
    list_filter = ('responsible_ministries',)
    search_fields = ['goal_name_eng']
    resource_classes = [GoalResource]
    
admin.site.register(StrategicGoal,GoalAdmin)

class AnnualAdmin(ImportExportModelAdmin):
    autocomplete_fields = ["indicator"]
    search_fields = ['indicator__kpi_name_eng']
    resource_classes = [AnnualPlanResource]

admin.site.register(AnnualPlan,AnnualAdmin)


class QuarterProgressAdmin(ImportExportModelAdmin):
    autocomplete_fields = ["indicator"]
    search_fields = ['indicator__kpi_name_eng']

admin.site.register(QuarterProgress,QuarterProgressAdmin)


class MonthProgressAdmin(ImportExportModelAdmin):
    autocomplete_fields = ["indicator"]
    search_fields = ['indicator__kpi_name_eng']

admin.site.register(MonthProgress,MonthProgressAdmin)


class DashboardSettingAdmin(ImportExportModelAdmin):
    filter_horizontal = ('indicator', )

admin.site.register(DashboardSetting,DashboardSettingAdmin)


class YearAdmin(ImportExportModelAdmin):
    resource_classes = [YearResource]

admin.site.register(Year,YearAdmin)



class QuarterAdmin(ImportExportModelAdmin):
    resource_classes = [QuarterResource]

admin.site.register(Quarter,QuarterAdmin)



class NationalPlanAdmin(ImportExportModelAdmin):
    resource_classes = [NationalPlanResource]

admin.site.register(NationalPlan,NationalPlanAdmin)


class PolicyAreaAdmin(ImportExportModelAdmin):
    resource_classes = [PolicyAreaResource]
    search_fields = ['policyAreaEng']

admin.site.register(PolicyArea,PolicyAreaAdmin)


