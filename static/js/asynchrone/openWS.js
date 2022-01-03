//ouverture d'un websocket
//appeler window.socket=newWebSocket("/qcm/tableau") par ex.


function newWebSocket(url) {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + url;
  console.log("test de connexion : " + ws_path );
  ws=new WebSocket(ws_path);
  console.log("connexion au websocket ok...");
  return ws;
};

//envoie d'un message, s=socket, data=dictionnaire
//function postMessage(s,commande,data)
    
