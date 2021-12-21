import uuid

import pytz
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
 
#from general_fonctions import *

from django.conf import settings # récupération de variables globales du settings.py
from datetime import datetime 
# Pour créer un superuser, il faut depuis le shell taper :
# from account.models import User
# User.objects.create_superuser("admin","admin@gmail.com","motdepasse", user_type=0).save()

def file_directory_path(instance, filename):
    return "factures/{}/{}".format(instance.user.id, filename)


def generate_code():
    '''
    Fonction qui génère un code pour les modèles suivantes :
    - Parcours
    - Group
    - Student
    - Supportfile
    '''
    return str(uuid.uuid4())[:8]


class ModelWithCode(models.Model):
    '''
    Ajoute un champ code à un modèle
    '''
    code = models.CharField(max_length=100, unique=True, blank=True, default=generate_code, verbose_name="Code")

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Modèle représentant un utilisateur. Possède les champs suivants hérités de la classe AbstractUser :

    first_name : Optional (blank=True). 100 characters or fewer.
    last_name : Optional (blank=True). 150 characters or fewer.
    email : Optional (blank=True). Email address.
    password : Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password.)
    groups : Many-to-many relationship to Group
    user_permissions : Many-to-many relationship to Permission
    is_staff : Boolean. Designates whether this user can access the admin site.
    is_active : Boolean. Designates whether this user account should be considered active.
    is_superuser : Boolean. Designates that this user has all permissions without explicitly assigning them.
    last_login : A datetime of the user’s last login.
    date_joined : A datetime designating when the account was created. Is set to the current date/time by default when the account is created.

    """
 
    #### user_type = 0 for student, 2 for teacher, 2 + is_superuser for admin,  5 for superuser

    STUDENT, PARENT, TEACHER = 0, 1, 2
    USER_TYPES = (
        (STUDENT, "Élève"),
        (PARENT, "Parent"),
        (TEACHER, "Enseignant"),
    )

    CIVILITIES = (
        ('Mme', 'Mme'),
        ('M.', 'M.'),
    )

    TZ_SET = []
    for tz in pytz.common_timezones:
        TZ_SET.append((tz,tz))

    user_type  = models.PositiveSmallIntegerField(editable=False, null=True, choices=USER_TYPES)
    civilite   = models.CharField(max_length=10, default='Mme', blank=True, choices=CIVILITIES, verbose_name="Civilité")
    time_zone  = models.CharField(max_length=100, null=True, blank=True, choices=TZ_SET, verbose_name="Fuseau horaire")
    is_extra   = models.BooleanField(default=0)
    is_manager = models.BooleanField(default=0)


    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    @property
    def is_student(self):
        return self.user_type == self.STUDENT

    @property
    def is_parent(self):
        return self.user_type == self.PARENT

    @property
    def is_teacher(self):
        return self.user_type == self.TEACHER

    @property
    def is_creator(self):
        return self.is_staff == True

    @property
    def sacado(self):
        """
        L'enseignant est un membre bénéficiaire de sacado
        """
        sacado_asso = False
        if self.school  :
            sacado_asso = True
        return sacado_asso

    @property
    def is_sacado_member(self):
        is_sacado = False
        today = datetime.now()
        try :
            abonnement = self.school.abonnement.last()
            if today < abonnement.date_stop and abonnement.is_active :
                is_sacado = True
        except :
            pass
        return is_sacado 


    def my_groups(self):
        group_string = ""
        try :
            groups = self.student.students_to_group.all()
            n , i = groups.count() , 1
            sep = ""
            for g in self.student.students_to_group.all():
                if n == i :
                    sep = "<br/>"
                group_string += g.name+" (<small>"+g.teacher.user.last_name +" "+g.teacher.user.first_name+"</small>)"+sep
                i+=1
        except : 
            pass   

        return group_string



class Student(ModelWithCode):
    """
    Modèle représentant un élève.
    """
    user      = models.OneToOneField(User, blank=True, related_name="student", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        lname = self.user.last_name.capitalize()
        fname = self.user.first_name.capitalize()

        return "{} {}".format(lname, fname)


  
class Teacher(models.Model):
    """
    Modèle représentant un enseignant.
    """
    user          = models.OneToOneField(User, blank=True, related_name="teacher", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.last_name.capitalize()} {self.user.first_name.capitalize()}"

    def notify_registration(self):
        """
        Envoie un email à l'enseignant l'informant de la réussite de son inscription
        """
        try :
            if self.user.email != '':
                send_templated_mail(
                    template_name="teacher_registration",
                    from_email= settings.DEFAULT_FROM_EMAIL ,
                    recipient_list=[self.user.email, ],
                    context={"teacher": self.user, }, )
        except :
            pass


    def notify_registration_to_admins(self):
        """
        Envoie un email aux administrateurs informant de l'inscription d'un nouvel enseignant
        """
        try :
            #admins = User.objects.filter(is_superuser=1)
            #admins_emails = list(admins.values_list('email', flat=True))
            admins_emails =["sacado.asso@gmail.com"]
            send_templated_mail(
                template_name="teacher_registration_notify_admins",
                from_email= settings.DEFAULT_FROM_EMAIL ,
                recipient_list=admins_emails,
                context={"teacher": self.user,}, )
        except :
            pass




    def sacado(self):
        """
        L'enseignant est un membre bénéficiaire de sacado
        """
        sacado_asso = False
        if self.user.school  :
            sacado_asso = True
        return sacado_asso


    def is_creator(self):
        """
        L'enseignant est un membre bénéficiaire de sacado
        """
        creator = False
        if self.user.is_creator  :
            creator = True
        return creator






class Newpassword(ModelWithCode):
    """
    Modèle de ré initialisation de password.
    """
    email = models.CharField(max_length=255 )  
 

    def __str__(self):
        email = self.email
        return "{}".format(email )