from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render




class LoginFormDashboard(forms.Form):

    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Email address'
    }))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Password'
    }))