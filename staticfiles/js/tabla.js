var idiv="";
var campos="";
var sfila="";
var tabla="";
var wtabla="";
var titcell="";
var wcelda = [];
var hcelda = 0;
var campo = [];
var valor = [];

var tipocelda =[];
var arraytextos=[];
var arrayvalores=[];
var valoresobj=[];
var editable=[];
var ifil = 0;
var icol = 0;


funtion iniciolst(texto,conf,wcelda,valores,tipocelda,editable){
div_id=conf[1];
id_tabla=conf[2];

wdivlist=conf[2];
hdivlist=conf[3];
hceldatit=conf[4];
wcelda=wcelda;
valores=valores;
tipocelda=tipocelda;
editable=editable;

}
function iniciar(texto,div_id){
nombre="listado"+idtabla;
tabla = document.createElement("div");
tabla.classList.add(nombre);
tabla.setAttribute("id",nombre);
tabla.setAttribute("name",nombre);
ifil = 0;
icol = 0;
titulo();
recorrerlineas(texto);
document.getElementById(div_id).appendChild(tabla)
}

function recorrerlineas(texto){

campo= ['id','fecha','codcli','nombre','factura','monto','formap','recep','codvend','verifc','respent','usuario'];
editable= [false,false,false,false,false,false,false,false,false,false,false,false];
if (tipotabla=="informe"){
editable= [true,true,true,true,true,true,true,true,true,true,true,true];
tipocelda=['text','text','text','text','text','text','text','text','text','text','text','text'];
}

const obj = JSON.parse(texto);
ifil = 0;


if (obj.length==0) {
ifil = 1;
valor= ['','','','','','','','','','','',''];
datosevaprov();
}

for (x of obj) {
ifil = ifil+1;
valor= [x.id,x.fecha, x.codcli, x.nombre, x.factura,x.monto,x.formap,x.recep, x.codvend,x.verifc,x.respent,x.usuario]
datosevaprov();
}

}


function titulo(){
titcell="titulo";
fila();
hcelda=hceldatit;
campo= valores;
valor= valort;
editable= editable;
for (var i = 0; i < campo.length; i++) {
ifil =0;
celdas(i,campo[i],valor[i],wcelda[i],"Title_form_fl24");
}
tabla.appendChild(sfila);
}

function datosevaprov(){
titcell="datos";
fila();
hcelda=30;
for (var i = 0; i < campo.length; i++) {
celdas(i,campo[i],valor[i],wcelda[i],"datos_form_fl24");
}
tabla.appendChild(sfila);
}

function celdas(i,campo,valor,iwith,sclass) {
if (titcell=="titulo"){pagin(i,campo,valor,iwith,sclass);}
else{
if (tipocelda[i]=="btn"){button(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="text"){text(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="select"){select(i,campo,valor,iwith,sclass);};
}
}


function text(i,campo,valor,iwith,sclass) {
idiv = document.createElement("div");
campos = document.createElement("input");
campos.type = "text";
campos.value = valor;
campos.disabled = editable[i];
campos.classList.add(sclass);
campos.setAttribute("id",campo+"_"+ifil);
campos.setAttribute("name",campo+"_"+ifil);
if (tipotabla=="informe"){iwith=Number.parseInt(iwith)+2};
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';

idiv.appendChild(campos);
sfila.appendChild(idiv);

}
function button(i,campo,valor,iwith,sclass,myScript) {

sclass="btn_form_fl24";
idiv = document.createElement("div");
var campos = document.createElement("button");
campos.setAttribute("onClick", " btn_"+campo+"('"+valor+"')");
campos.innerHTML = ">";
campos.classList.add(sclass);
campos.setAttribute("id","btn"+campo);
campos.setAttribute("name","btn"+campo);
iwith=Number.parseInt(iwith);
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';
idiv.appendChild(campos);
sfila.appendChild(idiv);
}

function pagin(i,campo,valor,iwith,sclass) {
idiv = document.createElement("div");
campos = document.createElement("p");
var newContent = document.createTextNode(valor);
campos.appendChild(newContent); //añade texto al div creado.
campos.disabled = editable[i];
campos.classList.add(sclass);
campos.setAttribute("id",campo);
campos.setAttribute("name",campo);
iwith=Number.parseInt(iwith);
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';

idiv.appendChild(campos);
sfila.appendChild(idiv);

}

function fila(){
nombre="fila";
sfila = document.createElement("div");
sfila.classList.add("Row_form_fl24");
}


//----------------------------------------------------------------------

function select(i,campo,valor,iwith,sclass) {
idiv = document.createElement("div");
arraytextos = [];
arrayvalores = [];
if (valores[i]=="calidad"){calidad();};
if (valores[i]=="respuesta"){respuesta();};
if (valores[i]=="puntualidad"){punt();};
if (valores[i]=="garantia"){cumpli();};
if (valores[i]=="postventa"){postvta();};
if (valores[i]=="especif"){especifi();};

ele = document.createElement('select');
ele.classList.add(sclass);
ele.addEventListener('change', updateValue);
ele.setAttribute("id",campo+"_"+ifil);
ele.setAttribute("name",campo+"_"+ifil);
iwith=Number.parseInt(iwith)+3;
ele.style.cssText = 'width:'+iwith+'px;';
//ele.style.cssText = 'height:'+hcelda+'px;';
let ultimo =arrayvalores.length ;

 for (i=0; i<ultimo; i++)
 {
 opt = document.createElement('option');
 opt.setAttribute("value",arrayvalores[i])
 opt.innerHTML = arraytextos[i];
 ele.appendChild(opt);
 }
 ele.value = valor;
 idiv.appendChild(ele);
 sfila.appendChild(idiv);
}



