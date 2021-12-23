import datetime
from django import forms
from .models import Tool , Question  , Choice  , Quizz , Diaporama , Slide , Qrandom ,Variable , Answerplayer, Videocopy
from account.models import Student , Teacher
from socle.models import Knowledge, Skill
from group.models import Group
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django.forms import MultiWidget, TextInput , CheckboxInput
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



 

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = '__all__'
		widgets = {
            'is_correct' : CheckboxInput(),  
        }


	def __init__(self, *args, **kwargs):
		quizz = kwargs.pop('quizz')
		super(QuestionForm, self).__init__(*args, **kwargs)

		levels = quizz.levels.all()
		themes = quizz.themes.all()
		subject = quizz.subject
		knowledges = []
		if len(levels) > 0 and len(themes) > 0  :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels, theme__in=themes )
		elif len(levels) > 0 :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,level__in=levels)
		elif len(themes) > 0 :
			knowledges = Knowledge.objects.filter(theme__subject = subject ,theme__in=themes)

		self.fields['knowledge'] = forms.ModelChoiceField(queryset=knowledges, required=False)


	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content)  
		audio_ = self.cleaned_data['audio']
		validation_file(audio_) 
		video_ = self.cleaned_data['video']
		validation_file(video_) 






class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = '__all__'
 

	def clean_content(self):
		content = self.cleaned_data['imagefile']
		validation_file(content) 







 

class AnswerplayerForm(forms.ModelForm):
 
	class Meta:
		model = Answerplayer
		fields = '__all__'


