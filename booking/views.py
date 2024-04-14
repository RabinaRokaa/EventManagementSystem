from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail

from django.shortcuts import redirect, render
from django.db.models import Q
from django.http import JsonResponse
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from .models import booking

import json

from django.core.serializers import serialize

# Create your views here.
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import booking

# def book_event(request):
#     if request.method == 'POST':
#         event_type = request.POST.get('event_type')
#         name = request.POST.get('name')
#         location = request.POST.get('location')
#         capacity = request.POST.get('capacity')
#         description = request.POST.get('description')
#         decoration = request.POST.get('decoration')
#         photography = request.POST.get('photography')
#         date = request.POST.get('date')
#         end_date = request.POST.get('end_date')
#         cost = request.POST.get('cost')

#         # Create and save the booking object
#         booking_obj = booking(
#             Event_Type=event_type,
#             Name=name,
#             Location=location,
#             Capacity=capacity,
#             Description=description,
#             Decoration=decoration,
#             Photography=photography,
#             Date=date,
#             EndDate=end_date,
#             Cost=cost
#         )
#         booking_obj.save()

#         # Assuming the booking was successful, you can return a success message
#         return JsonResponse({'message': 'Booking successful'})
#     else:
#         # If the request method is not POST, return an error message
#         return JsonResponse({'error': 'Invalid request method'})
from django.shortcuts import render
from django.http import JsonResponse
from .models import booking
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
@csrf_exempt
def book_event(request):
    if request.method == 'POST':
        # Get data from the POST request
        try:
            usr = request.user.id
            if usr is None:
                status = {"status" : 0}
                return JsonResponse(status)
            else:
                print("hi", usr)
                status = {"status" : 1}
                return JsonResponse(status)
        except Exception as e:
            return redirect('login')
            pass
        
       

# Create your views here.
def booking_list(request):
    bookings = booking.objects.all()  #fetch decorationss from the database
    return render(request, 'booking/bookinglist.html', {'bookings': bookings})



from django.shortcuts import render, redirect, get_object_or_404
# from .forms import bookingsForm






def update_booking(request, id):
    return render(request, "booking/booking_update.html", )

from django.http import JsonResponse

# def delete_image(request, image_id):
#     if request.method == 'POST':
#         image = get_object_or_404(ImageFile, pk=image_id)
#         image.delete()
#         return JsonResponse({'message': 'Image deleted successfully'}, status=200)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

# def update_booking(request, booking_id):
#     booking = get_object_or_404(Venues, pk=venue_id)

#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             venue = form.save(commit=False)
#             venue.save()

#             # Clear existing images associated with the venue
#             venue.Venue_image.clear()

#             # Handle multiple uploaded files and associate them with the venue
#             for image in request.FILES.getlist('Venue_image'):
#                 image_instance = ImageFile.objects.create(image=image)
#                 venue.Venue_image.add(image_instance)

#             return redirect('addvenue')  # Redirect to a success page or wherever you want
#     else:
#         form = VenuesForm(instance=venue)

#     return render(request, "Venues/venue_update.html", {'form': form, 'venue_id': venue_id})


# def update_venue(request, id):
#     venue = get_object_or_404(Venues, id=id)
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             # Handle deletion of old file if a new file is provided
#             if 'Venue_image' in form.changed_data:
#                 old_image = venue.Venue_image
#                 if old_image:  # Check if there is an old image
#                     old_image.delete()  # Delete old image from storage
#             form.save()
#             return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after update
#     else:
#         form = VenuesForm(instance=venue)
#     return render(request, 'Venues/venue_update.html', {'form': form})
# from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
# from .models import Venues
# from .forms import VenuesForm

# def update_venue(request, id):
#     venue = get_object_or_404(Venues, id=id)
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             # Delete old image if a new one is uploaded
#             if 'Venue_image' in request.FILES:
#                 old_image = venue.Venue_image
#                 if old_image:  # Check if there's an old image
#                     old_image.delete()  # Delete old image from storage
#             form.save()
#             return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after update
#     else:
#         form = VenuesForm(instance=venue)
#     return render(request, 'Venues/venue_update.html', {'form': form, 'venue': venue})



# def delete_booking(request, id):
#     bookings = get_object_or_404(booking, id=id)
#     if request.method == 'POST':
#         bookings.delete()
#         return HttpResponseRedirect('/booking_list')  # Redirect to booking list page after delete
#     return render(request, 'booking/delete_booking.html', {'bookings': bookings})



 
# pass id attribute from urls
#for showing one respective booking in admin view through id we have to pass id
def view_booking(request, id):
    # Fetch the booking with the given ID from the database(euta booking click garda tesko matra data display garna)
    bookings = get_object_or_404(booking, id=id)
    # Render the template with the booking data
    return render(request, 'booking/view_booking.html', {'bookings': bookings})



from django.shortcuts import render, get_object_or_404, redirect
from .models import booking


def booking_list(request):
    bookings = booking.objects.all()
    return render(request, 'booking/bookinglist.html', {'bookings': bookings})

def booking_detail(request, pk):
    bookings = get_object_or_404(booking, pk=pk)
    return render(request, 'booking/view_booking.html', {'bookings': bookings})

def booking_update(request, pk):
    bookings = get_object_or_404(booking, pk=pk)
    if request.method == 'POST':
    #     form = BookingForm(request.POST, instance=booking)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('booking_list')
    # else:
    #     form = BookingForm(instance=booking)
       return render(request, 'booking/update_booking.html', {'bookings': bookings})
    


from django.shortcuts import render, get_object_or_404, redirect
from .models import booking
#from .forms import BookingForm   Assuming you have a form defined

# def booking_update(request, pk):
#     booking_instance = get_object_or_404(booking, pk=pk)
    
#     if request.method == 'POST':
#         form = BookingForm(request.POST, instance=booking_instance)
#         if form.is_valid():
#             form.save()
#             return redirect('booking_list')  # Assuming you have a URL named 'booking_list'
#     else:
#         form = BookingForm(instance=booking_instance)
    
#     return render(request, 'booking/update_booking.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import booking

def delete_booking(request, id):
    
    bookings = get_object_or_404(booking, id=id)
    if request.method == 'GET':
        bookings.delete()
        return redirect('/booking_list')  # Redirect to the booking list page after deletion
    # return render(request, 'booking/deletebooking.html', {'bookings': bookings})


@csrf_exempt
def booking_process(request):
    if request.method=='POST':  
        data = json.loads(request.body.decode('utf-8'))
  
        name = data.get('name')
        location = data.get('location')
        capacity = data.get('capacity')
        event_type = data.get('event_type')
        cost = data.get('cost')
        check_in = data.get('date')

        check_out = data.get('end_date')
        print(check_in,check_out)
        check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

        # Create and save the booking object
        booking_obj = booking(
            User =request.user.username,
            Name=name,
            Location=location,
            Capacity=capacity,
            Event_Type=event_type,
            Cost=int(cost),
            Date=check_in,
            EndDate=check_out
        )
        booking_obj.save()
 # Construct a dictionary containing the data
        data = {
            'User': request.user.username,
            'FirstName': request.user.first_name,
            'LastName': request.user.last_name,
            'Email': request.user.email,
            
            'Name': name,
            'Location': location,
            'Capacity': capacity,
            'Event_Type': event_type,
            'Cost': int(cost),
            'Date': check_in,
            'EndDate': check_out
        }

        # Return the data in a JSON response
        return JsonResponse({'data': data, 'message': 'Booking successful'})
    else:
        print(request.user.username)
        print(request.user.first_name)

        # If the request method is not POST, return an error message
        return render(request, 'booking/bookingprocess.html',{'username':request.user.username})
    

from django.shortcuts import render
from .models import booking

def total_bookings_view(request):
    total_bookings = booking.total_bookings()
    print("chor",total_bookings)
    return render(request, 'loginAuthentication/adminpanel.html', {'total_bookings': total_bookings})

