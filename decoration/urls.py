from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('adddecoration', views.adddecoration, name= "adddecoration"),  #Path for the register page
    path('decoration_list', views.decoration_list, name= "decoration_list"),  #Path for the register page
    path('decorations', views.decorations, name= "decorations"),  #Path for the register page
    path('<int:id>/exploredecoration', views.exploredecoration, name="exploredecoration"),
    path('decoration_list', views.decoration_list, name= "decoration_list"),  #Path for the register page
    path('<id>/view_decoration', views.view_decoration, name= "view_decoration"),  #Path for the register page
    path('<decoration_id>/update_decoration', views.update_decoration, name= "update_decoration"),  #Path for the register page
    path('<id>/delete_decoration', views.delete_decoration, name= "delete_decoration"),  #Path for the register page
    path('api/filter_decorations', views.filter_decorations, name= "filter_decorations"),
    path('api/search_decoration', views.search_decoration, name= "search_decoration"),
   
    #  path('<id>/view_decoration', views.view_decoration, name= "view_decoration"),
    #  path('decoration', views.decorations, name= "decorations"),
    #  path('filterform', views.filterform, name= "filterform"),
    #  path('api/filter_decorations', views.filter_decorations, name= "filter_decorations"),
    #  path('api/search_decoration', views.search_decoration, name= "search_decoration"),
    #  path('<int:id>/exploredecoration', views.exploredecoration, name="exploredecoration"),
    #  path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),

    # path('api/search-city',views.searchCity,name='searchcity')

]