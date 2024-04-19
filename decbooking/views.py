from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import decbooking
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
   


@csrf_exempt
def booking_processd(request):
    if request.method=='POST':  
        data = json.loads(request.body.decode('utf-8'))
  
        name = data.get('name')
        location = data.get('location')
        cost = data.get('cost')
        check_in = data.get('date')

        check_out = data.get('end_date')
        print(check_in,check_out)
        check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

        # Create and save the booking object
        booking_obj = decbooking(
            User =request.user.username,
            Name=name,
            Location=location,
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
        return render(request, 'decbooking/bookingprocessd.html',{'username':request.user.username})
