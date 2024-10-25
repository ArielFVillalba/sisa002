
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if(document.getElementById('columnalst') ){
    if (document.querySelector('#columnalst')) {
         //document.getElementById('labusuario').innerHTML=" list "+ $(columnalst).width();

       $('.columnalst').css({'height':'40px'});
     if ($(columna).width()<1100){
        $('.columnalst').css({'height':'90px'});
        $('.columnalstt').css({'height':'80px'});
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
setTimeout(colorlistdo,2);
setTimeout(formatearcampos,2);
setTimeout(actcompelem(),1000);
setTimeout(cargarcombo(),7);
setTimeout(cargararbol(),1000);

}
function cargarcombo(){
crearcmbunidad();
crearcmbhabilitado();
crearcmbmuevestock();
cmbflia(0,0);
}
function buscararticulo(){

var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};

if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/articulos/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{
variable=0;
var url = "/articulos/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function buscdatosart(){
document.getElementById("descripcion").value="";
variable= document.getElementById('codigo').value;
let longitud = variable.length;
//if ( variable.length<=3) {alert(" CODIGO CORTO")}
if ( variable.length>4) {
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
if (document.querySelector('#cantidad')) { document.getElementById("cantidad").focus();}

 }
});
}
//else{ if (document.getElementById("descripcion")) {document.getElementById("descripcion").focus();}}
}

function buscdatosartdescri(){
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
if (document.querySelector('#cantidad')) { document.getElementById("cantidad").focus();}
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

function formatearcampos(){

formatearcampnumv("id_costo");
formatearcampnumv("id_precio");

const titleElement = document.getElementById('titleElement');
const titleText = titleElement.textContent.trim();
if   (titleText=="EDITAR  ARTICULO")  { extraercoma();};
}

function extraercoma(){
document.getElementById("id_costo").value=document.getElementById("id_costo").value.replace(/,/g, '');
document.getElementById("id_precio").value=document.getElementById("id_precio").value.replace(/,/g, '');

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
    document.body.appendChild(dataList
    );
}
function crearcmbiva(list){
   var values = ["5","10"];
     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "iva_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function crearcmbunidad(list){
   var values = ["unidad","kilo"];
     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "unidad_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function crearcmbhabilitado(list){
   var values = ["True","False"];
     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "habilitado_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function crearcmbmuevestock(list){
   var values = ["True","False"];
     //document.getElementById("id_tipodoc").value="contado";
        var dataList = document.createElement('datalist');
        dataList.id = "muevestock_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function cmbflia(nivel,codigo){
nivel=nivel+1;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbfamilia/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
     data: { 'codigo': codigo},
     success: function(data) {
     const obj = data.datos;
        crearcmbfila(obj,nivel);
    }
});
}

function crearcmbfila(list,nivel){
for (var i = nivel; i < 7; i++) {
if(document.getElementById("familia"+i+"_list")){
document.getElementById("familia"+i+"_list").remove();
document.getElementById("id_familia"+i).value="";
}}

if(document.getElementById("familia"+nivel+"_list")){
      while (lista.firstChild) {
        lista.removeChild(lista.firstChild);
      }

}else{
var dataList = document.createElement('datalist');
dataList.id = "familia"+nivel+"_list";
}

for (var i = 0; i < list.length; i++) {
  var familiai = list[i];
     var option = document.createElement('option');
        option.setAttribute('id', familiai.codigo);
        option.value = familiai.familia;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList
    );
}

function selecflia(n){

var selectElement = document.getElementById("id_familia"+n);
var valorselc = selectElement.value;
var datalist = document.getElementById("familia"+n+"_list");
var opciones = datalist.getElementsByTagName("option");
for (var i = 0; i < opciones.length; i++) {
            idvalor=opciones[i].id
            valor= opciones[i].value
            if (valor==valorselc){
                cmbflia(n,idvalor)
                i=opciones.length;
            }
}
}
function habilitarfamilia(){
 for (let i = 0 ; i < 7; i++) {
     e=i+1;
 document.getElementById("id_familia"+e).disabled = false;
}

}

function uploadFile(pkai) {
    var blobFile = document.getElementById("filechooser").files[0];
    var codigo= document.getElementById('id_codigo').value
    var formData = new FormData();
        formData.append("codigo", codigo); // Adjunta el código al FormData
        formData.append("imagen", blobFile); // Adjunta la imagen al FormData
    var url2="/articulos/"+pkai+"/editar/"
   var csrftoken = $("[name=csrfmiddlewaretoken]").val();
   $.ajax({
       url: "/articulosubirimagen/",
       type: "POST",
       data: formData,
       headers:{ "X-CSRFToken": csrftoken},
       processData: false,
       contentType: false,
       success: function(response) {
            window.location.href = url2;

       },
       error: function(jqXHR, textStatus, errorMessage) {
           console.log(errorMessage); // Opcional
       }
   });

}
