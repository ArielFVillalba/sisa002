from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import pre_delete ,post_save
from django.dispatch import receiver
from django.db.models import Sum

from compras import *
from inicio.models import *
from django.contrib.auth.models import User
from django.utils import timezone

from inicio.models import *
from stock.models import Articulo


class Proveedor(audit):
    idproveedor = models.AutoField(primary_key=True)
    nombre = models.TextField()
    cedula = models.TextField(blank=True, null=True)
    fechanac = models.DateField(blank=True, null=True)
    ruc = models.TextField(blank=True, null=True)
    timbrado = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    pkpr = None

    class Meta:
        db_table = 'proveedor'

        def __str__(self):
            return self.cedula


class Compracab(audit):
    idcompracab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrofactura = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    deposito = models.TextField()
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkf = None

    class Meta:
        db_table = 'compra_cab'


class Compradet(audit):
    idcompradet = models.AutoField(primary_key=True)
    idcompracab = models.ForeignKey(Compracab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkfd = None

    class Meta:
        db_table = 'compra_det'


class Comprascuotas(audit):
    idcomprascuotas = models.AutoField(primary_key=True)
    idcompracab = models.ForeignKey(Compracab, on_delete=models.DO_NOTHING)
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fechavto = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'comprascuotas'


class Pagoproveedor(audit):
    idpagoproveedor = models.AutoField(primary_key=True)
    fecha = models.DateField()
    recibo = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagoproveedor'

class Pagoprovforma(audit):
    idpagoprovforma = models.AutoField(primary_key=True)
    idpagoproveedor = models.ForeignKey(Pagoproveedor, on_delete=models.DO_NOTHING)
    idtipopago = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    banco  = models.TextField()
    ctacte  = models.TextField()
    nrodoc  = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagoprovforma'

class Pagoprovfact(audit):
    idpagoprovfact = models.AutoField(primary_key=True)
    idpagoproveedor = models.ForeignKey(Pagoproveedor, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idcomprascuotas = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagoprovfact'


class Ordencompcab(audit):
    idordencompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nroorden = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda =models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkf = None

    class Meta:
        db_table = 'ordencomp_cab'


class Ordencompdet(audit):
    idordencompdet = models.AutoField(primary_key=True)
    idordencompcab = models.ForeignKey(Ordencompcab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkfd = None

    class Meta:
        db_table = 'ordencomp_det'


class Pedidocompcab(audit):
    idpedidocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropedido = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkpc = None

    class Meta:
        db_table = 'pedidocomp_cab'


class Pedidocompdet(audit):
    idpedidocompdet = models.AutoField(primary_key=True)
    idpedidocompcab = models.ForeignKey(Pedidocompcab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkpcd = None

    class Meta:
        db_table = 'pedidocomp_det'


class Presupuestocompcab(audit):
    idpresupuestocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropresupuesto = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pkpc = None

    class Meta:
        db_table = 'presupestocomp_cab'


class Presupuestocompdet(audit):
    idpresupuestocompdet = models.AutoField(primary_key=True)
    idpresupuestocompcab = models.ForeignKey(Presupuestocompcab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkpcd = None

    class Meta:
        db_table = 'presupuestocomp_det'


class Notacreditocompcab(audit):
    idnotacreditocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nronota = models.TextField()
    idproveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    deposito = models.TextField(blank=True, null=True)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pknc = None

    class Meta:
        db_table = 'notacreditocomp_cab'


class Notacreditocompdet(audit):
    idnotacreditocompdet = models.AutoField(primary_key=True)
    idnotacreditocompcab = models.ForeignKey(Notacreditocompcab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    deposito = models.TextField(blank=True, null=True)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkncd = None

    class Meta:
        db_table = 'notacreditocomp_det'


class Notadebitocompcab(audit):
    idnotadebitocompcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrodebito = models.TextField()
    idproveedor = models.DecimalField(max_digits=20, decimal_places=0)
    proveedor = models.TextField()
    ruc = models.TextField()
    timbrado = models.TextField()
    tipodoc = models.TextField()
    condicion = models.TextField(blank=True, null=True)
    fechavto = models.DateField(blank=True, null=True)
    fecharece = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    gravada5 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada10 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    gravada = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    exenta = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=2)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    pknd = None

    class Meta:
        db_table = 'notadebitocomp_cab'


class Notadebitocompdet(audit):
    idnotadebitocompdet = models.AutoField(primary_key=True)
    idnotadebitocompcab = models.ForeignKey(Notadebitocompcab, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pkndd = None

    class Meta:
        db_table = 'notadebitocomp_det'
