from django import forms
from .models import Codigo

class FormCode(forms.ModelForm):
    class Meta:
        model = Codigo
        fields = ['code_file']
        