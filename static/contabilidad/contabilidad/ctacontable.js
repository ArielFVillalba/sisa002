
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if (document.querySelector('#columnalst')) {
    $('.columnalst').css({'height':'30px'});
    // document.getElementById('labusuario').innerHTML=$(columnalst).width();
     if ($(columna).width()<1100){
        $('.columnalst').css({'height':'80'});
        $('.columnalstt').css({'height':'80px'});
      }
      }
}

function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(actcompelem(),100);
document.getElementById('idbuscar').value="*";
}


function buscarctacontable(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;

if ( variable==0 || variable=="*" || variable=="" || variable=='' ) {
variable=0;

var url = "/ctacontable/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{

var url = "/ctacontable/" + variable + "/listar/";  // Construir la URL de la vista

window.location.href = url;
}
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
