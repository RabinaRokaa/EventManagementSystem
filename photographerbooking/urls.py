from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'photographerbooking'

urlpatterns = [
    # path('booking_list/', views.booking_list, name= "booking_list"),  #Path for the register page
    # path('view_booking/<booking_id>', views.view_booking, name="view_booking"),
    # path('delete/<int:id>', views.delete_booking, name='delete_booking'),
    # #path('delete_booking/<booking_id>/', views.delete_booking, name="delete_booking"),  
    # path('view_booking/<booking_id>/', views.view_booking, name="view_booking"),
    # path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    # path('booking/<int:pk>/update/', views.booking_update, name='booking_update'),
    # #path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('bookingprocessp/', views.booking_processp, name='bookingprocessp'),
    path('book_eventp/', views.book_eventp, name= "book_eventp"),  #Path for book event
    path('check_booking_availabilityp/', views.check_booking_availabilityp, name= "check_booking_availabilityp"),  #Path for book event
    path('api/verify_payment/', views.verify_payment, name='verify_payment'),
    
]