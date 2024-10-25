
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if (document.querySelector('#columnalst')) {
       $('.columnalst').css({'height':'30px'});
    // document.getElementById('labusuario').innerHTML=$(columnalst).width();
     if ($(columna).width()<1000){
        $('.columnalst').css({'height':'100px'});
        $('.columnalstt').css({'height':'80px'});

      }
}
}


function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(formatearcampos,2);
setTimeout(actcompelem(),1000);
cargarsucural();
busdetalle();
}

function actualizar_dep(){
var deposito = document.getElementById('id_deposito').value;
var sucursal = document.getElementById('id_sucursal').value;

valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/deposito_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'deposito': deposito,  'sucursal':sucursal},
    success: function(data) {

    if (data.success) {
        //Swal.fire(  '',  'El detalle ha sido actualizado.',  'success'  );
        nuevo()
        busdetalle()
        Swal.fire({  title: '',  text: 'ACTUALIZADO',
        icon: 'success',  customClass: {container: 'msnsuccess', }});
        } else {
        Swal.fire(  '',  'fallo.',  'success'   );

    }
      busdetalle();

  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus, errorThrown);
  }


});
}

}


function eliminar_dep(){
var deposito = document.getElementById('id_deposito').value;
  // Obtener el token CSRF de la cookie
  const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
  // Configurar el encabezado X-CSRFToken en la solicitud DELETE
  const headers = {'X-CSRFToken': csrftoken};
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, estoy seguro',
                cancelButtonText: 'No, cancelar'
            })
            .then((result) => {
                if (result.isConfirmed) {
                    fetch('/deposito/' + deposito + '/eliminar/', { method: 'DELETE', headers: headers  })
                    .then((response) => {
                    if (response.ok) {
                    nuevo()
                    busdetalle()
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                        Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                        Swal.fire({  title: '',  text: 'ERROR ',
                        icon: 'error',  customClass: {container: 'msnsuccess', }});

                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re
                    }}  // fin  if (result.isConfirmed) {
                    ) // fin del    .then((result) => {
}; //fin


function colorlistdo(){
const elementos = document.querySelectorAll('.columnalst');
e=1;  col='#D5F5E3';
elementos.forEach(elemento => {
  elemento.style.backgroundColor = col;
  e=e+1;
  if (e > 1 ){  if (e % 2 === 0) { col='#EAF2F8';   } else {  col='#D5F5E3';   }  }
});
}

function busdetalle(){
cargarsucural();

orden=0;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/deposito_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     success: function(data) {

     var list = data.datos;
     var html = '';

lin=0;
e=0;

for (var i = 0; i < list.length; i++) {
      var deposito = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#FCF3CF';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="columnalstd"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campo1"  > <input   id="deposito'+ e +'"  value="'+ deposito.deposito + '"</input> </div>';
      html += '<div class ="campo1" > <input id="sucursal'+ e +'" value="'+ deposito.sucursal + '"</input> </div>';
      html += '<div class ="campo1" ><button class="btnlstm" onClick="selectdep('+e+')"  >selecionar </button> </div>';
      html += '</div> ';
}

$('#deposito-list').html(html);
setTimeout(bloquearfilas,500);

}
});

}

function nuevo(){
document.getElementById('id_deposito').value="";
document.getElementById('id_sucursal').value="";
document.getElementById('id_deposito').focus();
}

function bloquearfilas(){

var valor=0
for (let i = 1; i < 200; i++) {
    const elemento = document.getElementById("deposito"+i);
    if (elemento) {
    valor=i+1;

    var ob="#deposito"+i;  $(''+ ob +'').prop('disabled', true);
    var ob="#sucursal"+i;  $(''+ ob +'').prop('disabled', true);

    } else {i=200;}
}

}
function selectdep(e){
document.getElementById('id_deposito').value=document.getElementById('deposito'+ e).value
document.getElementById('id_sucursal').value=document.getElementById('sucursal'+ e).value
}


function cargarcdep(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbdep/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbdep(obj);
    }
});
}

function cargarcombdep(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbdep/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbdep(obj);
    }
});
}

function crearcmbdep(list){
   // var values = [];\
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


function cargarsucural(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/sucursalesdep/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;

     crearcmbsucursal(obj);
    }
});
}


function crearcmbsucursal(list){
if(document.getElementById("sucursal_list")){
document.getElementById("sucursal_list").remove();
document.getElementById("id_sucursal").value="";
 }
if(document.getElementById("sucursal_list")){
      while (lista.firstChild) {
        lista.removeChild(lista.firstChild);
      }

}else{
var dataList = document.createElement('datalist');
dataList.id = "sucursal_list";
}

for (var i = 0; i < list.length; i++) {
  var sucursal = list[i];
     var option = document.createElement('option');
        option.setAttribute('id', sucursal.idsucursal);
        option.value = sucursal.sucursal;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList
    );
}


