from django.shortcuts import render, redirect
from sequence.models import Sequence, Folder
from sequence.forms import SequenceForm, FolderForm




def list_sequences(request):
 
    sequences = Sequence.objects.all()

    return render(request, 'socle/list_sequences.html', {'sequences': sequences , })



 
def create_sequence(request, id=0):

    form = SequenceForm(request.POST or None  )

    if form.is_valid():
        nf = form.save()
        return redirect('index')
    else:
        print(form.errors)

    context = {'form': form,   'sequence': None  }

    return render(request, 'event/form_sequence.html', context)

 
def update_event(request, id):

    sequence = Sequence.objects.get(id=id)
    event_form = SequenceForm(request.POST or None, instance=sequence )
    if request.method == "POST" :
        if event_form.is_valid():
            event_form.save()
            return redirect('sequences')
        else:
            print(event_form.errors)

    context = {'form': event_form,   'sequence': sequence,   }

    return render(request, 'sequence/form_sequence.html', context )


  
def delete_event(request, id):
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
