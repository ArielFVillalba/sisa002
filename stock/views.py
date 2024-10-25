import os

from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from inicio.funcion import *
from inicio.models import Sucursal
from sisa import settings
from stock.models import Deposito, Existencia, Articulo
from decimal import Decimal
from django.shortcuts import render, redirect

con1=1

def menustock(request):
    if request.user.is_authenticated:
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        #didempresa = desencriptar_datos(idempresa, skey)
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa)<1 or int(didsucursal)<1:
            return redirect('login')

        return render(request, "stock/menustock.html")
    else:
        return redirect('login')

    #request.COOKIES.get
    #usu = request.COOKIES.get('usuario')
    #psw = request.COOKIES.get('contraseña')
    #tipo = "dep"
    #modulo = "compras"
    #n = "{" + usu + "," + psw+ "," +  tipo + "," +  modulo +"}"
    #sql = "select controlingresomod('" + n + "');"
    #valor1 = seleccionar_datos2(con1, sql, usu, psw)
    #if valor1 == 'true':
    #else:
    #    return render(request, template_name="base/menu.html/")

def deposito(request):
    #usu = request.COOKIES.get('usuario')
    #psw = request.COOKIES.get('contraseña')
    #tipo = "dep"
    #modulo = "compras"
    #n = "{" + usu + "," + psw+ "," +  tipo + "," +  modulo +"}"
    #sql = "select controlingresomod('" + n + "');"
    #valor1 = seleccionar_datos2(con1, sql, usu, psw)
    #if valor1 == 'true':
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    # didempresa = desencriptar_datos(idempresa, skey)
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    return render(request, "stock/deposito.html")
    #else:
    #    return render(request, template_name="base/menu.html/")




def deposito_agregar(request):
    if request.method == 'POST':
        deposita = request.POST['deposito'].upper()
        isucursal = request.POST['sucursal'].upper()

        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        #didempresa = desencriptar_datos(idempresa, skey)
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa)<1 or int(didsucursal)<1:
            return redirect('login')

        obj = Sucursal.objects.filter(sucursal=isucursal ,idempresa=didempresa)
        idsucdep = ([str(detalle.idsucursal) for detalle in obj])[0]
        deposito = Deposito()
        deposito.deposito = deposita
        deposito.idsucdep =didsucursal
        deposito.sucursal = didempresa
        deposito.idempresa = idempresa
        deposito.idsucursal = idsucursal
        deposito.save()

        response = {'success': True}
        return JsonResponse(response)

def deposito_editar(request):
    if request.method == 'POST':
        ideposito = request.POST['deposito'].upper()
        isucursal = request.POST['sucursal'].upper()
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        #didempresa = desencriptar_datos(idempresa, skey)
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa)<1 or int(didsucursal)<1:
            return redirect('login')

        obj = Sucursal.objects.filter(sucursal=isucursal ,idempresa=didempresa)
        idsucdep = ([str(detalle.idsucursal) for detalle in obj])[0]

        var=True

        if ideposito is None or ideposito == "":
            var=False
        if isucursal is None or isucursal == "":
            var=False

        if var == False:
            response = {'success': False}
            return JsonResponse(response)

        habilitado = True
        diddep=""
        objetos = Deposito.objects.filter(deposito=ideposito,idempresa=didempresa)
        for objeto in objetos:
            diddep = objeto.iddeposito
        didsucursal
        if diddep:
            deposito = get_object_or_404(Deposito, iddeposito=diddep)
            deposito.idsucdep = idsucdep
            deposito.sucursal = isucursal
            deposito.save()

        if not diddep:
            deposito = Deposito()
            deposito.deposito = ideposito
            deposito.sucursal = isucursal
            deposito.idsucdep = idsucdep
            deposito.habilitado = habilitado
            deposito.idempresa = didempresa
            deposito.idsucursal = didsucursal
            deposito.save()

        response = {'success': True}
        return JsonResponse(response)


def deposito_eliminar(request,pk_token):
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    # didempresa = desencriptar_datos(idempresa, skey)
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    deposit = Deposito.objects.filter(deposito=pk_token, idempresa=didempresa)
    deposit.delete()
    response = {'success': True}
    return JsonResponse(response)

def deposito_listar(request):
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    # didempresa = desencriptar_datos(idempresa, skey)
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    objetos = Deposito.objects.filter(idempresa=didempresa)
    datos = []
    for objeto in objetos:
        datos.append({
            'deposito': objeto.deposito,
            'sucursal': objeto.sucursal,
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos})
    return Response


def cmbdep(request):
    if request.method == 'POST':
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        #didempresa = desencriptar_datos(idempresa, skey)
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa)<1 or int(didsucursal)<1:
            return redirect('login')
        deposito = Deposito.objects.filter(idempresa=didempresa).values_list('deposito', flat=True)
        nombres = list(deposito)
        Response = JsonResponse({'datos': nombres})
        return Response


def sucursalesdep(request):
    sucursales = []
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    # didempresa = desencriptar_datos(idempresa, skey)
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    objetos = Sucursal.objects.filter(idempresa=didempresa)
    i = 0
    for objeto in objetos:

        sucursales.append({
            'idsucural': objeto.idsucursal,
            'sucursal': objeto.sucursal,
        })

    Response = JsonResponse({'datos':sucursales})
    return Response

def actualizarexistencia(codigo,cantentrada,cantsalida,depentrada,depsalida,didempresa,didsucursal):
    #print("------  actualizarexistencia ")
    #print(" didempresa "+ str(didempresa) + " codigo "+ str(codigo) )
    #print(" cantentrada "+ str(cantentrada) + " cantsalida "+ str(cantsalida) )
    #print(" depentrada "+ str(depentrada) + " depsalida "+ str(depsalida) )

    art = Articulo.objects.filter(codigo=codigo,idempresa=didempresa)
    cantart = art.count()
    if cantart > 0:

        if depsalida and cantsalida:
            objsalida = Existencia.objects.filter(idempresa=didempresa, codigo=codigo,deposito=depsalida)
            cantr = objsalida.count()
            if cantr > 0:
                for objeto in objsalida:
                    objeto.cantidad =objeto.cantidad-Decimal(cantsalida)
                    objeto.save()
            else:
                crearexistencia(codigo,0,cantsalida,'',depsalida,didempresa,didsucursal)

        if depentrada and cantentrada:
            objentrada = Existencia.objects.filter(idempresa=didempresa, codigo=codigo,deposito=depentrada)
            cantr = objentrada.count()
            if cantr > 0:
                for objeto in objentrada:
                    objeto.cantidad = objeto.cantidad + Decimal(cantentrada)
                    objeto.save()
            else:
                crearexistencia(codigo,cantentrada,0,depentrada,'',didempresa,didsucursal)


def crearexistencia(codigo,cantent,cantsal,depent,depsal,didempresa,didsucursal):
    cantidad=0

    articulo = Articulo.objects.filter(idempresa=didempresa,codigo=codigo)
    unidad = ([detalle.unidad  for detalle in articulo])[0]

    if depent:
        cantidad=cantent
        dep=depent
    if depsal:
        cantidad=cantsal * -1
        dep=depsal

    exist = Existencia()
    exist.codigo = codigo
    exist.deposito = dep
    exist.cantidad = cantidad
    exist.unidad = unidad
    exist.idempresa = didempresa
    exist.idsucursal = didsucursal
    exist.save()

def verificardepostio(deposito,didempresa):
    valido = False
    objetos = Deposito.objects.filter(idempresa=didempresa,deposito=deposito)
    if  objetos:
        valido = True
    return valido