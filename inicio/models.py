from django.db import models
from crum import get_current_user
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models

class audit(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    #created_by = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    #user = models.DateTimeField(auto_now=True)
    #user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    idempresa = models.IntegerField(default=0)
    idsucursal = models.IntegerField(default=0)
    class Meta:
        abstract=True

class auditoria(models.Model):
    usuario = models.TextField()
    fecha_hora = models.DateTimeField()
    accion = models.TextField()
    usuario = models.TextField()
    tabla = models.TextField()
    old = models.JSONField()
    new = models.JSONField()

    class Meta:
        db_table = 'auditoria'


class Empresa(models.Model):
    idempresa = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=255)

    class Meta:
        db_table = 'empresa'


class Sucursal(models.Model):
    idsucursal = models.AutoField(primary_key=True)
    idempresa = models.DecimalField(max_digits=20, decimal_places=0)
    sucursal = models.CharField(max_length=255)

    class Meta:
        db_table = 'sucursal'

class userempresa(models.Model):
    iduserempresa = models.AutoField(primary_key=True)
    idusuario = models.DecimalField(max_digits=20, decimal_places=0)
    idempresa = models.DecimalField(max_digits=20, decimal_places=0)
    idsucursal = models.DecimalField(max_digits=20, decimal_places=0)

    class Meta:
        db_table = 'userempresa'





