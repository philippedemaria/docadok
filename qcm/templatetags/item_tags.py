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


