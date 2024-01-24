from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name= "home"),   #Path for the home page
    path('Register', views.register, name= "register"),  #Path for the register page
    path('Login', views.user_login, name= "login"),    #Path for the login page
    path('LogOut', views.logOut, name= "logOut"), #Path for the logout page
    path('activate/<uidb64>/<token>', views.activate, name= "activate"), #Path for the activated account
    path('dashboard/',views.dashboard,name='dashboard')
]
