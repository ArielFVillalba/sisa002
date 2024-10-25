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
var tipotabla="informe";
var tipocelda =[];
var arraytextos=[];
var arrayvalores=[];
var valoresobj=[];
var editable=[];
var ifil = 0;
var icol = 0;

function stabla_lstinv001(texto){
alert(texto);
document.getElementById('tabla').innerHTML="";
var n = texto.length;
if (n >0) {
configurarlist();
nombre="Table_lstinv001";
tabla = document.createElement("div");
tabla.classList.add(nombre);
tabla.setAttribute("id",nombre);
tabla.setAttribute("name",nombre);

ifil = 0;
icol = 0;
titulolstinv001();
reclinelistinv001(texto);
document.getElementById('tabla').appendChild(tabla)
}else{
alert( " no existe registro " );
}
}

function reclinelistinv001(texto){
campo= ['codigo','descripcion','famila', 'subfamilia', 'existencia','conteo','diferencia'];
editable= [false,false,false,false,false,false,false,false];

if (tipotabla=="informe"){
//editable= [true,true,true,true,true,true,true];
//tipocelda=['text','text','text','text','text','text','text'];
tipocelda=['text','text','text','text','num','num','num'];
}

const obj = texto;
ifil = 0;
if (obj.length==0) {
ifil = 1;
valor= ['','','','','','',''];
datosinf();
}
for (x of obj) {
ifil = ifil+1;
valor= [x[0],x[1], x[2], x[3], x[4],x[5], x[6]]
datoslisinv001();
}
}

function configurarlist(){
var tam=130;
hcelda=40;
wcelda=[100,200,200,200,70,70,70];
tipocelda=['text','text','text','text','num','num','num'];
valores=['codigo','descripcion','famila', 'subfamilia', 'existencia','conteo','diferencia'];
}

function titulolstinv001(){
titcell="titulo";
fila();
campo= ['codigo','descripcion','famila', 'subfamilia', 'existencia','conteo','diferencia'];
valor=['codigo','descripcion','famila', 'subfamilia', 'exit.','conteo','dif.'];
for (var i = 0; i < campo.length; i++) {
ifil =0;
celdas(i,campo[i],valor[i],wcelda[i],"Title_lstinv001");
}
tabla.appendChild(sfila);
}

function datoslisinv001(){
titcell="datos";
fila();
hcelda=30;
for (var i = 0; i < campo.length; i++) {
celdas(i,campo[i],valor[i],wcelda[i],"datos_listinv001");
}
tabla.appendChild(sfila);
}

function celdas(i,campo,valor,iwith,sclass) {
if (titcell=="titulo"){text(i,campo,valor,iwith,sclass);}
else{
if (tipocelda[i]=="btn"){button(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="text"){text(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="date"){date(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="num"){num(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="select"){select(i,campo,valor,iwith,sclass);};
}
}

function celdas(i,campo,valor,iwith,sclass) {
if (titcell=="titulo"){text(i,campo,valor,iwith,sclass);}
else{
if (tipocelda[i]=="btn"){button(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="text"){text(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="date"){date(i,campo,valor,iwith,sclass);};
if (tipocelda[i]=="num"){num(i,campo,valor,iwith,sclass);};
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
if (tipotabla=="informe"){iwith=Number.parseInt(iwith)+3};
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';
idiv.appendChild(campos);
sfila.appendChild(idiv);
}

function date(i,campo,valor,iwith,sclass) {
idiv = document.createElement("div");
campos = document.createElement("input");
campos.type = "text";
campos.value = convertDateFormatf(valor);
campos.disabled = editable[i];
campos.classList.add(sclass);
campos.setAttribute("id",campo+"_"+ifil);
campos.setAttribute("name",campo+"_"+ifil);
if (tipotabla=="informe"){iwith=Number.parseInt(iwith)+2};
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';
idiv.appendChild(campos);
sfila.appendChild(idiv);
}

function num(i,campo,valor,iwith,sclass) {
idiv = document.createElement("div");
campos = document.createElement("input");
campos.type = "text";
campos.value = valor;
campos.disabled = editable[i];
campos.classList.add(sclass);
campos.setAttribute("id",campo+"_"+ifil);
campos.setAttribute("name",campo+"_"+ifil);
if (tipotabla=="informe"){iwith=Number.parseInt(iwith)+2};
campos.style.cssText = ' padding-right:2px; text-align: right; width:'+(iwith+1)+'px; height:'+hcelda+'px;';
idiv.appendChild(campos);
sfila.appendChild(idiv);
}

function button(i,campo,valor,iwith,sclass,myScript) {
sclass="btn_form_promo";
idiv = document.createElement("div");
var campos = document.createElement("button");
campos.setAttribute("onClick", " btn_"+campo+"('"+valor+"')");
campos.innerHTML = ">";
campos.classList.add(sclass);
campos.setAttribute("id","btn"+campo);
campos.setAttribute("name","btn"+campo);
iwith=Number.parseInt(iwith);
campos.style.cssText = 'width:'+(iwith+3)+'px; height:'+hcelda+'px;';
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
iwith=Number.parseInt(iwith)+1;
campos.style.cssText = 'width:'+iwith+'px; height:'+hcelda+'px;';
idiv.appendChild(campos);
sfila.appendChild(idiv);
}

function fila(){
nombre="fila";
sfila = document.createElement("div");
sfila.classList.add("Row_form_lst");
}


