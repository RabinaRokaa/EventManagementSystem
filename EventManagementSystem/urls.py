"""
URL configuration for EventManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('adminpanel/', admin.views, name='admin'),
    path('', include('loginAuthentication.urls')),  #url for the loginapp
    path('', include('Venues.urls')),  #url for the venueapp
    path('', include('checking.urls')),  #url for the venueapp
    path('', include('booking.urls')),  #url for the bookingapp
    path('', include('decoration.urls')),  #url for the decorationapp
    path('', include('photographer.urls')),  #url for the decorationapp
    path('', include('photographerbooking.urls')),  #url for the photographer booking app
    path('', include('decbooking.urls')),  #url for the decoration booking app
    path('', include('feedback.urls')),  #url for the decoration booking app
    path('', include('chat.urls'))  #url for the decoration booking app
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)