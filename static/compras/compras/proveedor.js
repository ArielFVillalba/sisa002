
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if (document.querySelector('#columnalst')) {
    $('.columnalst').css({'height':'40px'});
    // document.getElementById('labusuario').innerHTML=$(columnalst).width();
     if ($(columna).width()<1000){
        $('.columnalst').css({'height':'100px'});
        $('.columnalstt').css({'height':'80px'});

      }
      }
}

function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(actcompelem(),1000);
document.getElementById('idbuscar').value="*";
}


function buscarproveedor(){
var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};

if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/proveedor/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{
variable=0;
var url = "/proveedor/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}


function proveedor_eliminar(pk) {
// Obtener el token CSRF de la cookie
  const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
  event.preventDefault(); // evita el envio del formulario
  // Configurar el encabezado X-CSRFToken en la solicitud DELETE
  const headers = {'X-CSRFToken': csrftoken};
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, estoy seguro',
                cancelButtonText: 'No, cancelar',
                customClass: {container: 'msnsuccess', }

            })
            .then((result) => {
                if (result.isConfirmed) {
                    fetch('/proveedor/' + pk + '/eliminar/',
                    {
                        method: 'DELETE',
                        headers: headers // Agregar el encabezado X-CSRFToken a la solicitud DELETE
                    })
                    .then((response) => {

                    // Manejar la respuesta de la petición DELETE
                    if (response.ok) {
                        // Si la eliminación fue exitosa, mostrar un mensaje de confirmación
                        Swal.fire({  title: '',  text: 'eliminado exitosamente ',
                         icon: 'success',  customClass: {container: 'msnsuccess', }});
                        document.location.href= "/proveedor/crear/";

                    } else {
                        // Si hubo un error al eliminar el artículo, mostrar un mensaje de error
                            Swal.fire({  title: '',  text: 'ERROR ',
                            icon: 'error',  customClass: {container: 'msnsuccess', }});
                    }// fin resultado ok eliminacino realizada restpuesta de servidor
                    }) // fin de respuesta eel servidor eliminado o no   .then((response) => {  re

                    }}  // fin  if (result.isConfirmed) {
                    ) // fin del    .then((result) => {

 }; //fin

function buscdatosprov(pk){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/prov_datos/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'pk': pk},
     success: function(data) {
     var list = data.datos;
     var proveedor = list[0];
     document.getElementById("id_ruc").value=proveedor.ruc;
     document.getElementById("id_timbrado").value=proveedor.timbrado;
     document.getElementById("id_idproveedor").value=proveedor.idproveedor;
    }
});
}

function crearcmbprov(list){
    var dataList = document.createElement('datalist');
    dataList.id = "porv_list";

for (var i = 0; i < list.length; i++) {
  var proveedor = list[i];
     //alert(proveedor.idproveedor );
    // alert(proveedor.nombre );
     var option = document.createElement('option');
        option.setAttribute('id', proveedor.idproveedor);
        option.value = proveedor.nombre;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList);
}


function codigoprov(val){
var lista = document.getElementById("porv_list");
var elementos = lista.getElementsByTagName("option");

Array.prototype.forEach.call(elementos, function(elemento) {
          if (elemento.value==val) {
             var input = document.getElementById("id_idproveedor");
             input.value = elemento.id;
             pk= elemento.id;
             buscdatosprov(pk);
           }
});
}

function busprov(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbprov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbprov(obj);
    }
});
}


function colorlistdo(){
const elementos = document.querySelectorAll('.columnalst');
e=1;  col='#D5F5E3';
elementos.forEach(elemento => {
  elemento.style.backgroundColor = col;
  e=e+1;
  if (e > 1 ){  if (e % 2 === 0) { col='#EAF2F8';   } else {  col='#D5F5E3';   }  }
});
}

function botones(var1 ,var2){

var ob="#guardar";  $(''+ ob +'').prop('disabled', var1);

}
