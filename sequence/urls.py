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
    path('tdb_sequence/<slug:code>', tdb_sequence, name='tdb_sequence'),
    path('show_sequence/<int:ids>', show_sequence, name='show_sequence'),
    path('play_sequence/<int:ids>', play_sequence, name='play_sequence'),

    path('moderate_sequence/<int:ids>', moderate_sequence, name='moderate_sequence'),
    path('compare_sequence/<int:ids>', compare_sequence, name='compare_sequence'),
    path('clone_sequence/<int:ids>', clone_sequence, name='clone_sequence'),
    path('export_sequence/<int:ids>', export_sequence, name='export_sequence'),
    path('import_sequence', import_sequence, name='import_sequence'),

    path('ajax_update_sequence', ajax_update_sequence, name='ajax_update_sequence'),
    path('ajax_update_checkbox_sequence', ajax_update_checkbox_sequence, name='ajax_update_checkbox_sequence'),
    path('ajax_sort_sequences', ajax_sort_sequences, name='ajax_sort_sequences'),

    path('create_activity/<int:ids>/<int:atype>/<int:ida>', create_activity, name='create_activity'),
    path('update_activity/<int:ids>/<int:atype>/<int:ida>', update_activity, name='update_activity'),
    path('delete_activity/<int:ids>/<int:ida>', delete_activity, name='delete_activity'),
    path('show_activity/<int:ida>', show_activity, name='show_activity'),

    path('export_activity/<int:ids>/<int:ida>', export_activity, name='export_activity'),
    path('clone_activity/<int:ids>/<int:ida>', clone_activity, name='clone_activity'),
    path('copy_link_activity/<int:ids>/<int:ida>', copy_link_activity, name='copy_link_activity'),
    path('embed_activity/<int:ids>/<int:ida>', embed_activity, name='embed_activity'),
    path('import_activity/<int:ids>', import_activity, name='import_activity'),
    path('ajax_sort_activities', ajax_sort_activities, name='ajax_sort_activities'),
 
    path('create_folder', create_folder, name='create_folder'),
    path('update_folder', update_folder, name='update_folder'),
    path('delete_folder/<int:idf>', delete_folder, name='delete_folder'),

    path('ajax_sort_folders', ajax_sort_folders, name='ajax_sort_folders'),
    path('ajax_include_folders', ajax_include_folders, name='ajax_include_folders'),

]
