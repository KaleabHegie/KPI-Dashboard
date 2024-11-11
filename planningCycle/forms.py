import datetime
from django import forms
from.models import DraftStrategicGoal,Comment,DraftKeyResultArea,DraftKPI,DraftMpttKPI,KRAComment,KPIComment,Annual_Plan
from ckeditor.widgets import CKEditorWidget
from mptt.forms import TreeNodeChoiceField


class GoalForm(forms.ModelForm):
    
    class Meta:
        model = DraftStrategicGoal
        fields = ('goal_name_eng', 'goal_name_amh','status', 'responsible_ministries' , 'description')
        widgets = {
            'description': CKEditorWidget(),
            'responsible_ministries':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
        }
     
class GoalCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }
        error_messages = {
            'body': {
                'required': "Please enter your comment.",
            }
        }

class KRAForm(forms.ModelForm):
    class Meta:
        model = DraftKeyResultArea
        fields = ('activity_name_eng','activity_name_amh','goal', 'responsible_ministries','krastatus','description')
        widgets ={
            'goal':forms.Select(attrs={'class':'form-control'}),
            'responsible_ministries':forms.Select(attrs={'class':'form-control'}),
            
            'krastatus':forms.Select(attrs={'class':'form-control'}),
            'description':CKEditorWidget(),
        } 

class KRACommentForm(forms.ModelForm):
    class Meta:
        model = KRAComment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }
        error_messages = {
            'body': {
                'required': "Please enter your comment.",
            }
        }
class KPIForm(forms.ModelForm):
   
    class Meta:
        model = DraftMpttKPI
        fields = ('kpi_name_eng','kpi_name_amh','kpi_measurement_units','kpi_characteristics','kpi_description', 'base_value','target', 'responsible_ministries' ,'kpistatus','kpi_weight','draftkra','year')
        widgets = {
            'kpi_description':CKEditorWidget(),
            'draftkra':forms.Select(attrs={'class':'form-control'}),
            'kpistatus':forms.Select(attrs={'class':'form-control'}),
            'responsible_ministries':forms.Select(attrs={'class':'form-control'}),
            'kpi_weight':forms.TextInput(attrs={'class':'form-control'}),
            'year':forms.Select(attrs={'class':'form-control'}),
        } 
    def __init__(self, *args, **kwargs):
        super(KPIForm, self).__init__(*args, **kwargs)
        self.fields['responsible_ministries'].empty_label = 'Select Ministry'


class MPTTKPIForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=DraftMpttKPI.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = DraftMpttKPI
        fields = (
            'parent', 'kpi_name_eng', 'kpi_name_amh', 'kpi_measurement_units', 'kpi_characteristics',
            'kpi_description', 'base_value', 'target', 'responsible_ministries', 'kpistatus',
            'kpi_weight', 'draftkra', 'year'
        )
        widgets = {
            'kpi_description': CKEditorWidget(),
            'draftkra': forms.Select(attrs={'class': 'form-control'}),
            'kpistatus': forms.Select(attrs={'class': 'form-control'}),
            'responsible_ministries': forms.Select(attrs={'class': 'form-control'}),
            'kpi_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(MPTTKPIForm, self).__init__(*args, **kwargs)
        self.fields['responsible_ministries'].empty_label = 'Select Ministry'

class KPICommentForm(forms.ModelForm):
    class Meta:
        model = KPIComment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }
        error_messages = {
            'body': {
                'required': "Please enter your comment.",
            }
        }

class QuarterForm(forms.ModelForm):
    class Meta:
        model = Annual_Plan
        fields = ('kpi','quarter1_target','quarter2_target','quarter3_target', 'quarter4_target')
        widgets = {
            'kpi':forms.Select(attrs={'class': 'form-control'}),
            
            'quarter1_target':forms.NumberInput(attrs={'class':'form-control'}),
            'quarter2_target':forms.NumberInput(attrs={'class':'form-control'}),
            'quarter3_target':forms.NumberInput(attrs={'class':'form-control'}),
            'quarter4_target':forms.NumberInput(attrs={'class':'form-control'}),
        } 
    