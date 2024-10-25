from django import forms

from stock.models import Articulo
from .models import *

class CajaapertcierreForm(forms.ModelForm):
    class Meta:
        model = cajaapertcierre
        fields = '__all__'

class seriedetForm(forms.ModelForm):
    class Meta:
        model = seriedet
        fields = ['inicio', 'fin', 'correlativa','timbrado','nrocaja','deposito']