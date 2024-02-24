from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import VenuesForm

from Venues.models import Venues



def venues(req):
    
    venues = Venues.objects.all()  #fetch venues from the database
    return render(req, 'venues/venue.html', {'venues': venues})

def venue_list(request):
    venues = Venues.objects.all()  #fetch venues from the database
    return render(request, 'venues/venue_list.html', {'venues': venues})
# Create your views here.
from .forms import VenuesForm

# def addvenue(request):
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES)
#         if form.is_valid():
#             venue = form.save(commit=False)
#             venue.save()
#             for image in request.FILES.getlist('Venue_image'):
#                 venue.venue_image.create(image=image)
#             return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
#     else:
#         form = VenuesForm()
#     return render(request, "Venues/addvenue.html", {'form': form})

# def addvenue(request):
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             for image in request.FILES.getlist('images'):
#                 Venues.Venue_image.create(image=image)
#             return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
#     else:
#         form = VenuesForm()
#     return render(request, "Venues/addvenue.html" , {'form' : form})

# def addvenue(request):
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES)
#         if form.is_valid():
#             venue = form.save()
            
#             return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
#     else:
#         form = VenuesForm()
#     return render(request, "Venues/addvenue.html" , {'form': form})


#last
from .models import Venues, ImageFile

def addvenue(request):
    if request.method == 'POST':
        form = VenuesForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)  # Save the form data without committing to the database yet
            venue.save()  # Save the venue instance to get an ID
            
            # Handle multiple uploaded files and associate them with the venue
            for image in request.FILES.getlist('Venue_image'):
                image_instance = ImageFile.objects.create(image=image)
                venue.Venue_image.add(image_instance)
            
            return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/addvenue";</script>')  # Redirect to a success page
    else:
        form = VenuesForm()
    return render(request, "Venues/addvenue.html" , {'form': form})

# def update_venue(request, id):
#     venue = get_object_or_404(Venues, id= id)
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after update
#     else:
#         form = VenuesForm(instance=venue)
#     return render(request, 'Venues/venue_update.html', {'form': form, 'venue': venue })

# from django.http import HttpResponseRedirect

# def update_venue(request, id):
#     venue = get_object_or_404(Venues, id=id)
#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/venue_list')  # Redirect to venue list page after update
#     else:
#         form = VenuesForm(instance=venue)
#     return render(request, 'Venues/venue_update.html', {'form': form, 'venue': venue})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import VenuesForm
from .models import ImageFile

def update_venue(request, venue_id):
    venue = get_object_or_404(Venues, pk=venue_id)

    if request.method == 'POST':
        form = VenuesForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.save()

            # Clear existing images associated with the venue
            venue.Venue_image.clear()

            # Handle multiple uploaded files and associate them with the venue
            for image in request.FILES.getlist('Venue_image'):
                image_instance = ImageFile.objects.create(image=image)
                venue.Venue_image.add(image_instance)

            return HttpResponse('<script>alert("Venue updated successfully!"); window.location.href = "/venue_list";</script>')  # Redirect to a success page or wherever you want
    else:
        form = VenuesForm(instance=venue)

    return render(request, "Venues/venue_update.html", {'form': form, 'venue': venue})


# def update_venue(request, venue_id):
#     venue = get_object_or_404(Venues, pk=venue_id)

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