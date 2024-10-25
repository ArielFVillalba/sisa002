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

function stabla_promo(texto){
document.getElementById('tabla').innerHTML="";
var n = texto.length;
if (n >0) {
configuracionpromo();
nombre="Table_form_promo";
tabla = document.createElement("div");
tabla.classList.add("Table_form_promo");
tabla.setAttribute("id",nombre);
tabla.setAttribute("name",nombre);
ifil = 0;
icol = 0;
titulopromo();
recorrerlineaspromo(texto);
document.getElementById('tabla').appendChild(tabla)
}else{
alert( " no existe registro " );
}
}

function recorrerlineaspromo(texto){
campo= ['eliminardet','codigo','central','cacique', 'slorenzo', 'soutlet','central','cacique', 'slorenzo', 'soutlet'];
editable= [false,false,false,false,false,false,false,false,false,false];

if (tipotabla=="informe"){
editable= [true,true,true,true,true,true,true,true,true,true];
tipocelda=['btn','text','text','text','text','text','text','text','text','text'];
}

const obj = texto;

ifil = 0;
if (obj.length==0) {
ifil = 1;
valor= ['','','','','',''];
datosevaprov();
}
for (x of obj) {
ifil = ifil+1;
valor= [x[0],x[0],x[1], x[2], x[3], x[4],x[5], x[6], x[7], x[8]  ]
datosevaprov();
}
}

function configuracionpromo(){
var tam=91;
wcelda=[ tam,100,tam,tam,tam,tam,tam,tam,tam,tam];
tipocelda=['text','text','text','text','text','text','text','text','text','text'];
valores=['codigo', 'codigo','central','cacique', 'slorenzo', 'soutlet','central','cacique', 'slorenzo', 'soutlet'];
}

function titulopromo(){
titcell="titulo";
fila();
hcelda=30;
campo= ['-','codigo','central1','cacique1', 'slorenzo', 'soutlet','central','cacique', 'slorenzo', 'soutlet'];
valor= ['-','CODIGO','CENTRAL','CACIQUE','S.LORENZO', 'OULET','CENTRAL','CACIQUE', 'SANLO', 'S OULET'];
editable= [true,true,true,true,true,true,true,true,true,true];
for (var i = 0; i < campo.length; i++) {
ifil =0;
celdas(i,campo[i],valor[i],wcelda[i],"Title_dato_promo");
}
tabla.appendChild(sfila);
}

function datosevaprov(){
titcell="datos";
fila();
hcelda=30;
for (var i = 0; i < campo.length; i++) {
celdas(i,campo[i],valor[i],wcelda[i],"datos_form_promo");
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
campos.value = number_format(valor);
campos.disabled = editable[i];
campos.classList.add(sclass);
campos.setAttribute("id",campo+"_"+ifil);
campos.setAttribute("name",campo+"_"+ifil);
if (tipotabla=="informe"){iwith=Number.parseInt(iwith)+2};
campos.style.cssText = 'text-align: right; width:'+iwith+'px; height:'+hcelda+'px;';
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
sfila.classList.add("Row_form_promo");
}

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
ele.style.cssText = 'height:'+hcelda+'px;';
let ultimo =arrayvalores.length ;

 for (i=0; i<ultimo; i++) {
 opt = document.createElement('option');
 opt.setAttribute("value",arrayvalores[i])
 opt.innerHTML = arraytextos[i];
 ele.appendChild(opt);
 }
 ele.value = valor;
 idiv.appendChild(ele);
 sfila.appendChild(idiv);
}

function tabla_promo(inf){
var fecini = document.getElementById('fechaini').value;
var fecfin = document.getElementById('fechafin').value;
let opt = $('input[name="optpromo"]:checked').val();
var actidesact=inf;
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
    url: "/tabla_promo/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
    data: {  'fecha_inicio': fecini, 'fecha_fin': fecfin, 'opt': opt, 'actidesact': actidesact, 'usuario': usuario, 'contraseña':contraseña},
    success: function(data) {
    stabla_promo(data.datos);
    }
});
}

function iniciarfilt() {
document.getElementById('fechaini').valueAsDate = new Date();
document.getElementById('fechafin').valueAsDate = new Date();
}