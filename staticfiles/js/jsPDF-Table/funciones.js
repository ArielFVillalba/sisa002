


function fc_controlstring(scampo){
scampo=scampo.trim();
if (scampo === null ||scampo === "") {scampo="";};
   return scampo;
}
function fc_valv(scampo,valor){
scampo=fc_controlstring(scampo);

if (scampo=="-"){scampo=parseFloat(0);}else { scampo=parseFloat(valor);}

return scampo;
}
function fc_control021(scampo){
if (scampo === null ||scampo === "") {scampo="";};
   return scampo;
}

function fc_controlnro(scampo){
scampo=fc_controlstring(scampo);
if (scampo!="" && scampo!="-"){scampo=parseFloat(scampo);}else {scampo=parseFloat(0);}
return scampo;
}

function fc_rm(num){
 if (num<10) {return "0"+num};   
return num;
}
function fhview(tip){
d= new Date();
dia =d.getDate();
mes=(d.getMonth()+1);
anio=d.getFullYear();
ihora =d.getHours();
min =d.getMinutes();

dia=fc_rm(dia);
mes=fc_rm(mes);
ihora=fc_rm(ihora);
min=fc_rm(min);

var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
var adia = new Array ("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado");

var fecha=dia +" / "+mes+" / "+anio;
var hora =ihora+":"+min;

if (tip==1){return fecha;}
if (tip==2){ return hora;}
if (tip==3){ return fecha +" "+hora;}

}
function espblanco(n){
    i=0;
    var esp="";
    while (i < n) {
    esp=esp+" ";
    i++;
    };

}
function formtatfecv( fecha){
var dateFormat = require('dateformat');
dateFormat(fecha, "dddd, mmmm dS, yyyy, h:MM:ss TT");
return num;
}
function convertDateFormatf(string) {
   if (string !="") {
     var info = string.split('-');
     return info[2] + '/' + info[1] + '/' + info[0];
  }else {return "";}
}
function number_format(amount, decimals) {

    amount += ''; // por si pasan un numero en vez de un string
    amount = parseFloat(amount.replace(/[^0-9\.]/g, '')); // elimino cualquier cosa que no sea numero o punto

    decimals = decimals || 0; // por si la variable no fue fue pasada

    // si no es un numero o es igual a cero retorno el mismo cero
    if (isNaN(amount) || amount === 0) 
        return parseFloat(0).toFixed(decimals);

    // si es mayor o menor que cero retorno el valor formateado como numero
    amount = '' + amount.toFixed(decimals);

    var amount_parts = amount.split('.'),
        regexp = /(\d+)(\d{3})/;

    while (regexp.test(amount_parts[0]))
        amount_parts[0] = amount_parts[0].replace(regexp, '$1' + ',' + '$2');

    return amount_parts.join('.');
}