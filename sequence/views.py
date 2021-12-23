from django.shortcuts import render, redirect
from django.http import JsonResponse 
from django.core import serializers
from django.template.loader import render_to_string

from sequence.models import Sequence, Folder
from sequence.forms import SequenceForm, FolderForm




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
