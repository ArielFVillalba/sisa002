from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

import sisa.signals
from caja.models import cajaventapago, seriedet, cajaapertcierre
from sisa.mixins import ValidarPermisoMixin
from django.dispatch import receiver
from inicio.funcion import *

from django.contrib import messages
from django.core.serializers import json
from sisa.signals import *
from stock.models import Articulo
from ventas.forms import VentacabForm
from ventas.models import *
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from django.forms.models import model_to_dict

from django.utils import timezone



def ventacaja_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'caja/ventacaja_filt.html')

def ventacaja_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idcliente = request.GET.get('idcliente', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    tipodoc = request.GET.get('tipodoc', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    ventacab = Ventacab.objects.all(idempresa=didempresa,idsucursal=didsucursal)
    if idcliente == '':
        idcliente = 0
    if ventacab.exists() and int(idcliente) >= 1:
        ventacab = ventacab.filter(idcliente_id=idcliente)
    if ventacab.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        ventacab = ventacab.filter(fecha__gte=fecha_inicio)
    if ventacab.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        ventacab = ventacab.filter(fecha__lte=fecha_fin)
    if ventacab.exists() and tipodoc:
        ventacab = ventacab.filter(tipodoc=tipodoc)

    for objeto in ventacab:
        objeto.pkf = encriptar_datos2(objeto.idventacab,request)
        objeto.save()

    cadena = ""
    return render(request, 'caja/ventacaja_listar.html', {'ventacab': ventacab, 'cadena': cadena})


def ventacaja_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    if cadena == "*":
        ventacab = Ventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/ventacab_listar.html')

    qs = Ventacab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Cliente.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Cliente.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Cliente.objects.filter(cliente__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Cliente.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    ventacab = qs
    return render(request, 'caja/ventacaja_listar.html', {'ventacab': ventacab, 'cadena': cadena})


class ventacaja_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_ventacab'
    model = VentacabForm
    form_class = VentacabForm
    template_name = 'caja/ventacaja.html'
    success_url = reverse_lazy('ventacaja_cargar')

    def get(self, request,pk_token):
        ventacab = None
        request.session['caja'] = 1
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        factura=0
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            ventacab = Ventacab.objects.get(idventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria
            obj = Ventacab.objects.filter(idventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria
            factura = ([(detalle.nrofactura) for detalle in obj])[0]
            print('factura ' + str(factura))

        else:

            idempresa = request.session.get('idempresa')
            idsucursal = request.session.get('idsucursal')
            didempresa = desencriptar_datos2(idempresa, request)
            didsucursal = desencriptar_datos2(idsucursal, request)
            if int(didempresa) < 1 or int(didsucursal) < 1:
                return redirect('login')

            request.session['pkfa'] = pk_token

            cajaapertc = cajaapertcierre.objects.filter(idempresa=didempresa, idsucursal=didsucursal, facturafin='')
            cantr = cajaapertc.count()
            if cantr == 0:
                return redirect('cajaapertura_cargar')

            id_usuario = request.user.id
            obj = seriedet.objects.filter(idusuario=id_usuario, iddocumentos=1, idempresa=didempresa)
            cantr = obj.count()
            factura=0
            timbrado=0
            if cantr > 0:
                factura = ([(detalle.correlativa) for detalle in obj])[0]
                print('correlativa ' + str(factura))

                timbrado = ([(detalle.timbrado) for detalle in obj])[0]

            obj = Ventacab.objects.filter(nrofactura=factura, idempresa=didempresa, timbrado=timbrado)  # Recuperar la compra por su clave primaria
            cantr = obj.count()
            if cantr > 0:

                idventacab = ([(detalle.idventacab) for detalle in obj])[0]
                pk_token = encriptar_datos2(idventacab,request)  # Asegúrate de que esta función esté implementada correctamente
                ventacab = Ventacab.objects.get(idventacab=idventacab)  # Recuperar la compra por su clave primaria
                factura=([(detalle.nrofactura) for detalle in obj])[0]

                return redirect('ventacaja_cargar', pk_token=str(pk_token))

            #idventacab=int(ventacabaux(idempresa, idsucursal, skey,id_usuario))
            #ventacab = Ventacab.objects.get(idventacab=idventacab)  # Recuperar la compra por su clave primaria
            #pk_token = encriptar_datos(idventacab,skey)  # Asegúrate de que esta función esté implementada correctamente

        #print(" total " + str(total) + " saldo " + str(saldo))


        request.session['caja'] = 1
        context = {'ventacab': ventacab}  # Crear un diccionario de contexto
        context['title'] = '  CAJA -  VENTA  '
        context['sidr'] = '/Ventacaja/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['factura'] = factura
        context['hab1']= True
        context['hab2']= False
        context['hab3']= "display: none;"
        context['hab4']= "display: block;"

        return render(request, self.template_name, context)


class ventacierre_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_ventacab'
    model = VentacabForm
    form_class = VentacabForm
    template_name = 'caja/ventacaja.html'
    success_url = reverse_lazy('ventacaja_cargar')

    def get(self, request,pk_token):

        ventacab = None
        if pk_token == "0":
            return redirect('ventacaja_cargar', pk_token=0)

        else:
            idventacab = desencriptar_datos2(pk_token,request)
            ventacab = Ventacab.objects.get(idventacab=idventacab)  # Recuperar la compra por su clave primaria
            request.session['pkfa'] = pk_token

            idempresa = request.session.get('idempresa')
            idsucursal = request.session.get('idsucursal')
            didempresa = desencriptar_datos2(idempresa, request)
            didsucursal = desencriptar_datos2(idsucursal, request)
            if int(didempresa) < 1 or int(didsucursal) < 1:
                return redirect('login')
            #idventacab=int(ventacabaux(idempresa, idsucursal, skey))
            #ventacab = Ventacab.objects.get(idventacab=idventacab)  # Recuperar la compra por su clave primaria
            #pk_token = encriptar_datos(idventacab,skey)  # Asegúrate de que esta función esté implementada correctamente

        detalles = Ventadet.objects.filter(idventacab=idventacab)
        total = int(sum([detalle.cantidad * detalle.precio for detalle in detalles]))
        detalles = cajaventapago.objects.filter(idventacab=idventacab)
        saldo =int(total-sum([detalle.monto for detalle in detalles]))
        #print(" total " + str(total) + " saldo " + str(saldo))
        total= f"{(total):,.0f}"
        saldo= f"{(saldo):,.0f}"
        #print(" total " + str(total) + " saldo " + str(saldo))


        context = {'ventacab': ventacab}  # Crear un diccionario de contexto
        context['title'] = ' CIERRE  '
        context['sidr'] = '/Ventacaja/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= False
        context['hab2']= True
        context['hab4']= "display: none;"
        context['hab3']= "display: block;"
        context['total']= str(total)
        context['saldo']= str(saldo)

        return render(request, self.template_name, context)

def ventacabaux(didempresa,didsucursal,id_usuario):

    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Formatear la fecha como año-mes-día
    fecha = fecha_actual.strftime("%Y-%m-%d")
    objetos = seriedet.objects.filter(idusuario=id_usuario,iddocumentos=1,idempresa=didempresa)
    cantr = objetos.count()

    for dato in objetos:
        factura=dato.correlativa
        timbrado=dato.timbrado
        nrocaja =dato.nrocaja
        serie =dato.idserie
        idtipodoc=dato.iddocumentos
        deposito=dato.deposito


        obj = Ventacab.objects.filter(nrofactura=factura, idempresa=didempresa,timbrado=timbrado)  # Recuperar la compra por su clave primaria
        cantr = obj.count()

        if cantr > 0:
            idventacab = ([(detalle.idventacab) for detalle in obj])[0]
            return idventacab
        else:
            cliente_instance = Cliente.objects.get(pk=int(1))  # Asegúrate de que `idcompracab` sea un entero
            print("control fecha hora "+ str(timezone.now()))
            venta = Ventacab()
            venta.fecha = fecha
            venta.fecha_hora = timezone.now()  # Asigna la fecha y hora actual correctamente
            venta.nrofactura = factura
            venta.timbrado = timbrado
            venta.idempresa = didempresa
            venta.idsucursal = didsucursal
            venta.tipodoc = 'contado'
            venta.deposito = deposito
            venta.cotizacion = 1
            venta.moneda = 'gs'
            venta.idcliente=cliente_instance
            venta.total=0
            venta.nrocaja=nrocaja
            venta.serie=serie
            venta.idtipodoc=idtipodoc
            venta.save()
            idventacab=venta.idventacab
            return idventacab

def ventacabauxant(didempresa,didsucursal,id_usuario):
    obj = Ventacab.objects.filter(total=0,idempresa=didempresa,idsucursal=didsucursal)  # Recuperar la compra por su clave primaria
    cantr = obj.count()

    if cantr>0:
        idventacab = ([(detalle.idventacab) for detalle in obj])[0]
        return idventacab
    else:
        # Obtener la fecha actual
        fecha_actual = datetime.now()
        # Formatear la fecha como año-mes-día
        fecha = fecha_actual.strftime("%Y-%m-%d")

        objetos = seriedet.objects.filter(idusuario=id_usuario,iddocumentos=1,idempresa=didempresa)
        for dato in objetos:
            factura=dato.correlativa
            timbrado=dato.timbrado
            nrocaja =dato.nrocaja
            serie =dato.idserie
            idtipodoc=dato.iddocumentos
            deposito=dato.deposito

            venta = Ventacab()
            venta.fecha = fecha
            venta.nrofactura = factura
            venta.timbrado = timbrado
            venta.idempresa = didempresa
            venta.idsucursal = didsucursal
            venta.tipodoc = 'contado'
            venta.deposito = deposito
            venta.cotizacion = 1
            venta.moneda = 'gs'
            venta.idcliente=0
            venta.total=0
            venta.nrocaja=nrocaja
            venta.serie=serie
            venta.idtipodoc=idtipodoc
            venta.save()
            idventacab=venta.idventacab
        return idventacab


class ventacaja_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_ordenventacab'

    model = Ventacab
    form_class = VentacabForm
    template_name = 'caja/ventacaja.html'
    success_url = reverse_lazy('ventacaja_crear')
    def dispatch(self, *args, **kwargs):
        return super(ventacaja_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR VENTA '
        context['sidr'] = '/ventacaja/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form,request):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        Ventacab = form.save(commit=False)
        Ventacab.idempresa = idempresa
        Ventacab.idsucursal = idsucursal
        Ventacab.save()

        messages.success(self.request, 'ventas creado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ventacaja_cargar', pk_token=str(pk_encriptado))

class ventacaja_editar(UpdateView):
    permission_required = 'ventas.change_ordenventacab'
    model = Ventacab
    form_class = VentacabForm
    template_name = 'ventas/ventacaja.html'
    success_url = '/ventacaja/0/listar/'

    def get_object(self, queryset=None):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Ventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR  VENTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/ventacaja/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'editado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ventacaja_cargar', pk_token=str(pk_encriptado))

class ventacaja_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_ventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,self.request)
            instance = get_object_or_404(Ventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'orden eliminado exitosamente.')
            return redirect('ventacaja_cargar', pk_token=0)
        else:
            return redirect('ventacaja_cargar', pk_token=str(pk_token))

def ventadet_caja_listar(request):
    if not request.user.has_perm('ventas.view_ventadet'):
        datos = None
        Response = JsonResponse(
            {'datos': datos, 'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    idventacab = request.POST['pkf']
    idventacab = desencriptar_datos2(idventacab,request)

    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Ventadet.objects.filter(idventacab=idventacab).order_by('orden')
    if int(orden) >= 1:
        objetos = Ventadet.objects.filter(idventacab=idventacab, orden=orden)
    datos = []

    for objeto in objetos:
        articulos = Articulo.objects.filter(codigo=float(objeto.codigo),idempresa=didempresa)
        uni = ([(detalle.unidad) for detalle in articulos])[0]
        cantidad= f"{(objeto.cantidad):.3f}"
        if uni == 'UNIDAD':
            cantidad = f"{(objeto.cantidad):.0f}"

        datos.append({
            'pkfd': encriptar_datos2(objeto.idventadet, request),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad':cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos, 'success': True, 'message': ''})
    return Response


def actventacaja(idventacab):

    #gravada10 = Ventadet.objects.filter(iva=10,idventacab=idventacab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Ventadet.objects.filter(iva=5,idventacab=idventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ventadet.objects.filter(iva=10, idventacab=idventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ventadet.objects.filter(iva=0, idventacab=idventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Ventacab.objects.filter(idventacab=idventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
        return total


def ventadetcaja_guardar(request):
    if not request.user.has_perm('ventas.add_ventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')



    if request.method == 'POST':
        idventacab = request.POST['pkf']
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']
        orden = request.POST['orden']

        id_usuario = request.user.id
        if idventacab != "0":
            idventacab = desencriptar_datos2(idventacab,request)
        if idventacab == "0":
            idventacab=ventacabaux(didempresa, didsucursal, id_usuario)

        if idventacab == 0:
            return redirect('ventacaja_cargar', pk_token=str(0))

        cantr = Ventadet.objects.filter(idventacab=idventacab).count()
        cantr=cantr+1
        ventacab_instance = Ventacab.objects.get(pk=int(idventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            ventadet = Ventadet()
            ventadet.idventacab =ventacab_instance
            ventadet.orden = cantr
            ventadet.idarticulo = articulo_instance
            ventadet.codigo =  articulo.codigo
            ventadet.descripcion = articulo.descripcion
            ventadet.cantidad = float(cantidad)
            ventadet.unidad = articulo.unidad
            ventadet.costo =articulo.costo
            ventadet.precio = float(precio)
            ventadet.iva = articulo.iva
            ventadet.idempresa = didempresa
            ventadet.idsucursal =didsucursal
            ventadet.deposito = deposito
            ventadet.cotizacion = 1
            ventadet.moneda = 'gs'
            ventadet.save()

            actordendet(idventacab)

            datos = []
            datos.append({
                'idventacab': encriptar_datos2(idventacab, request),
                'cantr': cantr,

            })

            Response = JsonResponse({'datos': datos, 'success': True, 'message': ''})
            return Response
            #if cantr == 1:
            #    skey = str(request.user.last_login) + str(request.user.username) + str( request.user.password)
            #    pk_encriptado = encriptar_datos(idventacab,skey)  # Asegúrate de que esta función esté implementada correctamente
            #    return redirect('ventacaja_cargar', pk_token=str(pk_encriptado))

            #else:
            #    response = {'success': True}
            #    return JsonResponse(response)
def actordendet(idventacab):
    orden = 0
    objetos = Ventadet.objects.filter(idventacab=idventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden = orden + 1
        objeto.save()


def ventacaja_editar(request):
    if not request.user.has_perm('ventas.add_ventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        idventacab = request.POST['pkf']
        idventacab = desencriptar_datos2(idventacab,request)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        deposito = request.POST['deposito']

        objetos = Ventadet.objects.filter(idventacab=idventacab,orden=orden)
        for ventadet in objetos:
            idventadet=ventadet.idventadet

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)

        for articulo in articulos:
            ventadet = get_object_or_404(Ventadet, pk=idventadet)
            ventadet.idventacab =float(idventacab)
            ventadet.orden = orden
            ventadet.idarticulo = articulo.idarticulo
            ventadet.codigo =  articulo.codigo
            ventadet.descripcion = articulo.descripcion
            ventadet.cantidad = float(cantidad)
            ventadet.unidad = articulo.unidad
            ventadet.costo =articulo.costo
            ventadet.precio = float(precio)
            ventadet.iva = articulo.iva
            ventadet.deposito = deposito
            ventadet.save()
            #actventacaja(idventacab)
            response = {'success': True}
            return JsonResponse(response)

def ventadetcaja_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_ventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    idventadet = int(desencriptar_datos2(pk_token,request))
    objetos = Ventadet.objects.filter(idventadet=idventadet)
    for objeto in objetos:
        idventacab= objeto.idventacab

    ventadet = get_object_or_404(Ventadet, idventadet=idventadet)
    ventadet.delete()
    actordendet(idventacab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)


def ventacajapago_guardar(request):

    if not request.user.has_perm('ventas.add_ventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':

        pkf = request.POST['pkf']
        idventacab = desencriptar_datos2(pkf, request)
        monto = request.POST['monto']
        detalles = Ventadet.objects.filter(idventacab=idventacab)
        total = sum([detalle.cantidad * detalle.precio for detalle in detalles])
        detalles = cajaventapago.objects.filter(idventacab=idventacab)
        saldoini = (total - sum([detalle.monto for detalle in detalles]))
        saldo = (total - sum([detalle.monto for detalle in detalles]) - int(monto))
        ipago = monto
        if saldo < 0:
            ipago=monto
            monto=saldoini

        #    response = {'success': False}
        #    return JsonResponse(response)


        id_idcliente = request.POST['id_idcliente']
        id_fpago = request.POST['id_fpago']
        desc = request.POST['desc']
        cantr = cajaventapago.objects.filter(idventacab=idventacab).count()
        cantr = cantr + 1

        cedula = ''
        ruc = ''
        print(' iscliente ' + str(id_idcliente))
        objetos = Cliente.objects.filter(idcliente=id_idcliente)
        cantr = objetos.count()
        if cantr > 0:
            for objeto in objetos:
                cliente = objeto.nombre
                cedula = objeto.cedula
                ruc = objeto.ruc
        else:
            id_idcliente=1
            cliente="SIN NOMBRE"
        cliente_instance = Cliente.objects.get(pk=int(id_idcliente))

        objetos = Ventacab.objects.filter(idventacab=idventacab)
        for objeto in objetos:
            objeto.idcliente = cliente_instance
            objeto.cliente = cliente
            objeto.cedula = cedula
            objeto.ruc = ruc
            objeto.save()

        pago = cajaventapago()
        pago.idventacab = float(idventacab)
        pago.orden = cantr
        pago.formapago = id_fpago
        pago.descripcion = desc
        pago.monto = monto
        pago.pago = ipago
        pago.idsucursal = didsucursal
        pago.idempresa = didempresa
        pago.cotizacion = 1
        pago.moneda = 'gs'
        pago.save()

    return redirect('ventacierre_cargar', pk_token=pkf)


def detallepagocaja_listar(request):

    if request.method == 'POST':
        idventacab = request.POST['pkf']
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        idventacab = desencriptar_datos2(idventacab, request)

            # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        objetos = cajaventapago.objects.filter(idventacab=idventacab).order_by('orden')
        datos = []

        if objetos.count() > 0:
            for objeto in objetos:
                datos.append({
                    'iddetpago':encriptar_datos2(objeto.idcajaventapago, request),
                    'orden': objeto.orden,
                    'formapago': objeto.formapago,
                    'monto': f"{(objeto.pago):,.0f}",
                    'descripcion': objeto.descripcion,
                })

        Response = JsonResponse({'datos': datos, 'success': True, 'message': ''})
        return Response


class cajapagocli_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_pagoclientesforma'

    def get(self, request,pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        pk = desencriptar_datos2(pk_token,request)

        obj = cajaventapago.objects.filter(idcajaventapago=pk)
        pk_token2 = (int(([(detalle.idventacab) for detalle in obj])[0]))
        pk_token3 = encriptar_datos2(pk_token2,request)


        if action == 'CONFIRMAR':
            instance = get_object_or_404(cajaventapago, pk=pk)
            try:
                instance.delete()

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            #messages.success(self.request, ' eliminado exitosamente.')

            return redirect('ventacierre_cargar', pk_token=pk_token3)
        else:
            return redirect('ventacierre_cargar', pk_token=pk_token3)

def ventacaja_cerrarventa(request,pk_token):
    print(' idventacab '+ str(pk_token))

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    idventacab = desencriptar_datos2(pk_token, request)
    print(' idventacab '+ str(idventacab))
    pk = pk_token

    detalles = Ventadet.objects.filter(idventacab=idventacab)
    total = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = cajaventapago.objects.filter(idventacab=idventacab)
    saldo = (total - sum([detalle.monto for detalle in detalles]))
    if saldo == 0:
        print(pk_token)

        oseriedet = seriedet.objects.filter(idserie=1, iddocumentos=1, idempresa=didempresa, idsucursal=didsucursal)
        for objetoe in oseriedet:
            objetoe.correlativa=objetoe.correlativa+1
            objetoe.save()

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        oVentacab = Ventacab.objects.filter(idventacab=idventacab)
        oVentadet = Ventadet.objects.filter(idventacab=idventacab)
        opago = cajaventapago.objects.filter(idventacab=idventacab).order_by('orden')
        actventacaja(idventacab)

        return redirect('ventacaja_cargar', pk_token=0)
    else:
        return redirect('ventacierre_cargar', pk_token=pk_token)



def printere(request,pk_token):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'caja/cajaapcierre.html')

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # Desactiva la verificación de CSRF para esta vista
def check_tickets(request):

    if request.method == 'POST':
        try:
            # Obtiene los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)
            pk_token = data.get('pk_token')
            idventacab = desencriptar_datos2(pk_token, request)

            # Aquí debes agregar la lógica para verificar si hay un nuevo ticket basado en pktoken
            # Este es solo un ejemplo simple; deberías adaptar esto según tu lógica de negocio
            ticket = Ventacab.objects.filter(idventacab=idventacab).first()

            if ticket:
                # Supongamos que 'ticket' es una instancia de un modelo y tiene una relación con detalles
                ticket = Ventacab.objects.filter(idventacab=idventacab).first()

                # Aquí asumimos que 'detalle_set' es el nombre del related name de la relación inversa
                #detalles = ticket.detalle_set.all()  # Obtén todos los detalles asociados al ticket
                detalles = Ventadet.objects.filter(idventacab=idventacab).order_by('orden')  # Recupera el ticket principal

                if timezone.is_naive(ticket.fecha_hora):
                    # Si es naive, hacerla aware
                    fecha_aware = timezone.make_aware(ticket.fecha_hora)
                else:
                    # Ya es aware
                    fecha_aware = ticket.fecha_hora

                fecha_local = timezone.localtime(fecha_aware)
                fecha_formateada = fecha_local.strftime("%d-%m-%Y %H:%M:%S")

                # Construye el diccionario
                ticket_dict = {
                    'tipo': {
                        'tipo': 1,
                        'obs': 'ninguno'
                    },
                    'cabecera': {
                        'nrofactura': ticket.nrofactura,
                        'ruc': ticket.ruc,
                        'cliente': ticket.cliente,
                        'fecha': fecha_formateada,  # Formatea la fecha como una cadena
                        'total': ticket.total,

                    },
                    'detalle': [  # Lista de detalles
                        {
                            'orden': detalle.orden,  # Asegúrate de que 'detalle' tenga el atributo correcto
                            'codigo': detalle.codigo,
                            'descripcion': detalle.descripcion,
                            'iva': detalle.iva,
                            'unidad': detalle.unidad,
                            'cantidad': detalle.cantidad,
                            'precio': detalle.precio,
                            'subtotal': detalle.precio * detalle.cantidad

                        }
                        for detalle in detalles
                    ]
                }

                # Imagina que `ticket.content` es el contenido que necesitas imprimir
                return JsonResponse({'hasNewTicket': True, 'ticketContent': ticket_dict})
            else:
                return JsonResponse({'hasNewTicket': False})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud mal formada'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def imprimirticket(request):
    return render(request, 'caja/imprimir.html')

