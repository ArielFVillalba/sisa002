
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
busdetalle();
}

function actualizar_tipomov(){
var tipomov = document.getElementById('id_tipomov').value;

valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajatipomov_editar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'tipomov': tipomov},
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


function eliminar_tipomov(){
var tipomov = document.getElementById('id_tipomov').value;
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
                    fetch('/cajatipomov/' + tipomov + '/eliminar/', { method: 'DELETE', headers: headers  })
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
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cajatipomov_listar/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken  },
     success: function(data) {

     var list = data.datos;
     var html = '';

lin=0;
e=0;

for (var i = 0; i < list.length; i++) {
      var cajatipomov = list[i];

      lin=lin+1;   e=i+1;  col='#D5F5E3';
      if (e > 1 ){  if (e % 2 === 0) { col='#FCF3CF';   } else {  col='#D5F5E3';   }  }
      html += '<div id= "lin0'+ lin +'" class ="columnalstd"  style="background-color:'+col+';"> ';
      html += '<div id= "lin'+ lin +'"  class ="detallelinea1"> ';
      html += '<div class ="campo1"  > <input   id="tipomov'+ e +'"  value="'+ cajatipomov.tipomov + '"</input> </div>';
      html += '<div class ="campo1" ><button class="btnlstdet" onClick="selectdep('+e+')"  >selecionar </button> </div>';
      html += '</div> ';
}

$('#cajatipomov-list').html(html);
setTimeout(bloquearfilas,500);

}
});

}

function nuevo(){
document.getElementById('id_tipomov').value="";
document.getElementById('id_tipomov').focus();
}

function bloquearfilas(){

var valor=0
for (let i = 1; i < 200; i++) {
    const elemento = document.getElementById("tipomov"+i);
    if (elemento) {
    valor=i+1;

    var ob="#tipomov"+i;  $(''+ ob +'').prop('disabled', true);

    } else {i=200;}
}

}
function selectdep(e){
document.getElementById('id_tipomov').value=document.getElementById('tipomov'+ e).value


}


function cargarctipomov(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbtipomov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbtipomov(obj);
    }
});
}

function cargarcombtipomov(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbcajatipomov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbtipomov(obj);
    }
});
}

function crearcmbtipomov(list){
   // var values = [];
   var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "cajatipomov-list";
    values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}


