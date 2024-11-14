from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import ResponsibleMinistry,Account,UserSector,ContactInfo
import tablib


#import Export 

admin.site.register(ContactInfo)

class ResponsibleMinistryResource(resources.ModelResource):
     class Meta:
          model = ResponsibleMinistry
          skip_unchanged = True
          report_skipped = True
          exclude = ('id')
          import_id_fields = ('responsible_ministry_eng', 'responsible_ministry_amh', 'code')


class ResponsibleMinistryAdmin(ImportExportModelAdmin):
    list_display = ('responsible_ministry_eng', 'responsible_ministry_amh', 'code','ministry_is_visable')
    list_editable = ('ministry_is_visable',)
    # resource_classes = [ResponsibleMinistryResource]



admin.site.register(ResponsibleMinistry, ResponsibleMinistryAdmin)


def handle_uploaded_responsible_ministry_file(file):
    try:
        resource  = ResponsibleMinistryResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result



class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login',
	                'is_admin', 'is_mopd', 'is_dpg', 'is_hopr', 'is_sector')
	search_fields = ('email','username',)
	icon_name = 'account_circle'
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()



admin.site.register(Account, AccountAdmin)


# @admin.register(Account)
# class PersonAdmin(ImportExportModelAdmin):
#     pass

@admin.register(UserSector)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ( 'user_sector','user')




###Confirm 
def confirm_file(imported_data, type):
        if type == 'responsible_ministries':
            resource  = ResponsibleMinistryResource()

        result = resource.import_data(imported_data, dry_run=True) 
        if not result.has_errors():
            resource.import_data(imported_data, dry_run=False)  # Actually import now
            return True, f"Data imported successfully: {len(imported_data)} records imported."
        else:
            return False, f"Error importing data: Please review your Document."
        