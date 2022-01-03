from django.shortcuts import render, redirect, get_object_or_404


def RT_Participant(request):
	return render(request,"qcm/fooParticipant.html")
def RT_Tbd(request):
	return render(request,"qcm/fooTbd.html")
def RT_Play(request):
	return render(request,"qcm/fooPlay.html")


