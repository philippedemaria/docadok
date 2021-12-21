from django.conf import settings # récupération de variables globales du settings.py
from django.shortcuts import render,redirect
from django.forms import formset_factory
 
from django.contrib.auth import   logout , login, authenticate
from django.contrib.auth.forms import  UserCreationForm,  AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.utils import formats, timezone
from django.contrib import messages
 
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count, Q

from account.forms import  UserForm, TeacherForm, StudentForm
from account.models import  User, Teacher, Student 

from event.forms import  CodeForm


from datetime import date, datetime , timedelta

from itertools import chain


import random
import pytz
import uuid
import time
import os
import fileinput 
import random
import json

##############   bibliothèques pour les impressions pdf    #########################
import os
from pdf2image import convert_from_path # convertit un pdf en autant d'images que de pages du pdf
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT 
############## FIN bibliothèques pour les impressions pdf  #########################


def end_of_contract() :

    data = {}
    date = datetime.now()

    if date.month < 6 :
        end = date.year
    else :
        end = int(date.year) + 1
    return end



def index(request):

    if request.user.is_authenticated :
        index_tdb = True  # Permet l'affichage des tutos Youtube dans le dashboard
        template = "dashboard.html"
        if request.user.is_teacher:
            form_code = CodeForm()
            context = { 'form_code' : form_code  }
        
        elif request.user.is_student:  ## student
            context = { }


        return render(request, template , context)


    else:  ## Anonymous

        form = AuthenticationForm()
        u_form = UserForm()
        cookie = request.session.get("cookie", None)

    
        context = {'u_form' : u_form,  'form' : form, }

        return render(request, 'home.html', context)






def logout_view(request):
    try:
        connexion = Connexion.objects.get(user=user)
        connexion.delete()
    except:
        pass

    form = AuthenticationForm()
    u_form = UserForm()
    t_form = TeacherForm()
    s_form = StudentForm()
    logout(request)
    levels = Level.objects.all()
    context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form, 'levels': levels, 'cookie': False}
    return render(request, 'home.html', context)



