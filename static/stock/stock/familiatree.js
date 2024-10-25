
function cargarfamilia(codigo,inf){
orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/familia_buscar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     data: { 'codigo': codigo, },
     success: function(data) {

     var list = data.datos;
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
html +='<a  class="boton" href="#" onclick="cerrarfliatree();">cancelar</a>';
html +='</div>';

$('#familia-list').html(html);

}
function abrirfliatree() {
  document.getElementById('familia').style.display = 'block';
}

function cerrarfliatree() {
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
//alert("elem "+elem );
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

mf="";
for (var e= 1; e <=7; e++) {
    if (familiam[i][e]){
        if (e >1 && familiam[i][e].length>0) {mf=mf+" - ";}
        mf=mf+ familiam[i][e] ;
    }
}

nf="";
for (var e= 1; e <=7; e++) {
    if (familian[i][e]){
        if ( e >1 && e<7) {nf=nf+"_";}
         nf=nf+ familian[i][e] ;
    }
}


if(document.getElementById('listadodetf') ){ pasartdatosfliainv(nf,mf);}
if(document.getElementById('id_familia1') ){ pasartdatosfliaart(nf,mf);}


}

function pasartdatosfliainv(nf,mf) {

var padre = document.getElementById("listadodetf");
cantph=$(padre).find('li').length;
//alert(" cantdida "+ cantph);

     e=cantph+1;
     htmlaux='';
     html = ' <div class ="listinf" > ';
     html += ' <div class ="listinfcod" id ="codflia'+ e +'" > '+ nf +' </div> ';
     mf = '  <li id=\'fli'+e+'\'><a>'+ mf +' </a> </li> ';
     html += ' <div class ="listinffam"  >  '+ mf +' </div> ';
     html +=  ' </div> ';
    //alert(html);
    var div = document.getElementById('listadodetf');
    div.innerHTML +=html ;
    cerrarfliatree();
}
function limpiarlstflia(){
    var div = document.getElementById('listadodetf');
    div.innerHTML = "";
}

function recuperardatos(){
var padre = document.getElementById("listadodetf");
cantph=$(padre).find('li').length;
//alert(" cantdida "+ cantph);
for (var e= 1; e <=cantph; e++) {
    var contenidoConId = document.getElementById('codflia2').textContent;
    // alert("Contenido recuperado con getElementById(): " + contenidoConId);
}

}

function pasartdatosfliaart(nf,mf) {

for (let i = 0; i < 7; i++) {
     e=i+1;
 document.getElementById('id_familia'+e).value="";
 if(document.getElementById('id_n'+e) ){ document.getElementById('id_n'+e).value="";}
}

fla = mf.split("-");
flan = nf.split("_");
if(document.getElementById('id_codigoflia') ){
cod = nf.replace(/_/g, '.');
document.getElementById('id_codigoflia').value= cod;
}

for (let i = 0; i < fla.length; i++) {
     e=i+1;
    document.getElementById('id_familia'+e).value=fla[i];
     if(document.getElementById('id_n'+e) ){document.getElementById('id_n'+e).value=flan[i];}

}
for (let i = fla.length ; i < 7; i++) {
     e=i+1;
      if(document.getElementById('id_n'+e) ){
            document.getElementById('id_n'+e).value=0;
        }
  // document.getElementById('id_familia'+e).value="al";
}

    cerrarfliatree();

}