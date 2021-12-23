from django.db import models
from datetime import date, datetime
from django.utils import   timezone
from django.db.models import Q
from random import uniform , randint
from time import strftime

from ckeditor_uploader.fields import RichTextUploadingField
from sequence.models import  Sequence
from account.models import  USer
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()
POLICES = (
        (16, '16'),
        (24, '24'), 
        (32, '32'), 
        (40, '40'),
        (48, '48'),
        (56, '56'),
    )


def question_directory_path(instance, filename):
    return "qcm/questions/{}".format(filename)

def choice_directory_path(instance, filename):
    return "qcm/choices/{}".format(filename)

 



class Question(models.Model):
    """
    Modèle représentant un associé.
    """
    title         = models.TextField(max_length=255, default='',  blank=True, verbose_name="Réponse écrite")
    calculator    = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    date_modified = models.DateTimeField(auto_now=True)
    qtype         = models.PositiveIntegerField(default=3, editable=False)

    imagefile  = models.ImageField(upload_to=question_directory_path, blank=True, verbose_name="Image", default="")
    audio      = models.FileField(upload_to=question_directory_path, blank=True, verbose_name="Audio", default="")
    video      = models.TextField( default='',  blank=True, verbose_name="Vidéo intégrée")

    is_publish = models.BooleanField(default=1, verbose_name="Publié ?")

    duration      = models.PositiveIntegerField(default=20, blank=True, verbose_name="Durée")
    point         = models.PositiveIntegerField(default=1000, blank=True, verbose_name="Point")

    ranking    = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    sequence   = models.ForeignKey(Sequence, related_name="sequences",  on_delete=models.CASCADE)

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




class Answerplayer(models.Model):

    sequence   = models.ForeignKey(Sequence,  related_name="answerplayer", default ="" ,  on_delete=models.CASCADE ) 
    user       = models.ForeignKey(User,  null=True, blank=True,   related_name='questions_player', on_delete=models.CASCADE,  editable= False)
    question   = models.ForeignKey(Question,  null=True, blank=True, related_name='questions_player', on_delete=models.CASCADE, editable= False)
    answer     = models.CharField( max_length=255, null=True, blank=True,  verbose_name="Réponse")  
    score      = models.PositiveIntegerField(default=0, editable=False)
    timer      = models.CharField(max_length=255, editable=False)  
    is_correct = models.BooleanField(default=0, editable=False) 

    def __str__(self):
        return self.user.last_name