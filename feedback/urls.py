from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'feedback'

urlpatterns = [
   
    path('contact/', views.contact_us, name='contact'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    
]