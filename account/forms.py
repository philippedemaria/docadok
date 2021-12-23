from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Organisateur, User, Participant,  Newpassword

from django.core.exceptions import ValidationError
from django.forms import BaseFormSet

from django.db import transaction
from django.contrib.auth.hashers import make_password


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé. Merci d'en choisir un autre.", code='invalid')
        return username

 
class AuthenticationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

 





class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'


class OrganisateurForm(forms.ModelForm):

    class Meta :
        model = Organisateur
        fields = '__all__'


