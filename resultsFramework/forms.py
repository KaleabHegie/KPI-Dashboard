from django import forms
from userManagement.models import ResponsibleMinistry
from .models import (
    Year,
    NationalPlan,
    StrategicGoal,
    KeyResultArea,
    Indicator,
    KpiAggregation
)





class ImportFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control'
    }))


class MinistriesForm(forms.ModelForm):
    class Meta:
        model = ResponsibleMinistry
        fields = ['responsible_ministry_eng', 'responsible_ministry_amh', 'code']
        widgets = {
            'responsible_ministry_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_ministry_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['year_eng', 'year_amh', 'visible']
        widgets = {
            'year_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'year_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'visible': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

class NationalPlanForm(forms.ModelForm):
    class Meta:
        model = NationalPlan
        fields = ['np_name_eng', 'np_name_amh', 'description_eng', 'description_amh', 'starting_date', 'ending_date']
        widgets = {
            'np_name_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'np_name_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'description_eng': forms.Textarea(attrs={'class': 'form-control', 'rows':'4', 'cols': '50'}),
            'description_amh': forms.Textarea(attrs={'class': 'form-control', 'rows':'4', 'cols': '50'}),
            'starting_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type' : 'datetime-local'}),
            'ending_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type' : 'datetime-local'}),
        }

class StrategicGoalForm(forms.ModelForm):
    class Meta:
        model = StrategicGoal
        fields = ['goal_name_eng', 'goal_name_amh', 'goal_weight', 'goal_is_shared', 'national_plan', 'responsible_ministries']
        widgets = {
            'goal_name_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'goal_name_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'goal_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal_is_shared': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'national_plan': forms.Select(attrs={'class': 'form-select'}),
            'responsible_ministries': forms.Select(attrs={'class': 'form-select'}),
        }

class KeyResultAreaForm(forms.ModelForm):
    class Meta:
        model = KeyResultArea
        fields = ['activity_name_eng', 'activity_name_amh', 'activity_weight', 'activity_is_shared', 'goal']
        widgets = {
            'activity_name_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_name_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_is_shared': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
        }

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['kpi_name_eng', 'kpi_name_amh', 'kpi_weight', 'kpi_measurement_units', 'kpi_characteristics', 'responsible_ministries', 'keyResultArea']
        widgets = {
            'kpi_name_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'kpi_name_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'kpi_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'kpi_measurement_units': forms.TextInput(attrs={'class': 'form-control'}),
            'kpi_characteristics': forms.Select(attrs={'class': 'form-select'}),
            'responsible_ministries': forms.Select(attrs={'class': 'form-select'}),
            'keyResultArea': forms.Select(attrs={'class': 'form-select'}),

        }

class SubIndicatorForm(forms.ModelForm):
    class Meta:
        model = KpiAggregation
        fields = ['sub_kpi_name_eng', 'sub_kpi_name_amh', 'category']
        widgets = {
            'sub_kpi_name_eng': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_kpi_name_amh': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }