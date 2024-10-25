$(window).resize(function(){
actcompelemcompa();
});

function actcompelemcompa(){

if (document.querySelector('#columnalst')) {
     $('.columnalst').css({'height':'35px'});
    // document.getElementById('labusuario').innerHTML=" list "+ $(columnalst).width();
     if ($(columnalst).width()<1000){
        $('.columnalst').css({'height':'70px'});
     }
}

var elemento = document.getElementById('detallelinea0');
if (elemento !== null) {
        $('.detallelinea0').css({'height':'30px'});
     if ($(columna0).width()<800 ){
         $('.detallelinea0').css({'height':'70px'});
     }
}
}

function funcompcab(){
cargarcombos();
}


function cargarcombos(){
setTimeout(cargaricombos,2);
}

function cargaricombos(){
//cargarcombdep();
//cargarcombserie();
//cargarcombdocumentos();

}


function cargarcombserie(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/caja_cmbserie/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbserie(obj);
    }
});
}

function crearcmbserie(list){
   // var values = [];\
    var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "serie_list";
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}

function cargarcombdocumentos(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/caja_cmbdocumentos/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbdocumentos(obj);
    }
});
}

function crearcmbdocumentos(list){
    var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "documentos_list";
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}
