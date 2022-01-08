define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
 $(document).ready(function () {
  console.log("chargement JS ajax-sequence.js OK");
        
        
var socket=newWebSocket('/RT/Cons/');
window.socket.onopen = function () {
       console.log("Connected to socket");
       socket.send(JSON.stringify({
       "command":"connexion_org_tdb",
	   "sequence": {{ sequence.id }} }));
};		  

$("body").on('change', '#activity_running' , function () { 
	console.log("changement d'activité");
	socket.send(JSON.stringify({
		"command":"changeActivity",
		"activity_id" : activity_id}));
		
});
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
	console.log("participant anonyme connecté");
	t=document.getElementById("table_participants");
	//insertion du participant dans le tableau à sa place alphabetique
	ligne=document.createElement("tr");
	col1=document.createElement("td");
	col1.innerHTML=data.from;
	ligne.appendChild(col1);
	i=0;
	while (i<t.childNodes.length &&
	       (data.pseudo>t.childNodes[i].pseudo))
	{i=i+1;}
	t.appendChild(ligne);
	for (j=i;j<t.childNodes.length;j++) {
	    t.childNodes[i+1]=t.childNodes[i];
	    }
	t.childNodes[i]=ligne;
	if (t.childNodes.length==1)
	  {personne=$('#personne');
	   personne.addClass("no_visu_on_load");
	  }
	
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
  
)});	    
 
