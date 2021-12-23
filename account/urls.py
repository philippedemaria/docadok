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
 
    path('init_password_organisateur/<int:id>', init_password_organisateur, name='init_password_organisateur'),

 

    path('update_organisateur/<int:pk>', update_organisateur, name='update_organisateur'),
    path('delete_organisateur/<int:id>', delete_organisateur, name='delete_organisateur'),
    path('dissociate_organisateur/<int:id>', dissociate_organisateur, name='dissociate_organisateur'),
 
    path('register_organisateur', register_organisateur, name='register_organisateur'),

    path('my_profile', my_profile, name='my_profile'),

]