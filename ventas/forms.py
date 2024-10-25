from django import forms
from .models import *

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['idcliente', 'nombre', 'cedula','fechanac'
            , 'ruc', 'timbrado','telefono', 'mail', 'direccion','ciudad']


class VentacabForm(forms.ModelForm):
    class Meta:
        model = Ventacab
        fields = ['idventacab', 'fecha', 'nrofactura','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs','deposito']



class VentadetForm(forms.ModelForm):
    class Meta:
        model = Ventadet
        fields = '__all__'
        # fields = ['idventadet', 'idventacab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']

class PagoclientesForm(forms.ModelForm):
    class Meta:
        model = Pagoclientes
        #fields = '__all__'
        fields = ['idpagocliente', 'fecha', 'recibo','idcliente','cliente']

class OrdenVentacabForm(forms.ModelForm):
    class Meta:
        model = Ordenventacab
        fields = ['idordenventacab', 'fecha', 'nroorden','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class OrdenventadetForm(forms.ModelForm):
    class Meta:
        model = Ordenventadet
        fields = '__all__'
        # fields = ['idordenventadet', 'idordenventacab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']

class PedidoventacabForm(forms.ModelForm):
    class Meta:
        model = Pedidoventacab
        fields = ['idpedidoventacab', 'fecha', 'nropedido','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class PedidoventadetForm(forms.ModelForm):
    class Meta:
        model = Pedidoventadet
        fields = '__all__'
        # fields = ['idpedidoventadet', 'idpedidoventacab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']



class PresupuestoventacabForm(forms.ModelForm):
    class Meta:
        model = Presupuestoventacab
        fields = ['idpresupuestoventacab', 'fecha', 'nropresupuesto','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']



class PresupuestoventadetForm(forms.ModelForm):
    class Meta:
        model = Presupuestoventadet
        fields = '__all__'


class NotacreditoventacabForm(forms.ModelForm):
    class Meta:
        model = Notacreditoventacab
        fields = ['idnotacreditoventacab', 'fecha', 'nronota','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs','deposito']



class NotacreditoVentadetForm(forms.ModelForm):
    class Meta:
        model = Notacreditoventadet
        fields = '__all__'
        # fields = ['idnotacreditoventadet', 'idnotacreditoventacab', 'orden','idarticulo','codigo', 'descripcion', 'cantidad','unidad', 'costo', 'precio','iva']


class NotadebitodeventacabForm(forms.ModelForm):
    class Meta:
        model = Notadebitoventacab
        fields = ['idnotadebitoventacab', 'fecha', 'nrodebito','idcliente'
            , 'cliente', 'ruc','timbrado', 'tipodoc', 'condicion','fechavto'
            , 'fecharece', 'obs']

class NotadebitodeventadetForm(forms.ModelForm):
    class Meta:
        model = Notadebitoventadet
        fields = '__all__'
     
