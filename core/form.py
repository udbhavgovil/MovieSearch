from django import forms
from django.db import models
from .models import Accounts


class MovieForm(forms.Form):
    keyword = forms.CharField(max_length=50)
    year = forms.IntegerField(required = False)
    
class LoginForm (forms.Form):
    user_id = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
     
class AccountForm (forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['user_id','password','Name']
