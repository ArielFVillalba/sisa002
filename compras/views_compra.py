from django.db import transaction
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from inicio.funcion import *
from django.shortcuts import redirect
import datetime
from datetime import datetime
from django.shortcuts import get_object_or_404
from sisa.mixins import ValidarPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from stock.views import actualizarexistencia, verificardepostio
from django.db.models.signals import pre_save,  post_delete
from django.dispatch import receiver

def compracab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'compras/compracab_filt.html')


def compracab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(" entra aqui ")
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    idproveedor = request.GET.get('idproveedor', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')
    tipodoc = request.GET.get('tipodoc', '')
    compracab = Compracab.objects.filter(idempresa=didempresa)

    if idproveedor == '':
        idproveedor = 0
    if compracab.exists() and int(idproveedor) >= 1:
        compracab = compracab.filter(idproveedor_id=idproveedor)
    if compracab.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        compracab = compracab.filter(fecha__gte=fecha_inicio)
    if compracab.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        compracab = compracab.filter(fecha__lte=fecha_fin)
    if compracab.exists() and tipodoc:
        compracab = compracab.filter(tipodoc=tipodoc)

    if compracab.exists():
        compracab = compracab.filter(idempresa=didempresa,idsucursal=didsucursal)

    for objeto in compracab:
        objeto.pkf = encriptar_datos2(objeto.idcompracab,request)
    cadena = ""
    return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena})


def compracab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

       
    if cadena == "*":
        compracab = Compracab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        #compracab.objects.update(idcompracab=encriptar_dato(compracab.idcompracab))
        return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena })

    if cadena=="0":

        return render(request, 'compras/compracab_listar.html')

    qs = Compracab.objects.filter(nombre=0)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Proveedor.objects.filter(fecha__contains=subcadenas[i])
        qs = qs.union(qs1)
        qs2 = Proveedor.objects.filter(nrofactura__contains=subcadenas[i])
        qs = qs.union(qs2)
        qs3 = Proveedor.objects.filter(proveedor__contains=subcadenas[i])
        qs = qs.union(qs3)
        qs4 = Proveedor.objects.filter(ruc__contains=subcadenas[i])
        qs = qs.union|(qs4)

    compracab = qs.objects.filter(idempresa=didempresa, idsucursal=didsucursal)

    #compracab.objects.update(idcompracab=encriptar_dato(compracab.idcompracab))
    return render(request, 'compras/compracab_listar.html', {'compracab': compracab, 'cadena': cadena})


class compracab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'
    context_object_name = 'compracab'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        compracab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,self.request)
            compracab = Compracab.objects.get(idcompracab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'compracab': compracab}  # Crear un diccionario de contexto
        context['title'] = '  COMPRA  '
        context['sidr'] = '/compracab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class compracab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'
    success_url = reverse_lazy('compracab_crear')

    def dispatch(self, *args, **kwargs):
        return super(compracab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR COMPRA '
        context['sidr'] = '/compracab/crear/'
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

        Compracab = form.save(commit=False)
        Compracab.idempresa = didempresa
        Compracab.idsucursal = didsucursal
        Compracab.save()

        messages.success(self.request, ' compra creado exitosamente.')
        response = super().form_valid(form)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('compracab_cargar', pk_token=pk_encriptado)

class compracab_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'compras.change_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            return get_object_or_404(Compracab, idcompracab=pk)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EDITAR COMPRAS'
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/compracab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'Compra editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('compracab_cargar', kwargs={'pk_token': pk_token})

    def form_valid(self, form):
        messages.success(self.request, 'Compra editado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Hubo un error al editar la compra. Por favor, corrija los errores e intente nuevamente.')
        return self.render_to_response(self.get_context_data(form=form))


class compracab_editar2(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_compracab'
    model = Compracab
    form_class = CompracabForm
    template_name = 'compras/compracab.html'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Compracab, idcompracab=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR COMPRAS  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/compracab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'compra editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('compracab_cargar', kwargs={'pk_token': pk_token})


class CompraCabEliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_compracab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE COMPRA "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,self.request)
            instance = get_object_or_404(Compracab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'compra eliminado exitosamente.')
            return redirect('compracab_cargar', pk_token=0)
        else:
            return redirect('compracab_cargar', pk_token=pk_token)


def compradet_listar(request):
    if not request.user.has_perm('compras.view_compradet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']
    idcompracab = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Compradet.objects.filter(idcompracab=idcompracab).order_by('orden')
    if int(orden) >=1:
        objetos = Compradet.objects.filter(idcompracab=idcompracab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idcompradet,request),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio*objeto.cantidad):.0f}"
        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response

def actcomprascab(idcompracab):

    detalles = Compradet.objects.filter(iva=5,idcompracab=idcompracab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Compradet.objects.filter(iva=10, idcompracab=idcompracab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Compradet.objects.filter(iva=0, idcompracab=idcompracab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta
    objetos = Compracab.objects.filter(pk=idcompracab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total

def busdep(request):
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

       
    if request.method == 'POST':
        sql = " select codigo from stk_dep where idempresa= "+idempresa
        usu = request.POST['usuario']
        cont = request.POST['contraseña']
        valor =0

       # valor = seleccionar_datos("stock", sql, usu, cont)
        Response = JsonResponse({'datos': valor})
        return Response

def guardardet(request):
    if not request.user.has_perm('compras.add_compradet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)



    if request.method == 'POST':

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        pkf = request.POST['pkf']
        idcompracab = int(desencriptar_datos2(pkf,request))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']

        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)

        cantr = Compradet.objects.filter(idcompracab=idcompracab).count()
        cantr=cantr+1

        compracab_instance = Compracab.objects.get(pk=int(idcompracab))  # Asegúrate de que `idcompracab` sea un entero

        if verificardepostio(deposito, didempresa)==False:
            response = {'success': False, 'message': 'deposito invalido'}
            return JsonResponse(response)

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            compradet = Compradet()
            compradet.idcompracab = compracab_instance  # Asignar la instancia de Compracab
            compradet.orden = cantr
            compradet.idarticulo = articulo_instance
            compradet.codigo =  articulo.codigo
            compradet.descripcion = articulo.descripcion
            compradet.cantidad = float(cantidad)
            compradet.unidad = articulo.unidad
            compradet.costo =articulo.costo
            compradet.precio = float(precio)
            compradet.iva = articulo.iva
            compradet.deposito = deposito
            compradet.idempresa = didempresa
            compradet.idsucursal = didsucursal
            compradet.save()
            actcomprascab(idcompracab)
            response = {'success': True}
            return JsonResponse(response)

def compradetmod(request):
    if not request.user.has_perm('compras.change_compradet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        idcompracab = int(desencriptar_datos2(pkf,request))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        deposito = request.POST['deposito']

        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)

        if verificardepostio(deposito, didempresa)==False:
            response = {'success': False, 'message': 'deposito invalido'}
            return JsonResponse(response)

        objetos = Compradet.objects.filter(idcompracab=idcompracab,orden=orden)
        for compradet in objetos:
            idcompradet=compradet.idcompradet

        compracab_instance = Compracab.objects.get(pk=int(idcompracab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)

        for articulo in articulos:
            articulo_instance = Articulo.objects.get(
                pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            compradet = get_object_or_404(Compradet, pk=idcompradet)
            compradet.idcompracab =compracab_instance
            compradet.orden = orden
            compradet.idarticulo = articulo_instance
            compradet.codigo =  articulo.codigo
            compradet.descripcion = articulo.descripcion
            compradet.cantidad = float(cantidad)
            compradet.unidad = articulo.unidad
            compradet.costo =articulo.costo
            compradet.precio = float(precio)
            compradet.iva = articulo.iva
            compradet.deposito = deposito
            compradet.save()
            actcomprascab(idcompracab)
            response = {'success': True}
            return JsonResponse(response)

def compradet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_compradet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operación'}
        return JsonResponse(response_data)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    pk = int(desencriptar_datos2(pk_token, request))

    try:
        with transaction.atomic():
            compradet_instance = Compradet.objects.get(pk=pk)
            idcompracab = compradet_instance.idcompracab_id
            print(f"Eliminando Compradet con idcompracab: {idcompracab}")
            compradet_instance.delete()

            # Reordenar objetos 'Compracab'
            objetos = Compradet.objects.filter(idcompracab=idcompracab).order_by('orden')
            orden = 0
            for objeto in objetos:
                orden += 1
                objeto.orden = orden
                objeto.save()

            # Llamar a la función de actualización para 'Compracab'
            actcomprascab(idcompracab)

        response = {'success': True, 'message': ''}
    except Compradet.DoesNotExist:
        response = {'success': False, 'message': 'Compradet no encontrado'}
    except Exception as e:
        response = {'success': False, 'message': str(e)}

    return JsonResponse(response)
#-----------------------------------------------------------------------

@receiver(pre_save,sender=Compradet)
def pre_save_det(sender, instance,  **kwargs):
    print('post_save_det pre_save_det')

    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depsalida=instance.deposito
    depentrada=instance.deposito

    try:
        previous_compradet = Compradet.objects.get(pk=instance.pk)
    except Compradet.DoesNotExist:
        # El objeto no existe previamente, es una creación
        previous_compradet = None
        # Ahora puedes comparar los valores anteriores con los nuevos
    if previous_compradet:
        # print("-  previous_ventadet cantidad:  " + str(instance.cantidad) + "  codigo  " + str(previous_ventadet.codigo)+"  instance.cantidad  "+str(instance.cantidad))
        # Ejemplo de comparación de campos
        if instance.cantidad != previous_compradet.cantidad:
            actualizarexistencia(codigo, instance.cantidad, previous_compradet.cantidad,depentrada,depsalida, didempresa, didsucursal)
    else:
        print("agregar compras")
        actualizarexistencia(codigo,instance.cantidad,0,depentrada,'', didempresa,didsucursal)


@receiver(post_delete, sender=Compradet)
def post_delete(sender, instance, **kwargs):
    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depentrada=''
    depsalida=instance.deposito
    actualizarexistencia(codigo,0,instance.cantidad,depentrada, depsalida, didempresa, didsucursal)
