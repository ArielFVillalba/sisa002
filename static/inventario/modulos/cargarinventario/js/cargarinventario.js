//var isCtrl = false;
//document.onkeyup=function(e){
//if(e.which == 17) isCtrl=false;
//}
//document.onkeydown=function(e){
//
//if(e.which == 17) isCtrl=true;
//if(e.which == 83 && isCtrl == true) {
//alert( e.which );
////Combinancion de teclas CTRL+S y bloquear su ejecucion en el navegador
//return false;
//}
//}

function cargarcombos(){
setTimeout(cargaricombos,2);
}
function cargaricombos(){
busdep();
busprov();
cargarcmbsecc(1);
stabla_secciones();
}

function busdep(){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/busdep/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     console.log(data)
     crearcmbdep(data.datos);
    }
});
}

function busprov(){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/busprov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     console.log(data)
    crearcmbprov(data.datos);
    }
});
}

function crearcmbprov(list){
   var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "porv_list";
     values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}
function buscodprov(nombprov){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/buscodprov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
     data: { 'usuario': usuario, 'contraseña':contraseña,'nombprov':nombprov},
     success: function(data) {
     const obj = data.datos;
     document.getElementById('txtcodprov').value=data.datos+"";
    }
});
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


function cargarcmbsecc(nro){
var sec1 = document.getElementById('combosecn1').value;
var sec2 = document.getElementById('combosecn2').value;
var sec3 = document.getElementById('combosecn3').value;
var sec4 = document.getElementById('combosecn4').value;
var sec5 = document.getElementById('combosecn5').value;
var sec6 = document.getElementById('combosecn6').value;
var sec7 = document.getElementById('combosecn7').value;

    usuario = obtener_cookie_por_nombre("usuario")
    contraseña = obtener_cookie_por_nombre("contraseña")
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
         url: "/buscseccn/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
         data: { 'usuario': usuario, 'contraseña':contraseña,'nro':nro,'sec1':sec1,'sec2':sec2,'sec3':sec3,'sec4':sec4,'sec5':sec5,'sec6':sec6},
         success: function(data) {
         const obj = data.datos;
         cargarcmbsecc2(nro,data.datos);
        }
    });
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

function crearsecciontree(list){
divmodal = document.createElement("div");
divmodal.classList.add("window-modal");
divmodal.setAttribute("id","window-modal");
divmodal.setAttribute("name","window-modal");
document.getElementById('window-modal').appendChild(divmodal);
}

function generarinv(nro){
var valida=true;
var seccion=cargarsecc();
var codprov=document.getElementById('txtcodprov').value;
var titulo=document.getElementById('txttitulo').value;
var deposito = document.getElementById('deposito').value;
if (deposito.length==0){valida=0; alert("CARGAR DEPOSITO"); }



if (nro==1){
if (titulo.length==0){ valida=0;  alert("CARGAR TITULO");}
if (seccion.length==0 && codprov.length==0){ valida=0;  alert("CARGAR SECCION o PROVEEDOR");}
if (codprov.length==0){codprov="."}
}
if (nro==2){
if (titulo.length==0){ titulo=".";}
 seccion=".";
}

if (valida==true){
const btngenerarinv1 = document.getElementById("btngenerarinv1");
const btngenerarinv2 = document.getElementById("btngenerarinv2");
btngenerarinv1.disabled = true;   btngenerarinv2.disabled = true;
deposito=deposito.toUpperCase();
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/generarinv/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: {  'deposito': deposito, 'nro': nro,  'codprov': codprov, 'seccion':seccion,'titulo': titulo,'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     document.getElementById('txtnrotoma').value = data.datos;
      alert( " NRO. TOMA GENERADO : " +data.datos);
      btngenerarinv1.disabled = false;   btngenerarinv2.disabled = false;
     }
});
}
}

function cargarsecc(){
var cantfila = document.getElementsByClassName("datos_form_secciones").length/7;
var seccion="";
scampo="";
scampon="";
if (cantfila>0){
        f=1;
        while (f <= cantfila) {
              seccion=seccion+"(";
        c=1;
            while (c < 8) {
                scampon="secc"+c+"_"+f;
                scampo= document.getElementById(scampon).value;
                if(scampo.length>0) {
                if (c>1){ seccion=seccion+"-";}
                seccion=seccion+scampo;
            }
            c=c+1;
            }
              seccion=seccion+")";
        f=f+1;
        }
}
return seccion;
}

