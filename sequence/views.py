from django.shortcuts import render, redirect
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
