from django import forms
from .customers.models import*

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'