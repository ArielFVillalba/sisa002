from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
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


def notadebitoventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'ventas/notadebitoventa_filt.html')

def notadebitoventacab_filtro_lst(request):
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
    notadebitoventacab = Notadebitoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
    if idcliente=='':
        idcliente=0
    if notadebitoventacab.exists() and int(idcliente) >=1:
            notadebitoventacab = notadebitoventacab.filter(idcliente_id=idcliente)
    if notadebitoventacab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            notadebitoventacab = notadebitoventacab.filter(fecha__gte=fecha_inicio)
    if notadebitoventacab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            notadebitoventacab = notadebitoventacab.filter(fecha__lte=fecha_fin)
    if notadebitoventacab.exists() and tipodoc:
        notadebitoventacab = notadebitoventacab.filter(tipodoc=tipodoc)

    for objeto in notadebitoventacab:
        objeto.pknd = encriptar_datos2(objeto.idnotadebitoventacab,request)
        print(" id " + str(objeto.pknd))
        objeto.save()

    cadena=""
    return render(request, 'ventas/notadebitoventa_lst.html', {'notadebitoventacab': notadebitoventacab, 'cadena': cadena })

def notadebitoventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    if cadena == "*":

        notadebitoventacab = Notadebitoventacab.objects.all(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/notadebitoventa_lst.html', {'notadebitoventacab': notadebitoventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/notadebitoventa_lst.html')

    qs = Notadebitoventacab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Notadebitoventacab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Notadebitoventacab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Notadebitoventacab.objects.filter(cliente__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Notadebitoventacab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)
        notadebitoventacab = qs


    return render(request, 'ventas/notadebitoventa_lst.html', {'notadebitoventacab': notadebitoventacab, 'cadena': cadena})

class notadebitoventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_notadebitoventacab'
    model = Notadebitoventacab
    form_class = NotadebitodeventacabForm
    template_name = 'ventas/notadebitoventa.html'
    success_url = reverse_lazy('notadebitoventacab_cargar')

    def get(self, request,pk_token):
        notadebitoventacab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            notadebitoventacab = Notadebitoventacab.objects.get(idnotadebitoventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'notadebitoventacab': notadebitoventacab}  # Crear un diccionario de contexto
        context['title'] = '   NOTA DEBITO - VENTA  '
        context['sidr'] = '/notadebitoventacab/' + str(pk_token) + '/cargar/'
        context['pknd'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False
        pk_token = self.kwargs['pk_token']
        return render(request, self.template_name, context)


class notadebitoventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_notacreditoventacab'
    model = Notadebitoventacab
    form_class = NotadebitodeventacabForm
    template_name = 'ventas/notadebitoventa.html'
    success_url = reverse_lazy('notadebitoventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(notadebitoventacab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NOTA DEBDITO DE VENTA '
        context['sidr'] = '/notadebitoventacab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self,request, form):
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')



        Notadebitoventacab = form.save(commit=False)
        Notadebitoventacab.idempresa = idempresa
        Notadebitoventacab.idsucursal = idsucursal
        Notadebitoventacab.save()

        response = super().form_valid(form)
        messages.success(self.request, 'creado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('notadebitoventacab_cargar', pk_token=str(pk_encriptado))


class notadebitoventacab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_notadebitoventacab'
    model = Notadebitoventacab
    form_class = NotadebitodeventacabForm
    template_name = 'ventas/notadebitoventa.html'
    success_url = '/notadebitoventacab/0/listar/'

    def get_object(self,request, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,request)
            return get_object_or_404(Notadebitoventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR ORDEN DE VETNA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/notadebitoventacab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pknd'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return redirect('notadebitoventacab_cargar', pk_token=str(pk_token))

class notadebitoventacab_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_notadebitoventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE ORDEN  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if pk_token =="0":
            return redirect('notadebitoventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Notadebitoventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'Nota eliminado exitosamente.')
            return redirect('notadebitoventacab_cargar', pk_token=0)
        else:
            return redirect('notadebitoventacab_cargar', pk_token=str(pk_token))

def notadebitoventadet_listar(request):
    if not request.user.has_perm('ventas.view_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idnotadebitoventacab = request.POST['pknd']
    idnotadebitoventacab = desencriptar_datos2(idnotadebitoventacab,request)

    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Notadebitoventadet.objects.filter(idnotadebitoventacab=idnotadebitoventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Notadebitoventadet.objects.filter(idnotadebitoventacab=idnotadebitoventacab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkndd': encriptar_datos2(objeto.idnotadebitoventadet,request),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actnotadebitoventacab(idnotadebitoventacab):

    detalles = Notadebitoventadet.objects.filter(iva=5,idnotadebitoventacab=idnotadebitoventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notadebitoventadet.objects.filter(iva=10, idnotadebitoventacab=idnotadebitoventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notadebitoventadet.objects.filter(iva=0, idnotadebitoventacab=idnotadebitoventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Notadebitoventacab.objects.filter(idnotadebitoventacab=idnotadebitoventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def notadebitoventadet_guardar(request):
    if not request.user.has_perm('ventas.add_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':
        idnotadebitoventacab = request.POST['pknd']
        idnotadebitoventacab = desencriptar_datos2(idnotadebitoventacab,request)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Notadebitoventadet.objects.filter(idnotadebitoventacab=idnotadebitoventacab).count()
        cantr=cantr+1

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        Notadebitoventacab_instance = Notadebitoventacab.objects.get(pk=int(idnotadebitoventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            notadebitoventadet = Notadebitoventadet()
            notadebitoventadet.idnotadebitoventacab =Notadebitoventacab_instance
            notadebitoventadet.orden = cantr
            notadebitoventadet.idarticulo = articulo_instance
            notadebitoventadet.codigo =  articulo.codigo
            notadebitoventadet.descripcion = articulo.descripcion
            notadebitoventadet.cantidad = float(cantidad)
            notadebitoventadet.unidad = articulo.unidad
            notadebitoventadet.costo =articulo.costo
            notadebitoventadet.precio = float(precio)
            notadebitoventadet.iva = articulo.iva
            notadebitoventadet.idempresa = idempresa
            notadebitoventadet.idsucursal = idsucursal
            notadebitoventadet.save()
            actnotadebitoventacab(idnotadebitoventacab)
            response = {'success': True}
            return JsonResponse(response)

def notadebitoventadet_editar(request):
    if not request.user.has_perm('ventas.add_notadebitoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':
        idnotadebitoventacab = request.POST['pknd']
        idnotadebitoventacab = desencriptar_datos2(idnotadebitoventacab,request)

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Notadebitoventadet.objects.filter(idnotadebitoventacab=idnotadebitoventacab,orden=orden)
        for notadebitoventadet in objetos:
            idnotadebitoventadet=notadebitoventadet.idnotadebitoventadet

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Notadebitoventacab_instance = Notadebitoventacab.objects.get(pk=int(idnotadebitoventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero
            notadebitoventadet = get_object_or_404(Notadebitoventadet, pk=idnotadebitoventadet)
            notadebitoventadet.idnotadebitoventacab =Notadebitoventacab_instance
            notadebitoventadet.orden = orden
            notadebitoventadet.idarticulo = articulo_instance
            notadebitoventadet.codigo =  articulo.codigo
            notadebitoventadet.descripcion = articulo.descripcion
            notadebitoventadet.cantidad = float(cantidad)
            notadebitoventadet.unidad = articulo.unidad
            notadebitoventadet.costo =articulo.costo
            notadebitoventadet.precio = float(precio)
            notadebitoventadet.iva = articulo.iva
            notadebitoventadet.save()
            actnotadebitoventacab(idnotadebitoventacab)
            response = {'success': True}
            return JsonResponse(response)

def notadebitoventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_notadebitoventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    idnotadebitoventadet = int(desencriptar_datos2(pk_token,request))
    objetos = Notadebitoventadet.objects.filter(idnotadebitoventadet=idnotadebitoventadet)
    for objeto in objetos:
        idnotadebitoventacab = objeto.idnotadebitoventacab

    notadebitoventadet = get_object_or_404(Notadebitoventadet, idnotadebitoventadet=idnotadebitoventadet)
    notadebitoventadet.delete()

    orden = 0
    objetos = Notadebitoventadet.objects.filter(idnotadebitoventacab=idnotadebitoventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden = orden + 1
        objeto.save()

    actnotadebitoventacab(idnotadebitoventacab)
    response = {'success': True}
    return JsonResponse(response)
