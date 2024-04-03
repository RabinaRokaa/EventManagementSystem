from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'checking'

urlpatterns = [
    path('venueList/', views.VenuesList, name= "VenuesList"),  #Path for the register page
    path('checkingList/', views.CheckingList.as_view(), name= "CheckingList"),  #Path for the register page
    path('book/', views.BookingView.as_view(), name= "booking_view"),  #Path for the register page
    path('room/', views.VenueDetailView.as_view(), name= "VenueDetailView"),  #Path for the register page
    
]

