from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Connexion,Resultat
from sequence.models import Sequence,Play 
from account.models import User
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from datetime import datetime

printc=print

@database_sync_to_async
def get_play_by_id(id):
    "le play à partir de son id"
    try :
        q=Play.objects.get(id=id)
        return q
    except :
        printc("play ",id," non trouvée en bdd")
        return None

@database_sync_to_async
def get_sequence_by_id(id):
    "la sequence à partir de son id"
    try :
        q=Sequence.objects.get(id=id)
        return q
    except :
        printc("sequence ", id," non trouvée en bdd")
        return None
@database_sync_to_async
def get_activity_by_rank(seq,r):
    "l'activité à partir de la sequence et le rang"
    try :
        q=Activity(sequence=seq,ranking=r)
        return q
    except :
        printc("activite de rang ", r," non trouvée dans la sequence",seq)
        return None

class Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        printc("ouverture websocket demandée")
        if self.scope['user'].is_anonymous :
            printc("ouverture websocket anonyme acceptee")
            await self.accept()
        elif self.scope['user'].is_participant :
            await self.accept()
            printc("ouverture websocket d'un participant acceptée")
        elif self.scope['user'].is_organisateur :
            await self.accept()
            printc("ouverture websocket d'un organisateur acceptée")
    async def disconnect(self, close_code):
        printc("deconnexion")
    async def receive_json(self,content):
        printc("message recu", content)
        command=content.get("command",None)
        if command=="connexion_pa" :
            printc("connexion d'un participant anonyme")
            if self.scope['user'].is_anonymous :   #en principe inutile
                pseudo=content.get("pseudo",None)
                printc("pseudo :", pseudo)
                sequence=content.get("sequence",None)
                printc("sequence : ",sequence)
                if sequence!=None :
                    sequence=await get_sequence_by_id(sequence)
                if pseudo!=None and sequence !=None :
                   q=Connexion(user=None, pseudo=pseudo, sequence=sequence,channel=self.channel_name)
                   await database_sync_to_async(q.save)()
                   play=await database_sync_to_async(Play.objects.filter)(sequence=sequence,status__lt=2)
                   long=await sync_to_async(len)(play)
                   printc("nombre de lignes dans play",long)
                   if long!=0 :
                       p=play[0]
                       await self.channel_layer.send(p.org_channel,
                            {"type":"connexionPA",
                             "from" : content.get("pseudo",None)})
                       await self.channel_layer.group_add("{}-{}".format(sequence.id,p.id), self.channel_name)
                       
                    
        elif command=="connexion_p" :
            printc("connexion d'un participant authentifié")
            if self.scope['user'].is_participant :  #en principe : inutile
                pseudo=content.get("pseudo",None)
                user=content.get("user")
                sequence=content.get("sequence",None)
                if sequence!=None :
                    sequence=await get_sequence_by_id(sequence)
                if user!=None and sequence !=None :
                   q=Connexion(user=user, pseudo=pseudo, sequence=sequence,channel=self.channel_name)
                   await database_sync_to_async(q.save)()
                   play=await database_sync_to_async(Play.objects.filter)(sequence=sequence,status__lt=2)
                   long=await sync_to_async(len)(play)
                   if long!=0 : #play deja initié, ce qui est le comportement normal
                       p=play[0]
                       await self.channel_layer.send(p.org_channel,
                            {"type":"connexionP",
                             "from" : self.scope['user']})
                       await self.channel_layer.group_add("tdb-{}-{}".format(sequence.id,p.id), self.channel_name)

                       
                             
        elif command=="connexion_org_tdb" :
            printc("l'organisateur a lancé la sequence : connexion de la fenetre tdb")
            if self.scope['user'].is_organisateur :
                printc("c'est bien un organisateur")
                sequence=content.get("sequence",None)
                if sequence!=None :
                    printc("recherche de la sequence ", sequence, "dans la bdd")
                    sequence=await get_sequence_by_id(sequence)
                    printc("sequence trouvée")
                if sequence!=None :
                    #on cherche si cette même séquence est deja ouverte
                    play=await database_sync_to_async(Play.objects.filter)(sequence=sequence)
                    long=await sync_to_async(len)(play)   # play non ouverte
                    if long==0 :                        
                        printc("play non ouverte : on l'ouvre")
                        p=Play(sequence=sequence, org_channel=self.channel_name,status=0, ranking=-1)
                        await database_sync_to_async(p.save)()
                        printc("ok normaleemnt")
                    else :
                        p=play[long-1]
                        p.org_channel=self.channel_name
                        await database_sync_to_async(p.save)()
                    await self.send_json({"type":"play.open","play":p.id})
                    await self.channel_layer.group_add("tdb-{}-{}".format(sequence.id,p.id),self.channel_name)
        elif command=="connexion_org_play" :
            printc("connexion depuis la fenetre de play")
            play=content.get("play",None)
            await self.channel_layer.group_add("play-{}-{}".format(play.sequence.id,play.id),self.channel_name)
            await self.channel_layer.send(play.tdb_channel,{"type":"play.ok","play_channel":self.channel_name})
        elif command=="play_ok" :
            await self.send_json({"type":"play_ok"})
        
        elif command=="start_play" :   
            printc("demarrage play")
            play=content.get("play_id",None)
            if play!=None :
                play=get_play_by_id(play)
                if play !=None and self.scope['user']==play.sequence.organisateur :
                    play.status=1
                    play.date_start=datetime.now()
                    play.ranking=0
                    await database_sync_to_async(play.save)()
                    data={"type":"play.activity","ranking":0,"activity":get_activity_by_rank(sequence,0)}
                    await self.channel_layer.group_send("{}-{}".format(sequence.id,play.id),data)
                    await self.channel_layer.group_send("play-{}-{}".format(sequence.id,play.id),data)

                    
        elif command=="stop_activity" :
            printc("fin d'activité")
            play=content.get("play_id",None)
            if play!=None :
                play=get_play_by_id(play)
                if play !=None and self.scope['user']==play.sequence.organisateur :
                    data={"type":"activity.stop","ranking":0,"activity":get_activity_by_rank(sequence,0)}
                    await self.channel_layer.group_send("{}-{}".format(sequence.id,play.id),data)
                    await self.channel_layer.group_send("play-{}-{}".format(sequence.id,play.id),data)
        elif command=="next_activity" :
            printc("activité suivante")
            play=content.get("play_id",None)
            if play!=None :
                play=get_play_by_id(play)
                if play !=None and self.scope['user']==play.sequence.organisateur :
                    r=play.ranking
                    next_a=get_activity_by_rank(play.sequence,r+1)
                    if next_a !=None : 
                       data={"type":"activity.next","ranking":r+1,"activity":next_a}
                       await self.channel_layer.group_send("{}-{}".format(sequence.id,play.id),data)
                       await self.channel_layer.group_send("play-{}-{}".format(sequence.id,play.id),data)

    async def connexionPA(self,data):
        if self.scope['user'].is_organisateur :
            printc("entree dans connexionPA")
            await self.send_json({"command":"connexionPA","from":data['from']})

    async def connexionP(self,data):
        if self.scope['user'].is_organisateur :
            await self.send_json({"command":"connexionP","from":data['from']})
