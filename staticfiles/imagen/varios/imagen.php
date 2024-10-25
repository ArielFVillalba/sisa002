<?php  
session_start();
include_once('../funciones/funcion.php');
if (funAutentificarusuario()=='true'){ };
if ($idcodtabla=="" or $idcodtabla==0) {$idcodtabla = "".trim($_GET["idcodtabla"])."";}
if ($idcodtabla ==""){ $idcodtabla = 0;}
if ($idtabla=="" or $idtabla==0) {$idtabla = "".trim($_GET["idtabla"])."";}
if ($idtabla ==""){ $idtabla = 0;}
if ($n=="" or $n==0) {$n = "".trim($_GET["n"])."";}
if ($n ==""){ $n = 1;}
////
//$idcodtabla =108;
//$idtabla =10;

$ext='""';
$nombrefoto='""';
$idfoto='""';

$SQL='select * from imagen where idcodtabla='.$idcodtabla.' and idtabla='.$idtabla;
$campo='idimagen';
 $idfoto= trim(Fun_BucarCampo($SQL,$campo));
$SQL='select * from imagen where idcodtabla='.$idcodtabla.' and idtabla='.$idtabla;
$campo='nombre';
$nombrefoto= trim(Fun_BucarCampo($SQL,$campo));
$SQL='select * from imagen where idcodtabla='.$idcodtabla.' and idtabla='.$idtabla;
$campo='ext';
 $ext= trim(Fun_BucarCampo($SQL,$campo));
//$urlfoto='../imagen/imagenes/53.jpg';
$urlfoto='../imagen/imagenes/'.$idfoto. $ext;
if ($nombrefoto==''){$nombrefoto=  "";};
if ($idfoto==""){ $urlfoto='../imagen/imagenes/ima0.GIF';};

echo ' <table width="150" border="0"  cellpadding="0"> ';	
echo ' <tr>  <td colspan="2" align="center">&nbsp;</td>  </tr>';
echo ' <tr>  <td colspan="2" align="center">&nbsp;</td>  </tr>';
echo ' <tr> ';
echo ' <td colspan="2" align="center" >';
echo ' <div id="fotos">';
echo ' <img src="'.$urlfoto.'" width="144px" height="150px">';
echo ' </div> </td>  </tr> ';

echo ' <tr>';
echo ' <td colspan="2" align="center">';
echo ' <label>'.$nombrefoto.'</label> ';
echo ' </td>';
echo ' </tr>';

echo ' <tr>  <td colspan="2" align="center">&nbsp;</td>  </tr>';
if ($idfoto==0){

echo ' <td colspan="2" align="center">';
echo ' <div id="upload'.$n.'" ><span>subir imagen<span></div><span id="status" ></span>';
echo ' </td>';
}
if ($idfoto<>0){
echo ' <td colspan="2" align="center">';
echo ' <button type="button" ';
echo ' name="btnsubirimagen" ';
echo ' onClick="Eliminarimagen('.$idfoto.');"';
echo ' onKeyPress="'.keypres($x).'"';
echo ' class="boton boton-'.$colboton.'">';
echo ' <span class="borde-h">';
echo ' <span class="borde-v">';
echo ' <span class="brillo">';
echo ' <span> Eliminar Imagen  </span>';
echo ' </span>';
echo ' </span> ';
echo ' </span>';
echo ' </button>';
echo ' </td>';
}
echo ' </table>';

?> 
