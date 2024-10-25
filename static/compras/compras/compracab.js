$(window).resize(function(){
actcompelemcomp();

});
function actcompelemcomp(){

if (document.querySelector('#columnalst')) {

     $('.columnalst').css({'height':'35px'});
     if ($(columnalst).width()<1000){
        $('.columnalst').css({'height':'70px'});
     }
}
 if (document.querySelector('#detallelinea0')) {
     $('.detallelinea0').css({'height':'30px'});
     if ($(detallelinea0).width()<960){
        $('.detallelinea0').css({'height':'100px'});
     }
}
   if ($('#columna0').length) { // Verifica si existe el elemento columna0
        var anchoColumna0 = $('#columna0').width(); // Obtiene el ancho de columna0
        // Mostrar el ancho de columna0 en labusuario para verificar
        // $('#labusuario').html(" abm " + anchoColumna0 );

        // Aplica una altura inicial fija de 140px
        $('.columna0').css({'height': '140px'});

        // Verifica si columna2 existe y aplica la suma de altos si ancho de columna0 es < 941
        if ($('#columna2').length && anchoColumna0 < 941) {
            var altoColumna1 = $('.columna1').height()+50; // Obtiene el alto de la columna 1
            var altoColumna2 = $('.columna2').height(); // Obtiene el alto de la columna 2
            var sumaalto2 = altoColumna1 + altoColumna2; // Suma los altos de columna 1 y 2
            $('.columna0').css({'height': sumaalto2 + 'px'});
        }

        // Verifica si columna3 existe y aplica la suma de altos si ancho de columna0 es < 636
        if ($('#columna3').length && anchoColumna0 < 636) {
            var altoColumna1 = $('.columna1').height()+50; // Obtiene el alto de la columna 1
            var altoColumna2 = $('.columna2').height()+50; // Obtiene el alto de la columna 2
            var altoColumna3 = $('.columna3').height(); // Obtiene el alto de la columna 3
            var sumaalto3 = altoColumna1 + altoColumna2 + altoColumna3; // Suma los altos de columna 1, 2 y 3
            $('.columna0').css({'height': sumaalto3 + 'px'});
        }
    }
}


function procesarfun(){
if (!document.querySelector('#columnalst')) {cargarcombos();}
setTimeout(colorlistdo(),10);
setTimeout(actcompelemcomp(),100);
}



function filtrarcompra(){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var idproveedor = document.getElementById('id_idproveedor').value;
var tipodoc = document.getElementById('id_tipodoc').value;
valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,
idproveedor:idproveedor,
tipodoc:tipodoc
};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/compracab_filtro_lst/?' + params;

// Open the new page in a new window
//window.open(url);
window.location.href = url;
}
}


function buscarfactura(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};
if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/compracab/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}else{
variable=0;
var url = "/compracab/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function eliminar_compracab(id_pkf) {
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
                    fetch('/compracab/' + id_pkf + '/eliminar/', { method: 'DELETE', headers: headers  })
                    .then((response) => {
                    if (response.ok) {
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                        Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                         var url = "/compracab/crear";  // Construir la URL de la vista
                            window.location.href = url;

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                        Swal.fire({  title: '',  text: 'ERROR ',
                        icon: 'error',  customClass: {container: 'msnsuccess', }});

                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re
                    buscarfactura();
                    }}  // fin  if (result.isConfirmed) {
                    ) // fin del    .then((result) => {
}; //fin
function cargarcombos(){
setTimeout(cargaricombos,2);
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

if (document.querySelector('#id_fechavto')) {
if  ((document.getElementById('id_fechavto').value).length==0 ){document.getElementById('id_fechavto').valueAsDate = new Date();}
}
crearcmbtipodoc();
busprov();
if (document.querySelector('#listadodet')) {
cargarcombdep();
busdetalle();
cargarcmbart();
}
}



function crearcmbtipodoc(list){
   var values = ["contado","credito"];
     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "tipodoc_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}


function crearcmbdep(list){
   // var values = [];
   var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "deposito_list";
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}
function busdetalle(){
var id_pkf = document.getElementById('id_pkf').value;
if (id_pkf.length>10){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/compradet_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'id_pk': id_pkf,'orden': orden},
     success: function(data) {
    if (data.success) {
     var list = data.datos;
     var html = '';

lin=0;
e=0;

total=0
for (var i = 0; i < list.length; i++) {
      if (i === 0){  html=listadocab();  }
      var compradet = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  > <input   id="orden'+ e +'"  value="'+ compradet.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input id="codigo'+ e +'" value="'+ compradet.codigo + '"</input> </div>';
      html += '<div class ="campdescr" > <input id="descripcion'+ e +'"  list="descrip_list" autocomplete="off"  value=" '+ compradet.descripcion + '"</input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input id="cantidad'+ e +'" value=" '+ number_format(compradet.cantidad,3) + '"</input> </div>';
      html += '<div class ="camplst" > <input id="precio'+ e +'" value=" '+ number_format(compradet.precio,0) + '"</input> </div>';
      html += '<div class ="campcantiva" > <input id="iva'+ e +'" value=" '+ compradet.iva + '"</input> </div>';
      html += '<div class ="camplst" > <input id="subtotal'+ e +'" value=" '+ number_format(compradet.subtotal,0) + '"</input> </div>';
      html += '<div class ="campbtn" > <button  class="btnlstm" onClick="editarcompradet('+ compradet.orden +')" >  EDITAR </button> ';
      html += '<button  class="btnlste" onClick="compradet_eliminar(\''+compradet.pkfd+'\')" >ELIMINAR </button> </div>';
      html += '</div> ';
      html += '</div> ';
      total=total+(compradet.cantidad*compradet.precio);

}

    if (total>0){html +=sumatotal(total);}
    html +=listadoagregardetalle(lin,e);

$('#compras-list').html(html);
    } else { // if succes false
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    } // fin del sccuses true /false
}// succes function

});
setTimeout(bloquearfilas,1000);
setTimeout(actcompelemcomp,1000);
setTimeout(limpiardet,1000);



}else{html=listadocab(); $('#compras-list').html(html);}
}

function listadocab(){
      html ="";
     // html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:#F8E35B;"> ';
      html += '<div id= "detallelinea0" class ="detallelinea0" "> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > ORDEN </div>';
      html += '<div class ="camplst"  style="text-align:center;"> CODIGO </div>';
      html += '<div class ="campdescr"  style="text-align:center;"> DESCRIPCION </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > CANT </div>';
      html += '<div class ="camplst"   style="text-align:center;"> PRECIO </div>';
      html += '<div class ="campcantiva"   style="text-align:center;">  IVA </div>';
      html += '<div class ="camplst"  style="text-align:center;" >  SUB TOT </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}

function sumatotal(total){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:with;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;">  </div>';
      html += '<div class ="campdescr"  style="text-align:center;">  </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"   style="text-align:center;">  </div>';
      html += '<div class ="campcantiva"   style="text-align:center;">TOTAL   </div>';
      html += '<div class ="camplst"  style="text-align:center;" >'+number_format(total, 0)  +' </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}

function listadoagregardetalle(lin,e){
        html ="";

        lin=lin+1;   e=e+1;  col='#D5F5E3';
      if (e > 1 ){ if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"';
      html += 'style="background-color:white;  padding-left: 100px;" > ';
      html += ' <label id="labtitdetmod" ';
      html += ' style= " color: #F8835B;  font-size: 22px;  line-height: 1; font-weight: bold;" ';
      html += ' >INGRESAR-DETALLE</label>  </div> ';
      //html += listadocab();


      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:white;"> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea1"> ';
      html += '<div class ="campcantiva" > <input id="orden"  value=" '+ e + '"</input> </div>';
      html += '<div class ="camplst" ><input class="tamletra" type="text" id="codigo"';
      html += ' onkeyup ="pasarcampo(event,id)"';
      html += ' placeholder ="ingresar codigo" > </input> </div>';
      html += '<div class ="campdescr" > <input class="tamletra" id="descripcion" ';
      html += ' onkeyup ="pasarcampo(event,id)" onfocus="buscdatosartcaja()"';
      html += ' placeholder =" ingresar descripcion"  list="descrip_list" </input> </div>';

      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input   id="cantidad" placeholder ="cantidad" onkeydown="pasarcampo(event,id)"  onkeyup ="calcularst(event)" </input> </div>';
      html += '<div class ="camplst" > <input   id="precio" placeholder ="precio" onkeydown="pasarcampo(event,id)"  onkeyup ="calcularst(event)" </input> </div>';
      html += '<div class ="campcantiva" > <input   id="iva" placeholder ="iva"  </input> </div>';
      html += '<div class ="camplst" > <input id="subtotal" placeholder ="sub total" </input> </div>';
      html += '<div class ="campbtn" > <button  id="btnguardardet" class="btnlstm" onClick="guardardet()" >  GUARDAR </button>  ';
      html += ' <button  class="btnlstm" onClick="limpiardet()" >  NUEVO </button>  ';
      html += '</div> ';
      html += '</div> ';
    return html;
}

function compradet_eliminar(pk){
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
                    fetch('/compradet/' + pk + '/eliminar/',
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
if (document.getElementById('labtitdetmod').textContent==="INGRESAR-DETALLE") {compradet_guardar(); }
if (document.getElementById('labtitdetmod').textContent==="EDITAR-DETALLE") {compradet_editar(); }
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', false);

}


function compradet_editar(){
var orden = document.getElementById('orden').value;
var pkf = document.getElementById('id_pkf').value;
var deposito = document.getElementById('id_deposito').value;
var codigo = document.getElementById('codigo').value;
var cantidad = document.getElementById('cantidad').value;
var precio = document.getElementById('precio').value;

valida=true;
if (valida==true){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/compradetmod/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,  'orden':orden,'codigo':codigo,'cantidad':cantidad,'precio':precio,'deposito':deposito },
    success: function(data) {
    if (data.success) {
        Swal.fire({  title: '',  text: 'ACTUALIZADO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    }
      busdetalle();

  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }

});
}
}

function compradet_guardar(){
var pkf = document.getElementById('id_pkf').value;
var codigo = document.getElementById('codigo').value;
var cantidad = document.getElementById('cantidad').value;
var precio = document.getElementById('precio').value;
var deposito = document.getElementById('id_deposito').value;

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/guardardet/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf, 'codigo':codigo,'cantidad':cantidad,'precio':precio ,'deposito':deposito},
     success: function(data) {
     const obj = data.datos;
    if (data.success) {
            busdetalle();
     } else {
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
     }
     }
});
}
}


function pasarcampo3(event,id){
alert(event.keyCode);
if (event.keyCode === 8 && id==="descripcion" ){
document.getElementById("codigo").value="";
document.getElementById("precio").value="";
}

if (event.keyCode === 13 && id==="codigo"){document.getElementById("descripcion").focus();}
if (event.keyCode === 13 && id==="descripcion" ){controldescripcaja();}
if (event.keyCode === 13 && id==="cantidad"){document.getElementById("codigo").focus();}
if (event.keyCode === 13 && id==="precio"){ document.getElementById("btnguardardet").focus(); }

}

function buscdatosartcod(event){
if (event.keyCode == 13 ||  event.keyCode === 32 ) {  buscdatosart();}
}
function buscdatosartdesc(event){
//if (event.keyCode == 13 ||  event.keyCode === 32 ) { buscdatosartdescri() ;}
}
function pasarcampo(event,id){
if (event.keyCode === 8 && id==="descripcion" ){
document.getElementById("codigo").value="";
document.getElementById("precio").value="";
}
if (event.keyCode === 13 && id==="codigo" ){buscdatosart();  }
if (event.keyCode === 13 && id==="descripcion" ){ controldescrip();}
if (event.keyCode === 13 && id==="cantidad"){ document.getElementById("precio").focus();  }
if (event.keyCode === 13 && id==="precio"){ document.getElementById("btnguardardet").focus();  }
}

function controldescrip(){
cod=document.getElementById("codigo").value;
prec=document.getElementById("precio").value;
    if ( cod.length==0  || prec.length==0 ) {
        buscdatosartdescri();
    }
document.getElementById("cantidad").focus();

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
document.getElementById("precio").value="";
document.getElementById("cantidad").value="";
document.getElementById("iva").value="";
document.getElementById("subtotal").value="";
document.getElementById("codigo").focus();
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
    var ob="#subtotal"+i;  $(''+ ob +'').prop('disabled', true);

    } else {i=200;}
}
setTimeout(document.getElementById("codigo").focus(),500);

}
function editarcompradet(orden){
document.getElementById('labtitdetmod').innerHTML="EDITAR-DETALLE";

var pkf = document.getElementById('id_pkf').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/compradet_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'id_pk': pkf,'orden': orden},
     success: function(data) {
     var list = data.datos;
     var detalle = list[0];

document.getElementById("orden").value=detalle.orden;
document.getElementById("codigo").value=detalle.codigo;
document.getElementById("descripcion").value=detalle.descripcion;
document.getElementById("precio").value=detalle.precio;
document.getElementById("cantidad").value=detalle.cantidad;
document.getElementById("iva").value=detalle.iva;
document.getElementById("subtotal").value=detalle.subtotal;
document.getElementById("codigo").focus();

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

function number_format(amount, decimals) {

    amount += ''; // por si pasan un numero en vez de un string
    amount = parseFloat(amount.replace(/[^0-9\.]/g, '')); // elimino cualquier cosa que no sea numero o punto

    decimals = decimals || 0; // por si la variable no fue fue pasada

    // si no es un numero o es igual a cero retorno el mismo cero
    if (isNaN(amount) || amount === 0)
        return parseFloat(0).toFixed(decimals);

    // si es mayor o menor que cero retorno el valor formateado como numero
    amount = '' + amount.toFixed(decimals);

    var amount_parts = amount.split('.'),
        regexp = /(\d+)(\d{3})/;

    while (regexp.test(amount_parts[0]))
        amount_parts[0] = amount_parts[0].replace(regexp, '$1' + ',' + '$2');

    return amount_parts.join('.');
}
