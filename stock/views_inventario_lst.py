from django.db import connections
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView, UpdateView, DeleteView
from openpyxl.compat import numbers
from openpyxl.styles import Alignment

from .forms import *
from django.contrib import messages
from reportlab.lib import colors
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from inicio.funcion import *
from django.shortcuts import redirect
import io
import csv
from reportlab.pdfgen import canvas
import time
import datetime
from datetime import datetime

from reportlab.lib.pagesizes import letter, landscape, inch, A4, A3, legal, B4, B5, A5, portrait
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from django.http import HttpResponse

def inv_inf_gral_listar(request):
    if not request.user.has_perm('stock.View_inventario_toma'):
        return redirect('views_inventario_lst')
    # -----------------------------------------------
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    deposito = request.GET.get('deposito', '')
    nrotoma = request.GET.get('nrotoma', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    inventario = Inventario_cab.objects.filter(idempresa=didempresa)
    if inventario.exists() and deposito:
        inventario = inventario.filter(deposito=deposito)
    if inventario.exists() and nrotoma:
        inventario = inventario.filter(nromov=nrotoma)
    if inventario.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        inventario = inventario.filter(fecha__gte=fecha_inicio, idempresa=didempresa, idsucursal=didsucursal)
    if inventario.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        inventario = inventario.filter(fecha__lte=fecha_fin, idempresa=didempresa, idsucursal=didsucursal)
        inventario = inventario.filter(fecha__gte=fecha_inicio, idempresa=didempresa, idsucursal=didsucursal)

    inventario = inventario.order_by('nromov')
    datos = []
    if inventario.count()>0:
        for objeto in inventario:
            datos= inv_inf_gral_datos(objeto, datos,'unidad',didempresa)
            datos= inv_inf_gral_datos(objeto, datos,'kilo',didempresa)

    context = {'datos':datos}  # Crear un diccionario de contexto
    return render(request, 'stock_inf/inv_gral_inf.html', context)

def inv_inf_gral_datos(objeto,datos,unidad,didempresa):
    nrotoma=objeto.nromov
    invdet = Inventario_det.objects.filter(idempresa=didempresa, nromov=nrotoma, unidad=unidad)
    if invdet.count()>0:
        fechaajuste = ([detalle.fechaajuste for detalle in invdet])
        costologico = sum([detalle.existlogica * detalle.costo for detalle in invdet]) if invdet else 0
        cantidadlogica = sum([detalle.existlogica for detalle in invdet]) if invdet else 0
        diferencia = sum([detalle.diferencia for detalle in invdet]) if invdet else 0
        difcosto = sum([detalle.difcosto for detalle in invdet]) if invdet else 0
        invdet = Inventario_toma.objects.filter(idempresa=didempresa, nromov=nrotoma, unidad=unidad) if invdet else 0
        costofisico = sum([detalle.exist * detalle.costo for detalle in invdet]) if invdet else 0
        cantidadfisica = sum([detalle.exist for detalle in invdet]) if invdet else 0
        cantdecimal = 3
        if unidad == 'unidad':
            cantdecimal = 0

        primera_fecha = fechaajuste[0]
        # fechaajuste = primera_fecha.strftime('%Y-%m-%d %H:%M:%S %Z')
        fechaajuste = primera_fecha.strftime('%d/%m/%Y')

        datos.append({
            'unidad': unidad,
            'fecha': objeto.fecha.strftime("%d/%m/%Y"),
            'fechaajuste': fechaajuste,
            'nromov': objeto.nromov,
            'deposito': objeto.deposito,
            'obs': objeto.obs,
            'costologico': formatnumver(costologico, 0),
            'cantidadlogica': formatnumver(cantidadlogica, cantdecimal),
            'costofisico': formatnumver(costofisico, 0),
            'cantidadfisica': formatnumver(cantidadfisica, cantdecimal),
            'difcosto': formatnumver(difcosto, 0),
            'difcantidad': formatnumver(diferencia, cantdecimal),
        })
    return datos

def inv_inf_det_listar(request):
    if not request.user.has_perm('stock.View_inventario_toma'):
        return redirect('views_inventario_lst')

    # -----------------------------------------------
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    deposito = request.GET.get('deposito', '')
    nrotoma = request.GET.get('nrotoma', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    inventario = Inventario_cab.objects.filter(idempresa=didempresa)
    if inventario.exists() and deposito:
        inventario = inventario.filter(deposito=deposito)
    if inventario.exists() and nrotoma:
        inventario = inventario.filter(nromov=nrotoma)
    if inventario.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        inventario = inventario.filter(fecha__gte=fecha_inicio, idempresa=didempresa, idsucursal=didsucursal)
    if inventario.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        inventario = inventario.filter(fecha__lte=fecha_fin, idempresa=didempresa, idsucursal=didsucursal)
        inventario = inventario.filter(fecha__gte=fecha_inicio, idempresa=didempresa, idsucursal=didsucursal)
    inventario = inventario.order_by('nromov')

    if inventario.count()==0:
        context = {'datos1':None,'datos2':None}  # Crear un diccionario de contexto
        return render(request, 'stock_inf/inv_det_inf.html', context)

    if inventario.count()>0:
        datos = []
        datosu = []
        datosk= []
        for i in range(1, 3):
            print(f"Iteración número {i}")
            if i == 1:
                unidad = 'unidad'
                datos = []

            if i == 2:
                unidad = 'kilo'
                datos = []

            for objeto in inventario:
                nrotoma= objeto.nromov
                invdet = Inventario_det.objects.filter(idempresa=didempresa,nromov=nrotoma,unidad=unidad)

                if invdet.count() > 0:
                    datos = []
                if invdet.count() > 0:
                    fechaajuste = ([detalle.fechaajuste for detalle in invdet])
                    tcostologico = sum([detalle.existlogica * detalle.costo for detalle in invdet]) if invdet else 0
                    tcantidadlogica = sum([detalle.existlogica for detalle in invdet]) if invdet else 0
                    tdiferencia = sum([detalle.diferencia for detalle in invdet]) if invdet else 0
                    tdifcosto = sum([detalle.difcosto for detalle in invdet])if invdet else 0
                    invtoma = Inventario_toma.objects.filter(idempresa=didempresa,nromov=nrotoma)
                    tcostofisico = sum([detalle.exist * detalle.costo for detalle in invtoma]) if invtoma else 0
                    tcantidadfisica = sum([detalle.exist for detalle in invtoma]) if invtoma else 0

                    primera_fecha = fechaajuste[0]
                    # fechaajuste = primera_fecha.strftime('%Y-%m-%d %H:%M:%S %Z')
                    fechaajuste = primera_fecha.strftime('%d/%m/%Y')
                    cantdecimal = 3
                    print (' unidad ' + str(unidad))
                    if unidad=='unidad':
                        cantdecimal =0

                    for objetodet in invdet:
                        invtoma = Inventario_toma.objects.filter(idempresa=didempresa, nromov=nrotoma,codigo=objetodet.codigo)
                        exist = sum([detalle.exist for detalle in invtoma]) if invtoma else 0
                        diferencia=exist-objetodet.existlogica
                        difcosto=diferencia*objetodet.costo
                        print(' datos ' + str(datos))

                        datos.append({
                        'fecha': objeto.fecha.strftime("%d/%m/%Y"),
                        'unidad': unidad,
                        'fechaajuste': fechaajuste,
                        'nromov': objeto.nromov,
                        'deposito': objeto.deposito,
                        'obs': objeto.obs,
                        'tcostologico': formatnumver(tcostologico, 0),
                        'tcantidadlogica': formatnumver(tcantidadlogica, cantdecimal),
                        'tcostofisico':formatnumver(tcostofisico, 0),
                        'tcantidadfisica': formatnumver(tcantidadfisica, cantdecimal),
                        'tdifcosto': formatnumver(tdifcosto, 0),
                        'tdifcantidad': formatnumver(tdiferencia, cantdecimal),
                        'codigo': objetodet.codigo,
                        'descripcion': objetodet.descripcion,
                        'existlogica': formatnumver(objetodet.existlogica, cantdecimal),
                        'existfisica': formatnumver(exist, cantdecimal),
                        'diferencia': formatnumver(diferencia, cantdecimal),
                        'costo': formatnumver(objetodet.costo, 0),
                        'difcosto': formatnumver(difcosto, 0),
                        })

                if i == 1:
                    datosu = datos
                if i == 2:
                    datosk = datos

    context = {'datos1':datosu,'datos2':datosk}  # Crear un diccionario de contexto
    return render(request, 'stock_inf/inv_det_inf.html', context)






