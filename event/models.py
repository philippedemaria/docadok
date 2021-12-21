from django.db import models
from datetime import date, datetime, timedelta

 
from django.utils import timezone
from account.models import Student, Teacher, ModelWithCode 
 
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
    teacher = models.ForeignKey(Teacher, related_name="folders", on_delete=models.CASCADE, default='', blank=True)
    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    def __str__(self):
        return "{}".format(self.title)




class Event(ModelWithCode):
 

    icon      = models.CharField(max_length=255, null=True, blank=True, editable=False)
    title     = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    date      = models.DateField(auto_now_add=True, verbose_name="Date de création")
    folder    = models.ForeignKey(Folder, related_name="events", on_delete=models.CASCADE, default='', blank=True )
    ranking   = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)

    def __str__(self):     
        return "{}".format(self.title)
 
 


class Question(models.Model):
    """
    Modèle représentant un associé.
    """

    title         = models.TextField(max_length=255, default='',  blank=True, verbose_name="Réponse écrite")
    date_modified = models.DateTimeField(auto_now=True)
    vignette      = models.ImageField(upload_to=question_directory_path, verbose_name="Vignette d'accueil", blank=True, null = True , default ="")
 

    def __str__(self):
        return self.title

 

class Choice(models.Model):
    """
    Modèle représentant un associé.
    """
    imageanswer = models.ImageField(upload_to=choice_directory_path,  null=True,  blank=True, verbose_name="Image", default="")
    answer      = models.TextField(max_length=255, default='', null=True,  blank=True, verbose_name="Réponse écrite")
    is_correct  = models.BooleanField(default=0, verbose_name="Réponse correcte ?")
    question    = models.ForeignKey(Question, related_name="choices", blank=True, null = True,  on_delete=models.CASCADE)
    def __str__(self):
        return self.answer 

 


