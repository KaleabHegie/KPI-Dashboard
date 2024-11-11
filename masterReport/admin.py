from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import *



class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'quarter', 'year', 'deadline', 'recorded_by', 'created_at', 'updated_at')
    list_filter = ('quarter', 'year', 'recorded_by', 'created_at', 'updated_at')
    search_fields = ('type', 'year__year_amh', 'recorded_by__username')

    fieldsets = (
        (None, {
            'fields': ('type', 'type_amh_name','quarter', 'year', 'deadline', 'recorded_by', 'report_guideline')
        }),
       
    )

admin.site.register(ReportType, ReportTypeAdmin)


admin.site.register(Report)
admin.site.register(ReportSection)
admin.site.register(ReportGuideline)


class MasterReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'quarter', 'year', 'responsible_ministry', 'report_doc', 'created_at', 'updated_at')
    search_fields = ('name', 'responsible_ministry__responsible_ministry_eng')
    list_filter = ('quarter', 'year', 'created_at', 'updated_at')

admin.site.register(MasterReport, MasterReportAdmin)