
$(window).resize(function(){
actcompelemcomp();
});

function actcompelemcomp(){
if (document.querySelector('#grpcabecera')) {
    $('.grpdetfil0').css({'height':'30px'});
    $('.grpcabecera').css({'height':'150px'});


    //$('.grpdetalle').css({'height':'200px'});
     if (document.querySelector('#grpcabecera')) {

     if ($(columna0).width()<670){
        $('.grpcabecera').css({'height':'250px'});
        $('.grpdetfil0').css({'height':'80px'});
       // $('.grpdetalle').css({'height':'400px'});
     }
     }
}

if (document.querySelector('#columnalst')) {
    $('.columnalst').css({'height':'30px'});
   // $('.celdalistb').css({'padding-left':'20px'});

    // document.getElementById('labusuario').innerHTML=$(columnalst).width();
     if ($(columna).width()<850){
        //$('.celdalistb').css({'padding-left':'100px'});
        $('.columnalst').css({'height':'70px'});

      }
}

}
function scrollAlFinal() {
    var grpdetalle = document.getElementById('grpdetalle');
    grpdetalle.scrollTop = grpdetalle.scrollHeight;
}


function actualizar(){
if (document.querySelector('#grpdetalle')) {
setTimeout(scrollAlFinal, 100); // Retraso de 1 segundos
}

if (document.querySelector('#id_fecha')) {
if  ((document.getElementById('id_fecha').value).length==0 ){document.getElementById('id_fecha').valueAsDate = new Date();}
}
if (document.querySelector('#id_fechaini')) {
if  ((document.getElementById('id_fechaini').value).length==0 ){document.getElementById('id_fechaini').valueAsDate = new Date();}
if  ((document.getElementById('id_fechafin').value).length==0 ){document.getElementById('id_fechafin').valueAsDate = new Date();}

}
ocultarbotones('block','none');
//ocultarbotones('none','block');
setTimeout(colorlistdo,2);
setTimeout(actcompelemcomp(),100);

}
function ocultarbotones(var1,var2){
//var1='block';
//var2='none';
if (document.querySelector('#btnagregar')) {
 document.getElementById('btnagregar').style.display = var1;}
if (document.querySelector('#btnmodificar')) {
 document.getElementById('btnmodificar').style.display = var2;}
}


function buscarasiento(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;

if ( variable==0 || variable=="*" || variable=="" || variable=='' ) {
variable=0;

var url = "/asiento/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{

var url = "/asiento/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}
}


function cargarasientodet(pk_token) {
var orden = document.getElementById('id_orden').value;
var cuenta = document.getElementById('id_cuenta').value;
var denominacion = document.getElementById('id_denominacion').value;
var debe = document.getElementById('id_cdebe').value;
var haber = document.getElementById('id_chaber').value;

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/asiento_det_crear/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pk_token': pk_token, 'orden':orden,'cuenta':cuenta,'denominacion':denominacion ,'debe':debe,'haber':haber},
     success: function(data) {
     const obj = data.datos;
     var url = "/asiento/" + pk_token + "/cargar/";  // Construir la URL de la vista
     window.location.href = url;


     }
});
}

}

function actcambiar(valor) {
let pk_token_det = document.getElementById('btnmodificar').getAttribute('data-pk');
alert(pk_token_det);
 document.getElementById('btnmodificar').setAttribute('data-pk', valor);
}
function actastdet(col,varlor) {
let texto = varlor + "";
ocultarbotones('none','block');
document.getElementById('btnmodificar').setAttribute('data-pk-det',texto);
let pk_token_det = document.getElementById('btnmodificar').getAttribute('data-pk-det');

document.getElementById('id_orden').value=document.getElementById("id_orden"+col).innerText;
document.getElementById('id_cuenta').value=document.getElementById('id_cuenta'+col).innerText;
document.getElementById('id_denominacion').value=document.getElementById('id_denominacion'+col).innerText;
document.getElementById('id_cdebe').value=document.getElementById('id_debe'+col).innerText.replace(/,/g, '');
document.getElementById('id_chaber').value=document.getElementById('id_haber'+col).innerText.replace(/,/g, '');

}

function actasientodet() {
var orden = document.getElementById('id_orden').value;
var cuenta = document.getElementById('id_cuenta').value;
var denominacion = document.getElementById('id_denominacion').value;
var debe = document.getElementById('id_cdebe').value;
var haber = document.getElementById('id_chaber').value;

// Obtener el botón por su ID
var btn = document.getElementById("btnmodificar");

// Obtener los valores de los atributos data-pk y data-pk-det
var pk_token = btn.getAttribute("data-pk");
var pk_token_det = btn.getAttribute("data-pk-det");

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/asiento_det_actualizar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pk_token': pk_token,'pk_token_det': pk_token_det, 'orden':orden,'cuenta':cuenta,'denominacion':denominacion ,'debe':debe,'haber':haber},
     success: function(data) {

     const obj = data.datos;

    //if (data.success) {

     //} else {
     //if (data.message==""){error="ERROR"}else{ error=data.message};
     //  Swal.fire({  title: '',  text: error,
     //  icon: 'error',  customClass: {container: 'msnsuccess', }});
     //}
     }
});
}

     var url = "/asiento/" + pk_token + "/cargar/";  // Construir la URL de la vista
     window.location.href = url;
      cancelar_det();
}
function cancelar_det(){
document.getElementById('id_orden').value="";
document.getElementById('id_cuenta').value="";
document.getElementById('id_denominacion').value="";
debe = document.getElementById('id_cdebe').value="";
haber = document.getElementById('id_chaber').value="";
document.getElementById('btnmodificar').setAttribute('data-pk','');
ocultarbotones('block','none');

}

function optecla(event, id) {
    // 8: retroceso, 13: enter

    if (event.keyCode === 13 && id === "id_cuenta") {
        document.getElementById('id_cdebe').focus();

    }

    if (event.keyCode === 13 && id === "id_denominacion") {
        document.getElementById('id_cdebe').focus();
    }


    if (event.keyCode === 13 && id === "id_cdebe") {
         document.getElementById('id_chaber').focus();
    }

    if (event.keyCode === 13 && id === "id_chaber") {
     var elemento = document.getElementById('btnagregar');
     if (elemento && elemento.offsetParent !== null) {
         document.getElementById('btnagregar').focus();
        } else {
        document.getElementById('btnmodificar').focus();
        }
    }
}

function ofcuenta(){
 var cuenta = document.getElementById('id_cuenta').value;
  buscardenominacion(cuenta);
}

function ofdenominacion(){
var denominacion = document.getElementById('id_denominacion').value;
var valor = obteneriddenominacion();
buscarcuenta(valor);
}


function obteneriddenominacion() {
    var denominacion = document.getElementById('id_denominacion').value;
    var options = document.getElementById('cuenta_cont_list').options;

    for (var i = 0; i < options.length; i++) {
        if (options[i].value === denominacion) {
            return options[i].id;  // Retorna el id de la opción seleccionada
        }
    }
    return null;  // Retorna null si no encuentra coincidencias
}

function buscdatosdenomi(){

//alert("oon focus buscdatosdenomi");
}

function buscardenominacion(cuenta){
var denominacion=""
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/bucardenominacion/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
     data: {'cuenta':cuenta},
     success: function(data) {
            denominacion = data.denominacion;
            var denominacion = data.denominacion;
            document.getElementById('id_denominacion').value = denominacion;
            document.getElementById('id_cdebe').focus();
     }
});

}
function buscarcuenta(id){
var denominacion=""
var cuenta=""
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/buscarcuentalist/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
     data: {'id':id},
     success: function(data) {
         if (data.success) {
         var list = data.datos;
         var cuentacont = list[0];
            cuenta=cuentacont.cuenta ;
            denominacion= cuentacont.denominacion ;
            document.getElementById('id_cuenta').value = cuenta;
            document.getElementById('id_cdebe').focus();
         }
     }
});
}
function colorlistdo(){
if (document.querySelector('#columnalst')) {
const elementos = document.querySelectorAll('.columnalst');
e=1;  col='#D5F5E3';
elementos.forEach(elemento => {
  elemento.style.backgroundColor = col;
  e=e+1;
  if (e > 1 ){  if (e % 2 === 0) { col='#EAF2F8';   } else {  col='#D5F5E3';   }  }
});
}
}
