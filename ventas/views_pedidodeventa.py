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


def pedidoventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    return render(request, 'ventas/pedidodeventa_filt.html')

def pedidoventacab_filtro_lst(request):
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

    pedidoventacab = Pedidoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idcliente=='':
        idcliente=0
    if pedidoventacab.exists() and int(idcliente) >=1:
            pedidoventacab = pedidoventacab.filter(idcliente_id=idcliente)
    if pedidoventacab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            pedidoventacab = pedidoventacab.filter(fecha__gte=fecha_inicio)
    if pedidoventacab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            pedidoventacab = pedidoventacab.filter(fecha__lte=fecha_fin)
    if pedidoventacab.exists() and tipodoc:
        pedidoventacab = pedidoventacab.filter(tipodoc=tipodoc)

    for objeto in pedidoventacab:
        objeto.pkpv = encriptar_dato(objeto.idpedidoventacab)


    cadena=""
    return render(request, 'ventas/pedidodeventa_lst.html', {'pedidoventacab': pedidoventacab, 'cadena': cadena })

def pedidoventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if cadena == "*":
        print("valor"+ cadena)
        pedidoventacab = Pedidoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/pedidodeventa_lst.html', {'pedidoventacab': pedidoventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/pedidodeventa_lst.html')

    qs = Pedidoventacab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Pedidoventacab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Pedidoventacab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Pedidoventacab.objects.filter(cliente__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Pedidoventacab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    pedidoventacab = qs
    return render(request, 'ventas/pedidodeventa_lst.html', {'pedidoventacab': pedidoventacab, 'cadena': cadena})


class pedidoventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_pedidoventacab'
    model = Pedidoventacab
    form_class = PedidoventacabForm
    template_name = 'ventas/pedidodeventa.html'
    success_url = reverse_lazy('pedidoventacab_cargar')

    def get(self, request,pk_token):
        pedidoventacab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            pedidoventacab = Pedidoventacab.objects.get(idpedidoventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'pedidoventacab': pedidoventacab}  # Crear un diccionario de contexto
        context['title'] = '  PEDIDO DE VENTA  '
        context['sidr'] = '/Pedidoventacab/' + str(pk_token) + '/cargar/'
        context['pkpv'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)

class pedidoventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_pedidoventacab'

    model = Pedidoventacab
    form_class = PedidoventacabForm
    template_name = 'ventas/pedidodeventa.html'
    success_url = reverse_lazy('pedidoventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(pedidoventacab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR PEDIDO DE VENA '
        context['sidr'] = '/pedidoventacab/crear/'
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Pedidoventacab = form.save(commit=False)
        Pedidoventacab.idempresa = didempresa
        Pedidoventacab.idsucursal = didsucursal
        Pedidoventacab.save()

        response = super().form_valid(form)
        messages.success(self.request, 'creado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('pedidoventacab_cargar', pk_token=pk_encriptado)

class pedidoventacab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_pedidoventacab'

    model = Pedidoventacab
    form_class = PedidoventacabForm
    template_name = 'ventas/pedidodeventa.html'
    success_url = '/pedidoventacab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        if pk_token != "0":

            pk = desencriptar_datos(pk_token,self.request)
            return get_object_or_404(Pedidoventacab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR PEDIDO  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/pedidoventacab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        compracab = self.object
        messages.success(self.request, ' pedido editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        #return reverse_lazy('compracab_editar', kwargs={'pk_token': pk_encriptado})
        return reverse_lazy('pedidoventacab_cargar', kwargs={'pk_token': pk_token})

class pedidoventacab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_pedidoventacab'

    def get(self, request, pk_token):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk = desencriptar_datos(pk_token,request)
        instance = get_object_or_404(Pedidoventacab, pk=pk)
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE PEDIDO "


        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if pk_token =="0":
            return redirect('pedidoventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Pedidoventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'orden eliminado exitosamente.')
            return redirect('pedidoventacab_cargar', pk_token=0)
        else:
            return redirect('pedidoventacab_cargar', pk_token=pk_token)



def actpedidoventacab(idpedidoventacab):

    #gravada10 = Compradet.objects.filter(iva=10,idventacab=idventacab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Pedidoventadet.objects.filter(iva=5,idpedidoventacab=idpedidoventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Pedidoventadet.objects.filter(iva=10, idpedidoventacab=idpedidoventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Pedidoventadet.objects.filter(iva=0, idpedidoventacab=idpedidoventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Pedidoventacab.objects.filter(idpedidoventacab=idpedidoventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def pedidoventadet_listar(request):
    if not request.user.has_perm('ventas.view_pedidoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['pkpv']
    idpedidoventacab = int(desencriptar_datos2(pk,request))

    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Pedidoventadet.objects.filter(idpedidoventacab=idpedidoventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Pedidoventadet.objects.filter(idpedidoventacab=idpedidoventacab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkpvd': encriptar_datos2(objeto.idpedidoventadet,request),
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




def pedidoventadet_guardar(request):
    if not request.user.has_perm('ventas.add_pedidoventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

    if request.method == 'POST':
        pk = request.POST['pkpv']
        idpedidoventacab = int(desencriptar_datos2(pk,request))

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Pedidoventadet.objects.filter(idpedidoventacab=idpedidoventacab).count()
        cantr=cantr+1
        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)

        for articulo in articulos:
            pedidoventadet = Pedidoventadet()
            pedidoventadet.idpedidoventacab =float(idpedidoventacab)
            pedidoventadet.orden = cantr
            pedidoventadet.idarticulo = articulo.idarticulo
            pedidoventadet.codigo =  articulo.codigo
            pedidoventadet.descripcion = articulo.descripcion
            pedidoventadet.cantidad = float(cantidad)
            pedidoventadet.unidad = articulo.unidad
            pedidoventadet.costo =articulo.costo
            pedidoventadet.precio = float(precio)
            pedidoventadet.iva = articulo.iva
            pedidoventadet.idempresa = didempresa
            pedidoventadet.idsucursal = didsucursal
            pedidoventadet.save()
            actpedidoventacab(idpedidoventacab)
            response = {'success': True}
            return JsonResponse(response)

def pedidoventadet_editar(request):
    if not request.user.has_perm('ventas.change_pedidoventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

    if request.method == 'POST':
        pkpv = request.POST['pkpv']
        idpedidoventacab = int(desencriptar_datos2(pkpv,request))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Pedidoventadet.objects.filter(idpedidoventacab=idpedidoventacab,orden=orden)
        for pedidoventadet in objetos:
            idpedidoventadet=pedidoventadet.idpedidoventadet

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            pedidoventadet = get_object_or_404(Pedidoventadet, pk=idpedidoventadet)
            pedidoventadet.idpedidoventacab =float(idpedidoventacab)
            pedidoventadet.orden = orden
            pedidoventadet.idarticulo = articulo.idarticulo
            pedidoventadet.codigo =  articulo.codigo
            pedidoventadet.descripcion = articulo.descripcion
            pedidoventadet.cantidad = float(cantidad)
            pedidoventadet.unidad = articulo.unidad
            pedidoventadet.costo =articulo.costo
            pedidoventadet.precio = float(precio)
            pedidoventadet.iva = articulo.iva
            pedidoventadet.save()
            actpedidoventacab(idpedidoventacab)
            response = {'success': True}
            return JsonResponse(response)


def pedidoventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_pedidoventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

    idpedidoventadet = int(desencriptar_datos2(pk_token,request))
    objetos = Pedidoventadet.objects.filter(idpedidoventadet=idpedidoventadet)
    for objeto in objetos:
        idpedidoventacab= objeto.idpedidoventacab

    pedidoventadet = get_object_or_404(Pedidoventadet, pk=idpedidoventadet)
    pedidoventadet.delete()

    orden=0
    objetos = Pedidoventadet.objects.filter(idpedidoventacab=idpedidoventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actpedidoventacab(idpedidoventacab)
    response = {'success': True}
    return JsonResponse(response)
