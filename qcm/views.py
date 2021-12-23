from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail

from qcm.models import Question  , Choice  , Quizz Answerplayer 
from qcm.forms import QuestionForm ,  ChoiceForm 

import uuid
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.forms import inlineformset_factory

from django.db.models import Q , Sum
from random import  randint, shuffle
import math
import json
import time
############### bibliothèques pour les impressions pdf  #########################
import os
from django.utils import formats, timezone
from io import BytesIO, StringIO
from django.http import  HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape , letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image , PageBreak,Frame , PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import yellow, red, black, white, blue
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from html import escape
cm = 2.54
#################################################################################
import re
import pytz
from datetime import datetime , timedelta



############################################################################################################
############################################################################################################
########## Question
############################################################################################################
############################################################################################################


def list_questions(request):
    
    request.session["tdb"] = False # permet l'activation du surlignage de l'icone dans le menu gauche 
    questions = Question.objects.all()
    return render(request, 'qcm/list_question.html', {'questions': questions  })


 
def create_question(request,ids,idq=0,qtype=0):
    
    sequence = Sequence.objects.get(pk = ids)

    form     = QuestionForm(request.POST or None, request.FILES or None, sequence = sequence)
    formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct') , extra=2)
    form_ans = formSet(request.POST or None,  request.FILES or None)

    if request.method == "POST"  :
        if form.is_valid():
            nf         = form.save(commit=False) 
            nf.teacher = request.user.teacher
            nf.qtype   = qtype
            nf.save()
            form.save_m2m()

            #############Position dans la liste de la séquence
            last_position = sequence.rankings.last().position + 1
            Ranking.objects.create( sequence=sequence, appid = "qcm_"+str(nf.pk) ,  position = last_position )
            #############
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()

            return redirect('create_question')

 
    context.update( {  'form' : form , 'form_ans' : form_ans   })
    template = 'qcm/form_question.html'

    return render(request, template , context)




def update_question(request,ids,idq,qtype):
    

    sequence = Sequence.objects.get(pk = ids)

    form     = QuestionForm(request.POST or None, request.FILES or None, instance = question, sequence = sequence)
    formSet  = inlineformset_factory( Question , Choice , fields=('answer','imageanswer','is_correct') , extra=0)
    form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    if request.method == "POST"  :
        if form.is_valid():
            nf         = form.save(commit=False) 
            nf.teacher = request.user.teacher
            nf.qtype   = qtype
            nf.save()
            form.save_m2m() 
            last_position = sequence.rankings.last().position + 1
            Ranking.objects.create( sequence=sequence, appid = "qcm_"+str(nf.pk) ,  position = last_position )
 
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()


            return redirect('create_question')

 
    context.update( {  'form' : form ,  'form_ans' : form_ans   })
    template = 'qcm/form_question.html'

    return render(request, template , context)





 
def delete_question(request,ids,idq,qtype=0):
    
    question = Question.objects.get(pk= id)
    if question.quizz.count() == 0 :
        question.delete()
    else :
        messages.error(request, "  !!!  Cette question est utiolisée dans un quizz  !!! Suppression interdite.")
    return redirect ('create_question')



 
def show_question(request,ids,idq,qtype=0):
 
    question = Question.objects.get(pk= idq)
    context = {'form': form, "question" : question }

    return render(request, 'qcm/form_question.html', context)


def clone_question(request,ids,idq,qtype=0):

    sequence = Sequence.objects.get(pk = ids)
    question = Question.objects.get(pk= idq)
    if question.quizz.count() == 0 :
        question.delete()
    else :
        messages.error(request, "  !!!  Cette question est utiolisée dans un quizz  !!! Suppression interdite.")
    return redirect ('create_question')


#######################################################################################################################
############################ Ajax  ####################################################################################
#######################################################################################################################
 
@csrf_exempt 
def question_sorter(request):  
    try :
        question_ids = request.POST.get("valeurs")
        question_tab = question_ids.split("-") 

        for i in range(len(question_tab)-1):
            Question.objects.filter(  pk = question_tab[i]).update(ranking = i)
    except :
        pass

    data = {}
    return JsonResponse(data)  

 

