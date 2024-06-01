from django.contrib import admin
from .models import ResponsibleMinistry
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(ResponsibleMinistry)
class PersonAdmin(ImportExportModelAdmin):
    pass