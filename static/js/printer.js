class PrinterEscPos {
    constructor(apiPath){
        this.apiRouter = apiPath;
        this.dataPrinter = [];
    }
    static getPrinters = (apiPath="http://127.0.0.1:5656/")=> {
        return $.ajax({
            type: "GET",
            url: apiPath+"printers",
            async:false,
            contentType:"application/json",
            success: function (response) {
                if(response.status == "OK"){
                    console.log("success");
                }else if(response.status == "ERROR"){
                    console.log("error: "+response.error);
                }
            }
        });
    };
    setText = (text) => {
        var data = {
            type:"text",
            data:text +"\n"
        };
        this.dataPrinter.push(data);
    };
    openCash = () =>{
        var data = {
            type:"openpartial"
        };
        this.dataPrinter.push(data);
    };
    openCashPartial = () =>{
        var data = {
            type:"open"
        };
        this.dataPrinter.push(data);
    };
    setImage = (image) =>{
        var data = {
            type:"image",
            data:image
        };
        this.dataPrinter.push(data);
    };
    setQR = (qrDigits)=>{
        var data = {
            type:"qr",
            data:qrDigits
        };
        this.dataPrinter.push(data);
    };
    setImage = (pathImage,width = 600,height=200) =>{
        var data = {
            type:"img",
            data:pathImage,
            width:width,
            height:height
        };
        this.dataPrinter.push(data);
    };
    setConfigure = (align = "left",font="a",bold=false) => {
        var data = {
            type:"configure",
            align:align,
            typeFont:font,
            bold:bold
        };
        this.dataPrinter.push(data);
    };
    setBarCode = (code,typeBarCode = "CODE93") =>{
        var data = {
            type:"barcode",
            data:code,
            typeCode:typeBarCode
        };
        this.dataPrinter.push(data);
    };
    printerIn = (namePrinter) =>{
        return $.ajax({
            type: "POST",
            url: this.apiRouter+"command/" + namePrinter,
            data: JSON.stringify(this.dataPrinter),
            dataType: "json",
            success: function (response) {
                if(response.status == "OK"){
                    console.log("success");
                }else if(response.status == "ERROR"){
                    console.log("error: "+response.error);
                }
                this.dataPrinter = [];
            },error: error =>{
                console.log("error con el servidor");
                console.log(error);
                this.dataPrinter = [];
            }
        });
    };

}




const obtenerImpresoras = () => {
    var impresora = new PrinterEscPos();
    impresora.getPrinters().then(response =>{
        if(response.status == "OK"){
            response.listPrinter.forEach(namePrinter =>{
                console.log(namePrinter);
            });
        }
    });
};

const imprimirTicket = ()=>{
    var impresora = new PrinterEscPos();
    impresora.setText("hola mundo"); // metodo para imprimir texto
    impresora.setQR("123"); // metodo para imprimir codigos QR
    impresora.setBarCode("21","code93"); // metodo para imprimir codigo de barra tiene dos argumentos (codigo, tipo de codigo)
    impresora.setImage("image.png"); // metodo para imprimir imagenes al igual acepta enlaces de imagenes de internet
    impresora.setConfigure(
        font='a',
        bold= true,
        align= "center"
    ); // este metodo solo puede mandar 3 argumentos, para la fuente 'a' o 'b', letras negritas y la aliniacion del texto 'center','right','left'
    impresora.printerIn("lp0"); // una vez configurado el ticket pasamos a mandarlo a la impresora que deseamos imprimir el ticket
};