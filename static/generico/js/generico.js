function inidep(){
setTimeout(busdep(),2);
setTimeout(busprov(),2);
}

function busdep(){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/busdep/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     console.log(data)
     crearcmbdep(data.datos);
    }
});
}
function busprov(){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/busprov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'usuario': usuario, 'contraseña':contraseña},
     success: function(data) {
     const obj = data.datos;
     console.log(data)
    crearcmbprov(data.datos);
    }
});
}
function crearcmbprov(list){
   // var values = [];
   var values =list
    var dataList = document.createElement('datalist');
    dataList.id = "porv_list";
     values.forEach(value =>{
        var option = document.createElement('option');
        option.innerHTML = value;
        option.value = value;
        dataList.appendChild(option);
    })
    document.body.appendChild(dataList);
}
function buscodprov(nombprov){
usuario = obtener_cookie_por_nombre("usuario")
contraseña = obtener_cookie_por_nombre("contraseña")
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/buscodprov/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken },
     data: { 'usuario': usuario, 'contraseña':contraseña,'nombprov':nombprov},
     success: function(data) {
     const obj = data.datos;
     document.getElementById('txtcodprov').value=data.datos+"";
    }
});
}
//------------------------------------------------------------------------
