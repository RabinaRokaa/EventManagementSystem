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
    path('<venue_id>/update_venue', views.update_venue, name= "update_venue"),  #Path for the register page
    path('<id>/delete_venue', views.delete_venue, name= "delete_venue"),  #Path for the register page
   
     path('<id>/view_venue', views.view_venue, name= "view_venue"),
     path('venue', views.venues, name= "venues"),
     path('filterform', views.filterform, name= "filterform"),
     path('api/filter_venues', views.filter_venues, name= "filter_venues"),
     path('api/search_venue', views.search_venue, name= "search_venue"),
     path('<int:id>/explorevenue/', views.explorevenue, name="explorevenue"),
     path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),

    # path('api/search-city',views.searchCity,name='searchcity')

]