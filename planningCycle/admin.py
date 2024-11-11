from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . models import *
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Policy_Area)
class Policy_Data (ImportExportModelAdmin):
    list_display = ('policy_area_eng_name','created_date')

@admin.register(DraftStrategicGoal)
class goaldata(ImportExportModelAdmin):
    list_display= ('goal_name_eng','status','responsible_ministries')
    search_fields = ('goal_name_eng','status','responsible_ministries')

@admin.register(DraftKeyResultArea)
class KRAdata(ImportExportModelAdmin):
    list_display= ('activity_name_eng','responsible_ministries','krastatus','kra_desc')
    
    def kra_desc(self,obj):
        return mark_safe(obj.description)
    kra_desc.allow_tags =True

@admin.register(DraftKPI)
class KPIdata(ImportExportModelAdmin):
    list_display= ('kpi_name_eng','responsible_ministries',)

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('strategicgoal','commenter_name','body','date_added')
@admin.register(KRAComment)
class KRAComment(admin.ModelAdmin):
    list_display = ('strategickra','kra_commenter','body','date_added')
@admin.register(KPIComment)
class KPIComment(admin.ModelAdmin):
    list_display = ('strategickpi','kpi_commenter','body','date_added')

admin.site.register(Status)

admin.site.register(Plan_type)

@admin.register(Planning_period)
class Planning_period(admin.ModelAdmin):
    list_display= ('plan_name','start_date','end_date','plan_type')



@admin.register(DraftMpttKPI)
class DrafttKPI(MPTTModelAdmin):
    list_display = ('kpi_name_eng','target', 'id', 'responsible_ministries')
    
admin.site.register(Annual_Plan)