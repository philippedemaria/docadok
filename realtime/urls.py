from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [path('RT_P',RT_Participant,name="RT_Participant"),
               path('RT_Tbd',RT_Tbd,name="RT_Tbd"),
               path('RT_Play',RT_Play,name="RT_Play"),
]
