from datetime import timezone

from django.http import JsonResponse, response
from inicio.funcion import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from inicio.models import userempresa, Empresa, Sucursal
from crum import get_current_user
from django.utils import timezone
from django.utils import timezone
from crum import get_current_user

app_name = 'inicio'
con1=1;
# Create your views here.


def current_time(request):
    # Obtener el usuario actual
    user = get_current_user()
    # Obtener la hora actual con la zona horaria configurada
    now = timezone.localtime(timezone.now())
    # Otras operaciones...
    return JsonResponse({'current_time': now.isoformat(), 'user': str(user)})


def loginc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print('usuer '+str(user))
        if user is not None:
            login(request, user)

            #user_permissions = user.user_permissions.all()
            #valor=str(user.last_login)+str(user.username)+str(user.password)

            #print(str(valor))

            # Imprime los permisos
            # for permission in user_permissions:
            #  print(permission)
            #usuario = request.user
            #user = request.user
            now = timezone.now()
            current_user = get_current_user()
            user = get_current_user()
            print(user)
            print(request.user.last_login)
            print(timezone.localtime(timezone.now()))


            # Obtener la hora actual con la zona horaria configurada
            #now = timezone.localtime(timezone.now())
            # Otras operaciones...
            #print(current_user)
            #print(now)

            #return redirect('menu')  # Cambia 'home' por el nombre de tu vista principal
            return redirect('empsucursal')  # Cambia 'home' por el nombre de tu vista principal

        else:
            errors = "Invalid login credentials."
            return render(request, 'base/login.html', {'messages': errors})

    else:
        errors = ""
        if request.user.is_authenticated:
            logout(request)
        request.session['idempresa'] = 0
        request.session['idsucursal'] = 0
        request.session['empresa'] = ""
        request.session['sucursal'] = ""
        titulo= "INICIAR SESION"
    return render(request, 'base/login.html', {'messages': errors, 'title':titulo})


def sisa(request):
 return render (request, "base/sisa.html")

#def login(request):
#    return render(request, "base/login.html")

def menuini(request):
    return render(request, "base/menu-ini.html")
def pagcofirmacion(request):
    return render(request, "base/pagcofirmacion.html")
def logoini(request):
    return render(request, "base/logo-ini.html")

def buscar_usuario(request):
    if request.method == "POST":
        usu = request.POST['user']
        psw = request.POST['psw']
        n="{"+ usu +","+ psw +"}"
        sql = "select controlusuario('" + n + "');"
        valor1 = retorno_valor(con1, sql, usu, psw)
        if valor1 is False:
            valor2= False;
        else:
             valor2 = valor1[0]
        data = {
            'user': valor2,
         }
        Response = JsonResponse({'datos': data})
    return Response

def menu(request):
    if request.user.is_authenticated:
        if request.session['idempresa']== 0:
            return redirect('empsucursal')

        contexto = {
            'habcmp': True,
            'habprov': True
        }


        return render(request, "base/menu.html",contexto)
    else:
        return redirect('login')

def base(request):
    n1 = request.POST['user']
    data = {
        'usuario': n1,
    }
    return render(request, "base/base.html",{'datos': data})
def base2(request):
    n1 = request.POST['user']
    data = {
        'usuario': n1,
    }
    return render(request, "base/base2.html",{'datos': data})

def casap(request):
    return render(request, "base/casap.html")

def login2(request):
    return render(request, "base/login2.html")

def empsucursal(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Accede a los valores del formulario
        empresa = request.POST.get('empresa', '')
        sucursal = request.POST.get('sucursal', '')
        if empresa=="" or sucursal=="":
            return redirect('empsucursal')

        obj = Empresa.objects.filter(empresa=empresa)
        didempresa = ([str(detalle.idempresa) for detalle in obj])[0]

        obj = Sucursal.objects.filter(sucursal=sucursal ,idempresa=didempresa)
        didsucursal = ([str(detalle.idsucursal) for detalle in obj])[0]

        if didempresa==0 or didsucursal==0:
            return redirect('empsucursal')

        didempresa = encriptar_datos2(didempresa,request)
        didsucursal = encriptar_datos2(didsucursal, request)

        request.session['idempresa'] = didempresa
        request.session['empresa'] = empresa
        request.session['idsucursal'] = didsucursal
        request.session['sucursal'] = sucursal
        current_user = get_current_user()

        # Puedes redirigir a otra página después de procesar el formulario
        return redirect('menu')  # Cambia 'home' por el nombre de tu vista principal

    user_id = request.user.id
    empresas = []
    sucursales = []
    title=" EMPRESA / SUCURSAL"
    i=0
    idemp=0
    objetos = userempresa.objects.filter(idusuario=user_id).order_by('idempresa')
    cantr = objetos.count()
    if cantr==0 :
        return redirect('login')

    for objeto in objetos:
        idempresa = int(objeto.idempresa)
        obj = Empresa.objects.filter(idempresa=idempresa)
        nempresa = ([str(detalle.empresa) for detalle in obj])[0]

        if i == 0:
            didempresa=idempresa
            dnempresa=nempresa
            i=1
        if idemp < idempresa:
            empresas.append({
                'idempresa': idempresa,
                'empresa': nempresa,
            })
        idemp=idempresa

    objetos = Sucursal.objects.filter(idempresa=didempresa)
    i = 0
    for objeto in objetos:
        if i == 0:
            didsucursal=objeto.idsucursal
            dnsucursal=objeto.sucursal
            i=1

        sucursales.append({
            'idsucural': objeto.idsucursal,
            'sucursal': objeto.sucursal,
        })

    return render(request, "base/empsucursal.html",{'title': title,'dnempresa': dnempresa, 'dnsucursal': dnsucursal,  'empresas': empresas,'sucursales': sucursales})

def sucursales(request):
    sucursales = []
    empresa = request.POST['idempresa']
    obj = Empresa.objects.filter(empresa=empresa)
    didempresa = ([str(detalle.idempresa) for detalle in obj])[0]
    objetos = Sucursal.objects.filter(idempresa=didempresa)
    i = 0
    for objeto in objetos:
        sucursales.append({
            'idsucural': objeto.idsucursal,
            'sucursal': objeto.sucursal,
        })

    Response = JsonResponse({'datos':sucursales})
    return Response