from django.contrib import admin
from .models import Year, Quarter, Month, NationalPlan, StrategicGoal, KeyResultArea, Indicator, DashboardCategory, DashboardSetting, Category, KpiAggregation, QuarterProgress, AnnualPlan, MonthProgress
from import_export.admin import ImportExportModelAdmin
from .resource import GoalResource

admin.site.register(Year)
admin.site.register(Quarter)
admin.site.register(Month)
admin.site.register(NationalPlan)
admin.site.register(DashboardCategory)
admin.site.register(Category)
admin.site.register(KpiAggregation)
admin.site.register(QuarterProgress)

admin.site.register(MonthProgress)

@admin.register(KeyResultArea)
class KeyResultAreaAdmin(ImportExportModelAdmin):
    list_display = ('activity_name_eng', 'activity_name_amh',
                    'activity_weight', 'activity_is_shared', 'goal')
   

@admin.register(Indicator)
class IndicatorAdmin(ImportExportModelAdmin):
    list_display = ('id', 'kpi_name_eng', 'kpi_weight', 'kpi_measurement_units',
                    'kpi_characteristics', 'responsible_ministries', 'keyResultArea')
    search_fields = (
        "kpi_name_eng",)

class GoalAdmin(ImportExportModelAdmin):
    list_display = ('goal_name_eng', 'goal_name_amh',
                    'goal_weight', 'goal_is_shared', 'national_plan')
    list_filter = ('responsible_ministries',)
    
admin.site.register(StrategicGoal,GoalAdmin)

class AnnualAdmin(ImportExportModelAdmin):
    autocomplete_fields = ["indicator"]
    search_fields = ['indicator__kpi_name_eng']

admin.site.register(AnnualPlan,AnnualAdmin)


class DashboardSettingAdmin(ImportExportModelAdmin):
    filter_horizontal = ('indicator', )

admin.site.register(DashboardSetting,DashboardSettingAdmin)


#