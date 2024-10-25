from django.db import models

# Create your models here.

from inicio.models import *

class Cuentacontable(audit):
    idcuentacontable = models.AutoField(primary_key=True)
    cuenta = models.TextField(null=True, blank=True)
    codigocta = models.TextField(null=True, blank=True)
    denominacion=models.TextField(null=True, blank=True)
    nivel=models.IntegerField(default=0)
    naturaleza=models.TextField(null=True, blank=True)
    asentable = models.TextField(null=True, blank=True)
    centro_costo=models.TextField(null=True, blank=True)
    moneda=models.TextField(null=True, blank=True)
    tipo_cambio=models.TextField(null=True, blank=True)
    n1 = models.IntegerField(default=0)
    n2 = models.IntegerField(default=0)
    n3 = models.IntegerField(default=0)
    n4 = models.IntegerField(default=0)
    n5 = models.IntegerField(default=0)
    n6 = models.IntegerField(default=0)
    n7 = models.IntegerField(default=0)
    cuenta1 = models.TextField(blank=True, null=True)
    cuenta2 = models.TextField(blank=True, null=True)
    cuenta3 = models.TextField(blank=True, null=True)
    cuenta4 = models.TextField(blank=True, null=True)
    cuenta5 = models.TextField(blank=True, null=True)
    cuenta6 = models.TextField(blank=True, null=True)
    cuenta7 = models.TextField(blank=True, null=True)
    pkctacont = None
    class Meta:
        db_table = 'cuentacontable'
        constraints = [
            models.UniqueConstraint(fields=['cuenta', 'idempresa'], name='unique_cuenta_empresa')
        ]


class asiento(audit):
    idasiento = models.AutoField(primary_key=True)
    nroasiento = models.IntegerField(default=0)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    fecha_hora = models.DateTimeField()
    debe = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    habilitado = models.BooleanField(default=True , null=True)
    pkas = None
    class Meta:
        db_table = 'asiento'

class asiento_det(audit):
    idasientodet = models.AutoField(primary_key=True)
    idasiento = models.ForeignKey(asiento, on_delete=models.DO_NOTHING)
    idcuentacontable = models.ForeignKey(Cuentacontable, on_delete=models.DO_NOTHING)
    nroasiento = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    fecha_hora = models.DateTimeField()
    cuenta = models.TextField(null=True, blank=True)
    denominacion=models.TextField(null=True, blank=True)
    debe = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    habilitado = models.BooleanField(default=True , null=True)
    pkasdet = None
    class Meta:
        db_table = 'asiento_det'
