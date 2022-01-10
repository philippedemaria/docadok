import random
import re
import html
from django import template
register = template.Library()
import re




@register.filter
def decode(arg):
    '''HTML entity decode'''
    string = html.unescape(arg)
    return string



@register.filter
def decrypt_results(arg):
    '''Pour les flashcards'''
    tab = arg.split("-")
    string = ""
    for r in tab :
        if int(r) == 1 :
            score = "danger"
        elif int(r) == 3 :
            score = "validate"
        elif int(r) == 5 :
            score = "success"
        string += "<i class='fa fa-square fa-xs text-"+score+"'></i>"
        
    return string





@register.filter
def cleanhtml(raw_html): #nettoie le code des balises HTML
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub('\n', '', cleantext)
    return cleantext


 

@register.filter
def decimal2number(decimal): #enlève la virgule et met un point
    d_tab = str(decimal).replace(",",".") 
    return d_tab



@register.filter
def abreviation(raw_html): #nettoie le code des balises HTML
    if raw_html.isdigit():
        if raw_html == "Term" :
            return str("T<sup>erm</sup>")
        elif raw_html == "1" :
            return str("1<sup>ère</sup>")
        elif raw_html == 2 :
            return str("2<sup>nde</sup>")
        else :
            return str(raw_html) + "<sup>ème</sup>" 
    else :
        return raw_html


 

@register.filter
def create_template(a): #enlève la virgule et met un point 
    return "activity/activity_"+str(a)+".html"



 

@register.filter
def play_template(a): #enlève la virgule et met un point 
    return "activity/play_"+str(a)+".html"

 

@register.filter
def type_activity(atype): #enlève la virgule et met un point
    if atype  == 0 :
        ntype = 'Q.C.M'
    elif atype == 1 :
        ntype = 'sondage'
    elif atype == 2 :
        ntype = 'Nuage de mots'
    elif atype == 3 : # TODO
        ntype = 'legender une image'
    elif atype == 4 : # TODO
        ntype = "Trouver sur l'image"
    elif atype == 5 : # TODO
        ntype = 'Caster une image'
    elif atype == 6 :
        ntype = 'Association'
    elif atype == 7 :
        ntype = 'Brainstorming'
    elif atype == 8 :
        ntype = 'Echelle'
    elif atype == 9 :
        ntype = 'Classement'
    elif atype == 10 :
        ntype = 'Priorisation'
    elif atype == 11 :
        ntype = 'Texte à trous'
    elif atype == 12 :
        ntype = 'Post it'
    return ntype

 
@register.filter
def shuffle(arg): #enlève la virgule et met un point
    listes = list(arg.values("associate","imageassociate") )
    random.shuffle(listes)
    return listes



@register.filter
def fill_the_blank(arg): #enlève la virgule et met un point
    tab_string = arg.split('___') 
    new_str = ""
    for i in range(0,len(tab_string)):
        if i%2==0 :
            new_str += tab_string[i]
        else :
            for k in range(len(tab_string[i])):
                new_str += "_"
    return new_str



@register.filter
def fill_the_blank_input(arg): #enlève la virgule et met un point
    tab_string = arg.split('___') 
    new_str = ""
    for i in range(0,len(tab_string)):
        if i%2==0 :
            new_str += tab_string[i]
        else :
            for k in range(len(tab_string[i])):
                k+=1
            wdth = k*20
            new_str += " <input type='text' name='fill_the_blank"+str(i)+"' id='fill_the_blank' class='fill_the_blank_input' style='width:"+str(wdth)+"px' /> "
    return new_str
 