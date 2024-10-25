from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .forms import *

from django.contrib import messages

from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from inicio.funcion import *
from django.shortcuts import redirect
import datetime
from datetime import datetime
from django.shortcuts import get_object_or_404
from sisa.mixins import ValidarPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def pagoprovcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('compras.view_compradet'):
        return redirect('login')

    return render(request, 'compras/pagoprov_filt.html')


def pagoprovcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('compras.view_pagoproveedor'):
        return redirect('login')


    idproveedor = request.GET.get('idproveedor', '')
    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

       
    pagoproveedor = Pagoproveedor.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
    if idproveedor == '':
        idproveedor = 0
    if pagoproveedor.exists() and int(idproveedor) >= 1:
        pagoproveedor = pagoproveedor.filter(idproveedor_id=idproveedor,idempresa=didempresa,idsucursal=didsucursal)
    if pagoproveedor.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        pagoproveedor = pagoproveedor.filter(fecha__gte=fecha_inicio,idempresa=didempresa,idsucursal=didsucursal)
    if pagoproveedor.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        pagoproveedor = pagoproveedor.filter(fecha__lte=fecha_fin,idempresa=didempresa,idsucursal=didsucursal)
        skey = iskey(request)

    for objeto in pagoproveedor:
        objeto.pkf = encriptar_datos2(objeto.idpagoproveedor,request)

    cadena = ""
    return render(request, 'compras/pagoprov_listar.html', {'pagoproveedor': pagoproveedor, 'cadena': cadena})


def pagoprovcab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.has_perm('compras.view_pagoproveedor'):
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


       
    if cadena == "*":
        pagoproveedor = Pagoproveedor.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'compras/pagoprov_listar.html', {'pagoproveedor': pagoproveedor, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/pagoprov_listar.html')

    qs = Pagoproveedor.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Pagoproveedor.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Pagoproveedor.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Pagoproveedor.objects.filter(proveedor__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Pagoproveedor.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    pagoproveedor = qs

    return render(request, 'compras/pagoprov_listar.html', {'pagoproveedor': pagoproveedor, 'cadena': cadena})


class pagoprovcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_pagoproveedor'
    model = Pagoproveedor
    form_class = PagoproveedorForm
    template_name = 'compras/pagoproveedor.html'
    context_object_name = 'Pagoproveedor'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        pagoproveedor = None
        if pk_token != "0":
            skey=str(self.request.user.last_login)+str(self.request.user.username)+str(self.request.user.password)
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            pagoproveedor = Pagoproveedor.objects.get(idpagoproveedor=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'pagoproveedor': pagoproveedor}  # Crear un diccionario de contexto
        context['title'] = '  PRAGO A PROVEEDOR  '
        context['sidr'] = '/pagoprovcab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class pagoprovcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_pagoproveedor'
    model = Pagoproveedor
    form_class = PagoproveedorForm
    template_name = 'compras/pagoproveedor.html'
    success_url = reverse_lazy('pagoprovcab_crear')

    def dispatch(self, *args, **kwargs):
        return super(pagoprovcab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR PAGO PROVEEDOR '
        context['sidr'] = '/pagoprovcab/crear/'
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




        Pagoproveedor = form.save(commit=False)
        Pagoproveedor.idempresa = didempresa
        Pagoproveedor.idsucursal = didsucursal
        Pagoproveedor.save()

        messages.success(self.request, ' PAGO creado exitosamente.')
        response = super().form_valid(form)
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('pagoprovcab_cargar', pk_token=pk_encriptado)


class pagoprovcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_pagoproveedor'

    model = Pagoproveedor
    form_class = PagoproveedorForm
    template_name = 'compras/pagoproveedor.html'
    success_url = reverse_lazy('pagoprovcab_editar')

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Pagoproveedor, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)

        context['title'] = '  EDITAR PAGO PROVEEOR  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/pagoprovcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'PAGO editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('pagoprovcab_cargar', kwargs={'pk_token': pk_token})


class pagoprovcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.delete_pagoproveedor'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        pk = desencriptar_datos2(pk_token,self.request)
        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagoproveedor, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoprovcab_cargar', pk_token=0)
        else:
            return redirect('pagoprovcab_cargar', pk_token=pk_token)


def pagoprovfact_listar(request):
    if not request.user.has_perm('compras.view_pagoprovfact'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response
    pk = request.POST['id_pk']
    idpagoproveedor = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']
    print(' promveedor ' + str(idpagoproveedor))
    if int(orden) == 0:
        objetos = Pagoprovfact.objects.filter(idpagoproveedor=idpagoproveedor).order_by('orden')
    if int(orden) >= 1:
        objetos = Pagoprovfact.objects.filter(idpagoproveedor=idpagoproveedor, orden=orden)

   # print(str(objetos.count()))

    datos = []

    for objeto in objetos:
        factura = ''
        idcomprascuotas = (objeto.idcomprascuotas)
        obj = Comprascuotas.objects.filter(idcomprascuotas=idcomprascuotas)
        idcompracab = ([(detalle.idcompracab) for detalle in obj])[0].idcompracab
        print(" idcompracab "+ str(idcompracab))

        obj = Comprascuotas.objects.filter(idcomprascuotas=idcomprascuotas)
        nrocuota = ([(detalle.orden) for detalle in obj])[0]
        print(" nrocuota "+ str(nrocuota))
        obj = Compracab.objects.filter(idcompracab=idcompracab)
        factura = ([(detalle.nrofactura) for detalle in obj])[0]
        print(" factura "+ str(factura))

        formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"
        fecha = objeto.fecha.strftime(formato)
        fecha = datetime.strptime(fecha, "%y-%m-%d")
        fecha = str(fecha.day) + "-" + str(fecha.month) + "-" + str(fecha.year)

        datos.append({
            'pkfd': encriptar_datos2(objeto.idpagoprovfact,request),
            'orden': objeto.orden,
            'fecha':fecha,
            'factura': factura,
            'nrocuota': nrocuota,
            'saldo': f"{(objeto.saldo):.0f}",
            'monto': f"{(objeto.monto):.0f}",
        })
      #  print(" datos   " + str(datos))

    Response = JsonResponse({'datos':datos,'success': True, 'message': ''})
    return Response

class pagoprovfact_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_Pagoprovfact'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        skey = iskey(request)

        action = request.POST.get('action')
        pk = desencriptar_datos2(pk_token,request)
        obj = Pagoprovfact.objects.filter(idpagoprovfact=pk)
        pk_token2 = (int(([(detalle.idpagoproveedor) for detalle in obj])[0].idpagoproveedor))
        pk_token3 = encriptar_datos2(pk_token2,request)
        #print ("  pk_token2 " +str(pk_token2))
        #print ("  pk_token3 " +str(pk_token3))


        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagoprovfact, pk=pk)
            try:
                instance.delete()
                orden = 0
                objetos = Pagoprovfact.objects.filter(idpagoproveedor=pk_token2).order_by('orden')
                for objeto in objetos:
                    objeto.orden = orden = orden + 1
                    objeto.save()

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoprovcab_cargar', pk_token=pk_token3)
        else:
            return redirect('pagoprovcab_cargar', pk_token=pk_token3)



class pagoprovafact_listar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_Pagoprovfact'

    def get(self, request, pk_token):
        if pk_token == "0":
            return redirect('pagoprovcab_cargar', pk_token=0)
        datos = []
        idpagoproveedor = desencriptar_datos2(pk_token,request)
        print( ' idpagoproveedor   ' + str(idpagoproveedor))

        obj = Pagoproveedor.objects.filter(idpagoproveedor=idpagoproveedor)
        idproveedor = ([(detalle.idproveedor) for detalle in obj])[0].idproveedor

        print( ' proveedor 1  ' + str(idproveedor))
        #objetos = Comprascuotas.objects.filter(idproveedor_id=idproveedor,saldo__gt=0).order_by('fechavto')  # Recuperar la compra por su clave primaria
        objetos = Comprascuotas.objects.filter(idproveedor_id=idproveedor,saldo__gt=0).order_by('fechavto')  # Recuperar la compra por su clave primaria
        cantr=objetos.count()

        print( ' proveedor 2 ' + str(idproveedor))
        print( ' cantr ' + str(cantr))


        for objeto in objetos:
            formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"

            idcompracab = objeto.idcompracab.idcompracab
            print(  ' idcompracab ' + str(idcompracab))
            obj = Compracab.objects.filter(idcompracab=idcompracab)
            factura = ([(detalle.nrofactura) for detalle in obj])[0]
            fecha = ([(detalle.fecha) for detalle in obj])[0].strftime(formato)
            fecha = datetime.strptime(fecha, "%y-%m-%d")
            fecha =  str(fecha.day) + "-"+ str(fecha.month) + "-"+str(fecha.year)

            total = ([(detalle.total) for detalle in obj])[0]

            formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"
            fechavto=objeto.fechavto.strftime(formato)
            fechavto = datetime.strptime(fechavto, "%y-%m-%d")
            fechavto =  str(fechavto.day) + "-"+ str(fechavto.month) + "-"+str(fechavto.year)

            obj = Pagoprovfact.objects.filter(idcomprascuotas=objeto.idcomprascuotas)
            salodpag = sum([detalle.monto for detalle in obj])
            saldo=objeto.monto-(salodpag)
            if saldo>0:
                datos.append({
                    'pkfd': encriptar_datos2(objeto.idcomprascuotas,request),
                    'pkpp': encriptar_datos2(idpagoproveedor,request),
                    'fechafactura': fecha,
                    'factura': factura,
                    'total': f"{(total):,.0f}",
                    'fechavto': fechavto,
                    'cuota': objeto.orden,
                    'saldo': f"{(saldo):,.0f}",
                    'monto': f"{(saldo):,.0f}",
                })

        return render(request, 'compras/provcuotalst.html', {'cuota': datos,'pk_token': pk_token})


class pagoprovfact_agregar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.add_Pagoprovfact'

    def get(self, request, pk_token1,pk_token2):

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        idpagoproveedor = desencriptar_datos2(pk_token1, request)
        idcomprascuotas = desencriptar_datos2(pk_token2, request)
        instance_pag_prov = Pagoproveedor.objects.get(pk=int(idpagoproveedor))  # Asegúrate de que `idcompracab` sea un entero
        instance_comp_cuotas = Comprascuotas.objects.get(pk=int(idcomprascuotas))  # Asegúrate de que `idcompracab` sea un entero

        obj = Pagoprovfact.objects.filter(idcomprascuotas=idcomprascuotas)
        totalpago = sum([detalle.monto for detalle in obj])
        objetos = Comprascuotas.objects.filter(idcomprascuotas=idcomprascuotas)
        for objeto in objetos:
            saldo=objeto.monto-totalpago

            pagoprovfact = Pagoprovfact()
            pagoprovfact.idpagoproveedor = instance_pag_prov
            pagoprovfact.idcomprascuotas = idcomprascuotas
            pagoprovfact.orden = objeto.orden
            pagoprovfact.fecha = objeto.fechavto
            pagoprovfact.saldo = saldo
            pagoprovfact.monto = saldo
            pagoprovfact.idempresa = didempresa
            pagoprovfact.idsucursal = didsucursal
            pagoprovfact.save()

            orden = 0
            objetos = Pagoprovfact.objects.filter(idpagoproveedor=idpagoproveedor).order_by('idpagoprovfact')
            for objeto in objetos:
                objeto.orden = orden = orden + 1
                objeto.save()

        return redirect('pagoprovcab_cargar', pk_token=pk_token1)


def pagoprovfact_editar(request):
    if not request.user.has_perm('compras.change_pagoprovfact'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idpagoproveedor = int(desencriptar_datos2(pkf,request))
        orden = request.POST['orden']
        monto = request.POST['monto']


        objetos = Pagoprovfact.objects.filter(idpagoproveedor=idpagoproveedor, orden=orden)
        idcomprascuotas= ([(detalle.idcomprascuotas) for detalle in objetos])[0]
        anterior = sum([ detalle.monto for detalle in objetos])
        objetos = Pagoprovfact.objects.filter(idcomprascuotas=idcomprascuotas)
        totalpagado = sum([ detalle.monto for detalle in objetos])
        obj = Comprascuotas.objects.filter(idcomprascuotas=idcomprascuotas)
        cuota = (int(([(detalle.monto) for detalle in obj])[0]))
        saldo=float(totalpagado)-float(anterior)+float(monto)
        saldo=float(cuota)-saldo
        valmax=float(cuota)-(float(totalpagado)-float(anterior))

        #print (" anterior " + str(anterior))
        #print (" totalpagado " + str(totalpagado))
        #print (" cuota " + str(cuota))
        #print (" monto " + str(monto))
        #print (" saldo " + str(saldo))
        #print (" valmax " + str(valmax))

        if saldo < 0:
            response = {'success': False, 'message': 'Monto supera la cuota valor maximo '+ str(valmax)}
            return JsonResponse(response)

        objetos = Pagoprovfact.objects.filter(idpagoproveedor=idpagoproveedor,orden=orden)
        for objeto in objetos:
            objeto.monto = monto
            objeto.save()
        response = {'success': True}
        return JsonResponse(response)


def pagoprovpago_listar(request):
    if not request.user.has_perm('compras.view_Pagoprovforma'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk_token = request.POST['id_pk']
    if pk_token == "0":
        return redirect('pagoprovcab_cargar', pk_token=0)

    pk = request.POST['id_pk']
    skey = iskey(request)

    idpagoproveedor = int(desencriptar_datos2(pk,request))
    #print("idpagoproveedor "+ str(idpagoproveedor))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Pagoprovforma.objects.filter(idpagoproveedor=idpagoproveedor)
    if int(orden) >= 1:
        objetos = Pagoprovforma.objects.filter(idpagoproveedor=idpagoproveedor)
   # print(str(objetos.count()))

    datos = []
    tipopago = ['efectivo', 'cheque', 'tarjeta']

    for objeto in objetos:
        itipopago = objeto.idtipopago
        stp = tipopago[int(itipopago)]

        datos.append({
            'pkpf': encriptar_datos2(objeto.idpagoprovforma,request),
            'tipopago': stp,
            'monto': f"{(objeto.monto):,.0f}",
            'nrodoc': objeto.nrodoc,
            'banco': objeto.banco,
            'ctacte': objeto.ctacte,
        })
      #  print(" datos   " + str(datos))

    Response = JsonResponse({'datos':datos,'success': True, 'message': ''})
    return Response



def pagoprovpago_agregar(request):
    if not request.user.has_perm('compras.add_pagoprovforma'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idpagoproveedor = int(desencriptar_datos2(pkf,request))
        idtipopago = request.POST['tipopago']
        montop = request.POST['montop']
        nrodoc = request.POST['nrodoc']
        banco = request.POST['banco']
        ctacte= request.POST['ctacte']
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        instance_pag_prov = Pagoproveedor.objects.get(pk=int(idpagoproveedor))  # Asegúrate de que `idcompracab` sea un entero

        tipopago = ['efectivo', 'cheque', 'tarjeta']
        obj = Pagoproveedor.objects.filter(idpagoproveedor=idpagoproveedor)
        idproveedor = ([(detalle.idproveedor) for detalle in obj])[0]
        fecha = ([(detalle.fecha) for detalle in obj])[0]

        for i in range(3):
            if idtipopago==tipopago[i]:
                idtipopago=i

        pvf = Pagoprovforma()
        pvf.idpagoproveedor=instance_pag_prov
        pvf.idtipopago = idtipopago
        pvf.monto = montop
        pvf.nrodoc = nrodoc
        pvf.fecha=fecha
        pvf.banco=banco
        pvf.idproveedor = idproveedor
        pvf.ctacte = ctacte
        pvf.idempresa = didempresa
        pvf.idsucursal = didsucursal
        pvf.save()
        response = {'success': True}
        return JsonResponse(response)


class pagoprovpago_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_pagoprovforma'

    def get(self, request,pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        skey = iskey(request)
        pk = desencriptar_datos2(pk_token,request)
        #print ("  pk " +str(pk))

        obj = Pagoprovforma.objects.filter(idpagoprovforma=pk)
        pk_token2 = int(([(detalle.idpagoproveedor) for detalle in obj])[0].idpagoproveedor) if obj else 0
        pk_token3 = encriptar_datos2(pk_token2,request)
       # print ("  pk_token " +str(pk))
        #print ("  pk_token2 " +str(pk_token2))
        #print ("  pk_token3 " +str(pk_token3))

        if action == 'CONFIRMAR':
            instance = get_object_or_404(Pagoprovforma, pk=pk)
            try:
                instance.delete()

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')

            return redirect('pagoprovcab_cargar', pk_token=pk_token3)
        else:
            return redirect('pagoprovcab_cargar', pk_token=pk_token3)


