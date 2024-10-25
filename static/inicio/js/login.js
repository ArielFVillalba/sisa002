

function ingresarlog(){
var usu = document.getElementById('username').value;
var psw = document.getElementById('password').value;
verusuario(usu ,psw);
}

function obtener_cookie_por_nombre(cookieName) {
  let cookie = {};
  document.cookie.split(';').forEach(function(el) {
    let [key,value] = el.split('=');
    cookie[key.trim()] = value;
  })
  return cookie[cookieName];
}

function cookie_usuario(){
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$.ajax({
    url: '/guardar_usuario/',
    type: 'POST',
    datatype: 'json',
    headers:{
        "X-CSRFToken": csrftoken
    },
    data: {
        'usuario': document.getElementById('username').value,
        'contraseña': document.getElementById('password').value
    },
    success: function(data) {
     ingreso(data.datos.usuario)
    }
});
}


function ingreso(estevalor) {
    valor=estevalor;
if (valor.valueOf()!=0){
    document.getElementById('msne').innerHTML=" Ingrerso a exitoso";
    document.getElementById('labusuario').innerHTML=valor;
    menuempresas();
}else {
  document.getElementById('msne').innerHTML=" usuario o clave incorrecta";
  document.cookie = "usuario=; max-age=0; path=/";
  document.cookie = "contraseña=; max-age=0; path=/";
}
}

function registrarse(){


}


