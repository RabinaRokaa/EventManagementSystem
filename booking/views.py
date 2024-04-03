from django.shortcuts import render

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

def book_event(request):
    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        event_type = request.POST.get('type')
        cost = request.POST.get('cost')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Create and save the booking object
        booking_obj = booking(
            Name=name,
            Location=location,
            Capacity=capacity,
            Event_Type=event_type,
            Cost=cost,
            Date=check_in,
            EndDate=check_out
        )
        booking_obj.save()

        # Return a success message
        return JsonResponse({'message': 'Booking successful'})
    else:
        # If the request method is not POST, return an error message
        return JsonResponse({'error': 'Invalid request method'})