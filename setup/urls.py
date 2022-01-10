
from django.urls import path, re_path
from .views import *
from sequence.views import play_sequence

urlpatterns = [

    re_path(r'^$', index, name='index'),


    path('play/<slug:code>', play_sequence, name='play_sequence'),
   

]


 