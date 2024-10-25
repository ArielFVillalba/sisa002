$(window).resize(function(){
actcompelemcomp();
});

function actcompelemcomp(){

if (document.querySelector('#columnalst')) {
     $('.columnalst').css({'height':'35px'});
    // document.getElementById('labusuario').innerHTML=" list "+ $(columnalst).width();
     if ($(columnalst).width()<1200){

         $('.contimagen').css({'display':'none'});

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
detallepago();
}


function filtrarventa(){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var idcliente = document.getElementById('id_idcliente').value;
var tipodoc = document.getElementById('id_tipodoc').value;
valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,
idcliente:idcliente,
tipodoc:tipodoc
};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = '/ventacab_filtro_lst/?' + params;

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
var url = "/ventacab/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}else{
variable=0;
var url = "/ventacab/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function eliminar_ventacab(pk) {
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
                    fetch('/ventacab/' + pk + '/eliminar/', { method: 'DELETE', headers: headers  })
                    .then((response) => {
                    if (response.ok) {
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                        Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});4
                         document.location.href= "/ventacab/crear/";

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                        Swal.fire({  title: '',  text: 'ERROR ',
                        icon: 'error',  customClass: {container: 'msnsuccess', }});
                        buscarfactura()
                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re

                    }}  // fin  if (result.isConfirmed) {
                    ) // fin del    .then((result) => {
}; //fin
function cargarcombos(){
setTimeout(cargaricombos,200);
}

function cargaricombos(){
cargarcmbformapago();
buscli();

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

busdetallef();
cargarcmbart();
cargarcombdep();
cargarcmbformapago();
}
}

function crearcmbtipodoc(list){
   var values = ["contado","credito"];
     document.getElementById("id_tipodoc").value="contado";
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
function busdetallef(){
var pkf = document.getElementById('id_pkf').value;
if (pkf.length>10){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventadet_caja_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'orden': orden},
     success: function(data) {
     if (data.success) {
     var list = data.datos;
     var html = '';

lin=0;
e=0;
total=0;
html =listadocab();
html += '<div id= "contscrt"  class ="contscr"> ';
for (var i = 0; i < list.length; i++) {
      var ventadet = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
       col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#E6FCFC';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  > <input class="tamletra" disabled  id="orden'+ e +'"  value="'+ ventadet.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input class="tamletra" disabled id="codigo'+ e +'" value="'+ ventadet.codigo + '"</input> </div>';
      html += '<div class ="campdescr" > <input class="tamletra"  disabled id="descripcion'+ e +'"  value=" '+ ventadet.descripcion + '"</input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class ="campcant" > <input class="tamletra" style="text-align:center;" disabled id="cantidad'+ e +'" value=" '+ ventadet.cantidad + '"</input> </div>';
      html += '<div class ="camprecio" > <input class="tamletra" style="text-align:right;"  disabled id="precio'+ e +'" value=" '+ number_format(ventadet.precio,0) + '"</input> </div>';
      html += '<div class ="campcantiva" > <input  class="tamletra" style="text-align:right;" disabled id="iva'+ e +'" value=" '+ ventadet.iva + '"</input> </div>';
      html += '<div class ="camplst" > <input  class="tamletra" style="text-align:right;" disabled id="subtotal'+ e +'" value=" '+ number_format(ventadet.subtotal,0) + '"</input> </div>';
      html += '<div class ="campbtn" > <button  class="btnlstdet" onClick="editarventadet('+ ventadet.orden +')" >  editar </button> ';
      html += '<button  class="btenlstdete" onClick="ventacajadet_eliminar(\''+ ventadet.pkfd +'\')" >eliminar </button> </div>';
      html += '</div> ';
      html += '</div> ';
      total=total+(ventadet.cantidad*ventadet.precio);

var nuevoCodigoArticulo = ventadet.codigo; // Ejemplo de nuevo código de artículo
 // Obtén la referencia al elemento de imagen por su ID
var imagenArticulo = document.getElementById("imagenArticulo");
// Crea la nueva ruta de la imagen
var nuevaRutaImagen = "/static/imagen/imagenes/" + nuevoCodigoArticulo + ".png";
// Actualiza el atributo src de la imagen con la nueva ruta
imagenArticulo.src = nuevaRutaImagen;
}
html += '</div> ';

if (total>0){
document.getElementById("total").innerHTML = " " + number_format(total, 0);
//html +=sumatotalf(e,total);
}
//html +=detalle;
html +=listadoagregardetalle(lin,e);

$('#venta-list').html(html);
    } else { // if succes false
       if (data.message==""){error="ERROR"}else{ error=data.message};
       Swal.fire({  title: '',  text: error,
       icon: 'error',  customClass: {container: 'msnsuccess', }});
    } // fin del sccuses true /false
}// succes function

});

setTimeout(bloquearfilas,1000);
setTimeout(actcompelemcomp, 1000); // Retraso de 1 segundos
setTimeout(scrollAlFinal, 1000); // Retraso de 1 segundos
setTimeout(limpiardet, 500); // limoia detalles



}else{
html=listadocab()+listadoaux()+listadoagregardetalle(0,0);
$('#venta-list').html(html);}
}
function scrollAlFinal() {  contscrt.scrollTop = contscrt.scrollHeight;   }

function listadocab(){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:white;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;"> CODIGO </div>';
      html += '<div class ="campdescr"  style="text-align:center;"> DESCRIPCION </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcant"  style="text-align:center;" > CANT </div>';
      html += '<div class ="camprecio"   style="text-align:center;"> PRECIO </div>';
      html += '<div class ="campcantiva"   style="text-align:center;">  IVA </div>';
      html += '<div class ="camplst"  style="text-align:center;" >  SUB TOT </div>';
      html += '</div> ';
      html += '</div> ';
      return html;
}
function sumatotalf(e,total){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:white;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;">  </div>';
      html += '<div class ="campdescr"  style="text-align:center;">  </div>';
      html += '</div> ';
      html += '<div class ="detallelinea2"  style="text-align:center;"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" > ITEMS </div>';
      html += '<div class ="camplst"   style="text-align:center; font-size: 24px;"> '+number_format(e, 0)  +' </div>';
      html += '<div class ="campdescr"   style="text-align:center; font-size: 24px;">TOTAL  .  '+number_format(total, 0)  +'</div>';
     // html += '<div class ="camplst"  style="text-align:right; font-size: 24px;" >'+number_format(total, 0)  +' </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}
function listadoaux(){
html="";
html += '<div id= "contscrt"  class ="contscr"> ';
lin=0;
e=0;
for (var i = 0; i < 10; i++) {

lin=lin+1;   e=i+1;  col='#D5F5E3';
col='#D5F5E3';
if (e > 1 ){  if (e % 2 === 0) { col='#E6FCFC';   } else {  col='#D5F5E3';   }  }
html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:'+col+';"> ';
html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
html += '<div class ="campcantiva"  > <input class="tamletra" disabled  id="orden'+ e +'"  value=""</input> </div>';
html += '<div class ="camplst" > <input class="tamletra" disabled id="codigo'+ e +'" value=""</input> </div>';
html += '<div class ="campdescr" > <input class="tamletra"  disabled id="descripcion'+ e +'"  value=" "</input> </div>';
html += '</div> ';
html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
html += '<div class ="campcant" > <input class="tamletra" style="text-align:right;" disabled id="cantidad'+ e +'" value=" "</input> </div>';
html += '<div class ="camprecio" > <input class="tamletra" style="text-align:right;"  disabled id="precio'+ e +'" value=""</input> </div>';
html += '<div class ="campcantiva" > <input  class="tamletra" style="text-align:right;" disabled id="iva'+ e +'" value=" "</input> </div>';
html += '<div class ="camplst" > <input  class="tamletra" style="text-align:right;" disabled id="subtotal'+ e +'" value=""</input> </div>';
html += '</div> ';
html += '</div> ';
}
html += '</div> ';

//html=""
return html;
}
function listadoagregardetalle(lin,e){
      html ="";
      lin=lin+1;   e=e+1;  col='#D5F5E3';
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"';
      html += 'style="background-color:white;  padding-left: 100px;" > ';
      html += ' <label id="labtitdetmod" ';
      html += ' style= " color: #F8835B;  font-size: 22px;  line-height: 1; font-weight: bold;" ';
      html += ' >INGRESAR-DETALLE</label>  </div> ';
      //html += listadocab();


      col='#D5F5E3';
      html += '<div id= "lin0'+ lin +'" class ="detallelinea0"  style="background-color:white;"> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea1"> ';
      html += '<div class ="campcant" > <input  class="tamletra"  id="cantidad" placeholder ="cantidad" onkeydown="pasarcampo(event,id)"  onkeyup ="calcularst(event)" value="1" </input> </div>';
      html += '<div class="oclultar" class ="campcantiva" > <input class="tamletra" disabled id="orden"  value=" '+ e + '"</input> </div>';
      html += '<div class ="camplst" ><input class="tamletra" type="text" id="codigo"';
      html += ' onkeyup ="pasarcampo(event,id)"';
      html += ' placeholder ="ingresar codigo" > </input> </div>';

      html += '<div class ="campdescr" style="width: 230px;"  > <input class="tamletra" id="descripcion" ';
      html += ' onkeyup ="pasarcampo(event,id)" onfocus="buscdatosartcaja()"';
      html += ' placeholder =" ingresar descripcion"  list="descrip_list" </input> </div>';
      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea2"> ';
      html += '<div class="oclultar"  class ="camprecio" > <input class="tamletra" disabled  id="precio" placeholder ="precio" onkeydown="pasarcampo(event,id)"  onkeyup ="calcularst(event)" </input> </div>';
      html += '<div class="oclultar" class ="campcantiva" > <input  class="tamletra"    disabled id="iva" placeholder ="iva"  </input> </div>';
      html += '<div class="oclultar"  class ="camplst" > <input  class="tamletra" disabled id="subtotal" placeholder ="sub total" </input> </div>';
      html += '<div class ="campbtn" > <button  id="btnguardardet" class="btnlstdet"  onClick="guardardetv()" >  GUARDAR </button>  ';
      html += ' <button  class="btnlstdet" onClick="limpiardet()" >  NUEVO </button>  ';
      html += '</div> ';
      html += '</div> ';
    return html;
}

function ventacajadet_eliminar(pk){
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
                    fetch('/ventadetcaja/' + pk + '/eliminar/',
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
                      busdetallef();
                    }else{
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                         Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                         busdetallef();

                    }

                    // Realizar otras acciones en función del mensaje recibido
                  })
                  .catch((error) => {
                   // console.error('Error:', error);
                  });
                 }}  // fin  if (result.isConfirmed) {
                 ) // fin del    .then((result) => {
  }// fin

function guardardetv(){
var botong = document.getElementById("btnguardardet");
botong.disabled = true;
if (document.getElementById('labtitdetmod').textContent==="INGRESAR-DETALLE") {ventadet_guardar(); }
if (document.getElementById('labtitdetmod').textContent==="EDITAR-DETALLE") {ventadet_editar(); }
botong.disabled = false;

}


function ventadet_editar(){
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
     url: "/ventadet_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
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
      busdetallef();
  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }
});
}
}

function ventadet_guardar(){
var pkf = document.getElementById('id_pkf').value;
var codigo = document.getElementById('codigo').value;
var deposito = document.getElementById('id_deposito').value;
var cantidad = document.getElementById('cantidad').value;
var precio = document.getElementById('precio').value;
var orden = document.getElementById('orden').value;

valida=true;

if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventadetcaja_guardar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'orden':orden , 'codigo':codigo,'cantidad':cantidad,'precio':precio,'deposito':deposito  },
     success: function(data) {
     if (data.success) {
        var list = data.datos;
        var ventadet = list[0];
        didfactura=ventadet.idventacab;
        cantr=ventadet.cantr;
        url="/ventacaja/" + didfactura + "/cargar/"
        if (cantr==1){ window.location.href = url; } else { busdetallef();}

      //  Swal.fire({  title: '',  text: 'ACTUALIZADO',
      // icon: 'success',  customClass: {container: 'msnsuccess', }});
    } else {
      // if (data.message==""){error="ERROR"}else{ error=data.message};
      // Swal.fire({  title: '',  text: error,
      // icon: 'error',  customClass: {container: 'msnsuccess', }});
            busdetallef();

    }
  },
    error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }
});
}
}

function buscdatosartcod(event){
if (event.keyCode == 13 ||  event.keyCode === 32 ) { buscdatosartcaja(); }
}

function buscdatosartcaja(){
document.getElementById("descripcion").value="";
variable= document.getElementById('codigo').value
let longitud = variable.length;
if ( variable.length>3) {
var codigo = document.getElementById('codigo').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/articulodatos/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'codigo': codigo},
     success: function(data) {
     var list = data.datos;
     var artículos = list[0];
if (document.querySelector('#descripcion')) { document.getElementById("descripcion").value=artículos.descripcion;}
if (document.querySelector('#precio')) { document.getElementById("precio").value=artículos.precio;}
if (document.querySelector('#iva')) { document.getElementById("iva").value=artículos.iva;}
if (document.querySelector('#cantidad')) { document.getElementById("btnguardardet").focus();}

}
});
}
}


function buscdatosartdesc(event){
if (event.keyCode == 13 ||  event.keyCode === 32 ) { buscdatosartdescricaja() ;}
}
function buscdatosartdescricaja(){
var desc = document.getElementById('descripcion').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/articulodatosdesc/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'desc': desc},
     success: function(data) {
     var list = data.datos;
     var artículos = list[0];
if (document.querySelector('#codigo')) { document.getElementById("codigo").value=artículos.codigo;}
if (document.querySelector('#precio')) { document.getElementById("precio").value=artículos.precio;}
if (document.querySelector('#iva')) { document.getElementById("iva").value=artículos.iva;}
if (document.querySelector('#cantidad')) { document.getElementById("btnguardardet").focus();}
    }
});
}

function pasarcampo(event,id){

if (event.keyCode === 8 && id==="descripcion" ){
document.getElementById("codigo").value="";
document.getElementById("precio").value="";
}

if (event.keyCode === 13 && id==="codigo"){document.getElementById("descripcion").focus();}
if (event.keyCode === 13 && id==="descripcion" ){controldescripcaja();}
if (event.keyCode === 13 && id==="cantidad"){document.getElementById("codigo").focus();}
if (event.keyCode === 13 && id==="precio"){ document.getElementById("btnguardardet").focus(); }
if (event.keyCode == 13 && id==="id_ruc"){ document.getElementById("id_cliente").focus();}
if (event.keyCode === 13 && id==="id_cliente" ){
document.getElementById("id_idcliente").value="";
cli=document.getElementById("id_cliente").value;
 buscdatoscli(cli);  }
}

function controldescripcaja(){
cod=document.getElementById("codigo").value;
prec=document.getElementById("precio").value;
if (cod.length==0 || prec.length==0) { buscdatosartdescricaja();}
//document.getElementById("cantidad").focus();
}
function clicidruc(){
document.getElementById("id_cliente").value="";
doc=document.getElementById("id_ruc").value;
buscdatoscliciruc(doc) ;

}
function cliciruc(){
if (event.keyCode == 13 ||  event.keyCode === 32 ) {

    document.getElementById("id_cliente").focus();

 }
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
document.getElementById("precio").value="";
document.getElementById("cantidad").value="1";
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
if (document.getElementById("codigo")){setTimeout(document.getElementById("codigo").focus(),500);}

}

function editarventadet(orden){
document.getElementById('labtitdetmod').innerHTML="EDITAR-DETALLE";
var pkf = document.getElementById('id_pkf').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ventadet_caja_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'orden': orden},
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



function procesarpago(event){
if (event.keyCode === 13 ){
cargarpago();
}
}

function cargarpago(){
var pkf = document.getElementById('id_pkf').value;
var monto = document.getElementById('monto').value;
var id_idcliente = document.getElementById('id_idcliente').value;
var id_cliente = document.getElementById('id_cliente').value;
var id_fpago = document.getElementById('id_fpago').value;
var desc = document.getElementById('desc').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
var longfp = id_fpago.length;
var longm = monto.length;
//if (id_cliente === "") { alert(" AGREGAR CLIENTE");}
if (id_cliente === "") { id_cliente=0;}

if (longfp > 0 && longm > 0 ) {

$.ajax({
     url: "/ventacajapago_guardar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf,'monto': monto,'id_idcliente': id_idcliente,'id_cliente': id_cliente,'id_fpago': id_fpago,'desc': desc},
     success: function(data) {
          detallepago();

}

});
}
}

var totalpagoado
function detallepago(){
var pkf = document.getElementById('id_pkf').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
totalpagoado=0
total=0

$.ajax({
     url: "/detallepagocaja_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pkf': pkf},
     success: function(data) {
     const obj = data.datos;
     if (data.success) {
     var list = data.datos;
     var html = '';
lin=0;
e=0;
total=0;
for (var i = 0; i < list.length; i++) {
      var pago= list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#f2f2f2';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="detallelinea00"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea01"> ';
      html += '<div class ="campcantiva"  > <input disabled   id="orden'+ e +'"  value="'+ pago.orden + '"</input> </div>';
      html += '<div class ="camplst" > <input disabled  id="formapago'+ e +'" value="'+ pago.formapago + '"</input> </div>';
      html += '<div class ="camplst" > <input disabled  style="text-align:right;" id="montop'+ e +'" value="'+ number_format(pago.monto,0) + '"</input> </div>';

      html += '</div> ';
      html += '<div id= "lin'+ lin +'" class ="detallelinea02"> ';
      html += '<div class ="camplst" > <input  disabled  id="nrodoc'+ e +'"value=" '+ pago.descripcion + '"</input> </div>';
      html += '	<a class="btenlstdete" href="/cajapagocli/'+pago.iddetpago+'/eliminar/" >ELIMINAR</a>';

      html += '</div> ';
      html += '</div> ';
      total=parseFloat(total)+parseFloat(pago.monto.replace(/,/g, ''));
    }

    var totalp = document.getElementById('idtotal').value;
    totalp=parseFloat(totalp.replace(/,/g, ''));
    var saldo =parseFloat(totalp)-total;
    if (saldo<0){
        document.getElementById('idsaldo').value=0;
        document.getElementById('idvuelto').value=number_format(saldo * -1,0);
        document.getElementById('monto').value="";
    }else{
    document.getElementById('idsaldo').value=number_format(saldo,0);
    document.getElementById('monto').value="";
    document.getElementById('idvuelto').value=0;
    }

    if (total>0){
    html +=sumapagtotal(total);
    }
    html2=""
    html2=html;
    html=""
    html+=listadocabp()+html2;
    $('#pagoclifpago-list').html(html);
   }
}
});
 document.getElementById("id_fpago").focus;

}

function codigocli_caja(){
didruc =document.getElementById("id_ruc").value;
codigocli(didruc);
}


function listadocabp(){
      html ="";
     // html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:#F8E35B;"> ';
      html += '<div id= "detallelinea0" class ="detallelinea0" "> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"  style="text-align:center;"> TIPO PAGO </div>';
      html += '<div class ="camplst"  style="text-align:center;"> MONTO </div>';
      html += '<div class ="camplst"  style="text-align:center;"> DESCRIP </div>';
      html += '</div> ';
      return html;
}

function sumapagtotal(total){
      html ="";
      html += '<div id= "detallelinea0" class ="detallelinea0" style="background-color:with;"> ';
      html += '<div class ="detallelinea1"> ';
      html += '<div class ="campcantiva"  style="text-align:center;" >  </div>';
      html += '<div class ="camplst"   style="text-align:center;">TOTAL   </div>';
      html += '<div class ="camplst" > <input disabled  style="text-align:right;" value="'+ number_format(total,0) + '"</input> </div>';
      html += '</div> ';
      html += '</div> ';
     return html;
}
function imprimir001() {
    // Crear un objeto de impresión
    var impresora = window.open('', '');

    // Construir el contenido a imprimir
    var contenido = '<h1>¡Hola Mundo!</h1>';

    // Escribir el contenido en el objeto de impresión
    impresora.document.write(contenido);

    // Imprimir el documento
    impresora.print();

    // Cerrar el objeto de impresión después de imprimir
    setTimeout(function(){impresora.close();}, 500);
}
function imprimirpdf() {
       var contenido = "";
    contenido += "Ticket de Compra\n";
    contenido += "-------------------\n";
    contenido += "Cliente: Juan Pérez\n";
    contenido += "Productos:\n";
    contenido += "- Producto 1: $10\n";
    contenido += "- Producto 2: $20\n";
    contenido += "-------------------\n";
    contenido += "Total: $30\n";

    // Crear una función de impresión usando la API de impresión del navegador
    var ventanaImpresion = window.open('', '_blank');
    ventanaImpresion.document.write(contenido);
    ventanaImpresion.print();
    ventanaImpresion.document.close();
    ventanaImpresion.close();
}

function imprimir002() {

var opcionesImpresion = {
  mode: 'iframe', // Usa un marco separado para imprimir
  popClose: false, // No cierres la ventana después de imprimir
  popTitle: '', // No muestres un título para la ventana emergente
  popHt: 10, // Altura del marco de impresión
  popWd: 10 // Anchura del marco de impresión
};

// Ejecuta la impresión con las opciones definidas
window.print(opcionesImpresion);
}
function imprimir003() {
  var contenido = `
    <style>
      /* Estilos para el ticket */
      body {
        font-family: Arial, sans-serif;
      }
      .ticket {
        width: 200px;
        padding: 10px;
        //border: 1px solid #000;
      }
    </style>
    <div class="ticket">
      <h2>Ticket de Compra</h2>
      <p>Fecha: 28/05/2024</p>
      <p>Producto: Artículo X</p>
      <p>Precio: $10.00</p>
      <p>Cantidad: 1</p>
      <p>Total: $10.00</p>
    </div>
  `;

  var ventanaImpresion = window.open('', '_blank'); // Abre una nueva ventana
  ventanaImpresion.document.write(contenido); // Escribe el contenido en la ventana
  ventanaImpresion.print(); // Imprime la ventana
  setTimeout(function(){ventanaImpresion.close();}, 500);

}

