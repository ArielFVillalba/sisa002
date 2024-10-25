function createREQ() {
try {
     req = new XMLHttpRequest(); /* p.e. Firefox */
     } catch(err1) {
       try {
       req = new ActiveXObject('Msxml2.XMLHTTP'); /* algunas versiones IE */
       } catch (err2) {
         try {
         req = new ActiveXObject("Microsoft.XMLHTTP"); /* algunas versiones IE */
         } catch (err3) {
          req = false;
         }
       }
     }
     return req;
}
function requestGET(url, query, req) {
myRand=parseInt(Math.random()*99999999);
req.open("GET",url+'?'+'query'+'&rand='+myRand,true);
req.send(null);
}
function requestPOST(url, query, req) {
req.open("POST",url,true);
req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
req.send(query);
}
function doCallback(callback,item) {
eval(callback + '(item)');
}

function doAjax(url,query,callback,reqtype,getxml) {
// crea la instancia del objeto XMLHTTPRequest 

var myreq = createREQ();

myreq.onreadystatechange = function() {
if(myreq.readyState == 4) {
   if(myreq.status == 200) {
      var item = "";
      if(getxml==0) {
	        item = myreq.responseText;	
      }
      if(getxml==1) {
         item = myreq.responseXML;
      }
      doCallback(callback, item);
    }
  }
}
if(reqtype=='post') {

requestPOST(url,query,myreq);
} else {
requestGET(url,query,myreq);
}
}



