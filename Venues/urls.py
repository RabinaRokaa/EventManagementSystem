from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_venue 

urlpatterns = [
    path('addvenue', views.addvenue, name= "addvenue"),  #Path for the register page
    path('venue_list', views.venue_list, name= "venue_list"),  #Path for the register page
    path('<id>/update_venue', views.update_venue, name= "update_venue"),  #Path for the register page
    path('<id>/delete_venue', views.delete_venue, name= "delete_venue"),  #Path for the register page
   
     path('<id>/view_venue', views.view_venue, name= "view_venue"),

]