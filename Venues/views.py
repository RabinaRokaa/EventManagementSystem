from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import VenuesForm

from Venues.models import Venues

def venue_list(request):
    venues = Venues.objects.all()
    return render(request, 'venues/venue_list.html', {'venues': venues})
# Create your views here.

def addvenue(request):
    if request.method == 'POST':
        form = VenuesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            for image in request.FILES.getlist('images'):
                Venues.images.create(image=image)
            return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
    else:
        form = VenuesForm()
    return render(request, "Venues/addvenue.html" , {'form' : form})

# def addvenue(request):
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES)
#         if form.is_valid():
#             venue = form.save()
#             for image in request.FILES.getlist('Venue_image'):
#                 venue.Venue_image.create(image=image)
#             return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
#     else:
#         form = VenuesForm()
#     return render(request, "Venues/addvenue.html" , {'form': form})

def update_venue(request, id):
    venue = get_object_or_404(Venues, id= id)
    if request.method == 'POST':
        form = VenuesForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after update
    else:
        form = VenuesForm(instance=venue)
    return render(request, 'Venues/venue_update.html', {'form': form})

def delete_venue(request, id):
    venue = get_object_or_404(Venues, id= id)
    if request.method == 'POST':
        venue.delete()
        return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after delete
    return render(request, 'Venues/delete_venue.html', {'venue': venue})



 
# pass id attribute from urls
def view_venue(request, id):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["data"] = Venues.objects.get(id = id)
         
    return render(request, "venues/view_venue.html", context)