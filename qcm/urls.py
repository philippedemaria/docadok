from django.urls import path, re_path
from .views import *

urlpatterns = [



    path('create_question/<int:ids>/<int:idq>/<int:qtype>', create_question, name='create_question'),
    path('update_question/<int:ids>/<int:idq>/<int:qtype>', update_question, name='update_question'),   
    path('delete_question/<int:ids>/<int:idq>/<int:qtype>', delete_question, name='delete_question'),
    path('clone_question/<int:ids>/<int:idq>/<int:qtype>' , clone_question , name='clone_question'),


] 