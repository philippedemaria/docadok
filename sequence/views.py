from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string
from django.forms import inlineformset_factory

from sequence.models import Sequence, Folder , Activity , Choice
from sequence.forms import SequenceForm, FolderForm, ActivityForm  




def list_sequences(request):
 
    sequences = Sequence.objects.all()

    return render(request, 'socle/list_sequences.html', {'sequences': sequences , })


 

 
def create_sequence(request, ids=0):

    organisateur = request.user.organisateur
    seq = Sequence.objects.create(title = 'Ma nouvelle séquence', folder = None , organisateur = organisateur)
    return redirect('update_sequence' , seq.pk )

 
def update_sequence(request, ids):

    sequence = Sequence.objects.get(id=ids)
    organisateur = request.user.organisateur
    form = SequenceForm(request.POST or None, instance=sequence , organisateur=organisateur  )
    if request.method == "POST" :
        if form.is_valid():
            form.save()
            return redirect('sequences')
        else:
            print(form.errors)

    context = {'form': form,   'sequence': sequence,   }

    return render(request, 'sequence/form_sequence.html', context )


  
def delete_sequence(request, ids):
    sequence = Sequence.objects.get(id=id)
    sequence.delete()

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

 

####################################################################################################
####################################################################################################
####################    folder
####################################################################################################
####################################################################################################
def create_folder(request):

    form = FolderForm(request.POST or None  )

    if form.is_valid():
        nf = form.save()
        return redirect('index')
    else:
        print(form.errors)

    context = {'form': form,   'folder': None  }

    return render(request, 'sequence/form_folder.html', context)

 
def update_folder(request, id):

    folder = Folder.objects.get(id=id)
    folder_form = FolderForm(request.POST or None, instance=folder )
    if request.method == "POST" :
        if folder_form.is_valid():
            folder_form.save()
            return redirect('index')
        else:
            print(folder_form.errors)

    context = {'form': folder_form,   'folder': folder,   }

    return render(request, 'event/form_folder.html', context )


  
def delete_folder(request, id):
    folder = Folder.objects.get(id=id)
    folder.delete()

    return redirect('index')



####################################################################################################
####################################################################################################
####################    Activity
####################################################################################################
####################################################################################################
def create_activity(request,ids,atype,ida=0):

    sequence = Sequence.objects.get(pk = ids)

    form     = ActivityForm(request.POST or None, request.FILES or None, sequence = sequence)
    formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=2)
    form_ans = formSet(request.POST or None,  request.FILES or None)

    if request.method == "POST"  :
        if form.is_valid():
            nf.save()
            form.save_m2m()
            #############
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()

            return redirect('update_sequence',ids)

    context = {  'form' : form , 'form_ans' : form_ans , 'sequence' : sequence  } 
    template = 'sequence/form_activity.html'
    return render(request, template , context)

 
def update_activity(request,ids,atype,ida):

    sequence = Sequence.objects.get(pk = ids)
    activity = Activity.objects.get(pk = ida)

    form     = ActivityForm(request.POST or None, request.FILES or None, instance = activity, sequence = sequence)
    formSet  = inlineformset_factory( Activity , Choice , fields=('label','imageanswer','is_correct') , extra=0)
    form_ans = formSet(request.POST or None,  request.FILES or None, instance = question)

    if request.method == "POST"  :
        if form.is_valid():
            nf.save()
            form.save_m2m() 
 
            form_ans = formSet(request.POST or None,  request.FILES or None, instance = nf)
            for form_answer in form_ans :
                if form_answer.is_valid():
                    form_answer.save()
            return redirect('update_sequence',ids)

    context = {  'form' : form ,  'form_ans' : form_ans   } 
    template = 'sequence/form_activity.html'

    return render(request, template , context)


  
def delete_folder(request, id):
    activity = Activity.objects.get(id=id)
    activity.delete()

    return redirect('index')
