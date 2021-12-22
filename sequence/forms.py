import datetime
from django import forms
from .models import Folder, Sequence
from account.models import Student , Teacher
 
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

from django.template.defaultfilters import filesizeformat
from django.conf import settings

from itertools import groupby
from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField
 

def validation_file(content):
    if content :
	    content_type = content.content_type.split('/')[0]
	    if content_type in settings.CONTENT_TYPES:
	        if content._size > settings.MAX_UPLOAD_SIZE:
	            raise forms.ValidationError("Taille max : {}. Taille trop volumineuse {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
	    else:
	        raise forms.ValidationError("Type de fichier non accepté")
	    return content


 


class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = '__all__'




class SequenceForm(forms.ModelForm):
	class Meta:
		model = Sequence 
		fields = '__all__'


class CodeForm(forms.ModelForm):
	class Meta:
		model = Sequence
		fields = ('code',) 