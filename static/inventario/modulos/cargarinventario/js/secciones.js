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

function stabla_secciones(){
document.getElementById('tabla').innerHTML="";
configuracionsecciones();
nombre="Table_form_secciones";
tabla = document.createElement("div");
tabla.classList.add("Table_form_secciones");
tabla.setAttribute("id",nombre);
tabla.setAttribute("name",nombre);
ifil = 0;
icol = 0;
titulosecciones();
document.getElementById('tabla').appendChild(tabla)
}

function agregarseccion(){

var sec1 = document.getElementById('combosecn1').value;
var sec2 = document.getElementById('combosecn2').value;
var sec3 = document.getElementById('combosecn3').value;
var sec4 = document.getElementById('combosecn4').value;
var sec5 = document.getElementById('combosecn5').value;
var sec6 = document.getElementById('combosecn6').value;
var sec7 = document.getElementById('combosecn7').value;
if (sec1.length>0){
cantfila=0;
var cantfila = document.getElementsByClassName("datos_form_secciones").length/7;
if (cantfila<7){
fila();
valor= [sec1,sec2,sec3,sec4,sec5,sec6,sec7];
campo= ['secc1','secc2','secc3','secc4', 'secc5', 'secc6', 'secc7'];
editable= [true,true,true,true,true,true,true];
ifil = cantfila+1;
for (var i = 0; i < campo.length; i++) {
celdas(i,campo[i],valor[i],wcelda[i],"datos_form_secciones");
}
tabla.appendChild(sfila);
}else{ alert("fila maxima "+cantfila)};
}else{ alert("cargar seccion")};
}

function configuracionsecciones(){
var tam=130;
wcelda=[ tam,tam,tam,tam,tam,tam,tam];
tipocelda=['text','text','text','text','text','text','text'];
}

function titulosecciones(){
titcell="titulo";
fila();
hcelda=25;
campo= ['secc1','secc2','secc3','secc4', 'secc5', 'secc6', 'secc7'];
valor=['SECCION 1','SECCION 2','SECCION 3','SECCION 4', 'SECCION 5', 'SECCION 6', 'SECCION 7'];
editable= [true,true,true,true,true,true,true];
for (var i = 0; i < campo.length; i++) {
ifil =0;
celdas(i,campo[i],valor[i],wcelda[i],"Title_form_secciones");
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
sfila.classList.add("Row_form_seccion");
}
function limpiarseccion(){
stabla_secciones();
}


