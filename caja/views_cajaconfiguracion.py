from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from pyexpat.errors import messages
from django.contrib import messages

from caja.forms import *
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from stock.models import Deposito

def seriedet_listar(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    tseriedet = seriedet.objects.filter(idempresa=didempresa)
    for objeto in tseriedet:
        objeto.pksd = encriptar_datos2(objeto.idseriedet,request)
        objeto.serie = caja_obtenerserie(didempresa,objeto.idserie)
        objeto.documento = caja_obtenerdocumento(didempresa,objeto.iddocumentos)

    return render(request, 'caja/caja_seriedet_listar.html', {'seriedet': tseriedet })


class seriedet_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'caja.view_seriedet'
    model = seriedet
    form_class = seriedetForm
    template_name = 'caja/cajaseriedet.html'

    def get(self, request,pk_token):
        seriedets = None
        tseries = None
        tdocumentos = None
        tdeposito= None
        tusuario= None
        sserie=''
        sdocumento=''
        susuario=''

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        tseries=obtenerserie(didempresa, didsucursal)
        tdocumentos=obtenerdocumentos(didempresa, didsucursal)
        tdeposito=obtenerdepositos(didempresa, didsucursal)
        tusuario= obtenerusuarios(didempresa, didsucursal)
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token, request)
           # pk_desencriptado=1
            try:
                seriedets = seriedet.objects.get(idempresa=didempresa,idseriedet=pk_desencriptado)
                obj = serie.objects.filter(idempresa=didempresa, idserie=int(seriedets.idserie))
                sserie = ([(detalle.serie) for detalle in obj])[0] if obj else ''
                obj = documentos.objects.filter(idempresa=didempresa,iddocumentos=int(seriedets.iddocumentos))
                sdocumento = ([(detalle.documento) for detalle in obj])[0] if obj else ''
                obj = User.objects.filter(id=seriedets.idusuario)
                susuario = ([(detalle.username) for detalle in obj])[0] if obj else ''

            except (ValueError, seriedets.DoesNotExist):
                tseries = None
                tdocumentos = None
                tdeposito = None
                sserie = ''
                sdocumento = ''
                usuarios = ''


        context = {'seriedets': seriedets}  # Crear un diccionario de contexto
        context['title'] = '  SERIE DETALLE  '
        context['sidr'] = '/seriedet/' + str(pk_token) + '/cargar/'
        context['pka'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['var2']= False
        context['serie']= sserie
        context['documento']= sdocumento
        context['series']= tseries
        context['depositos']= tdeposito
        context['documentos']= tdocumentos
        context['susuario']= susuario
        context['usuarios']= tusuario

        return render(request, self.template_name, context)

class seriedet_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'caja.add_seriedet'
    model = seriedet
    form_class = seriedetForm
    template_name = 'caja/cajaseriedet.html'
    success_url = reverse_lazy('seriedet_crear')

    seriedets = None


    def dispatch(self, *args, **kwargs):
        return super(seriedet_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        tseries = obtenerserie(didempresa, didsucursal)
        tdocumentos = obtenerdocumentos(didempresa, didsucursal)
        tdeposito = obtenerdepositos(didempresa, didsucursal)
        tusuario= obtenerusuarios(didempresa, didsucursal)

        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR DETALLE '
        context['sidr'] = '/seriedet/crear/'
        context['var1']= False
        context['var2']= True
        context['series']= tseries
        context['depositos']= tdeposito
        context['documentos']= tdocumentos
        context['usuarios']= tusuario

        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        sserieaux = self.request.POST.get('serie')
        documentoaux = self.request.POST.get('documento')
        usuario = self.request.POST.get('usuario')

        obj = serie.objects.filter(idempresa=didempresa, serie=sserieaux)
        didserie = ([(detalle.idserie) for detalle in obj])[0] if obj else '0'

        obj = documentos.objects.filter(idempresa=didempresa,documento=documentoaux )
        diddocumento = ([(detalle.iddocumentos) for detalle in obj])[0] if obj else '0'

        obj = User.objects.filter(username=usuario )
        didusuario = ([(detalle.id) for detalle in obj])[0] if obj else '0'
        eliminardidusuario(didusuario)

        seriedet = form.save(commit=False)
        seriedet.idempresa = didempresa
        seriedet.idsucursal = didsucursal
        seriedet.idserie = didserie
        seriedet.iddocumentos = diddocumento
        seriedet.idusuario = didusuario
        seriedet.save()

        messages.success(self.request, ' serie creado exitosamente.')
        response = super().form_valid(form)
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('seriedet_cargar', pk_token=pk_encriptado)


class seriedet_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'caja.chance_seriedet'
    model = seriedet
    form_class = seriedetForm
    template_name = 'caja/cajaseriedet.html'
    success_url = reverse_lazy('seriedet_editar')
    seriedets = None


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            idempresa = self.request.session.get('idempresa')
            idsucursal = self.request.session.get('idsucursal')
            didempresa = desencriptar_datos2(idempresa, self.request)
            didsucursal = desencriptar_datos2(idsucursal, self.request)
            if int(didempresa) < 1 or int(didsucursal) < 1:
                return redirect('login')

            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(seriedet, pk=pk)

    def get_context_data(self, **kwargs):
        pk_token = self.kwargs['pk_token']
        seriedets = None
        tseries = None
        tdocumentos = None
        tdeposito= None
        tusuario= None
        sserie=''
        sdocumento=''
        susuario=''

        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        tseries=obtenerserie(didempresa, didsucursal)
        tdocumentos=obtenerdocumentos(didempresa, didsucursal)
        tdeposito=obtenerdepositos(didempresa, didsucursal)
        tusuario= obtenerusuarios(didempresa, didsucursal)

        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,self.request)
           # pk_desencriptado=1
            try:
                seriedets = seriedet.objects.get(idempresa=didempresa,idseriedet=pk_desencriptado)
                obj = serie.objects.filter(idempresa=didempresa, idserie=int(seriedets.idserie))
                sserie = ([(detalle.serie) for detalle in obj])[0] if obj else ''
                obj = documentos.objects.filter(idempresa=didempresa,iddocumentos=int(seriedets.iddocumentos))
                sdocumento = ([(detalle.documento) for detalle in obj])[0] if obj else ''
                obj = User.objects.filter(id=seriedets.idusuario)
                susuario = ([(detalle.username) for detalle in obj])[0] if obj else ''


            except (ValueError, seriedets.DoesNotExist):
                tseries = None
                tdocumentos = None
                tdeposito = None
                tusuario = None
                sserie = ''
                sdocumento = ''
                susuario = ''

        context = {'seriedets': seriedets}  # Crear un diccionario de contexto
        context['title'] = '  EDITAR DETALLE  '
        context['sidr'] = '/seriedet/' + str(pk_token) + '/editar/'
        context['pka'] = pk_token
        context['pk_token'] = pk_token
        context['documento'] = sdocumento
        context['var1']= False
        context['var2']= True
        context['documento']= sdocumento
        context['series']= tseries
        context['serie']= sserie
        context['depositos']= tdeposito
        context['documentos']= tdocumentos
        context['susuario']= susuario
        context['usuarios']= tusuario

        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        sserieaux = self.request.POST.get('serie')
        documentoaux = self.request.POST.get('documento')
        usuario = self.request.POST.get('usuario')

        obj = serie.objects.filter(idempresa=didempresa, serie=sserieaux)
        didserie = ([(detalle.idserie) for detalle in obj])[0] if obj else '0'

        obj = documentos.objects.filter(idempresa=didempresa,documento=documentoaux )
        diddocumento = ([(detalle.iddocumentos) for detalle in obj])[0] if obj else '0'

        obj = User.objects.filter(username=usuario )
        didusuario = ([(detalle.id) for detalle in obj])[0] if obj else '0'
        eliminardidusuario(didusuario)
        seriedet = form.save(commit=False)
        seriedet.idempresa = didempresa
        seriedet.idsucursal = didsucursal
        seriedet.idserie = didserie
        seriedet.iddocumentos = diddocumento
        seriedet.idusuario = didusuario
        seriedet.save()

        messages.success(self.request, ' serie editado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('seriedet_cargar', pk_token=pk_encriptado)

def eliminardidusuario(didusuario):
    aseriedet = seriedet.objects.filter(idusuario=didusuario)
    # Itera sobre cada objeto de la serie y modifica el campo idusuario
    for serie_obj in aseriedet:
        serie_obj.idusuario = 0
        serie_obj.save()

class seriedet_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'stock.delete_seriedet'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        if pk_token == "0":
            return redirect('seriedet_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':

            skey = iskey(request)
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(seriedet, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('seriedet_cargar', pk_token=0)
        else:
            return redirect('seriedet_cargar', pk_token=pk_token)


def caja_configuracion(request):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    return render(request, 'caja/cajaconfiguracion.html')

def obtenerserie(idempresa,idsucursal):
    seriest = []
    series = serie.objects.filter(idempresa=idempresa,idsucursal=idsucursal).order_by('serie')
    cantr = series.count()
    if cantr==0 :
        return None
    for objeto in series:
        seriest.append({
            'idserie': objeto.idserie,
            'serie':  objeto.serie,
        })

    return seriest

def obtenerdocumentos(idempresa,idsucursal):
    sdocumento = []
    docs = documentos.objects.filter(idempresa=idempresa,idsucursal=idsucursal).order_by('documento')
    cantr = docs.count()
    if cantr==0 :
        return None
    for objeto in docs:
        sdocumento.append({
            'iddocumento': objeto.iddocumentos,
            'documento':  objeto.documento,
        })

    return sdocumento

def obtenerdepositos(idempresa, idsucursal):
    sdepositos = []
    dep = Deposito.objects.filter(idempresa=idempresa,idsucursal=idsucursal).order_by('deposito')
    cantr = dep.count()
    if cantr==0 :
        return None
    for objeto in dep:
        sdepositos.append({
            'iddeposito': objeto.iddeposito,
            'deposito':  objeto.deposito,
        })

    return sdepositos


def caja_cmbdocumentos(request):
    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        doc = documentos.objects.filter(idempresa=didempresa).values_list('documento')
        nombres = list(doc)
        Response = JsonResponse({'datos': nombres})
        return Response

def caja_obtenerdocumento(didempresa,diddocumemnto):
    sldoc=''
    doc = documentos.objects.filter(idempresa=didempresa,iddocumentos=diddocumemnto).values_list('documento')
    cantr = doc.count()
    if cantr > 0:
        sldoc = list(doc)[0][0]
        print(' documento '+str(sldoc))
    return sldoc


def caja_obtenerserie(didempresa, didserie):
    sldoc=''
    doc = serie.objects.filter(idserie=didserie, idempresa=didempresa).values_list('serie')
    cantr = doc.count()
    if cantr > 0:
        ldoc = list(doc)[0][0]
    return ldoc

def obtenerusuarios(didempresa, didsucursal):
    susuarios = []
    uempresa = userempresa.objects.filter(idempresa=didempresa).values_list('idusuario', flat=True).distinct()
    # Luego, puedes obtener los objetos de usuario utilizando estos IDs únicos
    usuarios_unicos = User.objects.filter(id__in=uempresa)
    cantr = usuarios_unicos.count()
    if cantr==0 :
        return None
    for objeto in usuarios_unicos:
        susuarios.append({
            'idusuario': objeto.id,
            'usuario':  objeto.username,
        })
    return susuarios
