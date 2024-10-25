from django import forms
from .models import *


class CtacontableForm(forms.ModelForm):
    class Meta:
        model = Cuentacontable
        fields = ['idcuentacontable', 'cuenta','denominacion'
       ,'nivel', 'naturaleza','asentable', 'centro_costo']


class AsientoForm(forms.ModelForm):
    class Meta:
        model = asiento
        fields = ['idasiento','nroasiento','descripcion', 'fecha']

class AsientodetForm(forms.ModelForm):
    class Meta:
        model = asiento_det
        fields = ['idasientodet','orden','idcuentacontable', 'cuenta','denominacion','debe','haber']

