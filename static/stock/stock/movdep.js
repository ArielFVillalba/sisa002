$(window).resize(function(){
procesorize();
});
function procesorize(){
actcompelem();
}
function actcompelem(){
if (document.querySelector('#columnalst')) {
     $('.columnalst').css({'height':'35px'});
    // document.getElementById('labusuario').innerHTML=" list "+ $(columnalst).width();
     if ($(columnalst).width()<1000){
        $('.columnalst').css({'height':'70px'});
     }
}
 if (document.querySelector('#detallelinea0')) {
     $('.detallelinea0').css({'height':'30px'});
     document.getElementById('labusuario').innerHTML=" abm "+ $(detallelinea0).width();
     if ($(detallelinea0).width()<960){
        $('.detallelinea0').css({'height':'70px'});
     }
}

}
function procesarfun(){
setTimeout(colorlistdo(),10);
setTimeout(actcompelem(),1000);

}


function filtrarmovdep(){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var nromov = document.getElementById('id_nromov').value;

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,
nromov:nromov
};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/movdepcab_filtro_lst/?' + params;

// Open the new page in a new window
//window.open(url);
window.location.href = url;
}
}



function buscarmovdep(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};
if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/movdepcab/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}else{
variable=0;
var url = "/movdepcab/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function eliminar_movdep(pk) {
  // Obtener el token CSRF de la cookie
  const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
  // Configurar el encabezado X-CSRFToken en la solicitud DELETE
  const headers = {'X-CSRFToken': csrftoken};
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, estoy seguro',
                cancelButtonText: 'No, cancelar'
            })
            .then((result) => {
                if (result.isConfirmed) {
                    fetch('/movdepcab/' + pk + '/eliminar/', { method: 'DELETE', headers: headers  })
                    .then((response) => {
                    if (response.ok) {
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                        Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                         document.location.href= "/movdepcab/crear/";

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                        Swal.fire({  title: '',  text: 'ERROR ',
                        icon: 'error',  customClass: {container: 'msnsuccess', }});

                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re
                    }}  // fin  if (result.isConfirmed) {
                    ) // fin del    .then((result) => {
}; //fin
function cargarcombos(){
setTimeout(cargaricombos,2);
}
function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(actcompelem,500);
}

function cargaricombos(){
if (document.querySelector('#id_fecha')) {
if  ((document.getElementById('id_fecha').value).length==0 ){document.getElementById('id_fecha').valueAsDate = new Date();}
}
if (document.querySelector('#id_fechaini')) {
if  ((document.getElementById('id_fechaini').value).length==0 ){document.getElementById('id_fechaini').valueAsDate = new Date();}
}
if (document.querySelector('#id_fechafin')) {
if  ((document.getElementById('id_fechafin').value).length==0 ){document.getElementById('id_fechafin').valueAsDate = new Date();}
}

if (document.querySelector('#listadodet')) {
busdetalle();
cargarcmbart();
cargarcdep()
}
}

function busdetalle(){
var pkmd = document.getElementById('id_pkmd').value;
if (pkmd.length>10){
    orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/movdepdet_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkmd': pkmd,'orden': orden},
     success: function(data) {
    if (data.success) {
var list = data.datos;
var html = '';
lin=0;
e=0;
total=0
 html=listadocab();
for (var i = 0; i < list.length; i++) {
     // if (i === 0){  html=listadocab();  }
      var movdepdet = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  > <input   id="orden'+ e +'"  value="'+ movdepdet.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input id="codigo'+ e +'" value="'+ movdepdet.codigo + '"</input> </div>';
      html += '<div class ="campdescr" > <input id="descripcion'+ e +'"  list="descrip_list"  value=" '+ movdepdet.descripcion + '"</input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input id="cantidad'+ e +'" value=" '+ movdepdet.cantidad + '"</input> </div>';
      html += '<div class ="camplst" > <input id="depsalida'+ e +'" value=" '+ movdepdet.depsalida + '"</input> </div>';
      html += '<div class ="camplst" > <input id="depentrada'+ e +'" value=" '+ movdepdet.depentrada + '"</input> </div>';
      html += '<div class ="campbtn" > <button  class="btnlstm" onClick="editarordenmovdepdet('+ movdepdet.orden +')" >  EDITAR </button> ';
      html += '<button  class="btnlste" onClick="movdepdet_eliminar(\''+movdepdet.pkmdd+'\' )" >ELIMINAR </button> </div>';
      html += '</div> ';
      html += '</div> ';
}
 html +=listadoagregardetalle(lin,e);
$('#movdep-list').html(html);
    } else { // if succes false
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    } // fin del sccuses true /false
}// succes function

});
setTimeout(bloquearfilas,500);
setTimeout(actcompelem,500);
}else{html=listadocab(); $('#movdep-list').html(html);}

}

function listadocab(){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:white;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > ORDEN </div>';
      html += '<div class ="camplst"  style="text-align:center;"> CODIGO </div>';
      html += '<div class ="campdescr"  style="text-align:center;"> DESCRIPCION </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > CANT </div>';
      html += '<div class ="camplst"   style="text-align:center;"> SALIDA </div>';
      html += '<div class ="camplst"   style="text-align:center;">  ENTRADA </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}


function listadoagregardetalle(lin,e){
        html ="";

      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"';
      html += 'style="background-color:white;  padding-left: 100px;" > ';
      html += ' <label id="labtitdetmod" ';
      html += ' style= " color: #F8835B;  font-size: 22px;  line-height: 1; font-weight: bold;" ';
      html += ' >INGRESAR-DETALLE</label>  </div> ';

      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:white;"> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea1"> ';
      html += '<div class ="campcantiva" > <input id="orden"  value=" '+ e + '"</input> </div>';
      html += '<div class ="camplst" >   <input type="text"   id="codigo" placeholder ="ingresar codigo" onkeydown="buscdatosartcod(event)"> </input> </div>';
      html += '<div class ="campdescr" > <input id="descripcion" ';
      html += ' onkeyup ="pasarcampo(event,id)" onfocus="buscdatosart()" onchange="buscdatosartdescri()"';
      html += ' placeholder =" ingresar descripcion"   list="descrip_list" </input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input   id="cantidad" placeholder ="cantidad" onkeydown="pasarcampo(event,id)"  onkeyup ="calcularst(event)" </input> </div>';
      html += '<div class ="camplst" > <input   list="deposito_list"  id="depsalida" placeholder ="dep. salida"  </input> </div>';
      html += '<div class ="camplst" > <input   list="deposito_list"  id="depentrada" placeholder ="dep. entrada"  </input> </div>';

      html += '<div class ="campbtn" > <button  id="btnguardardet" class="btnlstm" onClick="guardardet()" >  GUARDAR </button>  ';
      html += ' <button  class="btnlstm" onClick="limpiardet()" >  NUEVO </button>  ';
      html += '</div> ';
      html += '</div> ';
    return html;
}

function movdepdet_eliminar(pk){

 // Obtener el token CSRF de la cookie

  const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
  // Configurar el encabezado X-CSRFToken en la solicitud DELETE
  const headers = {'X-CSRFToken': csrftoken};

            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, estoy seguro',
                cancelButtonText: 'No, cancelar',
                customClass: {container: 'msnsuccess', }
            })
            .then((result) => {
                if (result.isConfirmed) {
                    fetch('/movdepdet/' + pk + '/eliminar/',
                    {
                        method: 'DELETE',
                        headers: headers // Agregar el encabezado X-CSRFToken a la solicitud DELETE
                    })

                 .then((response) => {
                    if (response.ok) {
                      return response.json(); // Leer el contenido JSON de la respuesta

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                         Swal.fire({  title: '',  text:'error',
                         icon: 'error',  customClass: {container: 'msnsuccess', }});
                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re

                  .then((data) => {
                    // Aquí puedes trabajar con los mensajes recibidos desde el servidor

                    if (!data.success) {
                         Swal.fire({  title: '',  text: data.message,
                         icon: 'error',  customClass: {container: 'msnsuccess', }});
                      busdetalle();
                    }else{
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                         Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                         busdetalle();

                    }


                    // Realizar otras acciones en función del mensaje recibido
                  })
                  .catch((error) => {
                   // console.error('Error:', error);
                  });
                 }}  // fin  if (result.isConfirmed) {
                 ) // fin del    .then((result) => {
}// fin

function guardardet(){
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', true);
setTimeout(document.getElementById("codigo").focus());
if (document.getElementById('labtitdetmod').textContent==="INGRESAR-DETALLE") {movdepdet_guardar(); }
if (document.getElementById('labtitdetmod').textContent==="EDITAR-DETALLE") {movdepdet_editar(); }
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', false);
}


function movdepdet_editar(){
var orden = document.getElementById('orden').value;
var pkmd = document.getElementById('id_pkmd').value;
var codigo = document.getElementById('codigo').value;
var cantidad = document.getElementById('cantidad').value;
var depentrada = document.getElementById('depentrada').value;
var depsalida = document.getElementById('depsalida').value;
valida=true;
if (valida==true){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/movdepdet_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkmd': pkmd,  'orden':orden,'codigo':codigo,'cantidad':cantidad,'depentrada':depentrada,'depsalida':depsalida },
    success: function(data) {
    if (data.success) {
        //Swal.fire(  '',  'El detalle ha sido actualizado.',  'success'  );
        Swal.fire({  title: '',  text: 'ACTUALIZADO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
        Swal.fire(  '',  'fallo.',  'success'   );

    }
      busdetalle();

  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }

});
}

}
function movdepdet_guardar(){
var pkmd = document.getElementById('id_pkmd').value;
var codigo = document.getElementById('codigo').value;
var cantidad = document.getElementById('cantidad').value;
var depentrada = document.getElementById('depentrada').value;
var depsalida = document.getElementById('depsalida').value;
//alert("  pkmd " + pkmd +"   codigo " + codigo + "  cantidad " + cantidad + "  depentrada " + depentrada +"  depsalida " + depsalida )
valida=true;

if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/movdepdet_guardar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkmd': pkmd, 'codigo':codigo,'cantidad':cantidad,'depentrada':depentrada,'depsalida':depsalida },
     success: function(data) {
     const obj = data.datos;
     busdetalle();
     }
});
}
}



function buscdatosartcod(event){
if (event.keyCode == 13 ||  event.keyCode === 32 ) { buscdatosart() ;}
}

function pasarcampo(event,id){
if (event.keyCode == 13 && id==="descripcion"){ document.getElementById("cantidad").focus();  }
if (event.keyCode == 13 && id==="cantidad"){ document.getElementById("precio").focus();  }
}
function cargarcmbart(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbarticulo/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbart(obj);
    }
});
}
function crearcmbart(list){
    var dataList = document.createElement('datalist');
    dataList.id = "descrip_list";

for (var i = 0; i < list.length; i++) {
  var artículo = list[i];

     var option = document.createElement('option');
        option.setAttribute('id', artículo.codigo);
        option.value = artículo.descripcion;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList);
}

function calcularst(event){
var precio=  document.getElementById("precio").value
var cantidad=  document.getElementById("cantidad").value
var valor = event.key
var subtotal=parseFloat(precio) * parseFloat(cantidad);
document.getElementById("subtotal").value =parseFloat(subtotal);
}
function limpiardet(){
document.getElementById('labtitdetmod').innerHTML="INGRESAR-DETALLE";
document.getElementById("orden").value=contar_linea();
document.getElementById("codigo").value="";
document.getElementById("descripcion").value="";
document.getElementById("cantidad").value="";
document.getElementById("depsalida").value="";
document.getElementById("depentrada").value="";

}

function contar_linea(){
var valor=0
for (let i = 1; i < 200; i++) {
const elemento = document.getElementById("orden"+i);
if (elemento) {  valor=i+1 } else {  i=200;}
}

return valor;
}
function bloquearfilas(){

var valor=0
for (let i = 1; i < 200; i++) {
    const elemento = document.getElementById("orden"+i);
    if (elemento) {
    valor=i+1;
    var ob="#orden";  $(''+ ob +'').prop('disabled', true);
    var ob="#iva";  $(''+ ob +'').prop('disabled', true);
    var ob="#subtotal";  $(''+ ob +'').prop('disabled', true);

    var ob="#orden"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#codigo"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#descripcion"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#cantidad"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#precio"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#iva"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#depentrada"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#depsalida"+i;  $(''+ ob +'').prop('disabled', true);
    } else {i=200;}
}



if (document.getElementById("codigo")){
setTimeout(document.getElementById("codigo").focus(),500);
setTimeout(document.getElementById("depentrada").value=document.getElementById("id_depentrada").value,500);
setTimeout(document.getElementById("depsalida").value=document.getElementById("id_depsalida").value,500);

}

}
function editarordenmovdepdet(orden){
document.getElementById('labtitdetmod').innerHTML="EDITAR-DETALLE";

var pkmd = document.getElementById('id_pkmd').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/movdepdet_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkmd': pkmd,'orden': orden},
     success: function(data) {
     var list = data.datos;
     var detalle = list[0];

document.getElementById("orden").value=detalle.orden;
document.getElementById("codigo").value=detalle.codigo;
document.getElementById("descripcion").value=detalle.descripcion;
document.getElementById("cantidad").value=detalle.cantidad;
document.getElementById("depentrada").value=detalle.depentrada;
document.getElementById("depsalida").value=detalle.depsalida;
document.getElementById("codigo").focus();

}
});
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