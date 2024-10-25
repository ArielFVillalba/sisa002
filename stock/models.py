from django.db import models
# Create your models here.
from inicio.models import *

class Articulo(audit):
    idarticulo = models.AutoField(primary_key=True)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=4, decimal_places=0,default=0)
    recarga_por=models.DecimalField(max_digits=20, decimal_places=0)
    codigoflia = models.TextField(blank=True, null=True)
    habilitado = models.BooleanField(default=True , null=True)
    muevestock = models.BooleanField(default=True , null=True)
    pka=None
    familia1=None
    familia2=None
    familia3=None
    familia4=None
    familia5=None
    familia6=None
    familia7=None

    class Meta:
        db_table = 'articulos'
        unique_together = ('codigo', 'idempresa')


class familia(audit):
    idfamilia = models.AutoField(primary_key=True)
    codigo = models.TextField()
    n1 = models.IntegerField(default=0)
    n2 = models.IntegerField(default=0)
    n3 = models.IntegerField(default=0)
    n4 = models.IntegerField(default=0)
    n5 = models.IntegerField(default=0)
    n6 = models.IntegerField(default=0)
    n7 = models.IntegerField(default=0)
    familia1 = models.TextField(blank=True, null=True)
    familia2 = models.TextField(blank=True, null=True)
    familia3 = models.TextField(blank=True, null=True)
    familia4 = models.TextField(blank=True, null=True)
    familia5 = models.TextField(blank=True, null=True)
    familia6 = models.TextField(blank=True, null=True)
    familia7 = models.TextField(blank=True, null=True)
    pkf=None

    class Meta:
        db_table = 'familia'



class Deposito(audit):
    iddeposito = models.AutoField(primary_key=True)
    deposito = models.TextField(blank=True, null=True)
    idsucdep = models.IntegerField()
    sucursal = models.TextField()
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = 'deposito'


 #   mi_entero = models.IntegerField(min_value=0, max_value=100)

class Movdepcab(audit):
    idmovdepcab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nromov = models.TextField()
    depsalida = models.TextField()
    depentrada = models.TextField()
    obs = models.TextField(blank=True, null=True)
    pkmd =None
    class Meta:
        db_table = 'movdep_cab'


class Movdepdet(audit):
    idmovdepdet = models.AutoField(primary_key=True)
    idmovdepcab = models.ForeignKey(Movdepcab,on_delete=models.DO_NOTHING)
    orden= models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idarticulo = models.ForeignKey(Articulo,on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.DecimalField(max_digits=4, decimal_places=0)
    depsalida= models.TextField()
    depentrada = models.TextField()
    usuario = models.TextField()
    pkmdd =None

    class Meta:
        db_table = 'movdep_det'

class Existencia(audit):
    codigo = models.DecimalField(max_digits=20, decimal_places=0)
    deposito = models.TextField()
    cantidad =models.DecimalField(max_digits=20, decimal_places=3)
    unidad = models.TextField()
    class Meta:
        db_table = 'existencia'

class Inventario_cab(audit):
    idinventario_cab = models.AutoField(primary_key=True)
    fecha = models.DateField()
    fechagenerado = models.DateField(null=True)
    fechatoma = models.DateField(null=True)
    fechaajuste = models.DateField(null=True)
    nromov = models.TextField()
    deposito = models.TextField()
    obs = models.TextField(blank=True, null=True)
    familias = models.TextField(blank=True, null=True)
    idempresaselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idsucursalselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    operador = models.TextField()

    class Meta:
        db_table = 'inventario_cab'

class Inventario_det(audit):
    idinventario_det = models.AutoField(primary_key=True)
    idinventario_cab = models.ForeignKey(Inventario_cab,on_delete=models.DO_NOTHING)
    idarticulo = models.ForeignKey(Articulo,on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    codigoflia = models.TextField()
    fechagenerado = models.DateTimeField(null=True, blank=True)
    fechatoma = models.DateTimeField(null=True, blank=True)
    fechaajuste = models.DateTimeField(null=True, blank=True)
    nromov = models.TextField()
    deposito = models.TextField()
    obs = models.TextField(blank=True, null=True)
    idempresaselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idsucursalselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    existlogica = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    exist = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    diferencia = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    costo = models.DecimalField(max_digits=20, decimal_places=0,default=0)
    difcosto = models.DecimalField(max_digits=20, decimal_places=0,default=0)
    operador = models.TextField()
    ajustado = models.BooleanField(default=False , null=True)

    class Meta:
        db_table = 'inventario_det'


class Inventario_toma(audit):
    idinventario_toma = models.AutoField(primary_key=True)
    idinventario_det = models.IntegerField()
    idinventario_det = models.ForeignKey(Inventario_det,on_delete=models.DO_NOTHING)
    idinventario_cab = models.ForeignKey(Inventario_cab,on_delete=models.DO_NOTHING)
    idarticulo = models.ForeignKey(Articulo,on_delete=models.DO_NOTHING)
    codigo = models.DecimalField(max_digits=12, decimal_places=0)
    descripcion = models.TextField()
    unidad = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    codigoflia = models.TextField()
    fechaajuste = models.DateTimeField(null=True, blank=True)
    fechatoma = models.DateTimeField(null=True, blank=True)
    fechaajuste = models.DateTimeField(null=True, blank=True)
    nromov = models.TextField()
    deposito = models.TextField()
    obs = models.TextField(blank=True, null=True)
    idempresaselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    idsucursalselec = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    existlogica = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    exist = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    diferencia = models.DecimalField(max_digits=20, decimal_places=3,default=0)
    costo = models.DecimalField(max_digits=20, decimal_places=0,default=0)
    difcosto = models.DecimalField(max_digits=20, decimal_places=0,default=0)
    operador = models.TextField()

    class Meta:
        db_table = 'inventario_toma'
