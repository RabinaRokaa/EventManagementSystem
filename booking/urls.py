from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'booking'

urlpatterns = [
    path('book_event/', views.book_event, name= "book_event"),  #Path for the register page
    
    
]



