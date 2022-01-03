from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
from django.contrib import messages
from sequence.models import Sequence, Folder , Activity , Choice
from sequence.forms import SequenceForm, FolderForm, ActivityForm , CodeActivityForm  , CodeSequenceForm



import qrcode
import qrcode.image.svg
from io import BytesIO

####################################################################################################
####################################################################################################
####################    folder
####################################################################################################
####################################################################################################
def create_folder(request):

    organisateur = request.user.organisateur
    form = FolderForm(request.POST or None , organisateur = organisateur )
    data = {}

    if form.is_valid():
        nf = form.save()
    else :
        print(form.errors)

    return redirect('index')

 
def update_folder(request):

    idf = request.POST.get("folder")
    title = request.POST.get("title")

    Folder.objects.filter(pk=idf).update(title = title)

    return redirect('index')


  
def delete_folder(request, idf):
    folder = Folder.objects.get(id=idf)
    if request.user.is_authenticated :
        if request.user.organisateur == folder.organisateur :
            folder.delete()
            messages.success(request,'Suppression réalisée avec succès')

    return redirect('index')


def ajax_sort_folders(request):

    sequence_ids  = request.POST.getlist("sequences")
    i=0
    for folder_id in sequence_ids:
        Folder.objects.filter( pk = folder_id ).update(ranking = i)
        i+=1
    data = {}
    return JsonResponse(data) 





####################################################################################################
####################################################################################################
####################    folder
####################################################################################################
####################################################################################################


def list_sequences(request):
 
    sequences = Sequence.objects.all()

    return render(request, 'socle/list_sequences.html', {'sequences': sequences , })


def create_sequence(request, ids=0):

    organisateur = request.user.organisateur
    seq = Sequence.objects.create(title = 'Ma nouvelle séquence', folder = None , organisateur = organisateur)
    return redirect('update_sequence' , seq.pk )

 
def update_sequence(request, ids):

    sequence = Sequence.objects.get(id=ids)
    activities = sequence.activities.order_by("ranking")
    organisateur = request.user.organisateur
    form = SequenceForm(request.POST or None, instance=sequence , organisateur=organisateur  )
    form_code = CodeActivityForm(request.POST or None, request.FILES or None, sequence = sequence )
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            return redirect('sequences')
        else:
            print(form.errors)

    context = {'form': form,   'sequence': sequence, 'activities' : activities , 'form_code' : form_code , }

    return render(request, 'sequence/form_sequence.html', context )


  
def delete_sequence(request, ids):

    sequence = Sequence.objects.get(id=ids)
    if request.user.is_authenticated :
        if request.user.organisateur == sequence.organisateur :
            sequence.delete()
            messages.success(request,'Suppression réalisée avec succès')

    return redirect('sequences')



def ajax_update_sequence(request):

    data = {}
    value =  request.POST.get("value")   
    champ =  request.POST.get("champ")  
    sequence_id =  request.POST.get("sequence_id")  
    if champ == 'title':
        Sequence.objects.filter(pk = sequence_id).update(title = value)
    else :
        Sequence.objects.filter(pk = sequence_id).update(code = value)
    return JsonResponse(data)
 


def ajax_update_checkbox_sequence(request):

    data = {}
    value =  request.POST.get("value")   
    sequence_id =  request.POST.get("sequence_id")  

    sequence = Sequence.objects.get(pk = sequence_id)
    if value == "id_temporisation" :
        if sequence.temporisation :
            sequence.temporisation = 0
            data["html"] = "btn-default off"
        else :
            sequence.temporisation = 1
            data["html"] = "btn-primary"
    elif value == "id_authentification" :
        if sequence.authentification :
            sequence.authentification = 0
            data["html"] = "btn-default off"
        else :
            sequence.authentification = 1
            data["html"] = "btn-primary"
    elif value == "id_pseudonyme" :
        if sequence.pseudonyme :
            sequence.pseudonyme = 0
            data["html"] = "btn-default off"
        else :
            sequence.pseudonyme = 1
            data["html"] = "btn-primary"
    elif value == "id_competition" :
        if sequence.competition :
            sequence.competition = 0
            data["html"] = "btn-default off"
        else :
            sequence.competition = 1
            data["html"] = "btn-primary"
    elif value == "id_terminal" :
        if sequence.terminal :
            sequence.terminal = 0
            data["html"] = "btn-default off"
        else :
            sequence.terminal = 1
            data["html"] = "btn-primary"
    elif value == "id_displayresult" :
        if sequence.displayresult :
            sequence.displayresult = 0
            data["html"] = "btn-default off"
        else :
            sequence.displayresult = 1
            data["html"] = "btn-primary"
    sequence.save()        
    return JsonResponse(data)

 

def moderate_sequence(request, ids):
    sequence = Sequence.objects.get(id=id)
    sequence.delete()

    return redirect('sequences')


def compare_sequence(request, ids):
    sequence = Sequence.objects.get(id=id)
    sequence.delete()

    return redirect('sequences')


def clone_sequence(request, ids):
    sequence = Sequence.objects.get(id=id)
    for a in sequence.activities.all():
        for c in a.choices.all():
            c.pk=None
            c.save()
        a.pk=None
        a.save()
    sequence.pk = None
    sequence.save()

    return redirect('sequences')


def export_sequence(request, ids):
    sequence = Sequence.objects.get(id=id)
    sequence.delete()

    return redirect('sequences')    


def import_sequence(request):

    organisateur = request.user.organisateur
    form  = CodeSequenceForm(request.POST or None, request.FILES or None, organisateur = organisateur )
    if request.method == "POST"  :
        if form.is_valid():
            nf = form.save()
            return redirect('index')



def tdb_sequence(request,ids):

    sequence = Sequence.objects.get(id=ids)
    activities = sequence.activities.order_by("ranking")
    organisateur = request.user.organisateur
    participants = sequence.participants.order_by("user__last_name")
 


    context = {  'sequence': sequence, 'activities' : activities, 'participants' : participants ,  }

    return render(request, 'sequence/tdb_sequence.html', context )



def show_sequence(request,ids):

    sequence = Sequence.objects.get(id=ids)
    activities = sequence.activities.order_by("ranking")
    organisateur = request.user.organisateur
    participants = sequence.participants.order_by("user__last_name")
 
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make('https://play.docadok.org/'+str(sequence.id) , image_factory=factory, box_size=30)
    stream = BytesIO()
    img.save(stream)
    show_qr = stream.getvalue().decode()


    context = {  'sequence': sequence, 'activities' : activities, 'participants' : participants , 'show_qr' : show_qr , }

    return render(request, 'sequence/show_sequence.html', context )




def play_sequence(request,ids):

    sequence = Sequence.objects.get(id=ids)
    activities = sequence.activities.order_by("ranking")
    organisateur = request.user.organisateur
    participants = sequence.participants.order_by("user__last_name")
 
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make('https://play.docadok.org/'+str(sequence.code) , image_factory=factory, box_size=30)
    stream = BytesIO()
    img.save(stream)
    show_qr = stream.getvalue().decode()


    context = {  'sequence': sequence, 'activities' : activities, 'participants' : participants , 'show_qr' : show_qr , }

    return render(request, 'sequence/play_sequence.html', context )


def ajax_sort_sequences(request):

    sequence_ids  = request.POST.getlist("sequences")
    i=0
    for sequence_id in sequence_ids:
        Sequence.objects.filter( pk = sequence_id ).update(ranking = i)
        i+=1
    data = {}
    return JsonResponse(data) 



def ajax_include_folders(request):

    sequence_id  = request.POST.get("sequence_id")
    folder_id  = request.POST.get("folder_id")
    Sequence.objects.filter( pk = sequence_id ).update(folder_id = folder_id)
    data = {}
    return JsonResponse(data) 

 


####################################################################################################
####################################################################################################
####################    Activity
####################################################################################################
####################################################################################################

def get_form(atype,new) :

    if atype == 0 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=extra)
        template = 'sequence/form_qcm.html'
    elif atype == 1 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer') , extra=extra)
        template = 'sequence/form_sondage.html'
    elif atype == 2 :
        formSet  = inlineformset_factory( Activity , Choice , fields=('is_correct',) , extra=0)
        template = 'sequence/form_cloud.html'
    elif atype == 3 : # TODO
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=extra)
        template = 'sequence/form_legend_image.html'
    elif atype == 4 : # TODO
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=extra)
        template = 'sequence/form_find_image.html'
    elif atype == 5 : # TODO
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=extra)
        template = 'sequence/form_cast_image.html'
    elif atype == 6 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','associate','imageassociate') , extra=extra)
        template = 'sequence/form_association.html'
    elif atype == 7 :
        if new : extra=1
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label',) , extra=extra)
        template = 'sequence/form_brainstorming.html'
    elif atype == 8 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer') , extra=extra)
        template = 'sequence/form_ladder.html'
    elif atype == 9 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer') , extra=extra)
        template = 'sequence/form_classement.html'
    elif atype == 10 :
        if new : extra=2
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer') , extra=extra)
        template = 'sequence/form_priorisation.html'
    elif atype == 11 :
        if new : extra=1
        else : extra=0
        formSet  = inlineformset_factory( Activity , Choice , fields=('textarea',) , extra=extra)
        template = 'sequence/form_fill_the_blanks.html'
    return formSet, template


def title_activity(atype) :
    titles_activity = ['Créer une question à choix multiple','Sondage','Nuage de mots','Légender une image',"Trouver l'image","Capture d'image",'Association','Brainstorming','Echelle','Classement','Priorisation','Texte à trous']
    title = titles_activity[atype]
    return title 

def create_activity(request,ids,atype,ida=0):

    sequence = Sequence.objects.get(pk = ids)
    form     = ActivityForm(request.POST or None, request.FILES or None, sequence = sequence, atype = atype)
    formSet, template = get_form(atype,True) 
    form_ans = formSet(request.POST or None,  request.FILES or None)

    if request.method == "POST"  :
        if form.is_valid():
            nf = form.save()
            #############
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()

            return redirect('update_sequence',ids)
        else :
            print(form.errors)

    context = {  'form' : form , 'form_ans' : form_ans , 'sequence' : sequence, 'atype' : atype , 'title_activity' : title_activity(atype)  } 

    return render(request, template , context)

 
def update_activity(request,ids,atype,ida):

    sequence = Sequence.objects.get(pk = ids)
    activity = Activity.objects.get(pk = ida)
    form     = ActivityForm(request.POST or None, request.FILES or None, instance = activity, sequence = sequence, atype = atype)
    formSet, template = get_form(atype,False)  
    form_ans = formSet(request.POST or None  , request.FILES or None, instance = activity)

    if request.method == "POST"  :
        if form.is_valid():
            nf = form.save()
  
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()
            return redirect('update_sequence',ids)

    context = {  'form' : form ,  'form_ans' : form_ans  , 'sequence' : sequence, 'atype' : atype , 'title_activity' : title_activity(atype)    } 
 

    return render(request, template , context)


  
def delete_activity(request,ids,ida):

    sequence = Sequence.objects.get(id=ids)
    activity = Activity.objects.get(id=ida)
    if request.user.is_authenticated :
        if request.user.organisateur == sequence.organisateur :
            activity.delete()
            messages.success(request,'Suppression réalisée avec succès')

    return redirect('index')




def export_activity(request,ids,ida):
    activity = Activity.objects.get(id=ida)
    activity.delete()

    return redirect('update_sequence',ids)


def clone_activity(request,ids,ida):
    activity = Activity.objects.get(id=ida)
    activity.delete()

    return redirect('update_sequence',ids)

def copy_link_activity(request,ids,ida):
    activity = Activity.objects.get(id=ida)
    activity.delete()

    return redirect('update_sequence',ids)


def embed_activity(request,ids,ida):
    activity = Activity.objects.get(id=ida)
    activity.delete()

    return redirect('update_sequence',ids)



def show_activity(request, ida):
    activity = Activity.objects.get(id=ida)
    context = {  'activity' : activity   } 
    template = 'activity/show_activity.html'

    return render(request, template , context)


def import_activity(request,ids):

    sequence = Sequence.objects.get(pk = ids)
    form  = CodeActivityForm(request.POST or None, request.FILES or None, sequence = sequence )
    if request.method == "POST"  :
        if form.is_valid():
            nf = form.save()
            return redirect('update_sequence', ids)



def ajax_sort_activities(request):

    activity_ids  = request.POST.getlist("activities")
    i=0
    for activity_id in activity_ids:
        Activity.objects.filter( pk = activity_id ).update(ranking = i)
        i+=1
    data = {}
    return JsonResponse(data) 
