
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
busdetallefp();
}

function actualizar_cajaformapago(){
var formadepago = document.getElementById('id_formadepago').value;
valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajaformadepago_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'formadepago': formadepago},
    success: function(data) {

            if (data.success) {
                //Swal.fire(  '',  'El detalle ha sido actualizado.',  'success'  );
                nuevo()
                busdetallefp()
                Swal.fire({  title: '',  text: 'ACTUALIZADO',
                icon: 'success',  customClass: {container: 'msnsuccess', }});
                } else {
                Swal.fire(  '',  'fallo.',  'success'   );

            }
              busdetallefp();

          },
          error: function(jqXHR, textStatus, errorThrown) {
            console.log(textStatus, errorThrown);
          }


});
}

}



function eliminar_cajaformapago(){
var formadepago = document.getElementById('id_formadepago').value;
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
                    fetch('/cajaformadepago/' + formadepago + '/eliminar/', { method: 'DELETE', headers: headers  })
                    .then((response) => {
                    if (response.ok) {
                    nuevo()
                    busdetallefp()
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

function busdetallefp(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajaformadepago_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     success: function(data) {

     var list = data.datos;
     var html = '';

lin=0;
e=0;

for (var i = 0; i < list.length; i++) {
      var cajaformapago = list[i];
      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#FCF3CF';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="columnalstd"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campo1"  > <input   id="formadepago'+ e +'"  value="'+ cajaformapago.formadepago + '"</input> </div>';
      html += '<div class ="campo1" ><button class="btnlstdet" onClick="selectfp('+e+')"  >selecionar </button> </div>';
      html += '</div> ';
}

$('#cajaformapago-list').html(html);
setTimeout(bloquearfilas,500);

}
});

}

function nuevo(){
document.getElementById('id_formadepago').value="";
document.getElementById('id_formadepago').focus();
}

function bloquearfilas(){

var valor=0
for (let i = 1; i < 200; i++) {
    const elemento = document.getElementById("formadepago"+i);
    if (elemento) {
    valor=i+1;

    var ob="#formadepago"+i;  $(''+ ob +'').prop('disabled', true);

    } else {i=200;}
}

}
function selectfp(e){
document.getElementById('id_formadepago').value=document.getElementById('formadepago'+ e).value


}


function cargarcmbformapago(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbcajaformadepago/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbcajaformapago(obj);
    }
});
}

function crearcmbcajaformapago(list){
   // var values = [];
   var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "formadepago-list";
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}


