#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
import html
import random
import re
from django.conf import settings # récupération de variables globales du settings.py
from statistics import median, StatisticsError
import csv
import pytz
from datetime import datetime 
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q, Avg, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth import   logout
from account.models import User, Teacher, Student
 
 
from .forms import UserForm,StudentForm, TeacherForm
 
 
import uuid



def logout_view(request):
    tracker_execute_exercise(False,request.user)
    logout(request)
    return redirect('index')

                 

def list_teacher(request):
    teachers = User.objects.filter(user_type=User.TEACHER)
    return render(request, 'account/list_teacher.html', {'teachers': teachers})


 


class DashboardView(TemplateView): # lorsque l'utilisateur vient de se connecter.
    template_name = "dashboard.html"

    # Lors de la connexion, analyse les exercices de tous les parcours qui doivent être visible à partir de cette date

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            this_user = User.objects.get(pk=self.request.user.id)
            
            today = time_zone_user(this_user)
            relationships = Relationship.objects.filter(is_publish = 0,start__lte=today,exercise__supportfile__is_title=0)
            for r in relationships :
                Relationship.objects.filter(id=r.id).update(is_publish = 1)

            if self.request.user.is_teacher:  # Teacher

                teacher = Teacher.objects.get(user=self.request.user.id)

                groups = Group.objects.filter(teacher = teacher)

                relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__teacher=teacher, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("parcours")
                parcourses = Parcours.objects.filter(teacher=teacher,is_trash=0) # parcours non liés à un groupe

                communications = Communication.objects.filter(active=1)
                parcours_tab = Parcours.objects.filter(students=None, teacher=teacher)

                context = {'this_user': this_user, 'teacher': teacher, 'relationships': relationships,
                           'parcourses': parcourses, 'groups': groups, 'parcours_tab': parcours_tab, 'today' : today , 
                           'communications': communications, }
            elif self.request.user.is_student:  # Student
                student = Student.objects.get(user=self.request.user.id)

                parcourses = Parcours.objects.filter(students=student, linked=0, is_evaluation=0, is_publish=1,is_trash=0)
                groups = student.students_to_group.all()

                parcours = []
                for p in parcourses:
                    parcours.append(p)
 

                relationships = Relationship.objects.filter(Q(is_publish=1) | Q(start__lte=today), parcours__in=parcours, is_evaluation=0, date_limit__gte=today,exercise__supportfile__is_title=0).order_by("date_limit")
                exercise_tab = []
                for r in relationships:
                    if r not in exercise_tab:
                        exercise_tab.append(r.exercise)

                num = 0
                for e in exercise_tab:
                    if Studentanswer.objects.filter(student=student, exercise=e).count() > 0:
                        num += 1

                nb_relationships = Relationship.objects.filter(Q(is_publish = 1)|Q(start__lte=today), parcours__in=parcours, date_limit__gte=today,exercise__supportfile__is_title=0).count()
                try:
                    ratio = int(num / nb_relationships * 100)
                except:
                    ratio = 0

                ratiowidth = int(0.9*ratio)

                evaluations = Parcours.objects.filter(start__lte=today, stop__gte=today, students=student, is_evaluation=1,is_trash=0)
                studentanswers = Studentanswer.objects.filter(student=student)

                exercises = []
                for studentanswer in studentanswers:
                    if not studentanswer.exercise in exercises:
                        exercises.append(studentanswer.exercise)

                relationships_in_late = Relationship.objects.filter(Q(is_publish=1) | Q(start__lte=today),
                                                                    parcours__in=parcours, is_evaluation=0,
                                                                    date_limit__lt=today).exclude(exercise__in=exercises).order_by("date_limit")

                context = {'student_id': student.user.id, 'student': student, 'relationships': relationships,
                           'ratio': ratio, 'evaluations': evaluations, 'ratiowidth': ratiowidth, 'today' : today , 
                           'relationships_in_late': relationships_in_late}
            elif self.request.user.is_parent:  # Parent

                parent = Parent.objects.get(user=self.request.user)
                students = parent.students.order_by("user__first_name")
                context = {'parent': parent, 'students': students, 'today' : today ,  }

        else: ## Anonymous

            form = AuthenticationForm()
            u_form = UserForm()
            t_form = TeacherForm()
            s_form = StudentForm()
            levels = Level.objects.all()
            exercise_nb = Exercise.objects.filter(supportfile__is_title=0).count()

            exercises = Exercise.objects.filter(supportfile__is_title=0)

            i = random.randrange(0, len(exercises))
            exercise = exercises[i]

            context = {'form': form, 'u_form': u_form, 't_form': t_form, 's_form': s_form,
                       'levels': levels, 'exercise_nb': exercise_nb, 'exercise': exercise }
 
        return context




########################################            MON COMPTE               #########################################

def myaccount(request):
 
    if request.user.is_teacher:
        teacher = Teacher.objects.get(user_id=request.session.get('user_id'))
        context = {'teacher': teacher, }
        return render(request, 'account/teacher_account.html', context)
    else:
        student = Student.objects.get(user_id=request.session.get('user_id'))
        context = {'student': student, }

        return render(request, 'account/student_account.html', context)

#####################################


 
def send_to_teachers(request):
    users = User.objects.filter(user_type=2)
    context = {"users" : users, }
    return render(request,'account/send_message_to_teachers.html', context)




def message_to_teachers_sent(request):
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    users = request.POST.getlist("users")

    rcv = []
    for u_id in users:
        u = User.objects.get(pk=u_id)
        if u.email:
            rcv.append(u.email)

    sending_mail(subject, cleanhtml(unescape_html(message)),  settings.DEFAULT_FROM_EMAIL , rcv)
 
    messages.success(request, 'message envoyé')

    return redirect("dashboard")  


 

 

def newpassword_student(request, id,idg):

    student = get_object_or_404(Student, user_id=id)
    user = student.user
    user.set_password("sacado2020")
    user.save()

    sending_mail('Réinitialisation de mot de passe Sacado', "Bonjour, votre mot de passe est réinitialisé. Il est générique. Votre identifiant est : "+user.username+"\n\n Votre mot de passe est : sacado2020.\n\n  Pour plus de sécurité, vous devez le modifier dès votre connexion.\n\n Pour vous connecter, redirigez-vous vers https://sacado.xyz et cliquez sur le bouton bleu Se connecter.\n Ceci est un mail automatique. Ne pas répondre.", settings.DEFAULT_FROM_EMAIL, [user.email])
 
    if idg > 0 :
        return redirect('show_group', idg )
    else :
        return redirect('school_students')

 

def sender_mail(request,form):

    if request.method == "POST" : 
        subject = request.POST.get("subject") 
        texte = request.POST.get("texte") 
        student_id = request.POST.get("student_id")
 
        student_user =  User.objects.get(pk=student_id)
        rcv = []
        if form.is_valid():
            nf = form.save(commit = False)
            nf.author =  request.user
            nf.save()
            nf.receivers.add(student_user)
            for r in nf.receivers.all():
                rcv.append(r.email)
            sending_mail( cleanhtml(subject), cleanhtml(texte) , settings.DEFAULT_FROM_EMAIL , rcv)
 

        else :
            print(form.errors)
 

 
##############################################################################################################
##
##    Close an account
##
############################################################################################################## 


def close_my_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('index')
    else:
        user = request.user
        today = time_zone_user(user)
        return render(request, 'account/close_my_account.html', {'user': user, 'communications': [], 'today': today, })

#########################################Teacher #######################################################################
 
def register_teacher(request):
    if request.method == 'POST':

        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = User.TEACHER
            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend' )
            teacher = Teacher.objects.create(user=user)

            try :
                #teacher.notify_registration()
                teacher.notify_registration_to_admins()
                msg = "Bonjour "+ user.first_name +" " + user.last_name+",\n\n Votre compte Sacado est maintenant disponible.\n\nVotre identifiant est : "+user.username+".\n\nVotre mot de passe est : "+password+" \n\nPour vous connecter, redirigez-vous vers  https://sacado.xyz .\n\nCeci est un mail automatique. Merci de ne pas répondre."
                msg_ = "Bonjour,\n\n Un enseignant vient de rejoindre SacAdo : " + user.last_name + "  "+user.first_name 
                if user.email :
                    send_mail('INSCRIPTION SACADO', msg ,settings.DEFAULT_FROM_EMAIL,[user.email, ])
            except :
                pass


        else:
            messages.error(request, user_form.errors)

    return redirect("index")



#@can_register
#@is_manager_of_this_school
def update_teacher(request, pk):

    user = get_object_or_404(User, pk=pk)
    teacher = get_object_or_404(Teacher, user=user)
    today = time_zone_user(user)
    user_form = ManagerUpdateForm(request.POST or None, instance=user)
    teacher_form = TeacherForm(request.POST or None, instance=teacher)
    new = False
    if all((user_form.is_valid(), teacher_form.is_valid())):
        user_form.save()
        teacher = teacher_form.save(commit=False)
        teacher.user = user
        teacher.save()
        teacher_form.save_m2m()
        messages.success(request, "Actualisation réussie !")

        test = request.POST.get("listing",None)
 
        if test :
            return redirect('list_teacher')
        elif request.user.is_manager :
            return redirect('school_teachers')
        else :
            return redirect('index') 

    return render(request, 'account/teacher_form.html',
                  {'user_form': user_form, 'new' : new , 'communications': [] , 'today' : today , 
                   'teacher_form': teacher_form,
                   'teacher': teacher})



#@can_register
#@is_manager_of_this_school
def delete_teacher(request, id):

    teacher = get_object_or_404(Teacher, user_id=id)

    supprime , sup  = False , False

    if request.user.is_manager and teacher.user.school == request.user.school : #Si l'enseignant est manager et administre le même étabissement que le prof à supprimer alors on supprime.
        supprime = True
        if teacher.groups.count() > 0 : # si le prof a déjà des groupes, seul lui peut se supprimer
            supprime = False

    if request.user.teacher == teacher or request.user.is_superuser   :
        sup = True
        
    if sup or supprime :
        teacher.user.delete()
        messages.success(request,"Le profil a été supprimé avec succès.")
    else :
        messages.error(request,"Permission refusée. Le profil n'a pas été supprimé. Des groupes sont attribués à cet enseignant. Il faut le dissocer de ses groupes.")

    if request.user.is_superuser :
        return redirect('list_teacher')
    elif request.user.is_manager :
        return redirect('school_teachers')
    else :
        return redirect('index') 


def dissociate_teacher(request, id):

    user = User.objects.get(pk=id)
    this_user = request.user

    if user == this_user or  this_user.is_manager :

        User.objects.filter(pk=id).update(school = None)
 

 
    msg = "Bonjour cher collègue, vous venez d'être dissocié de votre établissement d'affectation. Votre compte reste actif avec vos identifiants habituels. Vous pourrez utiliser Sacado dans votre prochaine affectation. Cordialement."

    if user.email :
        sending_mail('Disociation de compte à un établissement', msg ,
                      settings.DEFAULT_FROM_EMAIL,
                      [user.email, ])



    test = request.POST.get("listing",None)
    if test :
        return redirect('list_teacher')
    elif request.user.is_manager :
        return redirect('school_teachers')
    else :
        return redirect('index') 



#@can_register
#@is_manager_of_this_school
def register_teacher_from_admin(request):
    """"
    Enregistre un enseignant depuis la console admin d'un établissement
    """ 
    user_form = ManagerForm(request.POST or None,initial = {'time_zone': request.user.time_zone , 'country': request.user.country })
    teacher_form = TeacherForm(request.POST or None)
    school = this_school_in_session(request)
    new = False
    if request.method == 'POST':
        if all((user_form.is_valid(),teacher_form.is_valid())):
            u_form = user_form.save(commit=False)
            u_form.password = make_password("sacado2020")
            u_form.user_type = User.TEACHER
            u_form.is_extra = 0
            u_form.time_zone = request.user.time_zone
            u_form.school = school
            u_form.username = get_username(request , u_form.last_name, u_form.first_name)
            u_form.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = u_form
            teacher.save()
            teacher_form.save_m2m()

            sending_mail('Création de compte sur Sacado',
                          f'Bonjour {teacher.user}, votre compte Sacado est maintenant disponible.\r\n\r\nVotre identifiant est {u_form.username} \r\n\r\nVotre mot de passe est : sacado2020 \r\n\r\nVous pourrez le modifier une fois connecté à votre espace personnel.\r\n\r\nPour vous connecter, redirigez-vous vers https://sacado.xyz.\r\n\r\nCeci est un mail automatique. Ne pas répondre.',
                          settings.DEFAULT_FROM_EMAIL,
                          [u_form.email, ])
 
            return redirect('school_teachers')
        else:
            messages.error(request, user_form.errors)
    else:
        new = True

    return render(request, 'account/teacher_form.html',
                  {'user_form': user_form, 'communications': [] ,   "school" : school ,
                   'teacher_form': teacher_form,
                   'new': new, })

 
#@can_register
#@is_manager_of_this_school
def register_by_csv(request, key, idg=0):
    """
    Enregistrement par csv : key est le code du user_type : 0 pour student, 2 pour teacher
    """
    if idg > 0:
        group = Group.objects.get(pk=idg)
        is_teacher = False
    else :
        is_teacher = True
    if request.method == "POST":
        # try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier n'est pas format CSV")
            return HttpResponseRedirect(reverse("register_teacher_csv", args=[key, idg]))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Le fichier est trop lourd (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("register_teacher_csv", args=[key, idg]))
        try:
            file_data = csv_file.read().decode("utf-8")
        except UnicodeDecodeError:
            messages.error(request, 'Erreur..... Votre fichier contient des caractères spéciaux qui ne peuvent pas être décodés. Merci de vérifier que votre fichier .csv est bien encodé au format UTF-8.')
            return HttpResponseRedirect(reverse("register_teacher_csv", args=[key, idg]))

        lines = file_data.split("\r\n")
        # loop over the lines and save them in db. If error , store as string and then display = []
        list_names = ""
        for line in lines:
            try : 
            # loop over the lines and save them in db. If error , store as string and then display
                simple = request.POST.get("simple",None)
                ln, fn, username , password , email , group_name , level , is_username_changed = separate_values(request, line, 2 , simple)   # 2 donne la forme du CSV

                if key == User.TEACHER:  # Enseignant
                    user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=2,
                                                      school=this_school_in_session(request), time_zone=request.user.time_zone,
                                                      is_manager=0,
                                                      defaults={'username': username, 'password': password,
                                                                'is_extra': 0})
                    Teacher.objects.get_or_create(user=user, notification=1, exercise_post=1)
                    group = None
                else:  # Student
                    user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=0,
                                                               school=this_school_in_session(request),
                                                               time_zone=request.user.time_zone, is_manager=0,
                                                               defaults={'username': username, 'password': password,
                                                                         'is_extra': 0})
                    student, creator = Student.objects.get_or_create(user=user, level=group.level, task_post=1)
                    if not creator : #Si l'élève n'est pas créé alors il existe dans des groupes. On l'efface de ses anciens groupes pour l'inscrire à nouveau !
                        for g in student.students_to_group.all():
                            g.students.remove(student)
                    group.students.add(student)

                if is_username_changed :
                    list_names += ln+" "+fn+" : "+username+"; "

                if email != "" :
                    sending_mail('Création de compte sur Sacado',
                      f'Bonjour {user}, votre compte Sacado est maintenant disponible.\r\n\r\nVotre identifiant est {user.username} \r\n\r\nVotre mot de passe est : sacado2020 \r\n\r\nVous pourrez le modifier une fois connecté à votre espace personnel.\r\n\r\nPour vous connecter, redirigez-vous vers https://sacado.xyz.\r\n\r\nCeci est un mail automatique. Ne pas répondre.',
                      settings.DEFAULT_FROM_EMAIL, [email,])
            except :
                pass

        if len(list_names) >  0 :
            if key == User.TEACHER:
                user_type = " enseignants "
            else :
                user_type = " élèves "
            messages.error(request,"Les identifiants des "+user_type+" suivants ont été modifiés lors de la création "+list_names)
 

        if key == User.TEACHER:
            return redirect('school_teachers')
        else:
            return redirect('school_groups')
    else:
        if key == User.TEACHER:
            group = None
        else:
            group = Group.objects.get(pk=idg)

        return render(request, 'account/csv_teachers_or_students.html', {'key': key, 'idg': idg, 'communications' : [],  'group': group ,  'is_teacher': is_teacher })







#@can_register
#@is_manager_of_this_school
def register_users_by_csv(request,key):
    """
    Enregistrement par csv : key est le code du user_type : 0 pour student, 2 pour teacher
    """
    if request.method == "POST":
        # try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier n'est pas format CSV")
            return HttpResponseRedirect(reverse("register_teacher_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Le fichier est trop lourd (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("register_teacher_csv"))
        try:
            file_data = csv_file.read().decode("utf-8")
        except UnicodeDecodeError:
            return HttpResponse('Erreur..... Votre fichier contient des caractères spéciaux qui ne peuvent pas être décodés. Merci de vérifier que votre fichier .csv est bien encodé au format UTF-8.')
 
        lines = file_data.split("\r\n")
        list_names = ""
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            try : 
                simple = request.POST.get("simple",None)
                ln, fn, username , password , email , group_name , level , is_username_changed = separate_values(request, line, 1 , simple) # 2 donne la forme du CSV

                if key == User.TEACHER:  # Enseignant
                    user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=2,
                                                      school=this_school_in_session(request), time_zone=request.user.time_zone,
                                                      is_manager=0,
                                                      defaults={'username': username, 'password': password,
                                                                'is_extra': 0})
                    Teacher.objects.get_or_create(user=user, notification=1, exercise_post=1)
                else:  # Student
                    user, created = User.objects.get_or_create(last_name=ln, first_name=fn, email=email, user_type=0,
                                                               school=this_school_in_session(request),
                                                               time_zone=request.user.time_zone, is_manager=0,
                                                               defaults={'username': username, 'password': password,
                                                                         'is_extra': 0})
                    student, creator = Student.objects.get_or_create(user=user, level_id=level, task_post=1)

                if is_username_changed :
                    list_names += ln+" "+fn+" : "+username+"; "

            except :
                pass
     
        if len(list_names) >  0 :
            if key == User.TEACHER:
                user_type = " enseignants "
            else :
                user_type = " élèves "
            messages.error(request,"Les identifiants des "+user_type+" suivants ont été modifiés lors de la création "+list_names)

        if key == User.TEACHER:
            return redirect('school_teachers')
        else:
            return redirect('school_students')

    else :

        return render(request, 'account/csv_all_teachers_or_students.html', {'key': key , 'communications' : [], })

  
#########################################Lost password #################################################################


def updatepassword(request):

    today = time_zone_user(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            userport = form.save()
            update_session_auth_hash(request, userport) # Important!
            messages.success(request, 'Votre mot de passe a été modifié avec succès !')

            sending_mail('Changement de mot de passe sur sacAdo', 'Bonjour, votre nouveau mot de passe sacado est '+str(request.POST.get("new_password1"))+'. Pour vous connecter, redirigez-vous vers https://sacado.xyz .', settings.DEFAULT_FROM_EMAIL, [request.user.email])

            return redirect('logout')
        else :
            print(form.errors)  
    else:
        form = PasswordChangeForm(request.user)
 
    return render(request, 'account/password_form.html', { 'form': form, 'communications' : [], 'today' : today , })



##############################################################################################################
##############################################################################################################
#    PARENTS
##############################################################################################################
##############################################################################################################


def register_parent(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            code_student = request.POST.get("code_student")
            if Student.objects.filter(code=code_student).exists():
                username = user_form.cleaned_data['last_name'] + user_form.cleaned_data['first_name']
                user = user_form.save(commit=False)
                user.username = username
                user.user_type = User.PARENT
                password = request.POST.get("password1")
                user.set_password(password)
                user.save()
                parent, result = Parent.objects.get_or_create(user=user)
                student = Student.objects.get(code=code_student)
                parent.students.add(student)
            
                user = authenticate(username=username, password = password)
                login(request, user,  backend='django.contrib.auth.backends.ModelBackend' )
                messages.success(request, "Inscription réalisée avec succès !")            
                if user_form.cleaned_data['email'] :
                    sending_mail('Création de compte sur Sacado', 'Bonjour, votre compte SacAdo est maintenant disponible. \n\n Votre identifiant est '+str(username) +". \n\n votre mot de passe est "+str(password)+'.\n\n Pour vous connecter, redirigez-vous vers https://sacado.xyz.\n Ceci est un mail automatique. Ne pas répondre.', settings.DEFAULT_FROM_EMAIL, [request.POST.get("email")])
       
        else:
            messages.error(request, "Erreur lors de l'enregistrement. Reprendre l'inscription...")
    return redirect('index')



def update_parent(request, id):
    user = get_object_or_404(User, pk=id)
    parent = get_object_or_404(Parent, pk=id)
    user_form = UserUpdateForm(request.POST or None, instance=user)
    parent_form = ParentUpdateForm(request.POST or None, instance=student)
    if all((user_form.is_valid(), parent_form.is_valid())):
        user_form.save()
        parent_f = parent_form.save(commit=False)
        parent_f.user = user
        parent_f.save()
        return redirect('index')

    return render(request, 'account/parent_form.html',
                  {'user_form': user_form, 'parent_form': parent_form, 'parent': parent})


def delete_parent(request, id):
    parent = get_object_or_404(Parent, user_id=id)
    parent.delete()
    return redirect('index')




#####################################


def my_profile(request):
    user = request.user
    is_manager = user.is_manager
    is_extra   = user.is_extra
    is_testeur = user.is_testeur
    today = time_zone_user(user)
    if user.is_superuser :
        user_form = ManagerUpdateForm(request.POST or None, request.FILES or None, instance=user)        
    else :
        user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)

    new = False
    if request.user.is_teacher:
        teacher = Teacher.objects.get(user=user)

        teacher_form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
        if request.method == "POST":
            if all((user_form.is_valid(), teacher_form.is_valid())):
                teacher       = teacher_form.save(commit=False)
                teacher.user  = user
                teacher.save()
                teacher_form.save_m2m()
                uf            = user_form.save(commit=False) 
                uf.is_manager = is_manager
                uf.is_extra   = is_extra
                uf.is_testeur = is_testeur
                uf.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                if teacher.groups.count() == 0:
                    return redirect('index')
                else:
                    return redirect('profile')

        return render(request, 'account/teacher_form.html', 
                      {'teacher_form': teacher_form, 'user_form': user_form,'new' : new , 'communications': [] ,  'teacher': teacher, 'today' : today})

    elif request.user.is_student:

        student = Student.objects.get(user=user)
        form = StudentForm(request.POST or None, request.FILES or None, instance=student)
        if request.method == "POST":
            if all((user_form.is_valid(), form.is_valid())):
                user_form.save()
                student_f = form.save(commit=False)
                student_f.user = user
                student_f.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                return redirect('profile')

            else:
                print(form.errors)
        return render(request, 'account/student_form.html',
                      {'form': form, 'user_form': user_form, 'communications' : [],  'student': student, 'idg' : None , 'today' : today })

    else:
        parent = Parent.objects.get(user=user)
        form = ParentForm(request.POST or None, request.FILES or None, instance=parent)
        if request.method == "POST":
            if all((user_form.is_valid(), form.is_valid())):
                user_form.save()
                parent_f = form.save(commit=False)
                parent_f.user = user
                parent_f.save()
                messages.success(request, 'Votre profil a été changé avec succès !')
                return redirect('profile')

            else:
                print(form.errors)
        return render(request, 'account/parent_form.html', {'form': form, 'communications' : [],  'user_form': user_form, 'parent': parent, 'today' : today })


@csrf_exempt
def ajax_userinfo(request):
    username = request.POST.get("username")

    data = {}
    nb_user = User.objects.filter(username=username).count()

    if nb_user > 0:
        data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
        data['test'] = False
    else:
        data['html'] = "<br><i class='fa fa-check text-success'></i>"
        data['test'] = True

    return JsonResponse(data)


@csrf_exempt
def ajax_userinfomail(request):
    email = request.POST.get("email")

    data = {}
    nb_user = User.objects.filter(email=email).count()

    if nb_user > 0:
        data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
        data['test'] = False
    else:
        data['html'] = "<br><i class='fa fa-check text-success'></i>"
        data['test'] = True

    return JsonResponse(data)




def ajax_courseinfo(request):
    groupe_code = request.POST.get("groupe_code")
    data = {}
    try:
        nb_group = Group.objects.filter(code=groupe_code,lock=0).count()
        if nb_group == 1:
            data['htmlg'] = "<br><i class='fa fa-check text-success'></i>"
        else:
            data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Groupe inconnu ou verrouillé."
    except:
        data['htmlg'] = "<br><i class='fa fa-times text-danger'></i> Groupe inconnu ou verrouillé."

    return JsonResponse(data)


def ajax_control_code_student(request):
    data = {}
    try:
        code_student = request.POST.get("code_student")
        nb_user = Student.objects.filter(code=code_student).count()

        if nb_user == 1:
            student = Student.objects.get(code=code_student)
            data[
                'html'] = "<br><i class='fa fa-check text-success'></i> Paire avec " + student.user.first_name + " en " + student.level.name
            data['test'] = True

        else:
            data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
            data['test'] = False

    except:
        data['html'] = "<br><i class='fa fa-times text-danger'></i> Identifiant déjà utilisé."
        data['test'] = False

    return JsonResponse(data)




def ajax_detail_student(request):
    student_id = int(request.POST.get("student_id"))
    theme_id = int(request.POST.get("theme_id"))
    group_id = int(request.POST.get("group_id"))

    user = User.objects.get(pk=student_id)
    group = Group.objects.get(pk=group_id)
    student = Student.objects.get(user=user)

    if theme_id > 0:
        theme = Theme.objects.get(pk=theme_id)
        knowledges = group.level.knowledges.filter(theme=theme)
        context = {'student': student, 'theme': theme, 'group': group, 'knowledges': knowledges}
    else:
        themes = group.level.themes.all()
        context = {'student': student, 'themes': themes, 'group': group}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student.html', context)
 
    return JsonResponse(data)



def ajax_detail_student_exercise(request):
    student_id = int(request.POST.get("student_id"))
    parcours_id = int(request.POST.get("parcours_id"))

    parcours = Parcours.objects.get(pk=parcours_id)
    student = Student.objects.get(user_id=student_id)

    relationships = Relationship.objects.filter(parcours=parcours, students=student,exercise__supportfile__is_title=0).order_by("ranking")
    studentanswers = Studentanswer.objects.filter(student=student, parcours=parcours).order_by("exercise")

    context = {'student': student, 'parcours': parcours, 'studentanswers': studentanswers, 'communications' : [], 
               'relationships': relationships}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student_exercise.html', context)

    return JsonResponse(data)



def ajax_detail_student_parcours(request):
    student_id = int(request.POST.get("student_id"))
    parcours_id = int(request.POST.get("parcours_id"))

    student = Student.objects.get(user_id=student_id)
    parcours = Parcours.objects.get(pk=parcours_id)

    if student.user.school :
        stage = Stage.objects.get(school = student.user.school)
    else :
        stage = { 'low' : 30, 'medium' : 60 , 'up' :80 }        


    relationships = Relationship.objects.filter(parcours=parcours,exercise__supportfile__is_title=0).order_by("ranking")

    context = {'student': student, 'relationships': relationships, 'stage' : stage}

    data = {}
    data['html'] = render_to_string('account/ajax_detail_student_parcours.html', context)

    return JsonResponse(data)


########## oauth social ###################

def ask_usertype(request):
    """
    Authentification avec google et social_django, demande d'informations complémentaires comme
    le type de l'utilisateur ou la classe afin de compléter le profil
    """
    levels = Level.objects.all()
    return render(request, 'account/oauth_usertype.html', {'levels': levels})


##########################################################################################################################
##
## password reset
##
##########################################################################################################################


def passwordResetView(request):

    if request.method == 'POST':
        form = NewpasswordForm(request.POST)
        if form.is_valid():
            this_form = form.save()

            link = "https://sacado.xyz/account/newpassword/"+this_form.code
            msg = "Bonjour, \nvous venez de demander la réinitialisation de votre mot de passe. Cliquez sur le lien suivant : \n"+ link +"\n\nMerci. \n\n Ceci est un mail automatique, ne pas répondre."
          
            send_mail('SacAdo : Ré-initialisation de mot de passe', msg ,settings.DEFAULT_FROM_EMAIL,[this_form.email, ])
            return redirect("password_reset_done")
        else :
            messages.error(request, "une erreur est survenue. Contacter l'équipe SACADO.")
            return redirect('index')

    else :
        messages.error(request, "une erreur est survenue. Contacter l'équipe SACADO.")
        return redirect('index')


def passwordResetDoneView(request):
    return render(request, 'registration/password_reset_done.html', { })



def passwordResetConfirmView(request, code ):
    try :
        np = Newpassword.objects.get(code = code)
        validlink = True
        form = SetnewpasswordForm()
    except :
        validlink = False

    if request.method == 'POST':
        form = SetnewpasswordForm(request.POST)
        if form.is_valid():
            get_new_password = Newpassword.objects.get(code = code)
            users = User.objects.filter(email = get_new_password.email, user_type=2)
            cpt = 0
            for u in users :
                u.password = make_password(request.POST.get('password1'))
                u.save()
                cpt += 1
        if cpt > 1 :
            msg = "Bonjour, \n\n Plusieurs comptes sont associés à cette adresse email : "+ get_new_password.email +"\n\n Votre mot de passe " + request.POST.get('password1') + "\nest attribué à chaque compte associé à cette adresse mail.\n\n Ceci est un mail automatique, ne pas répondre."
        else :
            msg = "Bonjour, \n\n Votre mot de passe : " + request.POST.get('password1') + "\nest attribué.\n\n Ceci est un mail automatique, ne pas répondre."
 
        send_mail('SacAdo : Ré-initialisation de mot de passe', msg ,settings.DEFAULT_FROM_EMAIL,[get_new_password.email, ])
        return render(request, 'registration/password_reset_complete.html', { })


    return render(request, 'registration/password_reset_confirm.html', { 'validlink' : validlink , 'form' : form , 'code' : code , })



def init_password_teacher(request, id ):

    teacher = Teacher.objects.get(pk=id)
    password =  str(uuid.uuid4())[:8]
    teacher.user.password = make_password(password)
 
    msg = "Bonjour, \n\n Votre nouveau mot de passe : " + password + "\nest attribué. Il est généré automatiquement.\n\n Vous pouvez le modifer via votre profil. Ceci est un mail automatique, ne pas répondre.\n\nL'équipe SACADO."
    
    if teacher.user.email :
        send_mail('SacAdo : Ré-initialisation de mot de passe', msg ,settings.DEFAULT_FROM_EMAIL,[teacher.user.email, ])


    return redirect('list_teacher') 