function procesar(){
$('#retfiltro').css({'display':'none'});
$('#btnexport').css({'display':'none'});


if ($.fn.DataTable.isDataTable('#movdeplst')) {
    $('#movdeplst').DataTable().destroy();
}

if (document.querySelector('#id_fecha')) {
if  ((document.getElementById('id_fecha').value).length==0 ){document.getElementById('id_fecha').valueAsDate = new Date();}
}
if (document.querySelector('#id_fechaini')) {
if  ((document.getElementById('id_fechaini').value).length==0 ){document.getElementById('id_fechaini').valueAsDate = new Date();}
}
if (document.querySelector('#id_fechafin')) {
if  ((document.getElementById('id_fechafin').value).length==0 ){document.getElementById('id_fechafin').valueAsDate = new Date();}
}


}

function cargarcombos(){ cargarcdep();  }
function buscdatosartcod(event){
if (event.keyCode == 13 ||  event.keyCode === 32 ) {  buscdatosart();}
}

function retornlist(){
$('#btnexport').css({'display':'none'});
$('#retfiltro').css({'display':'none'});
$('#retorno').css({'display':'block'});
$('#menufiltro').css({'display':'block'});

if ($.fn.DataTable.isDataTable('#movdeplst')) {
      $('#movdeplst').DataTable().destroy();
      $('#movdeplst').css({'display':'none'});


 }
}

function listadoexport(web){
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var depentrada = document.getElementById('depentrada').value;
var depsalida = document.getElementById('depsalida').value;

var opciones = document.getElementsByName('optinforme');
if (opciones[0].checked) { tipolist="general";};
if (opciones[1].checked) { tipolist="detallado";};

pag="";
if (tipolist=="general"){

if (web=="pdf"){ pag="/movdepcabinfpdf/";  }
if (web=="excel"){ pag="/movdepcabinfexcel/"; }
if (web=="csv"){ pag="/movdepcabinfcsv/"; }
if (web=="imp"){ pag="/movdepcabinfimp/"; }
};
if (tipolist=="detallado"){
if (web=="pdf"){ pag="/movdepdetinfpdf/"; }
if (web=="excel"){ pag="/movdepdetinfexcel/"; }
if (web=="csv"){ pag="/movdepdetinfcsv/"; }
if (web=="imp"){ pag="/movdepcabinfimp/"; }
};

valida=true;
if (valida==true){
//usuario = obtener_cookie_por_nombre("usuario");
//contraseña = obtener_cookie_por_nombre("contraseña");
var myData = {
fechaini:fechaini,
fechafin:fechafin,
depsalida:depsalida,
depentrada:depentrada
};

// Encode the data as URL parameters
var params = Object.keys(myData).map(function(key) {
  return encodeURIComponent(key) + '=' + encodeURIComponent(myData[key]);
}).join('&');

// Define the URL of the new page, including the encoded parameters
var url = pag+'?' + params;

// Open the new page in a new window
//window.open(url);
window.location.href = url;
}
}


function listadomovdep(web){
if (web=="web"){
$('#menufiltro').css({'display':'none'});
$('#retorno').css({'display':'none'});
$('#informe').css({'display':'block'});
$('#btnexport').css({'display':'block'});
$('#retfiltro').css({'display':'block'});
$('#movdeplst').css({'display':'block'});

}
var fechaini = document.getElementById('id_fechaini').value;
var fechafin = document.getElementById('id_fechafin').value;
var depsalida = document.getElementById('depsalida').value;
var depentrada = document.getElementById('depentrada').value;
var opciones = document.getElementsByName('optinforme');
if (opciones[0].checked) { tipolist="general";};
if (opciones[1].checked) { tipolist="detallado";};


if (web=="web" && tipolist=="general"){ pag="/movdepcabinf_listar/"; }
if (web=="web" && tipolist=="detallado"){ pag="/movdepdetinf_listar/"; }

valida=true;
if (valida==true){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: pag,  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'fechaini': fechaini,'fechafin': fechafin,'depsalida': depsalida,'depentrada': depentrada },
     success: function(data) {
     var list = data.datos;
     if (web=="web" && tipolist=="general"){ listarmovdep(list);   }
     if (web=="web" && tipolist=="detallado") { listarmovdepdet(list);}

}});
}
}

function listarmovdep(list){
lin=0;
e=0;
    var html = '';
    if ($.fn.DataTable.isDataTable('#movdeplst')) {
        $('#movdeplst').DataTable().destroy();
    }
html+=' <thead>  <tr> ';
html+=' <th>fecha</th> <th>NRO MOV </th> <th>DEP SALIDA</th> <th>DEP ENTRADA </th>  ';
html+=' </tr> </thead>   ';

html+=' <tbody>  ';
for (var i = 0; i < list.length; i++) {
var movdep = list[i];
html+=' <tr> ';
html+=' <th>'+ movdep.fecha  +'</th> <th>'+ movdep.nromov +'</th>';
html+=' <th>'+ movdep.depsalida +'</th><th>'+ movdep.depentrada +'</th>';
html+=' </tr>   ';
}
html+='</tbody>   ';

$('#movdeplst').html(html);
$('#movdeplst').DataTable({
lengthMenu:[20],
searching: false,
columnDefs:[
    {orderable: false, target:[1,3]},
    {width: "15%", target:[0,1,3]},
    {width: "20%", target:[2]},
],

responsive: true,
language:espanol,
});
}


function listarmovdepdet(list){
lin=0;
e=0;
    var html = '';
    if ($.fn.DataTable.isDataTable('#movdeplst')) {
        $('#movdeplst').DataTable().destroy();
    }

var html = '';

html+=' <thead>  <tr> ';
html+=' <th>fecha</th> <th>NRO MOV </th>  <th>orden</th> <th>codigo </th> ';
html+=' <th>descripcion</th> <th>cantidad</th> <th> DEP SALIDA</th> <th>DEP ENTRADA </th> ';

html+=' </tr> </thead>   ';

html+=' <tbody>  ';
for (var i = 0; i < list.length; i++) {
var movdep = list[i];
html+=' <tr> ';

html+=' <th>'+ movdep.fecha +'</th> <th>'+ movdep.nromov +'</th>';
html+=' <th>'+ movdep.orden +'</th>';
html+=' <th>'+ movdep.codigo +'</th><th>'+ movdep.descripcion +'</th>';
html+=' <th>'+ movdep.cantidad +'</th><th>'+ movdep.depsalida +'</th>';
html+=' <th>'+ movdep.depentrada +'</th>';
html+=' </tr>   ';
}
html+='</tbody>   ';

$('#movdeplst').html(html);
$('#movdeplst').DataTable({
lengthMenu:[20],
searching: false,
columnDefs:[
    {orderable: false, target:[1,3,4]},
    {width: "8%", target:[0,2,5,6,7]},
    {width: "15%", target:[1,3,4]},
],

responsive: true,
language:espanol,
});
$('#movdeplst th').css({'font-size':'12px'});
$('#movdeplst thead th').css({'font-size':'12'});
$('#container').css({'width':'100%'});

}



function crearcmbtipodlist(){
   var values = ["totalizado","detallado"];
     //document.getElementById("id_tipolist").value="factura";
        var dataList = document.createElement('datalist');
        dataList.id = "tipolist_list";
        values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}




var espanol={
    "processing": "Procesando...",
    "lengthMenu": "Mostrar _MENU_ registros",
    "zeroRecords": "No se encontraron resultados",
    "emptyTable": "Ningún dato disponible en esta tabla",
    "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
    "infoFiltered": "(filtrado de un total de _MAX_ registros)",
    "search": "Buscar:",
    "infoThousands": ",",
    "loadingRecords": "Cargando...",
    "paginate": {
        "first": "Primero",
        "last": "Último",
        "next": "Siguiente",
        "previous": "Anterior"
    },
    "aria": {
        "sortAscending": ": Activar para ordenar la columna de manera ascendente",
        "sortDescending": ": Activar para ordenar la columna de manera descendente"
    },
    "buttons": {
        "copy": "Copiar",
        "colvis": "Visibilidad",
        "collection": "Colección",
        "colvisRestore": "Restaurar visibilidad",
        "copyKeys": "Presione ctrl o u2318 + C para copiar los datos de la tabla al portapapeles del sistema. <br \/> <br \/> Para cancelar, haga clic en este mensaje o presione escape.",
        "copySuccess": {
            "1": "Copiada 1 fila al portapapeles",
            "_": "Copiadas %ds fila al portapapeles"
        },
        "copyTitle": "Copiar al portapapeles",
        "csv": "CSV",
        "excel": "Excel",
        "pageLength": {
            "-1": "Mostrar todas las filas",
            "_": "Mostrar %d filas"
        },
        "pdf": "PDF",
        "print": "Imprimir",
        "renameState": "Cambiar nombre",
        "updateState": "Actualizar",
        "createState": "Crear Estado",
        "removeAllStates": "Remover Estados",
        "removeState": "Remover",
        "savedStates": "Estados Guardados",
        "stateRestore": "Estado %d"
    },
    "autoFill": {
        "cancel": "Cancelar",
        "fill": "Rellene todas las celdas con <i>%d<\/i>",
        "fillHorizontal": "Rellenar celdas horizontalmente",
        "fillVertical": "Rellenar celdas verticalmentemente"
    },
    "decimal": ",",
    "searchBuilder": {
        "add": "Añadir condición",
        "button": {
            "0": "Constructor de búsqueda",
            "_": "Constructor de búsqueda (%d)"
        },
        "clearAll": "Borrar todo",
        "condition": "Condición",
        "conditions": {
            "date": {
                "after": "Despues",
                "before": "Antes",
                "between": "Entre",
                "empty": "Vacío",
                "equals": "Igual a",
                "notBetween": "No entre",
                "notEmpty": "No Vacio",
                "not": "Diferente de"
            },
            "number": {
                "between": "Entre",
                "empty": "Vacio",
                "equals": "Igual a",
                "gt": "Mayor a",
                "gte": "Mayor o igual a",
                "lt": "Menor que",
                "lte": "Menor o igual que",
                "notBetween": "No entre",
                "notEmpty": "No vacío",
                "not": "Diferente de"
            },
            "string": {
                "contains": "Contiene",
                "empty": "Vacío",
                "endsWith": "Termina en",
                "equals": "Igual a",
                "notEmpty": "No Vacio",
                "startsWith": "Empieza con",
                "not": "Diferente de",
                "notContains": "No Contiene",
                "notStartsWith": "No empieza con",
                "notEndsWith": "No termina con"
            },
            "array": {
                "not": "Diferente de",
                "equals": "Igual",
                "empty": "Vacío",
                "contains": "Contiene",
                "notEmpty": "No Vacío",
                "without": "Sin"
            }
        },
        "data": "Data",
        "deleteTitle": "Eliminar regla de filtrado",
        "leftTitle": "Criterios anulados",
        "logicAnd": "Y",
        "logicOr": "O",
        "rightTitle": "Criterios de sangría",
        "title": {
            "0": "Constructor de búsqueda",
            "_": "Constructor de búsqueda (%d)"
        },
        "value": "Valor"
    },
    "searchPanes": {
        "clearMessage": "Borrar todo",
        "collapse": {
            "0": "Paneles de búsqueda",
            "_": "Paneles de búsqueda (%d)"
        },
        "count": "{total}",
        "countFiltered": "{shown} ({total})",
        "emptyPanes": "Sin paneles de búsqueda",
        "loadMessage": "Cargando paneles de búsqueda",
        "title": "Filtros Activos - %d",
        "showMessage": "Mostrar Todo",
        "collapseMessage": "Colapsar Todo"
    },
    "select": {
        "cells": {
            "1": "1 celda seleccionada",
            "_": "%d celdas seleccionadas"
        },
        "columns": {
            "1": "1 columna seleccionada",
            "_": "%d columnas seleccionadas"
        },
        "rows": {
            "1": "1 fila seleccionada",
            "_": "%d filas seleccionadas"
        }
    },
    "thousands": ".",
    "datetime": {
        "previous": "Anterior",
        "next": "Proximo",
        "hours": "Horas",
        "minutes": "Minutos",
        "seconds": "Segundos",
        "unknown": "-",
        "amPm": [
            "AM",
            "PM"
        ],
        "months": {
            "0": "Enero",
            "1": "Febrero",
            "10": "Noviembre",
            "11": "Diciembre",
            "2": "Marzo",
            "3": "Abril",
            "4": "Mayo",
            "5": "Junio",
            "6": "Julio",
            "7": "Agosto",
            "8": "Septiembre",
            "9": "Octubre"
        },
        "weekdays": [
            "Dom",
            "Lun",
            "Mar",
            "Mie",
            "Jue",
            "Vie",
            "Sab"
        ]
    },
    "editor": {
        "close": "Cerrar",
        "create": {
            "button": "Nuevo",
            "title": "Crear Nuevo Registro",
            "submit": "Crear"
        },
        "edit": {
            "button": "Editar",
            "title": "Editar Registro",
            "submit": "Actualizar"
        },
        "remove": {
            "button": "Eliminar",
            "title": "Eliminar Registro",
            "submit": "Eliminar",
            "confirm": {
                "_": "¿Está seguro que desea eliminar %d filas?",
                "1": "¿Está seguro que desea eliminar 1 fila?"
            }
        },
        "error": {
            "system": "Ha ocurrido un error en el sistema (<a target=\"\\\" rel=\"\\ nofollow\" href=\"\\\">Más información&lt;\\\/a&gt;).<\/a>"
        },
        "multi": {
            "title": "Múltiples Valores",
            "info": "Los elementos seleccionados contienen diferentes valores para este registro. Para editar y establecer todos los elementos de este registro con el mismo valor, hacer click o tap aquí, de lo contrario conservarán sus valores individuales.",
            "restore": "Deshacer Cambios",
            "noMulti": "Este registro puede ser editado individualmente, pero no como parte de un grupo."
        }
    },
    "info": "Mostrando _START_ a _END_ de _TOTAL_ registros",
    "stateRestore": {
        "creationModal": {
            "button": "Crear",
            "name": "Nombre:",
            "order": "Clasificación",
            "paging": "Paginación",
            "search": "Busqueda",
            "select": "Seleccionar",
            "columns": {
                "search": "Búsqueda de Columna",
                "visible": "Visibilidad de Columna"
            },
            "title": "Crear Nuevo Estado",
            "toggleLabel": "Incluir:"
        },
        "emptyError": "El nombre no puede estar vacio",
        "removeConfirm": "¿Seguro que quiere eliminar este %s?",
        "removeError": "Error al eliminar el registro",
        "removeJoiner": "y",
        "removeSubmit": "Eliminar",
        "renameButton": "Cambiar Nombre",
        "renameLabel": "Nuevo nombre para %s",
        "duplicateError": "Ya existe un Estado con este nombre.",
        "emptyStates": "No hay Estados guardados",
        "removeTitle": "Remover Estado",
        "renameTitle": "Cambiar Nombre Estado"
    }
}





