from django.db import models

# Create your models here.

from inicio.models import *


class cajaventapago(audit):
    idcajaventapago= models.AutoField(primary_key=True)
    idventacab = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)
    formapago = models.TextField()
    descripcion = models.TextField()
    pago = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    monto = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    moneda = models.TextField()
    cotizacion = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        db_table = 'cajaventapago'


class serie(audit):
    idserie= models.AutoField(primary_key=True)
    serie = models.TextField()
    class Meta:
        db_table = 'serie'

class seriedet(audit):
    idseriedet= models.AutoField(primary_key=True)
    idserie = models.IntegerField(default=0,null=True)
    iddocumentos = models.IntegerField(default=0,null=True)
    timbrado = models.TextField()
    inicio = models.IntegerField(default=0)
    fin = models.IntegerField(default=0)
    correlativa = models.IntegerField(default=0)
    deposito = models.TextField(null=True)
    nrocaja = models.IntegerField(default=0)
    idusuario = models.IntegerField(default=0)
    pksd = None
    serie = None
    documento = None
    usuario = None

    class Meta:
        db_table = 'seriedet'

class documentos(audit):
    iddocumentos= models.AutoField(primary_key=True)
    documento = models.TextField()

    class Meta:
        db_table = 'documentos'

class cajaformadepago(audit):
    idformadepago= models.AutoField(primary_key=True)
    formadepago = models.TextField()

    class Meta:
        db_table = 'cajaformadepago'

class cajatipomov(audit):
    idcajatipomov= models.AutoField(primary_key=True)
    tipomov = models.TextField()

    class Meta:
        db_table = 'cajatipomov'

class cajaapertcierre(audit):
    idcajaapertcierre= models.AutoField(primary_key=True)
    fecha = models.DateField()
    apertura = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    totalfactura = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    facturaini = models.TextField()
    facturafin = models.TextField()
    timbrado = models.TextField()
    iddocumentos = models.IntegerField(default=0)
    nrocaja = models.IntegerField(default=0)
    idusuario = models.IntegerField(default=0)
    usuario = None

    class Meta:
        db_table = 'cajaapertcierre'

class cajaapertcierredet(audit):
    idcajaapertcierredet= models.AutoField(primary_key=True)
    idcajaapertcierre = models.IntegerField(default=0)
    tipomov = models.TextField()
    monto = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tipo = models.TextField()

    class Meta:
        db_table = 'cajaapertcierredet'
