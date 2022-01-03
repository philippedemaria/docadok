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
    terminal         = models.BooleanField(default=0, verbose_name="Affichage des diapositives sur le terminal des participants ?")
    displayresult    = models.BooleanField(default=0, verbose_name="Résultats visibles par défaut ?")
    is_active        = models.BooleanField(default=0, verbose_name="En cours ?", editable=False)    
    participants     = models.ManyToManyField(Participant,  blank=True,  related_name="sequences" )

    def __str__(self):     
        return "{}".format(self.title)
 
 


class Activity(ModelWithCode):
 
    title        = models.CharField(max_length=255, null=True, blank=True,  verbose_name="Ecrire la question que vous souhaitez poser à votre audience")
    date         = models.DateField(auto_now_add=True, verbose_name="Date de création")
    imagefile    = models.ImageField(upload_to=question_directory_path, null=True, blank=True,  verbose_name="Image", default="")
    sequence     = models.ForeignKey(Sequence, related_name="activities", on_delete=models.CASCADE )
    is_score     = models.BooleanField(default=0, verbose_name="Score ?")
    score        = models.PositiveIntegerField( default=1000,  blank=True, null=True )
    atype        = models.PositiveIntegerField( default=0)


    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_timer     = models.BooleanField(default=0, verbose_name="Compte à rebours ?")
    timer        = models.BooleanField(default=0, verbose_name="Temps")
    is_publish   = models.BooleanField(default=0, verbose_name="Publié ?") 
    start_publish= models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    stop_publish = models.DateTimeField(null=True, blank=True, verbose_name="Date de verrouillage")

    liker        = models.BooleanField(default=0, verbose_name="Like")
    multiple     = models.BooleanField(default=0, verbose_name="Réponse multiple")
    ranking      = models.PositiveIntegerField(default=0,  blank=True, null=True, editable=False)
    is_shuffle   = models.BooleanField(default=0, verbose_name="Shuffle ?")

    def __str__(self):     
        return "{}".format(self.title)



    def icon(self):
        icons = ["question-circle","clipboard-data","cloud","card-image","images","camera","bezier2","boxes","ladder","list-ol","bricks","reception-0"]
        return "bi bi-"+icons[self.atype] 
 

    def choices_shuffle(self):
        self.choices.shuffle()
        return "bi bi-"+icons[self.atype] 



    def sorter(self):
        sorter = False 
        if self.atype == 6 or  self.atype == 9 or  self.atype == 10  : 
            sorter = True
        return sorter
 



class Choice(models.Model):
    """
    Modèle représentant un associé.
    """
    imageanswer    = models.ImageField(upload_to=choice_directory_path,  null=True,  blank=True, verbose_name="Image", default="")
    label          = models.CharField(max_length=255, default='', null=True,  blank=True, verbose_name="Réponse")
    is_correct     = models.BooleanField(default=0, verbose_name="Réponse correcte ?")
    activity       = models.ForeignKey(Activity, related_name="choices", blank=True, null = True,  on_delete=models.CASCADE)
    associate      = models.CharField(max_length=255, default='', null=True,  blank=True, verbose_name="Association")
    imageassociate = models.ImageField(upload_to=choice_directory_path,  null=True,  blank=True, verbose_name="Image", default="")
    textarea       = models.TextField( default='', null=True,  blank=True, verbose_name="Texte")
    def __str__(self):
        return self.label 

    def get_details(self):
        nb_answers     = Answerplayer.objects.filter( activity=self.activity).count()
        nb_this_choice = Answerplayer.objects.filter( choice=self ).count()

        data={}
        if nb_answers > 0 :
            answer_percent     = nb_this_choice/nb_answers
            answer_this_choice = nb_this_choice
        else :
            answer_percent     = 0
            answer_this_choice = 0

        data["answers"]            = answer_percent
        data["answer_this_choice"] = answer_this_choice

        return data








class Play(models.Model):
    sequence    = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    org_channel = models.CharField(max_length=60, null=True, help_text="channel de l'organisateur")
    status      = models.SmallIntegerField(default=0)
    #0 : par encore ouvert , 1 : ouvert, 2 : clos
    date_start  = models.DateTimeField(blank=True)
    date_end    = models.DateTimeField(blank=True)
    ranking     = models.IntegerField(default=-1,help_text="la numero de la dernière activité terminée") 



class Answerplayer(models.Model):

    participant = models.ForeignKey(Participant,  null=True, blank=True,   related_name='answers_player', on_delete=models.CASCADE )
    activity    = models.ForeignKey(Activity,  null=True, blank=True, related_name='answers_player', on_delete=models.CASCADE )
    choice      = models.ForeignKey(Choice,  null=True, blank=True, related_name='answers_player', on_delete=models.CASCADE )
    play        = models.ForeignKey(Play,  null=True, blank=True, related_name='answers_player', on_delete=models.CASCADE )
    answer      = models.CharField(max_length=1024, null=True, blank=True,  verbose_name="Réponse")  
    score       = models.IntegerField(default=0, editable=False)
    duration    = models.CharField(max_length=255, default=0 , editable=False,  verbose_name="durée")   
    is_correct  = models.BooleanField(default=0, editable=False) 

    def __str__(self):
        return self.participant.user.last_name



 
 
