from django import forms

from stock.models import Articulo
from .models import *


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['idproveedor', 'nombre', 'cedula','fechanac'
            , 'ruc', 'timbrado','telefono', 'mail', 'direccion','ciudad']


class CompracabForm(forms.ModelForm):
    class Meta:
        model = Compracab
        fields = ['idcompracab', 'fecha', 'nrofactura','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs','deposito']



class ComradetForm(forms.ModelForm):
    class Meta:
        model = Compradet
        fields = '__all__'
        # fields = ['idcompradet', 'idcompracab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']

class ComprascuotasForm(forms.ModelForm):
    class Meta:
        model = Comprascuotas
        fields = ['idcomprascuotas', 'idcompracab', 'orden','fechavto'
            , 'monto', 'moneda','cotizacion']


class PagoproveedorForm(forms.ModelForm):
    class Meta:
        model = Pagoproveedor
        fields = ['idpagoproveedor','fecha','recibo','idproveedor','proveedor']


class PagoprovfactForm(forms.ModelForm):
    class Meta:
        model = Pagoprovfact
        fields = '__all__'

class OrdendecompcabForm(forms.ModelForm):
    class Meta:
        model = Ordencompcab
        fields = ['idordencompcab', 'fecha', 'nroorden','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class OrdendecompdetForm(forms.ModelForm):
    class Meta:
        model = Ordencompdet
        fields = '__all__'
        # fields = ['idcompradet', 'idcompracab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']


class PedidodecompcabForm(forms.ModelForm):
    class Meta:
        model = Pedidocompcab
        fields = ['idpedidocompcab', 'fecha', 'nropedido','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class PedidodecompdetForm(forms.ModelForm):
    class Meta:
        model = Pedidocompdet
        fields = '__all__'
        # fields = ['idcompradet', 'idcompracab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']

class PresupuestodecompcabForm(forms.ModelForm):
    class Meta:
        model = Presupuestocompcab
        fields = ['idpresupuestocompcab', 'fecha', 'nropresupuesto','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class PresupuestodecompdetForm(forms.ModelForm):
    class Meta:
        model = Presupuestocompdet
        fields = '__all__'


class NotacreditodecompcabForm(forms.ModelForm):
    class Meta:
        model = Notacreditocompcab
        fields = ['idnotacreditocompcab', 'fecha', 'nronota','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs','deposito']


class NotacreditodecompdetForm(forms.ModelForm):
    class Meta:
        model = Notacreditocompdet
        fields = '__all__'
        # fields = ['idnotacreditocompdet', 'idcompracab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']


class NotadebitodecompcabForm(forms.ModelForm):
    class Meta:
        model = Notadebitocompcab
        fields = ['idnotadebitocompcab', 'fecha', 'nrodebito','idproveedor'
            , 'proveedor', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']


class NotadebitodecompdetForm(forms.ModelForm):
    class Meta:
        model = Notadebitocompdet
        fields = '__all__'
        # fields = ['idnotacreditocompdet', 'idcompracab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']

