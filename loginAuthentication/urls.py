from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views





urlpatterns = [
    path('', views.home, name= "home"),   #Path for the home page
    path('Register', views.register, name= "register"),  #Path for the register page
    path('Login', views.user_login, name= "login"),    #Path for the login page
    path('LogOut', views.logOut, name= "logOut"), #Path for the logout page
    path('activate/<uidb64>/<token>', views.activate, name= "activate"), #Path for the activated account
    # path('dashboard/',views.dashboard,name='dashboard'),
    path('landingpage/',views.landingpage,name='landingpage'),
    path('organizerpanel/',views.organizerpanel,name='organizerpanel'),
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('user_list/',views.userlist,name='userlist'),
    path('<id>/view_venue',views.view_user,name='view_user'),
    # path('<id>/delete_venue',views.delete_user,name='delete_user'),
     path('<id>/delete_user', views.delete_user, name='delete_user'),
    # path('password_reset/',views.resetpassword,name='password_reset'),
    #give template name for using the customized page not default django page
    path('password_reset_form/', views.PasswordResetCustomView.as_view(template_name='loginAuthentication/password_reset_form.html'), name='password_reset_form'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='loginAuthentication/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmCustomView.as_view(template_name='loginAuthentication/password_reset_confirm.html'), name ='password_reset_confirm'),
    
    # path('password_reset_confirm/',auth_views.PasswordResetConfirmView.as_view(template_name='loginAuthentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='loginAuthentication/password_reset_complete.html'), name='password_reset_complete'),
]



