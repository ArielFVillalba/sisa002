

function selecempresa(){
didempresa=document.getElementById("id_empresa").value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/sucursales/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'idempresa': didempresa},
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


