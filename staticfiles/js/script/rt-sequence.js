define(['jquery'], function ($) {
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
        
var sequenceId=$("#sequence_id").val();

var socket=newWebSocket('/RT/Cons/');
socket.onopen = function () {
       console.log("Connected to socket");
       socket.send(JSON.stringify({
       "command":"connexionOrgTdb",
	   "sequenceId": sequenceId })); 
};

var lastAct=-10;
chAct=function() {
	console.log("changement d'activité");
	newAct=$("#activity_id").val();
	if (newAct != lastAct)
	  {socket.send(JSON.stringify({
		"command":"chAct",
	    "activityId" : newAct }))
      };
      };

// Handle incoming messages                                              
socket.onmessage = function (message) {
     var data = JSON.parse(message.data); 
     // Handle errors                                                                        
    if (data.error) {
	console.log("erreur reception des données");
	return;}
    console.log("recu :",data);
    if (data.command=="connexionPA"){
	// connexion d'un participant anonyme
	
		console.log("participant anonyme connecté", data.pseudo);
		t=document.getElementById("table_participants");
		//insertion du participant dans le tableau à sa place alphabetique
		ligne=document.createElement("tr");
		ligne.setAttribute("id",data.channel_name);
		col1=document.createElement("td");
		col1.innerHTML=data.pseudo;
		ligne.appendChild(col1);
		ligne.appendChild(document.createElement("td"));
		console.log(ligne) 
		i=2; // les deux premières lignes du tableau sont hors sujet
		while (i<t.childNodes.length &&
			   (data.pseudo>t.childNodes[i].childNodes[0].innerHTML))
		  {i=i+1;}
		if (i==t.childNodes.length)
		{t.append(ligne);}  
		else {t.insertBefore(ligne,t.childNodes[i]);}   
		personne=$('#personne');
		if (t.childNodes.length>2)
		  {personne.addClass("no_visu_on_load");}
		else 
		 {personne.removeClass("no_visu_on_load");}
		} // fin connexion anonyme
	
	else if (data.command=="deconnexionPA") {
        t=document.getElementById("table_participants");
        i=2;
        console.log("deconnexion du participant de channel : ",data.channel_name);
        while (i<t.childNodes.length){
			if (t.childNodes[i].id==data.channel_name)
			    {t.removeChild(t.childNodes[i]); }
			i++;    
			}
		if (t.childNodes.length>2)
		  {personne.addClass("no_visu_on_load");}
		else 
		 {personne.removeClass("no_visu_on_load");}
		
    }
    else if (data.command=="connexionP"){// conexion d'un participant authentifié
	console.log("participant "+data.user.fname+" "+data.user.lname);
	t=document.getElementById("table_participants");
	//insertion du participant dans le tableau à sa place alphabetique
	ligne=document.createElement("tr");
	i=0;
	while (i<t.childNodes.length &&
	       (data.user.lname>t.childNodes[i].lname
		|| (data.user.lname=t.ChildNodes[i].lname && data.user.fname>t.ChildNodes[i].fname)))
	{i=i+1;}
	t.appendChild(ligne);
	for (j=i;j<t.childNodes.length;j++) {
	    t.childNodes[i+1]=t.childNodes[i];
	    }
	t.childNodes[i]=ligne;
    }
}

  
})});
 
