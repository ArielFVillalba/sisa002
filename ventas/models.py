from datetime import timezone

from django.db import models

# Create your models here.

from inicio.models import *
from sisa.signals import *
from stock.models import Articulo


class Cliente(audit):
    idcliente= models.AutoField(primary_key=True)
    nombre = models.TextField()
    cedula = models.TextField(blank=True, null=True)
    fechanac = models.DateField(blank=True, null=True)
    ruc = models.TextField(blank=True, null=True)
    timbrado = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    mail = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    pkcl= None

    class Meta:
        db_table = 'cliente'


class Ventacab(audit):
    idventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    fecha_hora = models.DateTimeField()  # Correcto
    nrofactura = models.TextField()
    idcliente = models.DecimalField(max_digits=20, decimal_places=0)
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    deposito = models.TextField(blank=True, null=True)
    nrocaja = models.IntegerField(default=0)
    serie = models.IntegerField(default=0)
    idtipodoc = models.IntegerField(default=0)

    pkf=None

    class Meta:
        db_table = 'venta_cab'

class Ventadet(audit):
    idventadet = models.AutoField(primary_key=True)
    idventacab = models.ForeignKey(Ventacab, on_delete=models.DO_NOTHING)
    orden= models.IntegerField(default=0)
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
    nrocaja = models.IntegerField(default=0)
    serie = models.IntegerField(default=0)

    pkfd=None

    class Meta:
        db_table = 'venta_det'


class Ventascuotas(audit):
    idventascuotas = models.AutoField(primary_key=True)
    idventacab = models.ForeignKey(Ventacab, on_delete=models.DO_NOTHING)
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fechavto = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    class Meta:
        db_table = 'ventascuotas'


class Pagoclientes(audit):
    idpagocliente = models.AutoField(primary_key=True)
    fecha = models.DateField()
    recibo = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente = models.TextField()
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    class Meta:
        db_table = 'pagocliente'


class Pagocliforma(audit):
    idpagocliforma = models.AutoField(primary_key=True)
    idpagocliente = models.DecimalField(max_digits=20, decimal_places=0)
    idtipopago = models.DecimalField(max_digits=20, decimal_places=0)
    fecha = models.DateField()
    banco  = models.TextField()
    ctacte  = models.TextField()
    nrodoc  = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagopcliforma'

class Pagoclifact(audit):
    idpagoclifact = models.AutoField(primary_key=True)
    idpagocliente = models.DecimalField(max_digits=20, decimal_places=0)
    idventascuotas = models.DecimalField(max_digits=20, decimal_places=0)
    orden = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    fecha = models.DateField()
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    monto = models.DecimalField(max_digits=12, decimal_places=3)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'pagoclifact'



class Ordenventacab(audit):
    idordenventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nroorden = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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

    pkov=None

    class Meta:
        db_table = 'ordenventa_cab'

class Ordenventadet(audit):
    idordenventadet = models.AutoField(primary_key=True)
    idordenventacab = models.ForeignKey(Ordenventacab, on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
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

    pkovd=None

    class Meta:
        db_table = 'ordenventa_det'





class Pedidoventacab(audit):
    idpedidoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropedido = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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

    pkpv =None

    class Meta:
        db_table = 'pedidoventa_cab'

class Pedidoventadet(audit):
    idpedidoventadet = models.AutoField(primary_key=True)
    idpedidoventacab = models.ForeignKey(Pedidoventacab, on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
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

    pkpvd = None
    class Meta:
        db_table = 'pedidoventa_det'


class Presupuestoventacab(audit):
    idpresupuestoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nropresupuesto = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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

    pkpv= None

    class Meta:
        db_table = 'presupestoventa_cab'

class Presupuestoventadet(audit):
    idpresupuestoventadet = models.AutoField(primary_key=True)
    idpresupuestoventacab = models.ForeignKey(Presupuestoventacab, on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
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

    pkpvd= None

    class Meta:
        db_table = 'presupuestoventa_det'

class Notacreditoventacab(audit):
    idnotacreditoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nronota = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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

    pknc=None
    class Meta:
        db_table = 'notacreditoventa_cab'

class Notacreditoventadet(audit):
    idnotacreditoventadet = models.AutoField(primary_key=True)
    idnotacreditoventacab = models.ForeignKey(Notacreditoventacab, on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
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

    pkncd=None

    class Meta:
        db_table = 'notacreditoventa_det'

class Notadebitoventacab(audit):
    idnotadebitoventacab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nrodebito = models.TextField()
    idcliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    cliente= models.TextField()
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

    pknd=None

    class Meta:
        db_table = 'notadebitoventa_cab'

class Notadebitoventadet(audit):
    idnotadebitoventadet = models.AutoField(primary_key=True)
    idnotadebitoventacab = models.ForeignKey(Notadebitoventacab, on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
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

    pkndd =None
    class Meta:
        db_table = 'notadebitoventa_det'

