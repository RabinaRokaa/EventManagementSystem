from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import view_photographer 

urlpatterns = [
    path('addphotographer', views.addphotographer, name= "addphotographer"),  #Path for the register page
    path('photographer_list', views.photographer_list, name= "photographer_list"),  #Path for the register page
    path('<photographer_id>/delete_photographer', views.delete_photographer, name= "delete_photographer"),  #Path for the register page
    path('<id>/view_photographer', views.view_photographer, name= "view_photographer"),  #Path for the register page
    path('<photographer_id>/update_photographer', views.update_photographer, name= "update_photographer"),  #Path for the register
    path('photographers', views.photographers, name= "photographers"),  #Path for the register page
    path('<int:id>/explorephotographer', views.explorephotographer, name="explorephotographer"),
    path('api/filter_photographers', views.filter_photographers, name= "filter_photographers"),
     path('api/search_photographer', views.search_photographer, name= "search_photographer"),
     path('delete_imagep/<int:image_id>/', views.delete_imagep, name='delete_imagep'),
]    