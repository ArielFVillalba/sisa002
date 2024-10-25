from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *


class inventario_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'stock.view_inventario_cab'
    model = Inventario_cab
    form_class = InvcabForm
    template_name = 'stock/inventario.html'
    success_url = reverse_lazy('inventario_cargar')

    def get(self, request,pk_token):
        idinvcab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token, request)
            idinvcab = Inventario_cab.objects.get(idinventario_cab=int(pk_desencriptado))  # Recuperar la compra por su clave primaria

        context = {'idinvcab': idinvcab}  # Crear un diccionario de contexto
        context['title'] = '  INVENTARIO  '
        context['sidr'] = '/inventario/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= False
        context['var2']= False
        context['hab1']= True
        context['hab2']= True
        return render(request, self.template_name, context)

def inv_generarbase(request):
    if not request.user.has_perm('ventas.view_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    operador = request.user.username
    fecha = request.POST['fecha']
    nrotoma = request.POST['nrotoma']
    deposito = request.POST['deposito']
    obs = request.POST['obs']
    flia = request.POST['flia']
    filam = flia.split("-")


    if es_numerico(nrotoma)==False:
        Response = JsonResponse({'success': False, 'message': 'Nro detoma invalida'})
        return Response

    obj = Deposito.objects.filter(idempresa=didempresa,deposito=deposito)
    dep = ([str(detalle.deposito) for detalle in obj])[0] if obj else None
    if dep is None:
        Response = JsonResponse({'success': False, 'message': 'Nro detoma invalida'})
        return Response

    obj = Inventario_cab.objects.filter(idempresa=didempresa,nromov=nrotoma)
    nrot = ([str(detalle.nromov) for detalle in obj])[0] if obj else None
    if nrot==nrotoma:
        Response = JsonResponse({'success': False, 'message': 'Nro detoma invalida'})
        return Response


    filamcant = len(filam)
    qs= None
    resultados = []
    for subcadena in filam:
        subcadena = subcadena.replace("_", ".")
        while ".0" in subcadena:
            subcadena = subcadena.replace(".0", "")

        subcadena=subcadena.strip()

        ifamiliaw = familia.objects.filter(codigo__startswith=subcadena,idempresa=didempresa)
        ifamilia = ifamiliaw.order_by('n1','n2','n3','n4','n5','n6','n7')
        resultados.extend(ifamilia)

    articulos = []
    codant='0'
    for objeto in resultados:
        codi = objeto.codigo

        if codant not in codi:
           # print(" codigo no sup  = " + str(objeto.codigo))
        #else:
            codant=objeto.codigo
           # print(" codigo sup  = " + str(objeto.codigo))
            auxcod=objeto.codigo
            iart = Articulo.objects.filter(codigoflia__startswith=auxcod, idempresa=didempresa)
            articulos.extend(iart)
    didinventariocab=inventariocab(fecha, nrotoma, deposito, obs, flia, didempresa, didsucursal,operador)
    didinventariocab=inventariodet(didinventariocab,articulos,nrotoma,deposito,didempresa,didsucursal,operador)

    Response = JsonResponse({'success': True, 'message': ''})
    return Response

def es_numerico(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False

def inventariocab(fecha,nromov,deposito,obs,familias,idempresa,idsucursal,operador):

    fecha_de_hoy = date.today()
    objeto = Inventario_cab()
    objeto.fecha = fecha_de_hoy
    objeto.fechagenerado = timezone.now()
    objeto.nromov = nromov
    objeto.deposito = deposito
    objeto.obs = obs
    objeto.familias = familias
    objeto.idempresaselec = 0
    objeto.idsucursalselec = 0
    objeto.idsucursal = idsucursal
    objeto.idempresa = idempresa
    objeto.operador = operador
    objeto.save()
    didinventariocab=objeto.idinventario_cab
    return didinventariocab

def inventariodet(didinventariocab,articulos,nromov,deposito,didempresa,didsucursal,operador):


    for artobj in articulos:
        didarticulo=artobj.idarticulo
        descripcion=artobj.descripcion
        precio=artobj.precio
        costo =artobj.costo
        codigo =artobj.codigo
        codigoflia=artobj.codigoflia
        unidad =artobj.unidad
        iva =artobj.iva
        unidad = unidad.lower()
        exist=0
        lexistencia = Existencia.objects.filter(codigo=codigo,deposito=deposito,idempresa=didempresa)
        for lexist in lexistencia:
            exist = lexist.cantidad
            if unidad == 'unidad':
                exist = int(exist)

        fecha_de_hoy = date.today()
        fecha_hora_actual = datetime.now()
        fecha_hora = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
        Inventario_cab_instance = Inventario_cab.objects.get(pk=int(didinventariocab))
        articulo_instance = Articulo.objects.get(pk=float(didarticulo))

        objeto = Inventario_det()
        objeto.idinventario_cab = Inventario_cab_instance
        objeto.idarticulo=articulo_instance
        objeto.codigo=codigo
        objeto.codigoflia=codigoflia
        objeto.descripcion=descripcion
        objeto.unidad=unidad
        objeto.precio=precio
        objeto.iva = iva
        objeto.costo = costo
        objeto.fechagenerado = timezone.now()
        objeto.nromov = nromov
        objeto.deposito = deposito
        objeto.existlogica = exist
        objeto.idempresaselec = 0
        objeto.idsucursalselec = 0
        objeto.idsucursal = didsucursal
        objeto.idempresa = didempresa
        objeto.operador = operador
        objeto.save()
    return didempresa


def inv_tomainv(request):

    if not request.user.has_perm('ventas.view_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    fecha = request.POST['fecha']
    nrotoma = request.POST['nrotoma']
    deposito = request.POST['deposito']

    datos='';
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response

def inv_toma_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.has_perm('stock.add_inventario_toma'):
                return redirect('inv_toma_empsuc')
            else:
                return redirect('inv_toma_login')
        else:
            return redirect('inv_toma_login')


    else:
        errors = ""
        if request.user.is_authenticated:
            logout(request)
        request.session['idempresa'] = 0
        request.session['idsucursal'] = 0
        request.session['empresa'] = ""
        request.session['sucursal'] = ""
        titulo = "INICIAR SESION"
        return render(request, 'stock/inventariologin.html', {'messages': errors, 'title': titulo})

def obtenerempre(user_id,request):
    empresas = []
    i=0
    idemp=0
    objetos = userempresa.objects.filter(idusuario=user_id).order_by('idempresa')
    cantr = objetos.count()
    for objeto in objetos:
        idempresa = int(objeto.idempresa)
        obj = Empresa.objects.filter(idempresa=idempresa)
        nempresa = ([str(detalle.empresa) for detalle in obj])[0]

        if i == 0:
            didempresa = idempresa
            dnempresa = nempresa
            i = 1
        if idemp < idempresa:
            empresas.append({
                'idempresa': encriptar_datos2(str(idempresa),request),
                'empresa': nempresa,
            })
        idemp = idempresa
    return empresas

def obtenersucursal(didempresa,request):
    sucursales = []
    objetos = Sucursal.objects.filter(idempresa=didempresa)
    i = 0
    cantr = objetos.count()
    for objeto in objetos:
        if i == 0:
            didsucursal=objeto.idsucursal
            dnsucursal=objeto.sucursal
            i=1

        sucursales.append({
            'idsucural': encriptar_datos2(str(objeto.idsucursal),request),
            'sucursal': objeto.sucursal,
        })


    return sucursales


def inv_toma_empsuc(request):
    if not request.user.has_perm('stock.add_inventario_toma'):
        return redirect('inv_toma_login')

    user_id = request.user.id
    empresa = obtenerempresa(user_id, request)
    if empresa:
        idempresa = empresa[0]['idempresa']
        sempresa = empresa[0]['empresa']
        idempresa = desencriptar_datos2(str(idempresa), request)
        sucursal = obtenersucursal(idempresa,request)
        if sucursal:
            ssucursal = sucursal[0]['sucursal']
            context = {'title': '  TOMA INVENTARIO  '}  # Crear un diccionario de contexto
            context['empresas'] = empresa
            context['sucursales'] = sucursal
            context['sempresa'] = sempresa
            context['ssucursal'] = ssucursal
            return render(request, 'stock/inventariotomaemp.html',context)
            #return render(request, 'stock/inventariotoma.html')

        else:
            return redirect('inv_toma_login')
    else:
        return redirect('inv_toma_login')


def inv_toma_carga(request):
    if not request.user.has_perm('stock.add_inventario_toma'):
        return redirect('inv_toma_login')

    nrotoma = request.GET.get('nrotoma', '')
    didempresa = request.GET.get('didempresa', '')
    didsucursal = request.GET.get('didsucursal', '')
    user_id = request.user.id
    operador= request.user.username
    didempresa = desencriptar_datos2(str(didempresa), request)
    didsucursal = desencriptar_datos2(str(didsucursal), request)

    valor = True
    valor=verificarusuemp(user_id, didempresa)
    if valor == True:
        valor = verificarnrotoma(didempresa, nrotoma)
    if valor == True:
        request.session['idempresa'] = encriptar_datos2(didempresa,request)
        request.session['idsucursal'] =encriptar_datos2(didsucursal,request)

    if valor ==False:
        return redirect('inv_toma_empsuc')

    obj = Inventario_cab.objects.filter(idempresa=didempresa,nromov=nrotoma)
    deposito = ([str(detalle.deposito) for detalle in obj])[0] if obj else None
    tomainv = obtenertomainv(nrotoma, didempresa, operador)

    context = {'title': '  TOMA INVENTARIO  '}  # Crear un diccionario de contexto
    context['nrotoma'] = nrotoma
    context['deposito'] = deposito
    context['tomainv'] = tomainv
    return render(request, 'stock/inventariotoma.html',context)


def cargarcodigo(request):
    if not request.user.has_perm('stock.add_inventario_toma'):
        return redirect('inv_toma_login')

    nrotoma = request.GET.get('nrotoma', '')
    codigo = request.GET.get('codigo', '')
    cantidad = request.GET.get('cantidad', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    user_id = request.user.id
    operador = request.user.username

    valor=True
    msn=''
    valor= es_numerico(nrotoma)
    if valor ==True:
        valor=es_numerico(codigo)
        msn = ' codigo '
    if valor == True:
        valor=es_numerico(cantidad)
        msn = ' cantidad  '
    if valor == True:
        obj = Articulo.objects.filter(idempresa=didempresa, codigo=codigo)
        nrocodigo = ([int(detalle.codigo) for detalle in obj])[0] if obj else None
        msn = ' codigo no existe  '
        if nrocodigo == None:
            valor=False

    if valor == True:
        codver=verificarcodigodet(didempresa,nrotoma,codigo)
        if codver == False:
            cargardetfaltante(codigo,nrotoma,didempresa,didsucursal,operador)
    if valor == False:
        operador = request.user.username
        obj = Inventario_cab.objects.filter(idempresa=didempresa, nromov=nrotoma)
        deposito = ([str(detalle.deposito) for detalle in obj])[0] if obj else None
        tomainv = obtenertomainv(nrotoma, didempresa, operador)  # listado de tomas realizadas
        context = {'title': '  TOMA INVENTARIO  '}  # Crear un diccionario de contexto
        context['nrotoma'] = nrotoma
        context['deposito'] = deposito
        context['tomainv'] = tomainv
        context['messages'] = ["error registrado", "error en "+msn]
        context['success'] = True  # Indicate success
        return render(request, 'stock/inventariotoma.html', context)

    obj = Inventario_cab.objects.filter(idempresa=didempresa,nromov=nrotoma)
    idinventario_cab = ([int(detalle.idinventario_cab) for detalle in obj])[0] if obj else None
    deposito = ([str(detalle.deposito) for detalle in obj])[0] if obj else None
    fechagenerado = ([str(detalle.fechagenerado) for detalle in obj])[0] if obj else None
    objdet = Inventario_det.objects.filter(idempresa=didempresa,nromov=nrotoma,codigo=codigo)
    idinventario_det = ([(detalle.idinventario_det) for detalle in objdet])[0] if objdet else None
    descripcion = ([str(detalle.descripcion) for detalle in objdet])[0] if objdet else None
    unidad = ([str(detalle.unidad) for detalle in objdet])[0] if objdet else None
    precio = ([(detalle.precio) for detalle in objdet])[0] if objdet else None
    iva = ([(detalle.iva) for detalle in objdet])[0] if objdet else None
    costo = ([(detalle.costo) for detalle in objdet])[0] if objdet else None
    existlogica = ([(detalle.existlogica) for detalle in objdet])[0] if objdet else None
    codigoflia = ([(detalle.codigoflia) for detalle in objdet])[0] if objdet else None
    operador= request.user.username
    diferencia =float(cantidad) - float(existlogica)
    difcosto=float(diferencia)*float(costo)

    Inventario_cab_instance = Inventario_cab.objects.get(pk=int(idinventario_cab))
    Inventario_det_instance = Inventario_det.objects.get(pk=int(idinventario_det))
    articulo_instance = Articulo.objects.get(codigo=float(codigo),idempresa=didempresa)

    fecha_de_hoy = date.today()
    objeto = Inventario_toma()
    objeto.idinventario_cab = Inventario_cab_instance
    objeto.idinventario_det=Inventario_det_instance
    objeto.idarticulo = articulo_instance
    objeto.codigo = codigo
    objeto.codigoflia=codigoflia
    objeto.exist = cantidad
    objeto.diferencia = diferencia
    objeto.difcosto = difcosto
    objeto.descripcion = descripcion
    objeto.fechatoma=timezone.now()
    objeto.unidad = unidad
    objeto.precio = precio
    objeto.iva = iva
    objeto.costo = costo
    objeto.fechagenerado = fechagenerado
    objeto.nromov = nrotoma
    objeto.deposito = deposito
    objeto.existlogica = existlogica
    objeto.idempresaselec = 0
    objeto.idsucursalselec = 0
    objeto.idsucursal = didsucursal
    objeto.idempresa = didempresa
    objeto.operador = request.user.username
    objeto.save()

    tomainv = obtenertomainv(nrotoma,didempresa,operador)  # listado de tomas realizadas
    context = {'title': '  TOMA INVENTARIO  '}  # Crear un diccionario de contexto
    context['nrotoma'] = nrotoma
    context['deposito'] = deposito
    context['tomainv'] = tomainv
    return render(request, 'stock/inventariotoma.html', context)

def obtenertomainv(nrotoma,didempresa,operador):
    conteo = []
    objetos = Inventario_toma.objects.filter(idempresa=didempresa,nromov=nrotoma,operador=operador).order_by('-idinventario_toma')
    i = 0
    for objeto in objetos:
        i=i+1
        if i == 8:
            return conteo
        cantidad= objeto.exist

        if objeto.unidad=='UNIDAD':
            canidadad=int(cantidad)
        else:
            canidadad=int(cantidad)

        conteo.append({
            'codigo': objeto.codigo,
            'cantidad': canidadad,
        })

    return conteo

def verificarusuemp(user_id,didempresa):
    valor=False
    objetos = userempresa.objects.filter(idusuario=user_id,idempresa=didempresa)
    cantr = objetos.count()
    if cantr>0:
        valor=True
    return valor

def verificarnrotoma(didempresa,nrotoma):
    valor=False
    objetos = Inventario_cab.objects.filter(idempresa=didempresa,nromov=nrotoma)
    cantr = objetos.count()
    if cantr>0:
        valor=True
    return valor

def verificarcodigodet(didempresa,nrotoma,codigo):
    valor=False
    objetos = Inventario_det.objects.filter(idempresa=didempresa,nromov=nrotoma,codigo=codigo)
    cantr = objetos.count()
    if cantr>0:
        valor=True
    return valor

def cargardetfaltante(codigo,nrotoma,didempresa,didsucursal,operador):

    obj = Inventario_cab.objects.filter(idempresa=didempresa, nromov=nrotoma)
    didinventariocab = ([int(detalle.idinventario_cab) for detalle in obj])[0] if obj else None
    deposito = ([str(detalle.deposito) for detalle in obj])[0] if obj else None
    objdet = Articulo.objects.filter(idempresa=didempresa,  codigo=codigo)
    articulos = ([str(detalle.descripcion) for detalle in objdet])[0] if objdet else None
    iart = Articulo.objects.filter(codigo=codigo, idempresa=didempresa)
    inventariodet(didinventariocab, iart, nrotoma, deposito, didempresa, didsucursal, operador)


def inv_ajuste_cargar(request):
    if not request.user.has_perm('stock.add_inventario_toma'):
        return redirect('inv_toma_login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    user_id = request.user.id

    context = {'title': '  AJUSTE INVENTARIO  '}  # Crear un diccionario de contexto
    return render(request, 'stock/inventarioajuste.html',context)


def inv_ajuste_procesar(request):
    if not request.user.has_perm('stock.add_inventario_toma'):
        return redirect('inv_toma_login')

    nrotoma = request.GET.get('nrotoma', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    procesar_ajuste(request,nrotoma,didempresa,didsucursal)
    context = {'title': '  AJUSTE INVENTARIO  '}  # Crear un diccionario de contexto
    return render(request, 'stock/inventarioajuste.html',context)

def procesar_ajuste(request,nrotoma,didempresa,didsucursal):
    objetos = Inventario_det.objects.filter(idempresa=didempresa,nromov=nrotoma,ajustado=False).order_by('codigo')
    for objeto in objetos:
        codigo=objeto.codigo
        deposito=objeto.deposito
        existlogica=objeto.existlogica
        detalles = Inventario_toma.objects.filter(idempresa=didempresa, nromov=nrotoma, codigo=codigo)
        exist = sum([detalle.exist for detalle in detalles])
        diferencia =exist-existlogica
        valor=verificarexistencia(didempresa, codigo, deposito)
        if valor==True:
            baseexistencia = Existencia.objects.filter(idempresa=didempresa, codigo=codigo, deposito=deposito)
            for baseexist in baseexistencia:
                baseexist.cantidad = float(baseexist.cantidad) + (float(diferencia))
                baseexist.save()
        else:
            agregarexistencia(didempresa,didsucursal, codigo, deposito, diferencia)

        fecha_hora_actual = datetime.now()
        fecha_hora= fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        aux = Inventario_det.objects.filter(idempresa=didempresa, nromov=nrotoma, codigo=codigo)
        for aux2 in aux:
            aux2.ajustado = True
            aux2.fechaajuste=timezone.now()
            aux2.exist =exist
            aux2.diferencia =diferencia
            aux2.difcosto=aux2.costo*diferencia
            aux2.operador= request.user.username
            aux2.save()

    return ''

def verificarexistencia(didempresa,codigo,deposito):
    valor=False
    objetos = Existencia.objects.filter(idempresa=didempresa,codigo=codigo,deposito=deposito)
    cantr = objetos.count()
    if cantr>0:
        valor=True
    return valor

def agregarexistencia(didempresa,didsucursal,codigo,deposito,cantidad):
    iart = Articulo.objects.filter(codigo=codigo, idempresa=didempresa)
    unidad = ([detalle.unidad for detalle in iart])[0] if iart else None
    objeto = Existencia()
    objeto.cantidad = cantidad
    objeto.codigo=codigo
    objeto.deposito=deposito
    objeto.unidad=unidad
    objeto.idempresa=didempresa
    objeto.idsucursal=didsucursal
    objeto.save()

def views_movdep_lst(request):
    return render(request, 'stock_inf/lstmovdeposito.html')

def views_inventario_lst(request):
    return render(request, 'stock_inf/inventarioinf.html')
