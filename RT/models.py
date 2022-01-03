from django.db import models
from sequence.models import Sequence,Activity
from account.models import User

class Connexion(models.Model) :
    user    = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    pseudo  = models.CharField(max_length=50, blank=True, null=True)
    date    = models.DateTimeField(auto_now=True)
    sequence= models.ForeignKey(Sequence, on_delete=models.CASCADE, blank=True, null=True)
    channel = models.CharField(max_length=60, default="non défini")
    def __str__(self):
        s="Connexion "
        if self.user!=None :
            s+="de "+user.lname
        else :
            s+="anonyme"
        if self.pseudo!=None :
            s+=" sous le pseudo "+self.pseudo
        return s+" à "+self.date+" sur la sequence : "+self.sequence

    
class Resultat(models.Model):
    connexion= models.ForeignKey(Connexion, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity,  on_delete=models.CASCADE, null=True)
    reponse  = models.CharField(max_length=100, blank=True)
    score    = models.IntegerField(default=0)
    
    

