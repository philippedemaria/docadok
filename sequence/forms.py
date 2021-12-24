import datetime
from django import forms
from .models import Folder, Sequence , Activity
from account.models import Participant , Organisateur
 
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

from django.template.defaultfilters import filesizeformat
from django.conf import settings

from itertools import groupby
from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField
import uuid 

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
        fields = [ 'title', 'organisateur', 'ranking' ]


    def __init__(self, *args, **kwargs):
        organisateur = kwargs.pop('organisateur')
        super(FolderForm, self).__init__(*args, **kwargs)
        if organisateur :
            try :
                r = organisateur.folders.order_by('ranking').last().ranking + 1
            except :
                r = 0
        # Champs invisibles
        self.fields['organisateur'].widget  = forms.HiddenInput()
        self.fields['organisateur'].initial = organisateur
        self.fields['ranking'].widget  = forms.HiddenInput()
        self.fields['ranking'].initial = r


class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        organisateur = kwargs.pop('organisateur')
        super(SequenceForm, self).__init__(*args, **kwargs)

        if organisateur :
            try :
                r = organisateur.sequences.order_by('ranking').last().ranking + 1
            except :
                r = 0
        # Champs invisibles
        self.fields['organisateur'].widget  = forms.HiddenInput()
        self.fields['organisateur'].initial = organisateur
        self.fields['ranking'].widget  = forms.HiddenInput()
        self.fields['ranking'].initial = r 


class CodeForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ('code',)





class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        sequence = kwargs.pop('sequence')
        super(ActivityForm, self).__init__(*args, **kwargs)

        self.fields['sequence'].initial    = sequence
 