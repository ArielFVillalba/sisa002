
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
setTimeout(colorlistdo,2);
setTimeout(formatearcampos,2);
setTimeout(actcompelem(),1000);
setTimeout(cargarcombos,7);

}
function cargarcombos(){
crearcmbunidad();
crearcmbhabilitado();
crearcmbmuevestock();

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


function cmbflia(nivel,codigo){
nivel=nivel+1;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbfamilia/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'codigo': codigo},
     success: function(data) {
     const obj = data.datos;
        crearcmbfila(obj,nivel);
    }
});
}

function crearcmbfila(list,nivel){
    var dataList = document.createElement('datalist');
    dataList.id = "familia"+nivel+"_list";

for (var i = 0; i < list.length; i++) {
  var familiai = list[i];
     var option = document.createElement('option');
        option.setAttribute('id', familiai.familia);
        option.value = familiai.familia;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList
    );
}

function buscarfamiliat(codigo){
//alert(codigo);
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbfamilia/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'codigo': codigo},
     success: function(data) {
     const obj = data.datos;
     crearcmbfila(obj,nivel);
    }
});
}

function cargarfamilia(codigo,inf){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/familia_buscar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     data: { 'codigo': codigo, },
     success: function(data) {

     var list = data.datos;
     //alert(creararbol(list));
     return creararbol(list);


}
});
}
var familiam = []; // Arreglo para almacenar las familias
var familian = []; // Arreglo para almacenar las familias

function creararbol(list){
$('#familia-list').html('');

html='';
html +='<div class="contenedor-menu-cat">';
var inivel=1;
var nivelant=0;
var codant=0;

for (var i = 0; i < list.length; i++) {
    var familia = list[i];
    codigo=familia.codigo;
        // Definir nombres de las familias
    familian.push([]);

    familian[i][1] =  familia.n1;
    familian[i][2] =  familia.n2;
    familian[i][3] =  familia.n3;
    familian[i][4] =  familia.n4;
    familian[i][5] =  familia.n5;
    familian[i][6] =  familia.n6;
    familian[i][7] =  familia.n7;

    familiam.push([]);
    familiam[i][1] =  familia.familia1;
    familiam[i][2] =  familia.familia2;
    familiam[i][3] =  familia.familia3;
    familiam[i][4] =  familia.familia4;
    familiam[i][5] =  familia.familia5;
    familiam[i][6] =  familia.familia6;
    familiam[i][7] =  familia.familia7;


      var ncod = codigo.replace(/\./g, "_");
      var icod = codigo.split(".");
      var nivel = icod.length;
      var nombre =familiam[i][nivel]
      var n = [];
      if (nivel == nivelant) { html +='</li>';  }
      if (nivel > nivelant) { html +='  <ul class="menu-cat" id= "'+ codant +'">';  }
      if (nivel < nivelant) {
            for (var e = nivel; e < nivelant; e++) {
                 html +='</li></ul>';
            }
      }
       html += '  <li id=\'li_'+ncod+'\'><a class="menu-cat" class ="atexttit" href="#"onclick="select(\''+ncod+'\');">'+codigo+' | '+ nombre +' <div class="icono derecha" onclick="selectdatosflia(\''+i+'\');">selec</div></a> ';
      nivelant=nivel;
      codant=ncod;

}
html +='<div class="espbtnfl"></div>';
html +='<a  class="boton" href="#" onclick="cerrarModal();">cancelar</a>';
html +='</div>';

$('#familia-list').html(html);

}
function abrirModal() {
  document.getElementById('familia').style.display = 'block';
}

function cerrarModal() {
  document.getElementById('familia').style.display = 'none';
}

function cargararbol(){
cargarfamilia('0','arbol');
}

function selecflia(cat,scat) {
if ($(document).width()<1300){  $('#categoria').hide();  $('#mostrador').show();}
cargapagina('mostrador.php?cat='+cat+'&scat='+scat,'mostrador');
selec();
}

function seleccab() {
    selec();

}


function select(elem){
alert("elem familia "+elem );
// $(inputElement).children('li').children('a').prepend('<span class="plus-sign">+</span>');
var padre = document.getElementById(elem);
var padreli = document.getElementById('li_'+elem);
//alert($(inputElement).hasClass('activado'));
        if($(padre).hasClass('activado')){
            $(padre).removeClass('activado');
            $(padre).find('li').removeClass('activado');
            $(padre).find('ul').removeClass('activado');
            $(padre).find('li').slideUp();
            $(padre).find('ul').slideUp();
            $(padre).find('a').first().find('span.plus-sign').remove();
            $(padre).children('li').children('a').find('span.plus-sign').remove();
            $(padreli).find('a').first().find('span.plus-sign').remove();
            $(padreli).find('a').first().prepend('<span class="plus-sign">+</span>');

           agregspflia(elem,'slideUp');

        }else{
            $(padre).addClass('activado');
            $(padre).children('li').addClass('activado');
            $(padre).children('ul').addClass('activado');
            $(padre).slideDown();
            $(padre).children('li').slideDown();
            $(padre).children('ul').slideDown();
            $(padreli).find('span.plus-sign').remove();
            agregspflia(elem,'slideDown');

        }
}
function agregspflia(elem,slide){
var padre = document.getElementById(elem);
var padreli = document.getElementById('li_'+elem);

cantph=$(padre).children('li').length;
 if ( cantph >0 ) {
   if (slide=="slideUp"){  }
   if (slide=="slideDown"){ $(padreli).find('a').first().prepend('<span class="plus-sign">-</span>');   }
}

$(padre).children('li').each(function() {
    var idDelLi = $(this).attr('id');
    var hijo = document.getElementById(idDelLi);
    canth=$(hijo).find('ul').first().children('li').length;
    if ( canth >0 ) {  $(hijo).find('a').first().prepend('<span class="plus-sign">+</span>'); }
});


//$('#mi_ul li').each(function() {
    // Agregar el texto de cada elemento li al array textos
  //  textos.push($(this).text());
//});

}

function selectdatosflia(i) {
alert(i);
nf="";
for (var e= 1; e <=7; e++) {
    nf=nf+ familian[i][e] ;
    alert(nf);

    if (e != 7) {nf=nf+"_";}
}
alert(nf);

}
