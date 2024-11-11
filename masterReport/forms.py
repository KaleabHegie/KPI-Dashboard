from django import forms
from .models import *


class ReportTypeForm(forms.ModelForm):
    class Meta:
        model = ReportType
        fields = ['type', 'year','deadline']
        widgets = {
            'type': forms.Select(attrs={"class": "form-control form-control-solid", "required": "True"}),
            'year': forms.Select(attrs={"class": "form-control form-control-solid", "id":"datetimepicker3'", "required": "True"}),
            'deadline': forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': "yyyy-mm-dd", "class": "form-control form-control-solid", "required": "True"})

        }
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields=['alternative_name','report_document']
        widgets = {
            'alternative_name': forms.TextInput(attrs={"class":"form-control form-control-solid", "required":"True"}),
          
            'report_document': forms.FileInput(attrs={"class": "form-control form-control-solid", "required": "True"})
        }

class ReportSectionForm(forms.ModelForm):
    class Meta:
        model = ReportSection
        fields=['title','section_content','word_count']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control form-control-solid", "required": "True"}),
            'section_content': forms.Textarea(attrs={"class": "form-control form-control-solid", "required": "True",'cols': 80, 'rows': 30}),
            'word_count': forms.NumberInput(attrs={"class": "form-control form-control-solid", "required": "True"})
        }