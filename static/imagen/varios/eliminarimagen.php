<?php
session_start();
include_once('../funciones/funcion.php');
if (funAutentificarusuario()=='true'){}



$did = trim($_GET["did"]);

if ($did ==""){$did =0;}
if ($did <=0){exit;}

echo  $SQL='select * from imagen where idimagen='.$did;
$campo='ext';
echo $ext= trim(Fun_BucarCampo($SQL,$campo));

 include('../conn/pg_connect.php'); 
 $consulta ='SELECT fc_eliminarimagen('.$did.');';
 $consulta= utf8_encode($consulta);
 $result = pg_query($consulta) ; 

 if (!$result) {  echo "An error occured.\n"; exit;	}
  $did = pg_fetch_result($result, 0, 0);
   logear($consulta,$did);
  include('../conn/pg_close.php');

if ($did <>0){ 
$directorio = $_SERVER['DOCUMENT_ROOT'].'/tresmarias/imagen/imagenes/'; 

unlink($directorio.$did.$ext);//sabiendo que estos son los parametros para tu caso  
}


?>