from django import forms
from django.contrib.auth.models import User

from . import models

class profileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['country','city','address_1','address_2','postal_code','phone']

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']
