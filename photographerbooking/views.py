from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import photographerbooking
import json
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from EventManagementSystem import settings

from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse, HttpResponseServerError

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
   
@csrf_exempt
def check_booking_availability(request):
    if request.method=="POST":
        event_type = request.POST.get('event_type')
        name = request.POST.get('name')
        date_str = request.POST.get('date')
        #Venue_image = request.POST.get('Venue_image')

        # Parse date string to datetime object
        date = datetime.fromisoformat(date_str)

        # Extract the date part
        date = date.date()

        print(date)
        print(name,date_str,request.user.username)
        # Check if there are any previous bookings
        previous_bookings = photographerbooking.objects.filter(
            Event_Type=event_type,
            Name=name,
            EndDate__gt=date, 
        )

        if previous_bookings.exists():
            return JsonResponse({'available': False, 'message': 'Booking not available for the selected date.'})
        else:
            return JsonResponse({'available': True, 'message': 'Booking available for the selected date.'})

import logging
logger = logging.getLogger(__name__)
@csrf_exempt
def booking_processp(request):
    if request.method=='POST':  
       try:
        data = json.loads(request.body.decode('utf-8'))  
        Username = data.get('Username')
        cost = data.get('cost')
        check_in = data.get('date')
        Venue_image = request.FILES.get('Venue_image')

        check_out = data.get('end_date')
        print(check_in,check_out)
        check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

        # Create and save the booking object
        booking_obj = photographerbooking(
            User =request.user.username,
            Username=Username,
            Cost=int(cost),
            Date=check_in,
           
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
            'Username': Username,
            'Cost': int(cost),
            'Date': check_in,
            #'Venue_image': Venue_image,
            'EndDate': check_out
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