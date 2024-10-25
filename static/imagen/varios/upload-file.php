<?php
session_start();
include_once('../funciones/funcion.php');
if (funAutentificarusuario()=='true'){}
$idcodtabla =$_GET["didentidad"];
$idtabla =$_GET["codigo"];

//$idcodtabla =108;
//$idtabla =10;
$error=0;

if ($didimagen=="" or $didimagen==0) {$didimagen = "".trim($_GET["didimagen"])."";}
if ($didimagen ==""){ $didimagen = 0;}

if ($idtabla ==""){$idtabla =0;}
if ($idcodtabla ==""){$idcodtabla =0;}


//Definimos la variable $max para establecer el l�mite m�ximo de tama�o del archivo.
$max=1500000;// (1.5Mb)
//Ahora ordenamos donde se almacenar� la imagen, hemos decidido que se cree un nuevo directorio dentro de la carpeta que hemos creado en el root de nuestro hosting para contener todas las subidas. Con la funci�n mkdir creamos el directorio el cual lo nombramos con la fecha de subida del archivo y el nombre de la imagen. 
$nombreclean=htmlspecialchars($email);// (htmlspecialchars, esteriliza el texto del campo "nombre" eliminando los caracteres que pudieran ejecutar alg�n script malicioso en nuestro servidor).
$hh=date("H")+8;
$hora = date("d-m-Y $hh:i:s"); 
$directorio = $_SERVER['DOCUMENT_ROOT'].'/frama/imagen/imagenes/'; 

$file =$uploaddir.basename($_FILES['uploadfile']['name']); 
//A continuaci�n tratamos el archivo de imagen, aplicando unas funciones en particular como medida de seguridad.
$filesize = $_FILES['uploadfile']['size'];
$filename = trim($_FILES['uploadfile']['name']); //(trim elimina los posibles espacios al final y al principio del nombre del archivo)
$tama= strlen($filename);
$ini=$tama-4;
$fin=$tama;
$ext =substr($filename, $ini,$fin);
//$filename = substr($filename, -20); //(con substr le decimos que coja solamente los �ltimos 20 caracteres por si el nombre fuera muy largo) 
//$filename = str_replace(" ", "", $filename); //(con esta funci�n eliminamos posibles espacios entre los caracteres del nombre) 
//Ahora creamos las condiciones que debe cumplir el archivo antes de ser almacenado en el servidor. Restringimos a .jpg � .gif (tanto en mayusculas como en min�sculas) y finalmente cambiamos el archivo de la carpeta temporal a la final elegida.
 
$error=0;
if($filesize > $max){$error=1;}
if($filesize <= 0){$error=2;}

if((".jpg"==$ext) || (".gif"== $ext) || (".JPG"== $ext)|| (".GIF"==$ext)){ $error=0; } else {$error=3;}
if(($idtabla ==0 ) || ($idcodtabla ==0 )){$error=4;}

include('../conn/pg_connect.php'); 
$filename2='\''.$filename.'\'';
$directorio2 ='\''.$directorio.'\'';
$descripcion2='\''.$descripcion.'\'';
$ext2='\''.$ext.'\'';
if($error == 0){
$consulta='SELECT fc_actualizarimagen('.$_SESSION['idAdmin'].','.$didimagen.','.$idtabla .','.$idcodtabla .','.$directorio2.','.$filename2.','.$descripcion2.','.$ext2.','.$_SESSION['idempresa'].','.$_SESSION['idperiodo'].','.$_SESSION['idsucursal'].','.$_SESSION['idcetrocosto'].');';

$consulta= utf8_encode($consulta);
$result = pg_query($consulta) ; 

if (!$result) { echo "An error occured.\n"; exit;	}
$did = pg_fetch_result($result, 0, 0);
logear($consulta,$did);
include('../conn/pg_close.php');
$uploadfile= $directorio.$did.$ext;
//$uploadfile= $directorio.$filename;
if (move_uploaded_file($_FILES['uploadfile']['tmp_name'], $uploadfile)) { 
echo "success"; 
} else {
echo "error";
}

}

?>