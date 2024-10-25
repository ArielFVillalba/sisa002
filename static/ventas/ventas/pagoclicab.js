$(window).resize(function(){
actcompelemcomp();

});
function actcompelemcomp(){

if (document.querySelector('#columnalst')) {

    // $('.columnalst').css({'height':'35px'});
    // if ($(columnalst).width()<1000){
    //    $('.columnalst').css({'height':'70px'});
    // }
}

 if (document.querySelector('#detallelinea0')) {
     $('.detallelinea0').css({'height':'30px'});
     if ($(detallelinea0).width()<960){
        $('.detallelinea0').css({'height':'70px'});
     }
}else{ }
bloquearfilas();

}


function procesarfun(){
if (!document.querySelector('#columnalst')) {cargarcombos();}
setTimeout(colorlistdo(),10);
setTimeout(actcompelemcomp(),1000);

}

function filtrarpagocli(){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var idcliente = document.getElementById('id_idcliente').value;
valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,
idcliente:idcliente,
};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/pagoclicab_filtro_lst/?' + params;

// Open the new page in a new window
//window.open(url);

window.location.href = url;
}
}


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
if (document.querySelector('#listpagofact')) {

buscli();
crearcmbtipopago();
pagoclifact();
pagoclipago();

}
}

function crearcmbtipopago(list){
   var values = ["efectivo","cheque","tarjeta"];
   var val = ["1","2","3"];

     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "tipofpago_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.setAttribute('id', val);
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function pagoclifact(){
var id_pkf = document.getElementById('id_pkf').value;
if (id_pkf.length>10){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/pagoclifact_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'id_pk': id_pkf,'orden': orden},
     success: function(data) {
    if (data.success) {
     var list = data.datos;
     var html = '';

lin=0;
e=0;
total=0
for (var i = 0; i < list.length; i++) {
      //if (i === 0){  html=listadocab();  }
      var pagofact = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  > <input   id="orden'+ e +'"  value="'+ pagofact.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input id="fecha'+ e +'" value="'+ pagofact.fecha + '"</input> </div>';
      html += '<div class ="camplst" > <input id="factura'+ e +'"value=" '+ pagofact.factura + '"</input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input id="cuota'+ e +'" value=" '+ pagofact.nrocuota + '"</input> </div>';
      html += '<div class ="camplst" > <input id="saldo'+ e +'" value=" '+ number_format(pagofact.saldo,0) + '"</input> </div>';
      html += '<div class ="camplst" > <input id="monto'+ e +'" value=" '+ number_format(pagofact.monto,0) + '"</input> </div>';

      html += '<div class ="campbtn" > <button  class="btnlstdet" onClick="editarfactclidet('+ pagofact.orden +')" >  EDITAR </button> ';
      html += '	<a class="btn" href="/pagoclifact/'+pagofact.pkfd+'/eliminar/" >ELIMINAR</a>';

      html += '</div> ';
      html += '</div> ';
      html += '</div> ';
      total=total+parseFloat(pagofact.monto);


}
    if (total>0){html +=sumatotalf(total);}
    html2=""
    html2=html;
    html=""
    html+=listadocab()+html2+listadoagregardetalle(lin,e);

$('#pagoclifact-list').html(html);

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

}else{html=listadocab(); $('#pagoclifact-list').html(html);  }
}

function listadocab(){
      html ="";
     // html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:#F8E35B;"> ';
      html += '<div id= "detallelinea0" class ="detallelinea0" "> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > ORDEN </div>';
      html += '<div class ="camplst"  style="text-align:center;"> FECHA </div>';
      html += '<div class ="camplst"  style="text-align:center;"> FACTURA </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >CUOTA </div>';
      html += '<div class ="camplst"   style="text-align:center;"> ANT-SALDO </div>';
      html += '<div class ="camplst"   style="text-align:center;">  PAGO </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}

function sumatotalf(total){
      html ="";
     // html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:#F8E35B;"> ';
      html += '<div id= "detallelinea0" class ="detallelinea0" "> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;">  </div>';
      html += '<div class ="camplst"  style="text-align:center;">  </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > </div>';
      html += '<div class ="camplst"   style="text-align:center;"> TOTAL </div>';
      html += '<div class ="camplst"   style="text-align:center;"> '+ number_format(total, 0)  +' </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}

function listadoagregardetalle(lin,e){
        html ="";
       lin=lin+1;   e=e+1;  col='#D5F5E3';
      if (e > 1 ){ if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "pagofactmod"; style= "display: none;" > ';
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"';
      html += 'style="background-color:white;  padding-left: 100px;" > ';
      html += ' <label id="labtitdetmod" ';
      html += ' style= " color: #F8835B;  font-size: 22px;  line-height: 1; font-weight: bold;" ';
      html += ' >INGRESAR-DETALLE</label>  </div> ';
      //html += listadocab();


      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:white;"> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea1"> ';
      html += '<div class ="campcantiva" > <input id="orden"  value=" '+ e + '"</input> </div>';
      html += '<div class ="camplst" > <input id="fecha"  </input> </div>';
      html += '<div class ="camplst" > <input id="factura"  </input> </div>';

      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcantiva" > <input   id="nrocuota"  </input> </div>';
      html += '<div class ="camplst" > <input   id="saldo" </input> </div>';
      html += '<div class ="camplst" > <input   id="monto" placeholder ="monto"  </input> </div>';
      html += '<div class ="campbtn" > <button  id="btnguardardet" class="btnlstdet" onClick="guardardet()" >  GUARDAR </button>  ';
      html += '<button  id="btncancelardetfact" class="btnlstdet" onClick="cancdetfact()">CANCELAR </button>  ';
      html += '</div> ';
      html += '</div> ';
      html += '</div> ';// id= "pagofactmod"';

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
setTimeout(document.getElementById("orden").focus());
pagoprovfact_editar();
var ob="#btnguardardet";  $(''+ ob +'').prop('disabled', false);

}

function cancdetfact(){
document.getElementById("pagofactmod").style.display = "none";

}
function pagoprovfact_editar(){
var pkf = document.getElementById('id_pkf').value;
var orden = document.getElementById("orden").value;
var monto = document.getElementById("monto").value;

valida=true;
if (valida==true){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/pagoclifact_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'orden':orden,'monto':monto },
    success: function(data) {
    if (data.success) {
        Swal.fire({  title: '',  text: 'ACTUALIZADO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    }
      pagoclifact();

  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }

});
}
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
document.getElementById("orden").value="";
document.getElementById("fecha").value="";
document.getElementById("factura").value="";
document.getElementById("nrocuota").value="";
document.getElementById("saldo").value="";
document.getElementById("monto").value="";
document.getElementById("pagofactmod").style.display = "none";

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
var ob="#orden";  $(''+ ob +'').prop('disabled', true);
var ob="#fecha";  $(''+ ob +'').prop('disabled', true);
var ob="#factura";  $(''+ ob +'').prop('disabled', true);
var ob="#nrocuota";  $(''+ ob +'').prop('disabled', true);
var ob="#cuota";  $(''+ ob +'').prop('disabled', true);
var ob="#saldo";  $(''+ ob +'').prop('disabled', true);

for (let i = 1; i < 200; i++) {
    const elemento = document.getElementById("orden"+i);
    if (elemento) {
    valor=i+1;
    var ob="#orden"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#fecha"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#factura"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#cuota"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#saldo"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#monto"+i;  $(''+ ob +'').prop('disabled', true);
    } else { ajustarlinea(i);  i=200;   }
}
//setTimeout(document.getElementById("orden").focus(),500);

}
function ajustarlinea(i){
if (document.querySelector('#detallelinea0')) {
var val=($(detallelinea0).height())+1;

if (i>0){
 // var res = (Math.floor((i) / 2))*val;
  if ($(detallelinea0).width()<960){  i=i-1 }
  var res = (i+4)*val;
  $('.listadodet').css({'height': res + 'px'});

 }
}
}

function editarfactclidet(orden){
document.getElementById("pagofactmod").style.display = "block";

document.getElementById('labtitdetmod').innerHTML="EDITAR-DETALLE";

var pkf = document.getElementById('id_pkf').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/pagoclifact_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'id_pk': pkf,'orden': orden},
     success: function(data) {
     var list = data.datos;
     var detalle = list[0];

document.getElementById("orden").value=detalle.orden;
document.getElementById("fecha").value=detalle.fecha;
document.getElementById("factura").value=detalle.factura;
document.getElementById("nrocuota").value=detalle.nrocuota;
document.getElementById("saldo").value=detalle.saldo;
document.getElementById("monto").value=detalle.monto;

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


function pagoclipago(){
var id_pkf = document.getElementById('id_pkf').value;
if (id_pkf.length>10){
orden=0;

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/pagoclipago_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     data: { 'id_pk': id_pkf,'orden': orden},
     success: function(data) {
    if (data.success) {
     var list = data.datos;
     var html = '';

lin=0;
e=0;
total=0
for (var i = 0; i < list.length; i++) {
      if (i === 0){    }
      var pago= list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  > <input   id="tipopago'+ e +'"  value="'+ lin + '"</input> </div>';
      html += '<div class ="camplst" > <input id="montop'+ e +'" value="'+ pago.tipopago + '"</input> </div>';
      html += '<div class ="camplst" > <input id="montop'+ e +'" value="'+ number_format(pago.monto,0) + '"</input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="camplst" > <input id="nrodoc'+ e +'"value=" '+ pago.nrodoc + '"</input> </div>';
      html += '<div class ="camplst" > <input id="banco'+ e +'" value=" '+ pago.banco + '"</input> </div>';
      html += '<div class ="camplst" > <input id="ctacte'+ e +'" value=" '+ pago.ctacte + '"</input> </div>';
      html += '	<a class="btn" href="/pagoclipago/'+pago.pkpf+'/eliminar/" >ELIMINAR</a>';
      html += '</div> ';
      html += '</div> ';
      html += '</div> ';

      //total=total+(compradet.cantidad*compradet.precio);

}
    if (total>0){html +=sumatotal(total);}
    html2=""
    html2=html;
    html=""
    html+=listadocabp()+html2+listadoagregardetallep(lin,e);
    $('#pagoclifpago-list').html(html);

} else { // if succes false
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
} // fin del sccuses true /false
}// succes function
});
//setTimeout(bloquearfilas,1000);
//setTimeout(actcompelemcomp,1000);
setTimeout(limpiardetp,1000);

}else{ html=listadocabp();  $('#pagoclifpago-list').html(html);}
}

function listadocabp(){
      html ="";
     // html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:#F8E35B;"> ';
      html += '<div id= "detallelinea0" class ="detallelinea0" "> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > ORDEN </div>';
      html += '<div class ="camplst"  style="text-align:center;"> TIPO PAGO </div>';
      html += '<div class ="camplst"  style="text-align:center;"> MONTO </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="camplst"  style="text-align:center;"> NRO DOC </div>';
      html += '<div class ="camplst"  style="text-align:center;" >BANCO </div>';
      html += '<div class ="camplst"   style="text-align:center;"> CTA CTE </div>';
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
      html += '<div class ="camplst"  style="text-align:center;">  </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="camplst"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"   style="text-align:center;">  </div>';
      html += '<div class ="campcantiva"   style="text-align:center;">TOTAL   </div>';
      html += '<div class ="camplst"  style="text-align:center;" >'+number_format(total, 0)  +' </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}

function listadoagregardetallep(lin,e){
        html ="";
       lin=lin+1;   e=e+1;  col='#D5F5E3';
      if (e > 1 ){ if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "pagofactpago"; style= "display: none;"  > ';
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"';
      html += 'style="background-color:white;  padding-left: 100px;" > ';
      html += ' <label id="labtitdetpag" ';
      html += ' style= " color: #F8835B;  font-size: 22px;  line-height: 1; font-weight: bold;" ';
      html += ' >INGRESAR-PAGO</label>  </div> ';
      //html += listadocab();


      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:white;"> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea1"> ';
      html += '<div class ="campcantiva" > <input id="orden"  value=" '+ e + '"</input> </div>';
      html += '<div class ="camplst" > <input id="tipopago"   list="tipofpago_list" </input> </div>';
      html += '<div class ="camplst" > <input id="montop"  </input> </div>';

      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="camplst" > <input id="nrodoc"  </input> </div>';
      html += '<div class ="camplst" > <input   id="banco"  </input> </div>';
      html += '<div class ="camplst" > <input   id="ctacte" </input> </div>';
      html += '<div class ="campbtn" > <button  id="btnguardardetp" class="btnlstdet" onClick="guardardetp()" >  GUARDAR </button>  ';
      html += ' <button  id="btnguardardetp4" class="btnlstdet" onClick="limpiardetp(2)" >  CANCELAR </button>  ';
      html += '</div> ';
      html += '</div> ';
      html += '</div> ';// id= "pagofactmod"';
    return html;
}

function limpiardetp(n){

if (n === undefined) { i=2; }else{i=n;};

document.getElementById('labtitdetpag').innerHTML="INGRESAR-PAGO";
document.getElementById("orden").value="";
document.getElementById("tipopago").value="";
document.getElementById("montop").value="";
document.getElementById("nrodoc").value="";
document.getElementById("banco").value="";
document.getElementById("ctacte").value="";
if (i==2){document.getElementById("pagofactpago").style.display = "none";};
if (i==1){document.getElementById("pagofactpago").style.display = "block"; document.getElementById("tipopago").focus();};
}

function guardardetp(){

var pkf = document.getElementById('id_pkf').value;
var tipopago = document.getElementById("tipopago").value;
var montop = document.getElementById("montop").value;
var nrodoc = document.getElementById("nrodoc").value;
var banco = document.getElementById("banco").value;
var ctacte = document.getElementById("ctacte").value;

valida=true;
if (valida==true){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/pagoclipago_agregar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'tipopago':tipopago,'montop':montop,'nrodoc':nrodoc,'banco':banco,'ctacte':ctacte },
    success: function(data) {
    if (data.success) {
        Swal.fire({  title: '',  text: 'ACTUALIZADO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    }
      pagoclipago();

  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }

});
}
}






