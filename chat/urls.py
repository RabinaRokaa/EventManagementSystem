from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat, name= "chat"),  #Path for chat event
    path('chatinside/', views.chatinside, name= "chatinside"),  #Path for chat inside event
    path('send_message/',views.send_message),
    path('chat_api/',views.chat_api)
]