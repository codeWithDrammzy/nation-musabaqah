
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from.models import *


class CreateUser(forms.ModelForm):  
    class Meta:
        model = User
        fields = ['username', 'email']


class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginUserForm(AuthenticationForm):
    class Meta:
        email = forms.CharField(widget=TextInput(attrs={'placeholder': 'email'}))
        password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'password'})) 
        

class StateUserForm(forms.ModelForm):
    class Meta:
        model = StateUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'state']
        exclude = ['role']