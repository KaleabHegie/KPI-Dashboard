from django import forms
from resultsFramework.models import DashboardSetting

from django import forms

class DashboardSettingForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        quarter = cleaned_data.get('quarter')

        if month and quarter:
            raise forms.ValidationError("Please fill either the month or the quarter, not both.")
        

    class Meta:
        model = DashboardSetting
        fields = ['name', 'year', 'month', 'quarter', 'indicator', 'performance', 'target']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'target': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'quarter': forms.Select(attrs={'class': 'form-control'}),
           'indicator': forms.SelectMultiple(attrs={ 'multiple': 'multiple' , 'size':"10"}) ,
           'target' : forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
            'performance' : forms.CheckboxInput(attrs={'class': 'form-check-input ml-2'}),
               }