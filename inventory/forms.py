from django import forms
from .models import StockMovement
from .models import Product
from django.forms.widgets import DateInput
from .models import Warehouse
from .models import Stock



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'critical_level', 'unit', 'min_temperature', 'max_temperature']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'critical_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'max_temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }



        
   
class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['quantity', 'movement_type', 'user', 'expiration_date']
        widgets = {
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'temperature']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'})
        }


