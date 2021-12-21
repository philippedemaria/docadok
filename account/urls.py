#################################
#### Auteur : philipe Demaria 
#### pour SACADO
#################################
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from account.views import *

urlpatterns = [
    path('login', view=LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout', logout_view, name='logout'),

    path('dashboard', view=DashboardView.as_view(), name='dashboard'),
 

    path('password/reset/', passwordResetView, name='password_reset'),
    path('password/reset/done/', passwordResetDoneView, name='password_reset_done'),
    path('newpassword/<slug:code>', passwordResetConfirmView, name='password_reset_confirm'),
 
    path('init_password_teacher/<int:id>', init_password_teacher, name='init_password_teacher'),

 

    path('update_teacher/<int:pk>', update_teacher, name='update_teacher'),
    path('delete_teacher/<int:id>', delete_teacher, name='delete_teacher'),
    path('dissociate_teacher/<int:id>', dissociate_teacher, name='dissociate_teacher'),
 
    path('register_teacher', register_teacher, name='register_teacher'),

    path('my_profile', my_profile, name='my_profile'),

]