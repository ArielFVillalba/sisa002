

function infinv01(inf){
var valida=true;
var nrotoma = document.getElementById('txtnrotoma').value;
if (nrotoma.length==0){valida=0; alert("CARGAR NRO TOMA"); }

if (valida==true){
usuario = obtener_cookie_por_nombre("usuario");
contraseña = obtener_cookie_por_nombre("contraseña");

let opt = $('input[name="optfinvin"]:checked').val();
var tipoinf=inf;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
     url: "/inf_inv_001/",    type: 'POST',    datatype: 'json',    headers:{ "X-CSRFToken": csrftoken    },
     data: {  'nrotoma': nrotoma, 'opt': opt},
     success: function(data) {
     const obj = data.datos;
     stabla_lstinv001(data.datos);
     }
});
}
}

