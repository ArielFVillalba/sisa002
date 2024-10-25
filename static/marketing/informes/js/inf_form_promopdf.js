var y = 0;
function inf_form_fl24pdf(text){

var val = '';
var x = 0;
var doc = new jspdf.jsPDF ({
  orientation: "landscape",
})

x=230;
y=5;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(8);
val=" impreso :   "+fhview(3);
doc.text(x,y,val);

x=60;
y=20;
doc.addFont("Arimo-Bold.ttf", "Arimo", "bold");
doc.setFontSize(16);
val=" CONTROL E-COMMERCE - FACTURACION ";
doc.text(x,y,val);

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

valor= ['FECHA','COD CLI','CLIENTE','FACTURA','MONTO','FORMA PAGO','RECEPCION','COD VENDEDOR','VERIFICADO','RESPONSABLE','USUARIO'];


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
       8: {cellWidth: 25,fontSize : 8},
       9: {cellWidth: 25,halign: "center",fontSize : 9}, 
       10: {cellWidth: 25,halign: "center",fontSize : 9}, 
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
         body.push([ convertDateFormatf(x.fecha), x.codcli, x.nombre, x.factura,number_format( x.monto),x.formap,x.recep, x.codvend,x.verifc,x.respent,x.usuario]
);
    }
    return body
  }

