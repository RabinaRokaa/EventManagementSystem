from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from EventManagementSystem import settings
from .models import photographerbooking
import json

@csrf_exempt
def book_eventp(request):
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
   


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError

@csrf_exempt
def check_booking_availabilityp(request):
    if request.method=="POST":
        
        username = request.POST.get('username')
        date_str = request.POST.get('date')
        #Venue_image = request.POST.get('Venue_image')

        # Parse date string to datetime object
        date = datetime.fromisoformat(date_str)

        # Extract the date part
        date = date.date()

        print(date)
        print(username,date_str,request.user.username)
        # Check if there are any previous bookings
        previous_bookings = photographerbooking.objects.filter(
            #Event_Type=event_type,
            username=username,
            end_date__gt=date, 
        )

        if previous_bookings.exists():
            return JsonResponse({'available': False, 'message': 'Booking not available for the selected date.'})
        else:
            return JsonResponse({'available': True, 'message': 'Booking available for the selected date.'})
    else:
                # Handle GET requests here, maybe return a default response
        return JsonResponse({'error': 'GET requests are not supported for this endpoint.'}, status=405)
def delete_booking(request, id):
    
    bookings = get_object_or_404(photographerbooking, id=id)
    if request.method == 'GET':
        bookings.delete()
        return redirect('/booking_list')  # Redirect to the booking list page after deletion
    # return render(request, 'booking/deletebooking.html', {'bookings': bookings})
import logging
logger = logging.getLogger(__name__)
@csrf_exempt
def booking_processp(request):
    if request.method=='POST':  
       try:
        data = json.loads(request.body.decode('utf-8'))  
        username = data.get('username')
        cost = data.get('cost')
        check_in = data.get('date')
        #Venue_image = request.FILES.get('Venue_image')

        check_out = data.get('end_date')
        print(check_in,check_out)
        check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

        # Create and save the booking object
        booking_obj = photographerbooking(
            User =request.user.username,
            username=username,
            cost=int(cost),
            date=check_in,
           
            end_date=check_out
        )
        #if Venue_image:  # Check if an image was uploaded
            #booking_obj.Venue_image = Venue_image # Associate the image with the venue
        
        booking_obj.save()
 # Construct a dictionary containing the data
        data = {
            'User': request.user.username,
            'FirstName': request.user.first_name,
            'LastName': request.user.last_name,
            'Email': request.user.email,            
            'username': username,
            'cost': int(cost),
            'date': check_in,
            #'Venue_image': Venue_image,
            'end_date': check_out
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
        return render(request, 'photobooking/bookingprocessp.html',{'username':request.user.username})
        # return render(request, 'decbooking/bookingprocessd.html',{'username':request.user.username})
    

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