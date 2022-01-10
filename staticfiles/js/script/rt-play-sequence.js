define(['jquery' ], function ($) {
 $(document).ready(function () {
 console.log("chargement JS ajax-sequence.js OK");
        
        
function newWebSocket(url) {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + url;
  console.log("test de connexion : " + ws_path );
  ws=new WebSocket(ws_path);
    console.log("connexion au websocket ok...");
    console.log("state", ws.readyState);
  return ws;
};

ok=true;        
if ($("#sequence_id").val()!=undefined) {
    var sequenceId=$("#sequence_id").val();
}
else {ok=false;}
if ($("#user_id").val()!=undefined) {
    var anonymous=false;
	var userId= $("#user_id").val();
}
else if ($("#pseudo").val()!=undefined) { 
    var anonymous=true;
	var pseudo= $("#pseudo").val();
}
else {console.log("problème : page ouvert par un utilisateur non authentifié et sans pseudo");
      ok=false}
	
if (ok) {
socket=newWebSocket("/RT/Cons/");
socket.onopen = function () {
  console.log("Connected to socket");
  if (anonymous) {
     socket.send(JSON.stringify({
        "command":"connexionPA",
        "pseudo": pseudo,
        "sequenceId":sequenceId}));
     console.log("connexion anonyme envoyée");
}
 else {
  socket.send(JSON.stringify({
        "command":"connexionP",
        "userId":userId,
        "sequenceId":sequenceId}));
     console.log("connexion authentifiée envoyée");
 }
}   //socket onopen

socket.onmessage = function (message) {
      var data = JSON.parse(message.data);
      console.log("message recu :",data);
      if (data.error) {return;}
      if (data.type=="message")
          {document.getElementById("blocReponse").innerHTML=data.message;}
      };
	                                                                                  

}
})}); 
 
