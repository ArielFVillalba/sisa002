var proceso=0;
function crearseccflia(){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/actfamilia/", type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'usuario': usuario, 'contraseña':contraseña,'nrotoma':nrotoma},
     success: function(data) {
     const obj = data.datos;
     alert( " SECCIONES. GENERADOS N. : " +data.datos);
     }
});
}
}


function verinfinv(inf){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

let opt = $('input[name="optfinvin"]:checked').val();
var tipoinf=inf;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/inf_inv_001/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: {  'nrotoma': nrotoma, 'opt': opt, 'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     stabla_lstinv001(data.datos);
     }
});
}
}

function iniciarfecha() {
document.getElementById('fechaini').valueAsDate = new Date();
document.getElementById('fechafin').valueAsDate = new Date();
}



function compraventa(){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
var nrotomaant = document.getElementById('txtnrotomaant').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }
if (nrotomaant.length==0){valida=0; alert("CARGAR NRO nrotomaant"); }
var fecini = document.getElementById('fechaini').value;
var fecfin = document.getElementById('fechafin').value;

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/compraventa/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: { 'nrotoma': nrotoma,'nrotomaant': nrotomaant, 'fecini': fecini, 'fecfin': fecfin,'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;

      alert( " COMPRA VENTA  GENERADOS ");
     }
});
}
}


function ajustarinv(tipo){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
var nrotomaant = document.getElementById('txtnrotomaant').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }



if (valida==true){
moveProgressBar(tipo);
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/ajusteinv/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: { 'nrotoma': nrotoma,'iajuste': tipo,'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     proceso=100;
     progressBar.style.width = proceso + '%';
     progresBarText.textContent = proceso + '%';
     }
});
}
}


function ajustarinvver(tipo){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
var nrotomaant = document.getElementById('txtnrotomaant').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }


if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/ajusteinv/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: { 'nrotoma': nrotoma,'iajuste': tipo,'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;

      alert( " INVENTARIO AJUSTADO ");
     }
});
}
}


function contajute(tipo){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
var nrotomaant = document.getElementById('txtnrotomaant').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/contajute/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: { 'nrotoma': nrotoma,'iajuste': tipo,'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     proceso=obj
     }
});
}
}

function moveProgressBar(tipo) {
    const progressBar = document.getElementById('myBar');
    const progresBarText = progressBar.querySelector('.progress-bar-text');
    let percent = 0;
    proceso= 0;
    progressBar.style.width = 65 + '%';
    progresBarText.textContent = 0 + '% PROCESANDO';

    let progress = setInterval(function() {
        if (proceso >= 100) {
            percent=proceso;
            progressBar.style.width =proceso + '%';
            progresBarText.textContent = proceso + '% PROCESADO';
            clearInterval(progress);
        } else {
            contajute(tipo);
            //percent = percent + 1;
            percent=proceso;
            if (proceso >= 65) {progressBar.style.width =proceso + '%';}
            progresBarText.textContent = proceso + '% PROCESANDO';
        }
    }, 1000*10);
}