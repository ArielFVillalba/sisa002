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
      $('.columna0').css({'height':'200px'});
     $('.detallelinea0').css({'height':'30px'});
     if ($(detallelinea0).width()<960){
     }
}

}

function cargarcombos(){
setTimeout(cargaricombos,100);
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
if (document.querySelector('#id_fechavt')) {
if  ((document.getElementById('id_fechavt').value).length==0 ){document.getElementById('id_fechavt').valueAsDate = new Date();}
}

busdetalle();

}



function busdetalle(){
var id_pkf = document.getElementById('id_pkf').value;
orden=0;
if (document.getElementById('id_orden')){ orden = document.getElementById('id_orden').value;}
if (id_pkf.length>10){
orden=-1;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventascuotas_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
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
      var ventascuotas = list[i];

      col='white';
      //col='#dcdcdc';
      lin=lin+1;
      //='#D5F5E3';
    //  if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div class ="campcantiva"  > <input class ="campcantiva"   id="orden'+ e +'"  value="'+ ventascuotas.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input class ="camplst"    id="fechavto'+ e +'" value="'+ ventascuotas.fechavto + '"</input> </div>';
      html += '<div class ="campdescr" > <input class ="campdescr"    id="monto'+ e +'"  value=" '+ ventascuotas.monto + '"</input> </div>';
      html += '<div class ="campbtn" > <button  class="btnlstm" onClick="editarventascuotas('+ ventascuotas.orden +')" >  EDITAR </button> ';
      html += '<button  class="btnlste" onClick="ventascuotas_eliminar(\''+ventascuotas.pkfd+'\')" >ELIMINAR </button> </div>';
      html += '</div> ';
      total=total+parseFloat(ventascuotas.monto2);
      e=parseFloat(ventascuotas.orden)
      e=i+1;

}
    if (total>0){html +=sumatotal(total);}
    html +=listadoagregardetalle(lin,e);

$('#ventascuotas-list').html(html);
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

}
}

function listadocab(){
      html ="";
      html += '<div class ="detallelinea0"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > CUOTA </div>';
      html += '<div class ="camplst"  style="text-align:center;"> FECHA </div>';
      html += '<div class ="campdescr"  style="text-align:center;">  MONTO</div>';
      html += '</div> ';
      return html;
}

function sumatotal(total){
      html ="";
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"></div>  ';
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:with;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;"> TOTAL </div>';
      html += '<div class ="campdescr"  style="text-align:center;">  '+number_format(total, 0)  +' </div>';
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
      html += '<div class ="campcantiva" > <input  class="campimp2" class ="campcantiva" id="orden"  value="'+ e + '"</input> </div>';
      html += '<div class ="camplst" >   <input class="campimp2" class ="camplst"  type="date"   id="fechavto" > </input> </div>';
      html += '<div class ="campdescr" > <input class="campimp2" class ="campdescr" id="monto" ';
      html += ' placeholder =" ingresar monto"   class="campimp2" list="descrip_list" </input> </div>';
      html += '</div> ';

      html += '<div class ="campbtng" > <button  id="btnguardardet" class="btnlstm" onClick="guardardet()" >  GUARDAR </button>  ';
      html += ' <button  class="btnlstm" onClick="limpiardet()" >  NUEVO </button>  ';
      html += '</div> ';
      html += '</div> ';
      return html;
}


function guardardet(){
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', true);
    setTimeout(document.getElementById("fechavto").focus());
if (document.getElementById('labtitdetmod').textContent==="INGRESAR-DETALLE") {ventascuotas_guardar(); }
if (document.getElementById('labtitdetmod').textContent==="EDITAR-DETALLE") {ventascuotas_editar(); }
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', false);

}

function ventascuotas_generar(){
var pkf = document.getElementById('id_pkf').value;
var entrega = document.getElementById('id_entrega').value;
var fechavto = document.getElementById('id_fechavt').value;
var cuota = document.getElementById('id_cantcuota').value;
var monto = document.getElementById('id_monto').value;

valida=true;
if (valida==true){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/ventascuotas_generar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,  'entrega':entrega,'fechavto':fechavto,'cuota':cuota,'monto':monto },
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

function editarventascuotas(orden){
document.getElementById('labtitdetmod').innerHTML="EDITAR-DETALLE";

var pkf = document.getElementById('id_pkf').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventascuotas_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'id_pk': pkf,'orden': orden},
     success: function(data) {
     var list = data.datos;
     var detalle = list[0];
document.getElementById("orden").value=detalle.orden;
document.getElementById("fechavto").value="20"+detalle.fechavto;
document.getElementById("monto").value=detalle.monto.replace(",", "");
}
});
}


function ventascuotas_editar(){
var orden = document.getElementById('orden').value;
var pkf = document.getElementById('id_pkf').value;
var fechavto = document.getElementById('fechavto').value;
var monto = document.getElementById('monto').value;

valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventascuotas_mod/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,  'orden':orden ,'fechavto':fechavto,'monto':monto },
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

function ventascuotas_guardar(){
var orden = document.getElementById('orden').value;
var pkf = document.getElementById('id_pkf').value;
var fechavto = document.getElementById('fechavto').value;
var monto = document.getElementById('monto').value;
valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventascuotas_guardar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'fechavto':fechavto,'monto':monto },
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



function ventascuotas_eliminar(pk){
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
                    fetch('/ventascuotas/' + pk + '/eliminar/',
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


function limpiardet(){
document.getElementById('labtitdetmod').innerHTML="INGRESAR-DETALLE";
document.getElementById("orden").value=contar_linea();
if (document.querySelector('#fechavto')) {
document.getElementById('fechavto').valueAsDate = new Date();
}
document.getElementById('monto').value=0;

}

function contar_linea(){
var valor=0
for (let i = 0; i < 200; i++) {
const elemento = document.getElementById("orden"+i);
if (elemento) {
valor=i+1
  } else {  i=200;}
}

return valor;
}
function bloquearfilas(){
var valor=0
for (let i = 0; i < 200; i++) {
    const elemento = document.getElementById("orden"+i);
    if (elemento) {
    valor=i+1;
    var ob="#orden"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#fechavto"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#monto"+i;  $(''+ ob +'').prop('disabled', true);
    } else {i=200;}
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
