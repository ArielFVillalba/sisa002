from django import forms

from caja.models import seriedet
from .models import *

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['idarticulo', 'codigo', 'descripcion','unidad', 'costo','recarga_por', 'precio','iva','habilitado', 'muevestock',
                  'codigoflia']


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = familia
        fields = ['idfamilia', 'codigo','familia1', 'familia2','familia3', 'familia4', 'familia5','familia6', 'familia7' ]


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = '__all__'

class MovdepcabForm(forms.ModelForm):
    class Meta:
        model = Movdepcab
        fields = ['idmovdepcab', 'fecha', 'nromov','depsalida', 'depentrada','obs']

class MovdepdetForm(forms.ModelForm):
    class Meta:
        model = Movdepdet
        fields = '__all__'

class ExistenciaForm(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = '__all__'

class InvcabForm(forms.ModelForm):
    class Meta:
        model = Inventario_cab
        fields = '__all__'

class InvdetForm(forms.ModelForm):
    class Meta:
        model = Inventario_det
        fields = '__all__'

class InvtomaForm(forms.ModelForm):
    class Meta:
        model = Inventario_toma
        fields = '__all__'


