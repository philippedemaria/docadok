from django.shortcuts import render, redirect
from event.models import Event, Folder
from event.forms import EventForm, FolderForm




def list_events(request):
 
    events = Event.objects.all()

    return render(request, 'socle/list_events.html', {'events': events, 'communications' : [] , })



 
def create_event(request):

    form = EventForm(request.POST or None  )

    if form.is_valid():
        nf = form.save()
        return redirect('index')
    else:
        print(form.errors)

    context = {'form': form,   'event': None  }

    return render(request, 'event/form_event.html', context)

 
def update_event(request, id):

    event = Event.objects.get(id=id)
    event_form = EventForm(request.POST or None, instance=event )
    if request.method == "POST" :
        if event_form.is_valid():
            event_form.save()
            return redirect('events')
        else:
            print(event_form.errors)

    context = {'form': event_form,   'event': event,   }

    return render(request, 'event/form_event.html', context )


  
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()

    return redirect('events')


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

    return render(request, 'event/form_folder.html', context)

 
def update_folder(request, id):

    folder = Event.objects.get(id=id)
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
    folder = Event.objects.get(id=id)
    folder.delete()

    return redirect('index')
