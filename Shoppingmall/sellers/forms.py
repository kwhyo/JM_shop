from django import forms
from .models import Item

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','price','description','stock','seller','category','image']
