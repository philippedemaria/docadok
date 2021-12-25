#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
from django.urls import path, re_path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('create_sequence/<int:ids>', create_sequence, name='create_sequence'),
    path('update_sequence/<int:ids>', update_sequence, name='update_sequence'),
    path('delete_sequence/<int:ids>', delete_sequence, name='delete_sequence'),

    path('moderate_sequence/<int:ids>', moderate_sequence, name='moderate_sequence'),
    path('compare_sequence/<int:ids>', compare_sequence, name='compare_sequence'),
    path('clone_sequence/<int:ids>', clone_sequence, name='clone_sequence'),
    path('export_sequence/<int:ids>', export_sequence, name='export_sequence'),

    path('ajax_update_sequence', ajax_update_sequence, name='ajax_update_sequence'),
    path('ajax_update_checkbox_sequence', ajax_update_checkbox_sequence, name='ajax_update_checkbox_sequence'),


    path('create_activity/<int:ids>/<int:atype>/<int:ida>', create_activity, name='create_activity'),
    path('update_activity/<int:ids>/<int:atype>/<int:ida>', update_activity, name='update_activity'),



 ]
