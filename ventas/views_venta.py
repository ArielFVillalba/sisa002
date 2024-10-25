from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from django.contrib import messages
from ventas.forms import VentacabForm, OrdenVentacabForm
from ventas.models import *
from stock.views import actualizarexistencia, verificardepostio

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from django.utils import timezone

def ventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'ventas/ventacab_filt.html')

def ventacab_filtro_lst(request):
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

    ventacab = Ventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
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
    return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena})


def ventacab_listar(request,cadena):
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
    return render(request, 'ventas/ventacab_listar.html', {'ventacab': ventacab, 'cadena': cadena})


class ventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_ventacab'
    model = Ordenventacab
    form_class = OrdenVentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = reverse_lazy('ventacab_cargar')

    def get(self, request,pk_token):
        ventacab = None
        if pk_token != "0":
            idempresa = request.session.get('idempresa')
            idsucursal = request.session.get('idsucursal')
            didempresa = desencriptar_datos2(idempresa, request)
            didsucursal = desencriptar_datos2(idsucursal, request)
            if int(didempresa) < 1 or int(didsucursal) < 1:
                return redirect('login')

            pk_desencriptado = desencriptar_datos2(pk_token,request)
            ventacab = Ventacab.objects.get(idventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'ventacab': ventacab}  # Crear un diccionario de contexto
        context['title'] = '   VENTA  '
        context['sidr'] = '/Ventacab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)

class ventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_ordenventacab'

    model = Ventacab
    form_class = VentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = reverse_lazy('ventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(ventacab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR VENTA '
        context['sidr'] = '/ventacab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Ventacab = form.save(commit=False)
        Ventacab.idempresa = didempresa
        Ventacab.idsucursal = didsucursal
        Ventacab.fecha_hora = timezone.now()  # Asigna la fecha y hora actual correctamente
        Ventacab.save()

        messages.success(self.request, ' compra creado exitosamente.')
        response = super().form_valid(form)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ventacab_cargar', pk_token=str(pk_encriptado))

class ventacab_editar(UpdateView):
    permission_required = 'ventas.change_ordenventacab'
    model = Ventacab
    form_class = VentacabForm
    template_name = 'ventas/ventacab.html'
    success_url = '/ventacab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Ventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' EDITAR  VENTA  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/ventacab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'editado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ventacab_cargar', pk_token=str(pk_encriptado))

class ventacab_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_ventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        if pk_token =="0":
            return redirect('ventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Ventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'venta eliminada exitosamente.')
            return redirect('ventacab_cargar', pk_token=0)
        else:
            return redirect('ventacab_cargar', pk_token=str(pk_token))

def ventadet_listar(request):
    if not request.user.has_perm('ventas.view_ventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
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
    if int(orden) >=1:
        objetos = Ventadet.objects.filter(idventacab=idventacab,orden=orden)
    datos = []

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idventadet,request),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': f"{(objeto.cantidad):.3f}",
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response



def actventacab(idventacab):

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


def ventadet_guardar(request):
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
        deposito = request.POST['deposito']

        if verificardepostio(deposito, didempresa) == False:
            response = {'success': False, 'message': 'deposito invalido'}
            return JsonResponse(response)


        ventacab_instance = Ventacab.objects.get(pk=int(idventacab))  # Asegúrate de que `idcompracab` sea un entero

        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)

        cantr = Ventadet.objects.filter(idventacab=idventacab).count()

        cantr=cantr+1
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
            ventadet.save()
            actventacab(idventacab)
            response = {'success': True}
            return JsonResponse(response)

def ventadet_editar(request):
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

        ventacab_instance = Ventacab.objects.get(pk=int(idventacab))  # Asegúrate de que `idcompracab` sea un entero


        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)
        

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            ventadet = get_object_or_404(Ventadet, pk=idventadet)
            ventadet.idventacab =ventacab_instance
            ventadet.orden = orden
            ventadet.idarticulo = articulo_instance
            ventadet.codigo =  articulo.codigo
            ventadet.descripcion = articulo.descripcion
            ventadet.cantidad = float(cantidad)
            ventadet.unidad = articulo.unidad
            ventadet.costo =articulo.costo
            ventadet.precio = float(precio)
            ventadet.iva = articulo.iva
            ventadet.deposito = deposito
            ventadet.save()
            actventacab(idventacab)
            response = {'success': True}
            return JsonResponse(response)

def ventadet_eliminar(request, pk_token):
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


    ventadet_instance = Ventadet.objects.get(pk=idventadet)
    idventacab = ventadet_instance.idventacab_id
    ventadet_instance.delete()

    orden=0
    objetos = Ventadet.objects.filter(idventadet=idventadet).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actventacab(idventacab)

    response = {'success': True, 'message': ''}
    return JsonResponse(response)


#-----------------------------------------------------------------------

@receiver(pre_save,sender=Ventadet)
def pre_save_det(sender, instance,  **kwargs):
    print('post_save_det pre_save_det')

    dididventadet= instance.idventadet
    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depsalida=instance.deposito
    depentrada=instance.deposito

    try:
        previous_ventadet = Ventadet.objects.get(pk=instance.pk)
    except Ventadet.DoesNotExist:
        # El objeto no existe previamente, es una creación
        previous_ventadet = None
        # Ahora puedes comparar los valores anteriores con los nuevos
    if previous_ventadet:
        # print("-  previous_ventadet cantidad:  " + str(instance.cantidad) + "  codigo  " + str(previous_ventadet.codigo)+"  instance.cantidad  "+str(instance.cantidad))
        # Ejemplo de comparación de campos
        if instance.cantidad != previous_ventadet.cantidad:
            actualizarexistencia(codigo, previous_ventadet.cantidad,instance.cantidad, depentrada,depsalida, didempresa, didsucursal)
            print("- cantidad ha cambiado de:", previous_ventadet.cantidad, "a:", instance.cantidad)
    else:
        actualizarexistencia(codigo,0, instance.cantidad, '',depsalida, didempresa,didsucursal)


@receiver(post_delete, sender=Ventadet)
def post_delete(sender, instance, **kwargs):
    dididventadet= instance.idventadet
    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depentrada=instance.deposito
    depsalida=''
    actualizarexistencia(codigo,instance.cantidad,0,depentrada, depsalida, didempresa, didsucursal)
