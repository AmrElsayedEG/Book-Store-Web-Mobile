from django import forms
from .models import order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ('customer_name','address_1','address_2','postal_code','city','country','phone','notes','payment_method')
