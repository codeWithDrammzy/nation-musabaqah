from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from.models import *

class LoginUserForm(AuthenticationForm):
    class Meta:
        username = forms.CharField(widget=TextInput(attrs={'placeholder': 'username'}))
        password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'password'})) 
        

class StateUserForm(forms.ModelForm):
    class Meta:
        model = StateUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'state']