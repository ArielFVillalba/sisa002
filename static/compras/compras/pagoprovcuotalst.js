$(window).resize(function(){
actcompelemcomp();
});
function actcompelemcomp(){
colorlistdo();

if (document.querySelector('#columnalst')) {
     $('.columnalst').css({'height':'35px'});
     if ($(columnalst).width()<1000){
        $('.columnalst').css({'height':'70px'});

     }
}

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
