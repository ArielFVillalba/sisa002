
 function cargapagina(url,id){
      cargapaginai(url,id);
 }
function createXMLHttpRequest(){
var xmlHttp=null;
if (window.ActiveXObject) xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
else if (window.XMLHttpRequest)
    xmlHttp = new XMLHttpRezquest();
return xmlHttp;
}

$(window).resize(function(){
actelementos();
});

function actelementos(){

    //document.getElementById('labusuario').innerHTML=$(cabecera).width()+obtener_cookie_por_nombre("usuario");
     //document.getElementById('labusuario').innerHTML=$(cabecera).width();
    $('.cabecera').css({'height':'15%'});
    $('.articuloscab').css({'width':'100vw'});



    if ($(cabecera).width()<840){
       $('.cabecera').css({'height':'30%'});
       $('.cabecera').css({'min-height':'130px'});

    }
    if (window.matchMedia("(max-width: 600px)").matches) {
       $('.cabecera').css({'height':$(panellogo).height()*2+10+'px'});


    } else {
  // código para resoluciones mayores a 600px
}

}

function actelementos2(){

      if ($(cabecera).width()<600){

       $('.cabecera').css({'height':'200px'});
       $('.btn-cat').css({'display':'block'});
       $('.menu-cat li ul').slideUp();
       $('.categoria').css({'display':'none'});
       $('.mostrador').css({'display':'block'});
       $('.zonabuscar').css({'width':$(panellogo).width()+'px'});
       $('.zonabuscar').css({'height':'15%'});

  }else{
       $('.cabecera').css({'height':'100px'});
       $('.categoria').css({'display':'none'});
       $('.btn-cat').css({'display':'none'});
       $('.mostrador').css({'padding':'30px 100px 5px;'});
       $('.zonabuscar').css({'width':'98%'});
       $('.zonabuscar').css({'height':'30%'});
    }

//   $('.zonabuscar').css({'width':$(panelini).width()+'px'})
    document.getElementById('lbltitulo').value=$(cabecera).width() +" a "+ $(document).width();

}


function cargarcategoria(){
  if ($('.categoria').is(':visible')) {
      $('.categoria').hide();
if ($(document).width()<1300){ $('.mostrador').show();}
} else {
    $('.categoria').show();
     if ($(document).width()<1300){$('.mostrador').hide();}
      cargapagina('categoria.php','categoria'); 
}

    //$('.btn-cat').css({'display':'none'});
   // $('.categoria').css({'display':'block'});
  
}

function inislaider1(){   
	$(document).ready(function(){	
		$("#slider").easySlider({
			auto:true, 
			continuous:true,
			numeric:false,
			speed:3000,
			pause:3000
		});
	});
}

function cargardiv(){
confvtns();
cargapagina('../logoini','panellogo');
cargapagina('../menuini','panelini');

$('.mostrador').css({'display':'block'});
cargapagina('../login','mostrador');

//$('.menul').css({'display':'block'});
//cargapagina('../empresas','menul');
//cargapagina('../menuinventario','menul');

}

function salir(){
document.getElementById('labusuario').innerHTML="";
document.location.href='/login/';
document.cookie = "usuario=; max-age=0; path=/";
document.cookie = "contraseña=; max-age=0; path=/";
}

function registrar(){
 if (validarusu()==true){
    confvtns();
     $('.mostrador').css({'display':'block'});
     cargapagina('../registroentidad','mostrador');
 setTimeout(iniciarfilt, 1000);
}


}
function cargarvarreg(){
document.getElementById('comprad').innerHTML =document.getElementById('labusuario').innerHTML;
document.getElementById('fecha').valueAsDate = new Date();
}


function cargarvarfil(){
iniciarfilt();
}


function validarusu(){
//if (document.getElementById('labusuario').innerHTML.trim().length>0){
usuario = obtener_cookie_por_nombre("usuario")
if (usuario.trim().length>0){

return true;   
}else {    
salir();   
return false; 
}     
 
}

function confvtns(){
document.getElementById("filtros").innerHTML="";
document.getElementById("mostrador").innerHTML="";
document.getElementById("menul").innerHTML="";

$('.menul').css({'display':'none'});
$('.filtros').css({'display':'none'});
$('.mostrador').css({'display':'none'});

 }
function inicio(){
  titulo();

}

function updateValue(e) {
var valor= e.target.value;
var did= e.target.id;
sumarvalores();
}



function barra(){
alert("fsa");
myProgress = document.createElement("myProgress");
//myProgress.setAttribute("id","myProgress");
//myProgress.setAttribute("name","myProgress");
//
//myBar = document.createElement("myBar");
//myBar.setAttribute("id","myBar");
//myBar.setAttribute("name","myBar");
//
//document.getElementById('myProgress').appendChild(myBar)
document.getElementById('mostrador').appendChild(myProgress)
}

function move() {
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}


function menuempresas() {
   document.location.href='/menu';
   document.getElementById('lbltitulo').innerHTML="Lomas ";
   document.getElementById('labusuario').innerHTML=obtener_cookie_por_nombre("usuario");



}

function menucompras(){
   document.location.href='/menucompras/';
}

function inffiltpromo01(){
if (validarusu()==true){
   document.location.href='/inffiltpromo';
   document.getElementById('lbltitulo').innerHTML="CASA PARANA";
   document.getElementById('labusuario').innerHTML=obtener_cookie_por_nombre("usuario");
}
}



function cargarcmbsecc2(nro,list){
var snom="";

if (nro==1){ snom="secn1";};
if (nro==2){ snom="secn2";};
if (nro==3){ snom="secn3";};
if (nro==4){ snom="secn4";};
if (nro==5){ snom="secn5";};
if (nro==6){ snom="secn6";};
if (nro==7){ snom="secn7";};

const n = 7;
for (let i = nro; i <= n; i++) {
if(document.getElementById("secn"+i)){
document.getElementById("secn"+i).remove();
document.getElementById("combosecn"+i).value="";
}}
    var values =list
    var dataList = document.createElement('datalist');
    dataList.id = snom;
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
      document.body.appendChild(dataList);

}

function menuinventario(){
document.location.href= "/menuinventario/";
}

function formatearcampnumv(id){
valor=document.getElementById(id).value.replace(/\./g, "").replace(",", ".");
if (isNaN(valor)==false && valor != "") {
valor = parseFloat(valor).toLocaleString('en-US', {minimumFractionDigits: 2});
document.getElementById(id).value=valor;
}
}
function elementovacio(elemento) {
var myElement = document.getElementById(elemento);
if (myElement.textContent.trim() === '') { valor=false;  } else { valor = true;}
return valor
}