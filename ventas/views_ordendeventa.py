from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from compras.forms import *

from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum




def ordenventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'ventas/ordendeventa_filt.html')

def ordenventacab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idcliente =  request.GET.get('idcliente', '')
    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    tipodoc =  request.GET.get('tipodoc', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    ordenventacab = Ordenventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idcliente=='':
        idcliente=0
    if ordenventacab.exists() and int(idcliente) >=1:
            ordenventacab = ordenventacab.filter(idcliente_id=idcliente)
    if ordenventacab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            ordenventacab = ordenventacab.filter(fecha__gte=fecha_inicio)
    if ordenventacab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            ordenventacab = ordenventacab.filter(fecha__lte=fecha_fin)
    if ordenventacab.exists() and tipodoc:
        ordenventacab = ordenventacab.filter(tipodoc=tipodoc)

    skey = iskey(request)

    for objeto in ordenventacab:
        objeto.pkov = encriptar_datos(objeto.idordenventacab,skey)

    cadena=""
    return render(request, 'ventas/ordendeventa_lst.html', {'ordenventacab': ordenventacab, 'cadena': cadena })

def ordenventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    if cadena == "*":
        ordenventacab = Ordenventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/ordendeventa_lst.html', {'ordenventacab': ordenventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/ordendeventa_lst.html')

    qs = Ordenventacab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Ordenventacab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Ordenventacab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Ordenventacab.objects.filter(proveedor__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Ordenventacab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    ordenventacab = qs
    return render(request, 'ventas/ordendeventa_lst.html', {'ordenventacab': ordenventacab, 'cadena': cadena})

class ordenventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_ordenventacab'
    model = Ordenventacab
    form_class = OrdenVentacabForm
    template_name = 'ventas/ordendeventa.html'
    success_url = reverse_lazy('ordenventacab_cargar')

    def get(self, request,pk_token):
        ordenventacab = None
        if pk_token != "0":
            skey = iskey(request)
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            ordenventacab = Ordenventacab.objects.get(idordenventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'ordenventacab': ordenventacab}  # Crear un diccionario de contexto
        context['title'] = '  ORDEN  - VENTA  '
        context['sidr'] = '/Ordenventacab/' + str(pk_token) + '/cargar/'
        context['pkov'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class ordenventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_ordenventacab'

    model = Ordenventacab
    form_class = OrdenVentacabForm
    template_name = 'ventas/ordendeventa.html'
    success_url = reverse_lazy('ordenventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(ordenventacab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR ORDEN DE VENTA '
        context['sidr'] = '/ordenventacab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context
    def form_valid(self, form):
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')



        Ordenventacab = form.save(commit=False)
        Ordenventacab.idempresa = idempresa
        Ordenventacab.idsucursal = idsucursal
        Ordenventacab.save()

        response = super().form_valid(form)
        messages.success(self.request, 'creado exitosamente.')
        skey = iskey(self.request)

        pk_encriptado = encriptar_datos(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ordenventacab_cargar', pk_token=str(pk_encriptado))


class ordenventacab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_ordenventacab'

    model = Ordenventacab
    form_class = OrdenVentacabForm
    template_name = 'ventas/ordendeventa.html'
    success_url = '/ordenventacab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = iskey(self.request)
            pk = desencriptar_datos2(pk_token,request)
            return get_object_or_404(Ordenventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR ORDEN DE VETNA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/ordenventacab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkov'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return redirect('ordenventacab_cargar', pk_token=str(pk_token))

class ordenventacab_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_ordenventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE ORDEN  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if pk_token =="0":
            return redirect('ordenventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            skey = iskey(self.request)
            pk = desencriptar_datos2(pk_token,request)
            #print(" instance " + str(pk))

            instance = get_object_or_404(Ordenventacab, pk=pk)
            #print(" instance " +instance)

            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'orden eliminado exitosamente.')
            return redirect('ordenventacab_cargar', pk_token=0)
        else:
            return redirect('ordenventacab_cargar', pk_token=str(pk_token))


def ordenventadet_listar(request):
    if not request.user.has_perm('ventas.view_ordenventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idordenventacab = request.POST['pkov']
    skey = iskey(request)
    idordenventacab = desencriptar_datos(idordenventacab,skey)

    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Ordenventadet.objects.filter(idordenventacab=idordenventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Ordenventadet.objects.filter(idordenventacab=idordenventacab,orden=orden)
    datos = []
    skey = iskey(request)

    for objeto in objetos:
        datos.append({
            'pkovd': encriptar_datos(objeto.idordenventadet,skey),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actordenventacab(idordenventacab):

    #gravada10 = Ventadet.objects.filter(iva=10,idventacab=idventacab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Ordenventadet.objects.filter(iva=5,idordenventacab=idordenventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ordenventadet.objects.filter(iva=10, idordenventacab=idordenventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ordenventadet.objects.filter(iva=0, idordenventacab=idordenventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Ordenventacab.objects.filter(idordenventacab=idordenventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def ordenventadet_guardar(request):
    if not request.user.has_perm('ventas.add_ordenventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        idordenventacab = request.POST['pkov']
        skey = iskey(request)
        idordenventacab = desencriptar_datos(idordenventacab,skey)

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Ordenventadet.objects.filter(idordenventacab=idordenventacab).count()

        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            ordenventadet = Ordenventadet()
            ordenventadet.idordenventacab =float(idordenventacab)
            ordenventadet.orden = cantr
            ordenventadet.idarticulo = articulo.idarticulo
            ordenventadet.codigo =  articulo.codigo
            ordenventadet.descripcion = articulo.descripcion
            ordenventadet.cantidad = float(cantidad)
            ordenventadet.unidad = articulo.unidad
            ordenventadet.costo =articulo.costo
            ordenventadet.precio = float(precio)
            ordenventadet.iva = articulo.iva
            ordenventadet.idempresa = idempresa
            ordenventadet.idsucursal = idsucursal
            ordenventadet.save()
            actordenventacab(idordenventacab)
            response = {'success': True}
            return JsonResponse(response)

def ordenventadet_editar(request):
    if not request.user.has_perm('ventas.change_ordenventadet'):
        datos = None
        Response = JsonResponse({'datos': datos, 'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':
        idordenventacab = request.POST['pkov']
        skey = iskey(request)
        idordenventacab = desencriptar_datos(idordenventacab,skey)

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Ordenventadet.objects.filter(idordenventacab=idordenventacab,orden=orden)
        for ordenventadet in objetos:
            idordenventadet=ordenventadet.idordenventadet

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            ordenventadet = get_object_or_404(Ordenventadet, pk=idordenventadet)
            ordenventadet.idventacab =float(idordenventacab)
            ordenventadet.orden = orden
            ordenventadet.idarticulo = articulo.idarticulo
            ordenventadet.codigo =  articulo.codigo
            ordenventadet.descripcion = articulo.descripcion
            ordenventadet.cantidad = float(cantidad)
            ordenventadet.unidad = articulo.unidad
            ordenventadet.costo =articulo.costo
            ordenventadet.precio = float(precio)
            ordenventadet.iva = articulo.iva
            ordenventadet.save()
            actordenventacab(idordenventacab)
            response = {'success': True}
            return JsonResponse(response)


def ordenventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_ordenventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    skey = iskey(request)
    idordenventadet = int(desencriptar_datos2(pk_token,request))

    objetos = Ordenventadet.objects.filter(idordenventadet=idordenventadet)

    for objeto in objetos:
        idordenventacab= objeto.idordenventacab

    ordenventadet = get_object_or_404(Ordenventadet, idordenventadet=idordenventadet)
    ordenventadet.delete()

    orden=0
    objetos = Ordenventadet.objects.filter(idordenventacab=idordenventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actordenventacab(idordenventacab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
