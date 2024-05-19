from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_GET
import requests

from EventManagementSystem import settings
from .models import booking
import json
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import JsonResponse
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



@csrf_exempt
def check_booking_availability(request):
    if request.method=="POST":
        event_type = request.POST.get('event_type')
        name = request.POST.get('name')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        Venue_image = request.POST.get('Venue_image')
        id = request.POST.get('id')

        # Parse date string to datetime object
        date = datetime.fromisoformat(date_str)

        # Extract the date part
        date = date.date()

        print(date)
        print(event_type,name,location,date_str,request.user.username)
        # Check if there are any previous bookings
        previous_bookings = booking.objects.filter(
            Event_Type=event_type,
            Name=name,
            Location=location,
            EndDate__gt=date, 
        )

        if previous_bookings.exists():
            return JsonResponse({'available': False, 'message': 'Booking not available for the selected date.'})
        else:
            return JsonResponse({'available': True, 'message': 'Booking available for the selected date.'})

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
from django.http import JsonResponse, HttpResponseServerError


def delete_booking(request, id):
    
    bookings = get_object_or_404(booking, id=id)
    if request.method == 'GET':
        bookings.delete()
        return redirect('/booking_list')  # Redirect to the booking list page after deletion
    # return render(request, 'booking/deletebooking.html', {'bookings': bookings})
import logging
logger = logging.getLogger(__name__)
@csrf_exempt
def booking_process(request):
    if request.method=='POST':  
       try:
        data = json.loads(request.body.decode('utf-8'))  
        print("ksjbjnsdkjfsdjkfns",data)
        name = data.get('name')
        location = data.get('location')
        capacity = data.get('capacity')
        event_type = data.get('event_type')
        cost = data.get('cost')
        check_in = data.get('date')
        Venue_image = request.FILES.get('Venue_image')
        id = request.FILES.get('id')
        check_out = data.get('end_date')
        print(check_in,check_out)
        check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')
        
        if data.get('paidbhayo')==1:
            

            # Create and save the booking object
            booking_obj = booking(
                User =request.user.username,
                Name=name,
                Location=location,
                Capacity=capacity,
                Event_Type=event_type,
                Cost=int(cost),
                Date=check_in,
                id = id,
                payment_status="paid",
                EndDate=check_out
            )
            if Venue_image:  # Check if an image was uploaded
                booking_obj.Venue_image = Venue_image # Associate the image with the venue
        else:
             # Create and save the booking object
            booking_obj = booking(
                User =request.user.username,
                Name=name,
                Location=location,
                Capacity=capacity,
                Event_Type=event_type,
                Cost=int(cost),
                Date=check_in,
                id = id,
                EndDate=check_out
            )
            if Venue_image:  # Check if an image was uploaded
                booking_obj.Venue_image = Venue_image # Associate the image with the venue
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
            'Venue_image': Venue_image,
            'EndDate': check_out,
            'id' : id,
        }

        print("Booking data:", data)

         # Send booking confirmation email with PDF attachment
        send_confirmation(request.user.email, data)

        # Return the data in a JSON response
        return JsonResponse({'data': data, 'message': 'Booking successful.confirmation email sent.'})
       except Exception as e:
            logger.exception("Error in booking process view: %s", e)
            return HttpResponseServerError('An error occurred while processing the booking request.')
    else:
        print(request.user.username)
        print(request.user.first_name)

        # If the request method is not POST, return an error message
        return render(request, 'booking/bookingprocess.html',{'username':request.user.username})
    

from django.shortcuts import render
from .models import booking

def total_bookings_view(request):
    total_bookings = booking.total_bookings()
    print("hi",total_bookings)
    return render(request, 'loginAuthentication/adminpanel.html', {'total_bookings': total_bookings})

from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# def generate_pdf(data):

#     print("Generating PDF content with data:", data)
#     # Generate PDF content
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="booking_confirmation.pdf"'
#     p = canvas.Canvas(response, pagesize=letter)
#     p.drawString(100, 750, "Booking Confirmation")
#     # Add more content as needed
#     p.showPage()
#     p.save()

#     return response.getvalue()
def generate_pdf(data):
    print("Generating PDF content with data:", data)
    
    # Generate PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="booking_confirmation.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Booking Confirmation")

    # Add booking details to the PDF
    y_offset = 700
    for key, value in data.items():
        if key != 'User':  # Skip 'User' field
            text = f"{key}: {value}"
            p.drawString(100, y_offset, text)
            y_offset -= 20  # Adjust vertical position for next line

    p.showPage()
    p.save()

    return response.getvalue()



def send_confirmation(user_email, data):

    print("Sending confirmation email to:", user_email)
    print("Booking data:", data)
    # Generate PDF content
    pdf_content = generate_pdf(data)
    # Send email with PDF attachment
    email_subject = 'Booking Confirmation'
    email_body = 'Please find your booking confirmation attached.'
    from_email = settings.EMAIL_HOST_USER  # Update with your email
    to_email = [user_email]

    email = EmailMessage(
        email_subject,
        email_body,
        from_email,
        to_email
    )
    email.attach('booking_confirmation.pdf', pdf_content, 'application/pdf')
    email.send()

# def view_booking(request, id):
#     # Fetch the booking with the given ID from the database(euta booking click garda tesko matra data display garna)
#     bookings = get_object_or_404(booking, id=id)
#     # Render the template with the booking data
#     return render(request, 'booking/view_booking.html', {'bookings': bookings})

def payment(request):
    return render(request,"booking/payment.html")

from Venues.models import Venues
from booking.models import VenueBookingWithKhalti


@csrf_exempt
def verify_payment(request):
    user = request.user
    print("req body:", request.body)
    try:
        
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    # print("JSOnnnnnnnnnnnnnnnnnnnnnnnnnn",json.loads(request.body))
    data = json.loads(request.body)
    user = user
    token = data.get('token')
    amount = data.get('amount')
    idx = data.get('idx')
    venue = data.get('venue')
    date = data.get('date')
    enddate = data.get('enddate')
    name = data.get('name')
    email = data.get('email')
    amounts = data.get('amount') / 100
    print("amount=========================================", amounts, venue)

    venue_ids = Venues.objects.get(id=venue)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount,
    }
    print(payload)

    headers = {
        # "Authorization": "Key {}".format(settings.KHALTI_SECRET_KEY)
        "Authorization": "Key test_secret_key_59649630408043658f15731f3b740d06"
    }

    print(request.body)
    response = requests.post(url, payload, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print('payment sucesssssssss')
        # email = request.session.get('email', None)
        # email = user.email
        booking = VenueBookingWithKhalti.objects.create(
            user=user,
            venue=venue_ids,
            date=date,
            name=name,
            email=email,
            enddate=enddate,
            status='pending',
            pid=idx,
            payment_status='Paid',
            amount=amounts
        )
        print("Paid amount", amounts)

        send_confirmation(email, data)

        # invoice(email, amount, data.get('product_name'), data.get('idx'))
        # redirect_url = reverse('loginAuthentication:userdashboard')
        # Return redirect response in JSONs
        print({
            'status': True,
            'details': response.json(),
            # 'redirect_url': redirect_url
        })
        return JsonResponse({
            'status': True,
            'details': response.json(),
            # 'redirect_url': redirect_url
        })
    
    else:
        return JsonResponse({
            'status': False,
            'message': 'Payment verification failed'
        })