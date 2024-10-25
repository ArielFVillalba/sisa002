import psycopg2
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect

from django.utils import timezone
from itsdangerous import URLSafeSerializer, BadSignature

from sisa.views import *

SECRET_KEY = 'Malage'  # Cambia esto por tu propia clave secreta


def conexion(db, usuario, contraseña):
    try:
        if db == 1:
                conn = psycopg2.connect(
                host="localhost",
                database="sisa",
                user=usuario,
                password=contraseña,
                port=5432
                )
                print(conn)
        if db == 2:
                conn = psycopg2.connect(
                host="192.168.2.111",
                database="parana",
                user=usuario,
                password=contraseña,
                port=5432
            )

        if db == "stock":
                conn = psycopg2.connect(
                host="192.168.2.95",
                database="stock",
                user=usuario,
                password=contraseña,
                port=5432
            )
        return conn
    except Exception as error:
        conn = False;
        return conn


def seleccionar_valor(db, fecha_inicio, fecha_fin, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)

    cur = conn.cursor()
    cur.execute("select * FROM prueba('" + fecha_inicio + "', '" + fecha_fin + "');")
    valores = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return valores

def seleccionar_usuario(db, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)
    cur = conn.cursor()
    cur.execute("select * FROM control_usuario('" + usuario + "', '" + contraseña + "');")
    valores = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    print(valores)
    return valores

def retorno_valor(db, sql, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)
    if conn is not False:
        cur = conn.cursor()
        cur.execute(sql)
        valores = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return valores
    else:
        valores = False;
        return valores

def contar_columnas(db, tabla, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = '"+tabla+"'")
    valores = cur.fetchall()
    columnas= []
    for valor in valores:
        columnas.append(valor[0])
    conn.commit()
    cur.close()
    conn.close()
    return columnas

def seleccionar_datos(db, sql, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)
    cur = conn.cursor()
    cur.execute(sql)
    valores = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    # for valor in len(valores):
    # print(valores[fila][columna])
    return valores

def seleccionar_datos2(db, sql, usuario, contraseña):
    conn = conexion(db, usuario, contraseña)
    cur = conn.cursor()
    cur.execute(sql)
    valores = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    # for valor in len(valores):
    # print(valores[fila][columna])
    return valores[0][0]

def seleccionar_datos3( sql):
    usuario="postgres"
    contraseña="sisa"
    db=1
    conn = conexion(db, usuario, contraseña)
    cur = conn.cursor()
    cur.execute(sql)
    valores = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    # for valor in len(valores):
    # print(valores[fila][columna])
    return valores


def formatearcampo(text,cantcaracter,alinear,tipo):
    text=text[0:cantcaracter]

    g=len(text)
    a = 1
    coma=text.count(".")
    if tipo=="n" and  coma==0:
        cantcaracter=cantcaracter-4

    #cantcaracter = cantcaracter - gi

    while g < cantcaracter:
     if alinear=="l": text=text + " "
     if alinear=="r": text =" " + text
     if alinear=="c": text = " " + text + " "
     g = len(text)

    return text

def formatnumver(num,cantdecimal):
    print(str(num))
    if cantdecimal == 0: numero ='{:,.0f}'.format(num)
    if cantdecimal == 1: numero ='{:,.1f}'.format(num)
    if cantdecimal == 2: numero ='{:,.2f}'.format(num)
    if cantdecimal == 3: numero ='{:,.3f}'.format(num)
    return numero

def formatnum(num,cantdecimal):
    x = round(num, cantdecimal)
    return x

def encriptar_datose(token,SECRET_KEY):

    serializer = URLSafeSerializer(SECRET_KEY)
    token = serializer.dumps(token)
    return token

def desencriptar_datose(token,SECRET_KEY):

    serializer = URLSafeSerializer(SECRET_KEY)
    try:
        pk = serializer.loads(token)
        return pk
    except BadSignature:
        raise error_404_view()


def iskey(request):
    skey =  str(request.user.last_login) + str(request.user.username) + str(request.user.password)
    #print(request.user.last_login)
    #print(timezone.localtime(request.user.last_login))
    #print(request.user)
    #print(timezone.localtime(timezone.now()))
    return skey

def desencriptar_datos2(token, request):
    SECRET_KEY=iskey(request)
    serializer = URLSafeSerializer(SECRET_KEY)
    try:
        pk = serializer.loads(token)
        return pk
    except BadSignature:
        return -1

def encriptar_datos2(token,request):
    SECRET_KEY=iskey(request)
    serializer = URLSafeSerializer(SECRET_KEY)
    token = serializer.dumps(token)
    return token
