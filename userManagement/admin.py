from django.contrib import admin
from .models import ResponsibleMinistry
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from userManagement.models import ResponsibleMinistry
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


 


# Register your models here.
@admin.register(ResponsibleMinistry)
class PersonAdmin(ImportExportModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="/media/{}" style="width="20" height="20" />'.format(obj.image))
    image_tag.short_description = 'Image'
    list_display = ['responsible_ministry_eng', 'code', 'image_tag',]