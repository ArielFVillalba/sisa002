
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if(document.getElementById('columnalst') ){
    if (document.querySelector('#columnalst')) {
       $('.columnalst').css({'height':'30px'});
     if ($(columna).width()<1000){
        $('.columnalst').css({'height':'120px'});
        $('.columnalstt').css({'height':'120px'});
      }
    }
    if (document.querySelector('#columna0')) {
       $('.columna0').css({'height':'910px'});
        if ($(columna0).width()<800){
             $('.columna0').css({'height':'600px'});
        }
    }
}
}

function procesarfun(){
setTimeout(actcompelem(),1000);
if (document.querySelector('#familia')) {setTimeout(cargararbol(),1000);}
setTimeout(cargarcombos(),1000);

if (document.querySelector('#id_fecha')) {
if  ((document.getElementById('id_fecha').value).length==0 ){document.getElementById('id_fecha').valueAsDate = new Date();}
}
}

function cargarcombos(){
if (document.querySelector('#id_deposito')) {cargarcombdep();}

}

function nuevo(){
document.getElementById('id_fecha').valueAsDate = new Date();
limpiarlstflia();
}

function generarainv(){
var fecha = document.getElementById('id_fecha').value;
var nrotoma = document.getElementById('id_nrotoma').value;
var deposito = document.getElementById('id_deposito').value;
var obs = document.getElementById('id_obs').value;

//cantph=cantidadflia();
//if (cantph==0){ alert(" seleccionar familia") }
flia=recuperardatosg();
generarbaseinv(fecha,nrotoma,deposito,flia,obs);

}

function cantidadflia(){
cantph=0;
var padre = document.getElementById("listadodetf");
cantph=$(padre).find('li').length;
return cantph
}

function buscarfamilia(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};

if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/familia/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{
variable=0;
var url = "/familia/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function colorlistdo(){
const elementos = document.querySelectorAll('.columnalst');
e=1;  col='#D5F5E3';
elementos.forEach(elemento => {
  elemento.style.backgroundColor = col;
  e=e+1;
  if (e > 1 ){  if (e % 2 === 0) { col='#EAF2F8';   } else {  col='#D5F5E3';   }  }
});
}

function recuperardatosg(){
var padre = document.getElementById("listadodetf");
var contenido="";
cantph=$(padre).find('li').length;
for (var e= 1; e <=cantph; e++) {
    var contenidoConId = document.getElementById('codflia'+e).textContent;
    contenido=contenido+contenidoConId;
    if (e <cantph){  contenido=contenido+ "-";}
}
return contenido;
}
function generarbaseinv(fecha,nrotoma,deposito,flia,obs){
//alert(" fecha "+ fecha + " nrotoma " + nrotoma + " deposito " + deposito+ " flia " + flia );

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/inv_generarbase/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     data: { 'fecha': fecha,'nrotoma': nrotoma,'deposito': deposito,'flia': flia,'obs': obs },
     success: function(data) {
     var list = data.datos;

     if (data.success) {
        Swal.fire({  title: '',  text: 'GENERADO EXITOSO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
        Swal.fire(  '',  'fallo.',  'success'   );

    }

}
});

}

function ingresarinv(){
var nrotoma = document.getElementById('id_nrotoma').value;
var username = document.getElementById('id_username').value;
var password = document.getElementById('id_password').value;
valida=true;
if (valida==true){
var myData = {
nrotoma:nrotoma,
username:username,
password:password
};
// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/inv_toma_ing/?' + params;

// Open the new page in a new window
//window.open(url);
window.location.href = url;
}
}
function recuperarid(einput,list){
var eInput = document.getElementById(einput); // Reemplaza 'tu_input' con el ID de tu elemento <input>
var eList = document.getElementById(list);

did=0
for (var i = 0; i < eList.options.length; i++) {
    if (eList.options[i].value === eInput.value) {
           selectedOption = eList.options[i];
        did = selectedOption.id;
        //break;
    }
}

return did;
}

function ingresarinves(){

var nrotoma = document.getElementById('id_nrotoma').value;
var didempresa= recuperarid('id_empresa','empresa_list');
var didsucursal= recuperarid('id_sucursal','sucursal_list');

valida=true;
if (valida==true){
var myData = {
nrotoma:nrotoma,
didempresa:didempresa,
didsucursal:didsucursal
};

var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');
var url = '/inv_toma_empsuc/?' + params;
window.location.href = url;
}
}


function ingresacargarcod(){
var nrotoma = document.getElementById('id_nrotoma').value;
var didempresa= recuperarid('id_empresa','empresa_list');
var didsucursal= recuperarid('id_sucursal','sucursal_list');

valida=true;
if (valida==true){
var myData = {
nrotoma:nrotoma,
didempresa:didempresa,
didsucursal:didsucursal
};

var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');
var url = '/inv_toma_carga/?' + params;
window.location.href = url;
}
}

function cargarcodigo(){
var nrotoma = document.getElementById('id_nrotoma').value;
var codigo = document.getElementById('id_codigo').value;
var cantidad = document.getElementById('id_cantidad').value;

valida=true;
if (valida==true){
var myData = {
nrotoma:nrotoma,
codigo:codigo,
cantidad:cantidad
};

var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');
var url = '/cargarcodigo/?' + params;
window.location.href = url;
}
}
function pasarcampo(event,id){
    var tecla = event.key;
if (event.key === "Enter" || event.keyCode === 13) {
if (id=="id_codigo"){ document.getElementById("id_cantidad").focus();}
if (id=="id_cantidad"){ cargarcodigo();}
    }
}
function actualizarBarraProgreso() {
    $.ajax({
        url: "{% url 'actualizar_progreso' %}",
        success: function(data) {
            $(".progress-bar").css("width", data.porcentaje + "%").attr("aria-valuenow", data.porcentaje);
            if (data.porcentaje < 100) {
                setTimeout(actualizarBarraProgreso, 1000);  // Actualizar cada segundo
            } else {
                // El proceso ha terminado
                alert("Proceso completado!");
            }
        }
    });
}
function generarajuste(){
var nrotoma = document.getElementById('id_nrotoma').value;
alert(nrotoma);
valida=true;
if (valida==true){
var myData = {
nrotoma:nrotoma
};

var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');
var url = '/inv_ajuste_procesar/?' + params;
window.location.href = url;
}
}
