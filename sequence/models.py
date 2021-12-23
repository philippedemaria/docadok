from django.db import models
from datetime import date, datetime, timedelta

 
from django.utils import timezone
from account.models import Participant, Organisateur, ModelWithCode 
 
from django.apps import apps
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q, Min, Max
import os.path
from django.utils import timezone
 



def question_directory_path(instance, filename):
    return "quiz/question/{}".format(filename)

def choice_directory_path(instance, filename):
    return "quiz/choice/{}".format(filename)
########################################################################################################
########################################################################################################
class Folder(models.Model):

    title   = models.CharField(max_length=255, verbose_name="Titre")
    organisateur = models.ForeignKey(Organisateur, related_name="folders", on_delete=models.CASCADE, default='', blank=True)
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True )

    def __str__(self):
        return "{}".format(self.title)




class Sequence(ModelWithCode):
 
    title            = models.CharField(max_length=255, null=True, blank=True, default="Ma nouvelle séquence" ,  verbose_name="Titre")
    date             = models.DateField(auto_now_add=True, verbose_name="Date de création")
    folder           = models.ForeignKey(Folder, related_name="sequences", on_delete=models.CASCADE,   blank=True, null=True )
    ranking          = models.PositiveIntegerField(  default=0,  blank=True, null=True )
    organisateur     = models.ForeignKey(Organisateur, related_name="sequences", on_delete=models.CASCADE, default='', blank=True)
    temporisation    = models.BooleanField(default=0, verbose_name="mode continu ?")
    authentification = models.BooleanField(default=0, verbose_name="Authentification ?")
    pseudonyme       = models.BooleanField(default=0, verbose_name="Pseudonyme ?")
    competition      = models.BooleanField(default=0, verbose_name="Compétition ?")
    terminal         = models.BooleanField(default=0, verbose_name="Afficage des diapositives sur le terminal des participants ?")
    displayresult    = models.BooleanField(default=0, verbose_name="Résultats visibles par defaut ?")

    def __str__(self):     
        return "{}".format(self.title)
 
 


class Ranking(models.Model):
 
    appid    = models.CharField(max_length=255, null=True, blank=True, editable=False)
    sequence  = models.ForeignKey(Sequence, related_name="rankings", on_delete=models.CASCADE , editable=False)
    position  = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    def __str__(self):     
        return "{}".format(self.appid)
 


