$(window).resize(function(){
actcompelemcompa();
});

function actcompelemcompa(){

if (document.querySelector('#columnalst')) {
     $('.columnalst').css({'height':'35px'});
    // document.getElementById('labusuario').innerHTML=" list "+ $(columnalst).width();
     if ($(columnalst).width()<1000){
        $('.columnalst').css({'height':'70px'});
     }
}

var elemento = document.getElementById('detallelinea0');
if (elemento !== null) {
        $('.detallelinea0').css({'height':'30px'});
     if ($(columna0).width()<800 ){
         $('.detallelinea0').css({'height':'70px'});
     }
}
}

function funcompcab(){
cargarcombos();
setTimeout(colorlistdo(),10);
}


function cargarcombos(){
setTimeout(cargaricombos,2);
cargarcombtipomov();
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
busdetalleing();
//cargarcmbart();
//cargarcombdep();j
//cargarcombtipomov();
}
}

function busdetalleing(){
var pkf = document.getElementById('id_pkf').value;
if (pkf.length>10){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajaapcierredet_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf},
     success: function(data) {
     if (data.success) {
     var list = data.datos;
     var html = '';

lin=0;
e=0;
total=0;
//html =listadocab();

var tipoegreso=0;
html +=html+fc_ingresosalida('ingreso');

for (var i = 0; i < list.length; i++) {

      var datos = list[i]
      //alert(datos.tipo);
      if (datos.tipo==="egreso"  && tipoegreso ===0){
        tipoegreso =1;
        html += '</div></div></div></div> ';
        html +=fc_ingresosalida('egreso');
      }
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      col='#D5F5E3';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea2"> ';
      html += '<div class ="campo1"  > <input disabled  id="tipomov'+ e +'"  value="'+ datos.tipomov + '"</input> </div>';
      html += '<div class ="campodet2" > <input disabled id="monto'+ e +'" value=" '+ number_format(datos.monto,0) + '"</input> </div>';
      html += '<button  class="btnlstdet" onClick="cajaapcierredet_eliminar(\''+ datos.pkfd +'\')" >x </button>';
      html += ' </div>';
      total=total+(datos.monto);
}
if (tipoegreso===0){
    html += '</div></div></div></div> ';
    html +=fc_ingresosalida('egreso');
    html += '</div></div></div></div> ';
}else{html += '</div></div></div></div> ';}


//if (total>0){html +=sumatotal(total);}

$('#cajacierre-list').html(html);
    } else { // if succes false
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    } // fin del sccuses true /false
}// succes function

});


}else{html=listadocab()+listadoagregardetalle(0,0);  $('#venta-list').html(html);}
}
//function scrollAlFinal() {  contscrt.scrollTop = contscrt.scrollHeight;   }

function fc_ingresosalida(tipo){
    htmlig='';
    htmlig += '<div id= "lin0'+ lin +'" class ="detallelinea0" > ';
    htmlig += '<div id= "lin'+ lin +'"  class ="detallelinea2"> ';
    htmlig += '<div class ="campo1"  >  </div>';
    htmlig += '<div class ="campodet2"  >  '+ tipo.toUpperCase(); +' </div>';
    htmlig += '</div>';
    htmlig += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
    htmlig +=listadoagregardetalle(lin, tipo );
    htmlig += '<div id= "contscrt"  class ="contscr"> ';

      return htmlig;
}
function listadocab(){
      html ="";
      html += '<div id= "detallelinea0" class ="columna0" style="background-color:white;"> ';
      html += '<div class ="columna1"> ';
      html += '<div class ="camplst"  style="text-align:center;" > TIPO MOVIM </div>';
      html += '<div class ="camplst"  style="text-align:center;"> MONTO </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}
function sumatotal(total){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:white;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:right;" >'+number_format(total, 0)  +' </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}

function listadoagregardetalle(lin,tipo){
      html ="";
      html += '<div id= "lin'+ lin +'"  class ="detallelinea2"> ';
      html += '<div  class="campo1" > <input type="text"  id="id_tipomovg'+tipo+'"  list="cajatipomov-list" > </div>';
      html += '<div class ="campodet2" > <input   id="id_montog'+tipo+'"  </input> </div>';
      html += '<button   id="btnguardardetapc" class="btnlstdet" onClick="guardarcajaapcdetdet(\''+ tipo +'\')" > Guardar </button> </div>';
      return html;
}
function listainisalida(){
      html ="";
      html += '<div id= "detallelinea0" class ="columna0" style="background-color:white;"> ';
      html += '<div class ="columna1"> ';
      html += '<div class ="camplst"  style="text-align:center;" > TIPO MOVIM </div>';
      html += '<div class ="camplst"  style="text-align:center;"> MONTO </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}

function guardarcajaapcdetdet(tipo){
var botong = document.getElementById("btnguardardetapc");
botong.disabled = true;
var pkf = document.getElementById('id_pkf').value;
var tipomovg = document.getElementById('id_tipomovg'+tipo).value;
var monto = document.getElementById('id_montog'+tipo).value;
valida=true;

if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajaapcierredet_guardar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf, 'tipomov':tipomovg,  'monto':monto ,'tipo':tipo },
     success: function(data) {
    if (data.success) {
      //  Swal.fire({  title: '',  text: 'ACTUALIZADO',
      // icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
      // if (data.message==""){error="ERROR"}else{ error=data.message};
      // Swal.fire({  title: '',  text: error,
      // icon: 'error',  customClass: {container: 'msnsuccess', }});
    }
      busdetalleing();
  },
    error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }
});
}
botong.disabled = false;
}

function cajaapcierredet_eliminar(pk){
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
                    fetch('/cajaapcierredet/' + pk + '/eliminar/',
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
                        busdetalleing();
                    }else{
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                         Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                         busdetalleing();

                    }


                    // Realizar otras acciones en función del mensaje recibido
                  })
                  .catch((error) => {
                   // console.error('Error:', error);
                  });
                 }}  // fin  if (result.isConfirmed) {
                 ) // fin del    .then((result) => {
  }// fin


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


