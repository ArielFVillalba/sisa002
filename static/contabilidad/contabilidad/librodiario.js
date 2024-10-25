
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if (document.querySelector('#columnalst')) {
    $('.columnalst').css({'height':'30px'});
     document.getElementById('labusuario').innerHTML=$(columnalst).width();
     if ($(columna).width()<1001){
        $('.columnalst').css({'height':'70'});

      }
      }
}

function actualizar(){

if (document.querySelector('#id_fechaini')) {
    if  ((document.getElementById('id_fechaini').value).length==0 ){document.getElementById('id_fechaini').valueAsDate = new Date();}
    if  ((document.getElementById('id_fechafin').value).length==0 ){document.getElementById('id_fechafin').valueAsDate = new Date();}
}

}


function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(actcompelem(),1000);
document.getElementById('idbuscar').value="*";
}


function buscarlibrodiario(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;

if ( variable==0 || variable=="*" || variable=="" || variable=='' ) {
variable=0;

var url = "/librodiario/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{

var url = "/librodiario/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}
}

function libro_diario_filtrar_lst(){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,

};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/libro_diario_filtrar_lst/?' + params;

// Open the new page in a new window
//window.open(url);
window.location.href = url;
}
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
