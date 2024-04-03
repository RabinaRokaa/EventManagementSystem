import datetime
from Venues.models import Venues
from checking.models import Checking

def check_availability(venue, check_in, check_out):
    avail_list =[]
    #like a one single timeline
    booking_list = Checking.objects.filter(venue=venue)
    for booking in booking_list:
        #If the preexsiting booking checkin is after i checkout means if the booking which exist is going to check in after we check out like we are booking
        #or the person who has already booked checkout before i check in then this is gonna be true so we can booked id not we cannot booked
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)        
