
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

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        exclude =['state_user']

class UpdateParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        exclude =['state_user','gender']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

class StateUserForgotForm(forms.Form):
    email = forms.EmailField(label="Your Registered Email")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields  = ['title', 'body', 'media']
