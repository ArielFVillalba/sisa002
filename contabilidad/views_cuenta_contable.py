from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from contabilidad.forms import CtacontableForm
from contabilidad.models import Cuentacontable, asiento_det
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
# Create your views here.
from django.db import transaction


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from contabilidad.forms import CtacontableForm
from contabilidad.models import Cuentacontable, asiento_det
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
# Create your views here.
from django.db import transaction


def ctacontable_filtar(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        return render(request, 'contabilidad/ctacontable_listar.html')
    else:
        return redirect('login')


def ctacontable_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    print("ctacontable_listar = "+str(cadena))
    cant=len(cadena)

    if cadena == "*"  or cadena == "0" or cadena == "":

        ictacontable = Cuentacontable.objects.filter(idempresa=didempresa).order_by('cuenta')
        for objeto in ictacontable:
            objeto.pkctacont = encriptar_datos2(objeto.idcuentacontable,request)
        return render(request, 'contabilidad/ctacontable_listar.html', {'ctacontable': ictacontable, 'cadena': '' })

    qs = Cuentacontable.objects.filter(idempresa=didempresa,cuenta=0)
    subcadenas = cadena.split(" ")
    for i in range(len(subcadenas)):

        qs1 = Cuentacontable.objects.filter(cuenta__icontains=subcadenas[i],idempresa=didempresa)
        qs=qs.union(qs1)
        qs = qs.union(qs1)
        qs2 = Cuentacontable.objects.filter(denominacion__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs2)
        qs3 = Cuentacontable.objects.filter(naturaleza__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs3)
        qs4 = Cuentacontable.objects.filter(nivel__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs4)
        qs5 = Cuentacontable.objects.filter(centro_costo__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs5)
        qs6 = Cuentacontable.objects.filter(asentable__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs6)

        ictacontable = qs
        for objeto in ictacontable:
            objeto.pkctacont = encriptar_datos2(objeto.idcuentacontable,request)

    return render(request, 'contabilidad/ctacontable_listar.html', {'ctacontable': ictacontable ,'cadena': cadena})


class ctacontable_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'contabiliad.view_cuentacontable'
    model = Cuentacontable
    form_class = CtacontableForm
    template_name = 'contabilidad/cuentacontable.html'
    context_object_name = 'cuentacontable'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        ctacontable = None
        if Cuentacontable.objects.filter(idempresa=1).exists():
            print("ya existe")
        else:
            cargar_cuentas_desde_json()

        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            ctacontable = Cuentacontable.objects.get(idcuentacontable=int(pk_desencriptado))  # Recuperar la compra por su clave primaria
            cuenta=ctacontable.cuenta
            denominacion=ctacontable.denominacion
            didempresa=ctacontable.idempresa
            nivel=ctacontable.nivel
            #reconocercuenta(cuenta, nivel)
            #ctolctamadre(cuenta, didempresa)
            #cargarcuenta(cuenta, denominacion, didempresa)
            #recorrregistro()}

        context = {'ctacontable': ctacontable}  # Crear un diccionario de contexto
        context['title'] = '  CUENTA CONTABLE  '
        context['sidr'] = '/ctacontable/' + str(pk_token) + '/cargar/'
        context['pkctacont'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        return render(request, self.template_name, context)

class ctacontable_crear(LoginRequiredMixin, ValidarPermisoMixin, CreateView):
    permission_required = 'contabiliad.add_cuentacontable'
    model = Cuentacontable
    form_class = CtacontableForm
    template_name = 'contabilidad/cuentacontable.html'
    success_url = reverse_lazy('ctacontable_crear')

    def dispatch(self, *args, **kwargs):
        return super(ctacontable_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CREAR CUENTA'
        context['sidr'] = '/ctacontable/crear/'
        context['var1'] = False
        context['var2'] = True
        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')

        try:
            didempresa = desencriptar_datos2(idempresa, self.request)
            didsucursal = desencriptar_datos2(idsucursal, self.request)
        except Exception as e:
            messages.error(self.request, f"Error en los datos de empresa o sucursal: {str(e)}")
            return self.form_invalid(form)

        if int(didempresa) < 1 or int(didsucursal) < 1:
            messages.error(self.request, "ID de empresa o sucursal inválido.")
            return redirect('login')

        cuenta = form.cleaned_data['cuenta']
        nivel = form.cleaned_data['nivel']
        asentable = form.cleaned_data['asentable']
        naturaleza = form.cleaned_data['naturaleza']
        denominacion= form.cleaned_data['denominacion']

        icuenta = len(cuenta.split("."))

        if int(nivel) != int(icuenta):
            messages.error(self.request, 'El nivel y la cuenta tienen distinto nivel.')
            return self.form_invalid(form)

        # Validaciones personalizadas
        if not (1 <= int(nivel) <= 7):
            messages.error(self.request, 'Nivel fuera del rango permitido (1 a 7).')
            return self.form_invalid(form)

        if asentable not in ("SI", "NO"):
            messages.error(self.request, 'El campo "Asentable" debe ser "SI" o "NO".')
            return self.form_invalid(form)

        if naturaleza not in ("DEUDOR", "ACREEDOR"):
            messages.error(self.request, 'El campo "Naturaleza" debe ser "DEUDOR" o "ACREEDOR".')
            return self.form_invalid(form)

        # Verificación de cuenta madre si el nivel es mayor a 1
        if int(nivel) > 1:
            cuentam = ctolctamadre(cuenta, didempresa)
            if not cuentam:
                messages.error(self.request, 'No existe cuenta madre para el nivel especificado.')
                return self.form_invalid(form)
        # Guardar la cuenta contable
        try:
            # Creamos la instancia sin guardar
            Cuentacontable = form.save(commit=False)
            Cuentacontable.idempresa = didempresa
            Cuentacontable.idsucursal = didsucursal
            Cuentacontable.save()

            cargarcuenta(cuenta, denominacion, didempresa)
            # Usamos la instancia Cuentacontable guardada para encriptar el pk
            pk_encriptado = encriptar_datos2(str(Cuentacontable.pk), self.request)
        except Exception as e:
            messages.error(self.request, f"Error al guardar la cuenta: {str(e)}")
            return self.form_invalid(form)

        messages.success(self.request, 'Cuenta creada exitosamente.')
        return redirect('ctacontable_cargar', pk_token=str(pk_encriptado))

    def form_invalid(self, form):
        # Sobrescribimos para mostrar mensajes de error
        messages.error(self.request, "Por favor corrige los errores en el formulario.")
        return super().form_invalid(form)


def cargarcuenta(cuenta, denominacion, didempresa):
    nivel = int(cuenta.count('.')) + 1
    cuentam = ctolctamadre(cuenta, didempresa) if nivel > 1 else cuenta

    print('cargarcuenta cuenta:', cuenta)
    print('cargarcuenta denominacion:', denominacion)
    print('cargarcuenta didempresa:', didempresa)

    # Obtener cuenta madre
    objetom = Cuentacontable.objects.get(cuenta=cuentam, idempresa=didempresa)

    # Inicializar niveles
    icod = cuenta.split(".")
    nivel = len(icod)
    n1 = icod[0] if nivel >= 1 else 0
    n2 = icod[1] if nivel >= 2 else 0
    n3 = icod[2] if nivel >= 3 else 0
    n4 = icod[3] if nivel >= 4 else 0
    n5 = icod[4] if nivel >= 5 else 0
    n6 = icod[5] if nivel >= 6 else 0
    n7 = icod[6] if nivel >= 7 else 0

    # Asignar denominaciones en el objeto madre
    if nivel == 1:
        objetom.cuenta1 = denominacion
    if nivel == 2:
        objetom.cuenta2 = denominacion
    if nivel == 3:
        objetom.cuenta3 = denominacion
    if nivel == 4:
        objetom.cuenta4 = denominacion
    if nivel == 5:
        objetom.cuenta5 = denominacion
    if nivel == 6:
        objetom.cuenta6 = denominacion
    if nivel == 7:
        objetom.cuenta7 = denominacion

    print(f"cargarcuenta n1: {n1}, n2: {n2}, n3: {n3}, n4: {n4}, n5: {n5}")
    print(f"Objetom cuenta1: {objetom.cuenta1}, cuenta2: {objetom.cuenta2}, cuenta3: {objetom.cuenta3}")

    try:
        # Buscar la cuenta a actualizar
        objeto = Cuentacontable.objects.get(cuenta=cuenta, idempresa=didempresa)
        print(f"cargarcuenta idcuentacontable: {objeto.idcuentacontable}")

        # Asignar valores a los campos
        objeto.n1 = n1
        objeto.n2 = n2
        objeto.n3 = n3
        objeto.n4 = n4
        objeto.n5 = n5
        objeto.n6 = n6
        objeto.n7 = n7

        objeto.cuenta1 = objetom.cuenta1
        objeto.cuenta2 = objetom.cuenta2
        objeto.cuenta3 = objetom.cuenta3
        objeto.cuenta4 = objetom.cuenta4
        objeto.cuenta5 = objetom.cuenta5
        objeto.cuenta6 = objetom.cuenta6
        objeto.cuenta7 = objetom.cuenta7

        objeto.save()
        objeto.refresh_from_db()  # Esto actualiza el objeto con los datos almacenados en la base de datos
        print("Después de guardar el objeto.")

        print("Objeto guardado exitosamente")
        objeto_recuperado = Cuentacontable.objects.get(idcuentacontable=objeto.idcuentacontable)
        print(f"Objeto recuperado: n3={objeto_recuperado.n3}, cuenta3={objeto_recuperado.cuenta3}")
        print(f"Objeto recuperado: objeto.idcuentacontable={objeto_recuperado.idcuentacontable}")

    except ObjectDoesNotExist:
        print(f"No se encontró un objeto con la cuenta {cuenta} y empresa {didempresa}.")


class ctacontable_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'contabiliad.chance_Cuentacontable'
    model = Cuentacontable
    form_class = CtacontableForm
    template_name = 'contabilidad/cuentacontable.html'

    def get_object(self, queryset=None):
        """ Obtiene el objeto a editar utilizando el token desencriptado """
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            return get_object_or_404(Cuentacontable, pk=pk)
        return None  # Asegurarse de que siempre se retorne algo

    def get_context_data(self, **kwargs):
        """ Agregar datos adicionales al contexto de la vista """
        context = super().get_context_data(**kwargs)

        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)

        # Redirigir si la empresa o sucursal no son válidas
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = self.kwargs['pk_token']
        ctacontable = None

        # Obtener la cuenta contable si el token no es "0"
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            ctacontable = Cuentacontable.objects.get(idcuentacontable=int(pk))

        # Contexto adicional
        context['title'] = 'EDITAR CUENTA'
        context['ctacontable'] = ctacontable
        context['sidr'] = f'/ctacontable/{pk_token}/editar/'
        context['pk_token'] = pk_token
        context['var1'] = False
        context['var2'] = True

        return context

    def form_valid(self, form):
        """ Valida el formulario antes de guardar los cambios """
        # Obtener los datos de la sesión
        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)

        # Verificar si la empresa y la sucursal son válidas
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        # Obtener los valores del formulario
        cuenta = form.cleaned_data['cuenta']
        nivel = form.cleaned_data['nivel']
        denominacion = form.cleaned_data['denominacion']
        asentable = form.cleaned_data['asentable']
        naturaleza = form.cleaned_data['naturaleza']

        icuenta = len(cuenta.split("."))

        if int(nivel) != int(icuenta):
            messages.error(self.request, 'El nivel y la cuenta tienen distinto nivel.')
            return self.form_invalid(form)


        # Verificación de duplicados (excluyendo la cuenta actual)
        if Cuentacontable.objects.filter(cuenta=cuenta, idempresa=didempresa).exclude(idcuentacontable=self.object.idcuentacontable).exists():
            messages.error(self.request, 'Ya existe una cuenta con esa combinación de cuenta e idempresa.')
            return self.form_invalid(form)

        # Validar el nivel de la cuenta
        if not (1 <= int(nivel) <= 7):
            messages.error(self.request, 'El nivel está fuera del rango permitido (1-7).')
            return self.form_invalid(form)

        # Validar los valores de "asentable" y "naturaleza"
        if asentable not in ("SI", "NO"):
            messages.error(self.request, 'El valor de "asentable" no es válido.')
            return self.form_invalid(form)

        if naturaleza not in ("DEUDOR", "ACREEDOR"):
            messages.error(self.request, 'El valor de "naturaleza" no es válido.')
            return self.form_invalid(form)

        # Verificar la cuenta madre si el nivel es mayor a 1
        if int(nivel) > 1:
            cuentam = ctolctamadre(cuenta, didempresa)
            if not cuentam:
                messages.error(self.request, 'No existe la cuenta madre para esta cuenta.')
                return self.form_invalid(form)

        # Si el formulario es válido, guardamos el objeto y luego llamamos a `cargarcuenta`
        with transaction.atomic():
            response = super().form_valid(form)  # Guardar el objeto principal

            # Llamar a la función para actualizar la cuenta
            try:
                cargarcuenta(cuenta, denominacion, didempresa)
            except Exception as e:
                messages.error(self.request, f'Error al cargar la cuenta: {str(e)}')
                return self.form_invalid(form)

            return response  # Retornar la respuesta después de guardar y actualizar

    def get_success_url(self):
        """ Redirigir a la página de éxito """
        messages.success(self.request, 'Cuenta editada exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('ctacontable_cargar', kwargs={'pk_token': pk_token})


class ctacontable_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'contabiliad.delete_cuentacontable'

    def get(self, request, pk_token):
        titulo = "¿ESTÁ SEGURO QUE DESEA ELIMINAR?"
        msg = "EL REGISTRO"
        if pk_token == "0":
            return redirect('ctacontable_cargar', pk_token=0)


        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)

        # Desencriptar el ID de la cuenta contable
        pk = desencriptar_datos2(pk_token, request)
        # Obtener la cuenta contable para su eliminación
        instance = get_object_or_404(Cuentacontable, pk=pk)
        cuenta = instance.cuenta
        print(f"Registrando esta cuenta: {cuenta}")

        #cuentas_hijas = Cuentacontable.objects.filter(cuenta__startswith=cuenta,idempresa=didempresa).exclude(idcuentacontable=pk)

        # Recorrer y mostrar cada cuenta hija
        #for cuenta_hija in cuentas_hijas:
        #    print(
        #        f"ID: {cuenta_hija.idcuentacontable}, Cuenta: {cuenta_hija.cuenta}, Denominación: {cuenta_hija.denominacion}")
        # Verificar si la cuenta tiene cuentas hijas
        asientodet = asiento_det.objects.filter(idcuentacontable=pk)
        for vastodet in asientodet:
            nro_asiento = vastodet.idasiento.nroasiento
            print(nro_asiento)  # O realizar la operación que desees con el número de asiento
            messages.error(self.request, 'cuenta utilizada por el asiento N° '+ str(nro_asiento))
            return redirect('ctacontable_cargar', pk_token=str(pk_token))

        # Verificar si la cuenta tiene cuentas hijas
        if Cuentacontable.objects.filter(cuenta__startswith=cuenta,idempresa=didempresa).exclude(idcuentacontable=pk).exists():
            messages.error(self.request, 'Esta cuenta contiene cuentas hijos y no puede ser eliminada.')
            return redirect('ctacontable_cargar', pk_token=str(pk_token))


        return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)

        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        # Desencriptar el ID de la cuenta contable
        pk = desencriptar_datos2(pk_token, request)
        # Obtener la cuenta contable para su eliminación
        instance = get_object_or_404(Cuentacontable, pk=pk)

        if pk_token == "0":
            return redirect('ctacontable_cargar', pk_token=0)

        # Si se confirma la acción, eliminar la cuenta
        if action == 'CONFIRMAR':
            try:
                instance.delete()
                messages.success(self.request, 'Cuenta eliminada exitosamente.')
                return redirect('ctacontable_cargar', pk_token=0)
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})

        # Si no se confirma, redirigir de vuelta
        return redirect('ctacontable_cargar', pk_token=str(pk_token))

def ctolctamadre(cuenta,didempresa):
    cuentam=""
    nivel =int(cuenta.count('.'))+1
    if nivel>1:
        cuentamadre=recuperar_cuenta_madre(cuenta).strip()
        print(' ctolctamadre 1  -'+ str(cuentamadre))
        print(' didempresa  '+ str(didempresa))
        objc=None
        try:
            objc = Cuentacontable.objects.get(cuenta=str(cuentamadre), idempresa=didempresa)
        except Cuentacontable.DoesNotExist:
            return ""
        cuentam = objc.cuenta

        objc = Cuentacontable.objects.get(cuenta=str(cuentamadre), idempresa=didempresa)
        print(' ctolctamadre 2 -'+ str(cuentam))

    return cuentam

def recuperar_cuenta_madre(cuenta):
    print (' recuperar_cuenta_madre cuenta entra '+ str( cuenta ))
    cant = len(cuenta.split(".")) -1  # Contamos los segmentos de la cuenta
    print (' recuperar_cuenta_madre cant  '+ str( cant ))
    icuenta=cuenta.split(".")
    cuentamadre =''

    #  for (i = 0; i < cant; i++) es:
    for i in range(0, cant):  # Desde 0 hasta cant - 1
        cuentamadre +=icuenta[i]
        if i < cant-1:
            cuentamadre += '.'
        print(' recuperar_cuenta_madre range  ' + str(cuentamadre))

    print( 'recuperar_cuenta_madre  salida ' + str(cuentamadre))
    return cuentamadre


def reconocercuenta(cuenta,nivel):
    print(' reconocercuenta  cuenta   ' + str(cuenta))
    cant = len(cuenta.split("."))  # Contamos los segmentos de la cuenta
    print(' reconocercuenta  cant   ' + str(cant))
    print(' reconocercuenta  nivel   ' + str(nivel))

    #if cant < nivel:   # solo que ya se haya puestp
    #    cuenta=cuenta +'.1'
    #    return cuenta
    if cant == nivel:
        return cuenta
    if cant==1 and nivel==1:
        return cuenta
    else:
        numero_con_puntos = ".".join(cuenta)
        scuenta=numero_con_puntos
        cant = len(numero_con_puntos.split("."))  # Contamos los segmentos de la cuenta

        if cant > nivel:
            cuenta=numero_con_puntos
            icuenta = cuenta.split(".")
            scuenta = ""  # Inicializar la cadena vacía para almacenar el resultado
            current_count = 0  # Contador para el índice
            for numero in icuenta:
                # Convertir el string a entero para eliminar los ceros a la izquierda
                scuenta += str(int(numero))   # Convertimos a int, luego a string
                current_count += 1
                if current_count < nivel:  # Añadir un punto si no es el último número
                    scuenta += '.'
            icuenta = scuenta.split(".")
            scuenta = [int(numero) for numero in icuenta]  # Convierte cada string a entero
            # Convierte cada entero de vuelta a string y los une con puntos, sin espacios
            scuenta_str = '.'.join(str(numero) for numero in scuenta)
            scuenta=scuenta_str.strip()
            print('scuenta: ' + str(scuenta))
    return scuenta


def recorrregistro():
    objetos = Cuentacontable.objects.all().order_by('cuenta')
    #objetos = Cuentacontable.objects.filter(cuenta='1.1.1.1')
    print(' ingresa en Registro recorrido: ')

    for objeto in objetos:
        print('Registro recorrido: ' + str(objeto.cuenta))
        scuenta = objeto.cuenta
        nivel = objeto.nivel
        if scuenta is not None:
            denominacion = objeto.denominacion
            didempresa = objeto.idempresa
            did = objeto.idcuentacontable
            didempresa=1
            print(' denominacion  ' + str(denominacion))
            print(' didempresa  ' + str(didempresa))
            print(' nueva_cuenta  ' + str(scuenta))
            print(' id  ' + str(did))
            cargarcuenta(scuenta, denominacion, didempresa)
            print('  recorrregistro scuenta  ' + str(scuenta) + ' recorrregistro nivel  ' + str(nivel) )
            nueva_cuenta='a'
            # Reconocer y modificar la cuenta según la función
            #nueva_cuenta = reconocercuenta(scuenta, nivel)
            print(' nueva_cuenta  ' + str(nueva_cuenta))

            # Si la cuenta ha cambiado, guardamos el objeto
            if nueva_cuenta != objeto.cuenta:
            #    objeto.cuenta = nueva_cuenta
            #    objeto.save()

                print(f"Cuenta actualizada a: {nueva_cuenta}")
            else:
                print(f"La cuenta {scuenta} no requiere cambios.")

    return ''


# contabilidad/utils.py
import json
import os
from contabilidad.models import Cuentacontable


def cargar_cuentas_desde_json():
    json_file_path = os.path.join(os.path.dirname(__file__), 'cuentas_exportadas.json')

    # Asegúrate de que el archivo JSON existe
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"El archivo {json_file_path} no fue encontrado.")

    # Abre y lee el archivo JSON
    with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)

    # Recorrer cada elemento del archivo JSON y cargarlo en la base de datos
    for item in data:
        Cuentacontable.objects.create(
            idempresa=1,
            idsucursal=1,
            cuenta=item.get('Cuenta'),
            denominacion=item.get('Denominación'),
            nivel=int(item.get('Nivel', 0)),
            naturaleza=item.get('Naturaleza'),
            asentable=item.get('Asentable'),
            centro_costo=item.get('Centro Costo'),
            moneda=item.get('Moneda'),
            tipo_cambio=item.get('Tipo_cambio') if item.get('Tipo_cambio') else None,
        )
    return "Cuentas cargadas correctamente"
