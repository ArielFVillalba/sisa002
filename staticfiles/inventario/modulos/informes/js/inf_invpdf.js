

function inf_inv_detalladopdf(text){

var val = '';
var x = 0;
var doc = new jspdf.jsPDF ({
  orientation: "landscape",
})
alert(text)
x=230;
y=5;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(8);
val=" impreso :   "+fhview(3);
doc.text(x,y,val);
alert(val);
x=60;
y=20;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(16);
val=" CONTROL E-COMMERCE - FACTURACION ";
doc.text(x,y,val);
alert(text)
y=y+10;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(16);
val="Formulario";
doc.text(x+50,y,val);

y=y+10;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(12);
val="Documento FL-24";
doc.text(x,y,val);

doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(12);
val="Revision N° 00";
doc.text(x+100,y,val);
valor= ['codigo','descripcion','famila', 'subfamilia', 'existencia','conteo','diferencia'];
editable= [false,false,false,false,false,false,false,false];

alert(text)
y=y+5;
var yi = y;
doc.autoTable({
    head: [valor],
    body: bodyRows(text),
       margin: {horizontal:5,top: 2}, startY:yi,
       styles: {fontSize :8},
       columnStyles: {
       0: {cellWidth: 20,fontSize : 8}, 
       1: {cellWidth: 25,halign: "center",fontSize : 9},   
       2: {cellWidth: 40,halign: "center",fontSize : 9}, 
       3: {cellWidth: 20,halign: "center",fontSize : 9}, 
       4: {cellWidth: 25,halign: "center",fontSize : 9}, 
       5: {cellWidth: 20,halign: "center",fontSize : 9}, 
       6: {cellWidth: 25,halign: "center",fontSize : 9}, 
       7: {cellWidth: 25,halign: "center",fontSize : 8}, 
       8: {cellWidth: 25,halign: "center",fontSize : 8},
       }
    }
)


//y=y+10;
//doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
//doc.setFontSize(16);
//val="INFORME DE EVALUACION DE PROVEEDORES";
//doc.text(x,y,val);

doc.save("informe.pdf");

}
function bodyRows(text) {          
        var body = []
    const obj = JSON.parse(text);
        ifil = 0;
        for (x of obj) {
         y=y+10;
         ifil = ifil+1;   
         body.push([ (x.codigo), x.descripcion, x.famila, x.subfamilia, x.existencia, x.conteo, x.diferencia]
);
    }
    return body
  }


function infinve(inf){

var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");
let opt1 = $('input[name="optfinvin1"]:checked').val();
let opt2 = $('input[name="optfinvin2"]:checked').val();
var tipoinf=inf;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
    url: "/inf_inv_res/",    type: 'POST',  datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
    data: {  'nrotoma': nrotoma, 'tipoinf': tipoinf, 'opt1': opt1, 'opt2': opt2, 'usuario': usuario, 'contraseña':contraseña},
    success: function(data) {
    const obj = data.datos;
    alert(data.datos);

    }
});
}
}

function infinvres(inf){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

var opt1 = $('input[name="optfinvin1"]:checked').val();
var opt2 = $('input[name="optfinvin1"]:checked').val();

var optvalres = $('input[name="optresdet"]:checked').val();
var tipoinf=inf;
if (optvalres=="optresumido") {  url='../inf_inv_respdf/'+ nrotoma +'/'+ opt1 +'/'+ opt2 +'/'+ tipoinf }
if (optvalres=="optdetallado"){  url='../inf_inv_detpdf/'+ nrotoma +'/'+ opt1 +'/'+ opt2 +'/'+ tipoinf }
window.open(url);

}
}