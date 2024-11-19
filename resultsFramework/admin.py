from django.contrib import admin
import tablib
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget  # For foreignkey
from import_export.fields import Field
from mptt.admin import MPTTModelAdmin
from import_export.admin import ImportExportModelAdmin
from userManagement.models import ResponsibleMinistry
from import_export.formats.base_formats import XLS

from .models import (

    Post,
    Year,
    Quarter,
    Month,
    NationalPlan,
    StrategicGoal,
    KeyResultArea,
    Indicator,

    IndicatorMetaData,
    SharedIndicator,
    QuarterProgress,
    AnnualPlan,

    Category,
    KpiAggregation,
    AnnualPlan2,
    ScoreCardRange,
    QuarterProgress2,
    DashboardSetting,
    IndicatorTempo,
    AnnualQuarter,
    PolicyArea,
    QuarterPlanTemp,
)
from .resource import GoalResource,TempIndicatorResource,AnnualQuarterResource,QuarterPlanTempResource, AgendaGoalsResource, SDGResource
from .models import SDG, AgendaGoals

# Register your models here.
from datetime import datetime

class AgendaGoalsAdmin(ImportExportModelAdmin):
    resource_classes = [AgendaGoalsResource]

admin.site.register(AgendaGoals,AgendaGoalsAdmin)


class SDGAdmin(ImportExportModelAdmin):
    resource_classes = [SDGResource]

admin.site.register(SDG,SDGAdmin)


from .utility import Quarter, Year, PerformanceEntryDate, QuarterPerformanceEntryDate, AnnualPerformanceEntryDate,QuarterPlanEntryDate

@admin.register(PolicyArea)
class PolicyAreaAdmin(ImportExportModelAdmin):
    list_display = ('id','rank','policyAreaEng','code','icon',)



@admin.register(QuarterPlanEntryDate)
class QuarterPlanEntryDateAdmin(admin.ModelAdmin):
    list_display = ('name', 'yearOfEntry', 'quarter',
                    'startDate', 'endDate', 'active', 'check_entryDate')
    list_filter = ('yearOfEntry', 'quarter', 'active')
    search_fields = ('name', 'yearOfEntry__name')

@admin.register(ScoreCardRange)
class ScoreCardRangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'starting', 'ending')
    search_fields = ('name',)


@admin.register(PerformanceEntryDate)
class PerformanceEntryDateAdmin(admin.ModelAdmin):
    list_display = ('name', 'yearOfEntry', 'startDate',
                    'endDate', 'active', 'check_entryDate')
    list_filter = ('yearOfEntry', 'active')
    search_fields = ('name', 'yearOfEntry__name')


@admin.register(QuarterPerformanceEntryDate)
class QuarterPerformanceEntryDateAdmin(admin.ModelAdmin):
    list_display = ('name', 'yearOfEntry', 'quarter',
                    'startDate', 'endDate', 'active', 'check_entryDate')
    list_filter = ('yearOfEntry', 'quarter', 'active')
    search_fields = ('name', 'yearOfEntry__name')


@admin.register(AnnualPerformanceEntryDate)
class AnnualPerformanceEntryDateAdmin(admin.ModelAdmin):
    list_display = ('name', 'yearOfEntry', 'startDate',
                    'endDate', 'active', 'check_entryDate')
    list_filter = ('yearOfEntry', 'active')
    search_fields = ('name', 'yearOfEntry__name')


@admin.register(Quarter)
class QuarterAdmin(ImportExportModelAdmin):
    list_display = ('quarter_eng', 'quarter_amharic')


@admin.register(Month)
class MonthAdmin(ImportExportModelAdmin):
    list_display = ('month_english', 'month_amh', 'month_ranked')
    list_filter = ('quarter',)




# class BookAdmin(ImportExportModelAdmin):
#     # resource_classes = [GoalResource]
#     list_display = ('goal_name_eng', 'responsible_ministries',
#                     'goal_weight', 'goal_is_shared', 'national_plan')
#     list_filter = ('responsible_ministries',)
#     list_editable = ('goal_is_shared', 'responsible_ministries')
    
    



# @admin.register(StrategicGoal)
# class StrategicGoalAdmin(ImportExportModelAdmin):





# @admin.register(Indicator)
# class IndicatorAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'kpi_name_eng', 'kpi_weight', 'kpi_measurement_units',
#                     'kpi_characteristics', 'responsible_ministries', 'keyResultArea')
#     list_filter = ('responsible_ministries',
#                    'keyResultArea__goal__national_plan')
#     search_fields = (
#         "kpi_name_eng",

#     )


@admin.register(IndicatorMetaData)
class IndicatorMetaDataAdmin(ImportExportModelAdmin):
    list_display = ('kpi', 'kpi_description_eng', 'source', 'base_value', 'base_year', 'calculation_method',
                    'interpretation', 'units_of_measurement', 'frequency_of_update', 'data_quality_and_validity', 'references')


@admin.register(SharedIndicator)
class SharedIndicatorAdmin(ImportExportModelAdmin):
    list_display = ('responsible_ministry', 'indicator', 'kpi_weight')


@admin.register(QuarterPlanTemp)
class QuarterPlanTempAdmin(ImportExportModelAdmin):
    pass



@admin.register(QuarterProgress)
class QuarterProgressAdmin(ImportExportModelAdmin):
    list_display = ( 'indicator', 'quarter_target', 'quarter', 'year', 'quarter_performance', 'quarter_date' ,)
    
    list_editable = ('quarter_target','quarter_performance')
    search_fields = ("indicator__kpi_name_eng",)

    autocomplete_fields = ['indicator']


# @admin.register(AnnualPlan)
# class AnnualPlanAdmin(ImportExportModelAdmin):
#     list_display = ('national_plan', 'indicator', 'sub_indicator',
#                     )
#     list_filter = ('indicator__responsible_ministries__responsible_ministry_eng',
#                    )
#     # list_editable = ('indicator', 'sub_indicator', 'year', 'annual_target',
#     #                  'annual_performance')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name_eng', 'name_amh')


# @admin.register(MPTTModelAdmin)
# class KpiAggregationAdmin(ImportExportModelAdmin):
#     list_display = ('sub_kpi_name_eng', 'category')


# class KpiAggregationAdmin(MPTTModelAdmin, ImportExportModelAdmin):
#     # specify pixel amount for this ModelAdmin only:
#     mptt_level_indent = 20


# admin.site.register(KpiAggregation, KpiAggregationAdmin)


admin.site.register(Post)



@admin.register(QuarterProgress2)
class QuarterProgress2Admin(ImportExportModelAdmin):

    list_filter = ('indicator__responsible_ministries__responsible_ministry_eng',
                   )



@admin.register(AnnualPlan2)
class AnnualPlan2Admin(ImportExportModelAdmin):
    list_display = ('indicator', 'sub_indicator', 'target_state', 'plan_year_2012', 'performance_year_2012',
                    'plan_year_2013', 'performance_year_2013', 'plan_year_2014', 'performance_year_2014',
                    'plan_year_2015', 'plan_year_2016', 'plan_year_2017', 'plan_year_2018')

    list_filter = ('indicator__responsible_ministries__responsible_ministry_eng',
                   )

class AnnualQuarterAdmin(ImportExportModelAdmin):
    resource_classes = [AnnualQuarterResource]
    list_display = ('indicator', 'performance_2015', 'target_2016',)
    list_filter = ('indicator__responsible_ministries__responsible_ministry_eng',
                   )

    search_fields = ['indicator__kpi_name_eng']  # Search by indicator name
    autocomplete_fields = ['indicator']
    

admin.site.register(AnnualQuarter, AnnualQuarterAdmin)

#Import Export
    


#### YEAR ####
class YearResource(resources.ModelResource):
     class Meta:
          model = Year
          skip_unchanged = True
          report_skipped = True
          ##exclude = ('id')
          #import_id_fields = ('year_eng', 'year_eng', 'visible')


class YearAdmin(ImportExportModelAdmin):
    resource_classes = [YearResource]

admin.site.register(Year, YearAdmin)



def handle_uploaded_year_file(file):
    try:
        resource  = YearResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    




### National Plan ###
class NationalPlanResource(resources.ModelResource):
     class Meta:
          model = NationalPlan
          skip_unchanged = True
          report_skipped = True
          #exclude = ('id')
          #import_id_fields = ('np_name_eng', 'np_name_amh', 'description_eng', 'description_amh','starting_date', 'ending_date')


class NationalPlanAdmin(ImportExportModelAdmin):
    resource_classes = [NationalPlanResource]

admin.site.register(NationalPlan, NationalPlanAdmin)



def handle_uploaded_national_plan_file(file):
    try:
        resource  = NationalPlanResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    

### Strategical Goal ###
class StrategicGoalResource(resources.ModelResource):
    policy_area = fields.Field(
        column_name='policy_area',
        attribute='policy_area',
        widget=ForeignKeyWidget(PolicyArea, field='code'),
        saves_null_values = True,
        )
    national_plan = fields.Field(
        column_name='national_plan',
        attribute='national_plan',
        widget=ForeignKeyWidget(NationalPlan, field='id'),
        saves_null_values = True,
        )
    class Meta:
          model = StrategicGoal
          skip_unchanged = True
          report_skipped = True
          fields = ('code','goal_name_eng', 'goal_name_amh', 'goal_weight', 'goal_is_shared','national_plan', 'policy_area', 'policy_area__policyAreaEng','goal_is_visable')
          exclude = ('id')
          import_id_fields = ('code','goal_name_eng','national_plan', 'policy_area')


class StrategicGoalAdmin(ImportExportModelAdmin):
    list_display = ('goal_name_eng','code','policy_area', 'goal_is_visable','responsible_ministries',)
    
    # Fields to add to the search functionality
    search_fields = ('goal_name_eng', 'goal_name_amh', 'code')
    
    # Fields to add to the filter functionality
    list_filter = ('goal_is_visable', 'policy_area')
    list_editable = ('goal_is_visable', 'policy_area')
    resource_classes = [StrategicGoalResource]

admin.site.register(StrategicGoal, StrategicGoalAdmin)



def handle_uploaded_strategical_goal_file(file):
    try:
        resource  = StrategicGoalResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    


### Key Result Area ###
class KeyResultAreaResource(resources.ModelResource):
    goal = fields.Field(
        column_name='goal',
        attribute='goal',
        widget=ForeignKeyWidget(StrategicGoal, field='code'),
        saves_null_values = True,
        )
    class Meta:
          model = KeyResultArea
          skip_unchanged = True
          report_skipped = True
          exclude = ('id')
          fields = ('code','activity_name_eng', 'activity_name_amh', 'activity_weight', 'activity_is_shared', 'goal', 'goal__goal_name_eng', 'kra_is_visable')
          import_id_fields = ('code','activity_name_eng','goal')
          

class KeyResultAreaAdmin(ImportExportModelAdmin):
    list_display = ('activity_name_eng', 'code', 'goal',)
    list_filter = ('goal',)
    search_fields = ('activity_name_eng', 'goal__goal_name_eng', 'code')
    list_editable = ( 'goal',
    )
    resource_classes = [KeyResultAreaResource]


admin.site.register(KeyResultArea, KeyResultAreaAdmin)



def handle_uploaded_key_result_area_file(file):
    try:
        resource  = KeyResultAreaResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    


### Indicator ###
class IndicatorResource(resources.ModelResource):
    responsible_ministries = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='code'),
        saves_null_values = True,
        )
    keyResultArea = fields.Field(
        column_name='keyResultArea',
        attribute='keyResultArea',
        widget=ForeignKeyWidget(KeyResultArea, field='code'),
        saves_null_values = True,
        )
    class Meta:
          model = Indicator
          skip_unchanged = True
          report_skipped = True
          fields = ('code','keyResultArea__goal__goal_name_eng','keyResultArea','kpi_name_eng', 'kpi_weight', 'responsible_ministries')
          exclude = ('id')
          import_id_fields = ('code','kpi_name_eng','responsible_ministries')


class IndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [IndicatorResource]
    list_display = ('kpi_name_eng', "code",
                    'kpi_characteristics','kpi_is_visable', 'responsible_ministries', 'keyResultArea','kpi_weight')
    search_fields = ("kpi_name_eng","code")
    list_editable = ( 'kpi_characteristics','responsible_ministries','kpi_weight')
    list_filter = ('responsible_ministries', 'kpi_is_visable',"keyResultArea__goal__policy_area")
    autocomplete_fields = ['keyResultArea']
admin.site.register(Indicator, IndicatorAdmin)




class TempIndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [TempIndicatorResource]
    list_display = ('id', 'kpi_name_eng', 
                    'kpi_characteristics', 'responsible_ministries', 'goal')
    search_fields = ("kpi_name_eng",)
    list_editable = ( 'goal',)
    list_filter = ('responsible_ministries', 'goal')
admin.site.register(IndicatorTempo, TempIndicatorAdmin)



def handle_uploaded_indicator_file(file):
    try:
        resource  = IndicatorResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    


## KpiAggregation
class KpiAggregationResource(resources.ModelResource):    
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='id'),
        saves_null_values = True,
    )
    
    kpi = fields.Field(
        column_name='kpi',
        attribute='kpi',
        widget=ForeignKeyWidget(Indicator, field='id'),
        saves_null_values = True,
    )

    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(KpiAggregation, field='id'),
        saves_null_values = True,
    )

    class Meta:
        model = KpiAggregation
        report_skipped = True
        skip_unchanged = True
        #fields = ('id','sub_kpi_name_eng', 'sub_kpi_name_amh', 'kpi', 'parent', 'category', 'composite_key')
        #import_id_fields = ('parent','sub_kpi_name_eng', 'sub_kpi_name_amh','kpi', 'category')
        export_order = ('id','parent','sub_kpi_name_eng', 'sub_kpi_name_amh','kpi', 'category','composite_key')


class KpiAggregationAdmin(ImportExportModelAdmin):
    resource_classes = [KpiAggregationResource]

admin.site.register(KpiAggregation, KpiAggregationAdmin)



class DashboardSettingAdmin(ImportExportModelAdmin):
    filter_horizontal = ('indicator', )

admin.site.register(DashboardSetting,DashboardSettingAdmin)



def handle_uploaded_kpiAggregation_file(file):
        def filterParent(item):
            '''
            filter parent Items
            '''
            if item['parent'] == None:
                return item
            

        def filterChild(itemParent, itemChild):
            '''
            filter Child Items
            '''
            try:
               if itemChild['parent'].strip() == itemParent.strip():
                   return itemChild
            except:
               pass
           
           
           

  
        resource  = KpiAggregationResource()
        dataset = tablib.Dataset()


        imported_data = dataset.load(file.read())
        total_data = []
            
        indicator_list = []
        for row in imported_data.dict:
            indicator_list.append({'kpi':row['kpi'],'parent':row['parent'], 'sub_kpi_name_eng':row['sub_kpi_name_eng'],  'sub_kpi_name_amh':row['sub_kpi_name_amh'],'category':row['category']})
                
        
        # get parent lists 
        parentIndicator = list(filter(lambda parent_item: filterParent(parent_item), indicator_list ))

        #Child 
        global current_id 
        current_id = 0
        def filterChildIndicator(parent_id, parent_name):
            global current_id
            childIndicator = filter(lambda child_item : filterChild(parent_name, child_item), indicator_list )
            childIndicator =  list(childIndicator)

            if len(childIndicator) != 0:
                for child in childIndicator:                    
                    data = (child['parent'],f'{child["kpi"].strip()}',child['sub_kpi_name_eng'],child['sub_kpi_name_amh'], child['category'])
                    child_dataset = tablib.Dataset(data, headers=['parent', 'kpi', 'sub_kpi_name_eng', 'sub_kpi_name_amh', 'category'])
                    result = resource.import_data(child_dataset, dry_run=True)
                    if not result.has_errors():
                        current_id = int(current_id) + 1
                        total_data.append(((int(current_id), parent_id,f'{child["kpi"].strip()}',child['sub_kpi_name_eng'],child['sub_kpi_name_amh'], child['category'])))
                        filterChildIndicator(int(current_id), child['sub_kpi_name_eng'])
                    else:
                        current_id = int(current_id) + 1
                        total_data.append((current_id, parent_id,f'{child["kpi"].strip()}',child['sub_kpi_name_eng'],child['sub_kpi_name_amh'], child['category']))
                        filterChildIndicator(int(current_id), child['sub_kpi_name_eng'])
                             
                
        #Parent  
        for parent in parentIndicator:
            data = (parent['parent'],f'{parent["kpi"].strip()}',parent['sub_kpi_name_eng'],parent['sub_kpi_name_amh'], parent['category'])
            parent_dataset = tablib.Dataset(data, headers=['parent', 'kpi', 'sub_kpi_name_eng', 'sub_kpi_name_amh', 'category'])
            result = resource.import_data(parent_dataset, dry_run=True)
            if not result.has_errors():
                for row_result in result:
                    get_id = ("%d" % (row_result.object_id))
                parent_id = get_id
                if current_id == 0:
                    current_id = int(current_id) + int(parent_id)
                else:
                    current_id = int(current_id) + 1
                total_data.append((current_id, None,f'{parent["kpi"].strip()}',parent['sub_kpi_name_eng'],parent['sub_kpi_name_amh'], parent['category']))
                filterChildIndicator(current_id, parent['sub_kpi_name_eng'])
            else:
                current_id = int(current_id) + 1
                total_data.append((current_id, None,f'{parent["kpi"].strip()}',parent['sub_kpi_name_eng'],parent['sub_kpi_name_amh'], parent['category']))
                filterChildIndicator(int(current_id), parent['sub_kpi_name_eng'])

        

        #Return the data
        data_set = tablib.Dataset(*total_data, headers=['id','parent', 'kpi' , 'sub_kpi_name_eng', 'sub_kpi_name_amh', 'category'])
        
        result = resource.import_data(data_set, dry_run=True)
        return True,data_set, result




### Annual  Plan ###
class AnnualPlanResource(resources.ModelResource):
    national_plan = fields.Field(
        column_name='national_plan',
        attribute='national_plan',
        widget=ForeignKeyWidget(NationalPlan, field='id'),
        saves_null_values = True,
        )
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field='code'),
        saves_null_values = True,
        )
    sub_indicator = fields.Field(
        column_name='sub_indicator',
        attribute='sub_indicator',
        widget=ForeignKeyWidget(KpiAggregation, field='id'),
        saves_null_values = True,
        )
    year = fields.Field(
        column_name='year',
        attribute='year',
        widget=ForeignKeyWidget(Year, field='year_amh'),
        saves_null_values = True,
        )
    class Meta:
          model = AnnualPlan
          skip_unchanged = True
          report_skipped = True
          #import_id_fields = ('indicator',)
        #   exclude = ('id')
          fields = ('id','national_plan','indicator__kpi_name_eng' ,'sub_indicator',  'year','annual_performance')
          #export_order = ('id', 'national_plan','indicator', 'sub_indicator', 'year','annual_performance')


class AnnualAdmin(ImportExportModelAdmin):
    resource_classes = [AnnualPlanResource]
    list_display = ( 'indicator', 'annual_target','year','annual_performance')
    list_filter = ('indicator__responsible_ministries__responsible_ministry_eng',
                   )
    search_fields = ("indicator__kpi_name_eng",)
    list_editable = ( 'annual_target',)
    autocomplete_fields = ['indicator']

admin.site.register(AnnualPlan, AnnualAdmin)



def handle_uploaded_annual_plan(file):
    try:
        resource  = AnnualPlanResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    

def handle_uploaded_quarter_plan1(file):
    result = None
    imported_data = None

    try:
        resource  = QuarterPlanTempResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result



###Confirm 
def confirm_file(imported_data, type):
        if type == 'year':
            resource  = YearResource()
        elif type == 'national_plan':
            resource = NationalPlanResource()
        elif type == 'strategical_goal':
            resource = StrategicGoalResource()
        elif type == 'key_result_area':
            resource = KeyResultAreaResource()
        elif type == 'indicator':
            resource = IndicatorResource()
        elif type == 'subIndicator':
            resource = KpiAggregationResource()
        elif type == 'annualPlan':
            resource = AnnualPlanResource()
        elif type =='quarterPlan':
            resource = QuarterPlanTempResource()


            

        result = resource.import_data(imported_data, dry_run=True) 
        if not result.has_errors():
            resource.import_data(imported_data, dry_run=False)  # Actually import now
            return True, f"Data imported successfully: {len(imported_data)} records imported."
        else:
            return False, f"Error importing data: Please review your Document."
        

