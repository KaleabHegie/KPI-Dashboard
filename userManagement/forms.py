
from django import forms
from django.contrib.auth import authenticate

from .models import Account, UserSector
from resultsFramework.models import DashboardSetting


from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm



class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")





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





class LoginFormDashboard(forms.Form):

    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Email address'
    }))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Password'
    }))



class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder' : 'Enter your email',
        }))


class UserPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Password',
    }))
    new_password2 = forms.CharField(label='Conform Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Confirm Password',
    }))
