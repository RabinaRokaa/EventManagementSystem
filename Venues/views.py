from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import VenuesForm
from Venues.models import Venues
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Q
from .models import Venues
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from .models import Venues

from django.core.serializers import serialize


def venues(req):
    venues = Venues.objects.all()  #fetch venues from the database
    print('lol')
    return render(req, 'venues/venue.html', {'venues': venues})

def explorevenue(request, id):
    # Fetch the venue with the given ID from the database(euta venue click garda tesko matra data display garna)
    venue = get_object_or_404(Venues, id=id)
    
    # Render the template with the venue data
    return render(request, 'venues/explorevenue.html', {'venue': venue})


@require_GET
def search_venue(request):
    searched = request.GET.get('searched', '')
    
    # Search through Name, Location, and Cost fields
    venues = Venues.objects.filter(
        Q(Name__icontains=searched) | 
        Q(Location__icontains=searched) | 
        Q(Cost__icontains=searched)
    ).prefetch_related('Venue_image')

    # Serialize venues data including the paths of multiple images
    venues_data = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'Name': venue.Name,
            'Location': venue.Location,
            'Type': venue.Type,
            'Description': venue.Description,
            'Capacity': venue.Capacity,
            'Cost': venue.Cost,
            # Retrieve paths of associated images
            'Venue_images': [image.image.url for image in venue.Venue_image.all()]
        }
        venues_data.append(venue_data)

    # Return JSON response
    return JsonResponse({'venues': venues_data})




# @require_GET
# def search_venue(request):
#     searched = request.GET.get('searched', '')
#     # Search through Name, Location, and Cost fields
#     venues = Venues.objects.filter(
#         Q(Name__icontains=searched) | 
#         Q(Location__icontains=searched) | 
#         Q(Cost__icontains=searched)
#     ).prefetch_related('Venue_image').values()
    
#     # Convert the QuerySet to a list and include related image data
#     venues_with_images = []
#     for venue in venues:
#         venue_data = {
#             'Name': venue['Name'],
#             'Location': venue['Location'],
#             'Type': venue['Type'],
#             'Description': venue['Description'],
#             'Capacity': venue['Capacity'],
#             'Cost': venue['Cost'],
#             'Venue_images': [image.image.url for image in venue['Venue_image']]
#         }
#         venues_with_images.append(venue_data)

#     print(venues_with_images)
#     return JsonResponse(venues_with_images, safe=False)


# @require_GET
# def search_venue(request):
#     searched = request.GET.get('searched', '')
#     venues = Venues.objects.filter(Location__icontains=searched).prefetch_related('Venue_image').values()
#     print(venues)
#     return JsonResponse(list(venues), safe=False)



# def search_venue(request):
#     if request.method == "POST":
#         # Getting the searched term from the form
#         searched = request.POST.get('searched')
#         # Query the database for venues matching the searched term
#         venues = Venues.objects.filter(
#     Q(Name__icontains=searched) | 
#     Q(Location__icontains=searched) | 
#     Q(Description__icontains=searched) | 
#     Q(Cost__icontains=searched)
# )

#         # Passing the searched term and the venues found to the template
#         return render(request, 'venues/searchvenue.html', {'searched': searched, 'venues': venues})
#     else:
#         return render(request, 'venues/searchvenue.html', {})



# def explorevenue(request, id):
#     if request.method == 'POST':
#         venue_id = request.POST.get('venue_id')
#         try:
#             venues = Venues.objects.get(id=venue_id)
#             # Fetch other necessary data
#             return render(request, 'venues/explorevenue.html', {'venues': venues})
#         except Venues.DoesNotExist:
#             # Handle venue not found error
#             pass
#     # Handle other cases or provide a default response
#     return render(request, 'venues/explorevenue.html', {})


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
            return HttpResponse('<script>alert("Venue added successfully!"); window.location.href = "/venue_list";</script>')  # Redirect to a success page
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
    from django.conf import settings

    venue = get_object_or_404(Venues, pk=venue_id)

    if request.method == 'POST':
        form = VenuesForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.save()

            # Clear existing images associated with the venue
            # venue.Venue_image.clear()

            # Handle multiple uploaded files and associate them with the venue
            for image in request.FILES.getlist('Venue_image'):
                image_instance = ImageFile.objects.create(image=image)
                venue.Venue_image.add(image_instance)

            return HttpResponse('<script>alert("Venue updated successfully!"); window.location.href = "/venue_list";</script>')  # Redirect to a success page or wherever you want
    else:
        form = VenuesForm(instance=venue)
    
        # Fetch image URLs associated with the venue
    image_urls = [request.build_absolute_uri(settings.MEDIA_URL + str(image.image)) for image in venue.Venue_image.all()]




    return render(request, "Venues/venue_update.html", {'form': form, 'venue': venue,'image_urls': image_urls})

from django.http import JsonResponse

def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ImageFile, pk=image_id)
        image.delete()
        return JsonResponse({'message': 'Image deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

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
#for showing one respective venue in admin view through id we have to pass id
def view_venue(request, id):
   
    # Fetch the venue with the given ID from the database(euta venue click garda tesko matra data display garna)
    venue = get_object_or_404(Venues, id=id)
    
    # Render the template with the venue data
    return render(request, 'venues/view_venue.html', {'venue': venue})


# from django.http import JsonResponse
# from django.views.decorators.http import require_GET
# # from .models import YourModel  # Replace YourModel with your actual model

# @require_GET
# def searchCity(request):
#     location = request.GET.get('location', '')
#     results = Venues.objects.filter(Location__icontains=location).values()  # Assuming location is a field in YourModel
#     return JsonResponse(list(results), safe=False)

from django.http import JsonResponse
from django.db.models import Q
from .models import Venues
@require_GET
def filter_venues(request):
    venues = Venues.objects.all()
    name_contains_query = request.GET.get('Name_contains')
    location_contains_query = request.GET.get('Location_exact')
    title_or_author_query = request.GET.get('Name_or_Location')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        venues = venues.filter(Name__icontains=name_contains_query)

    if location_contains_query != '' and location_contains_query is not None:
        venues = venues.filter(Location__icontains=location_contains_query)

    if title_or_author_query != '' and title_or_author_query is not None:
        venues = venues.filter(Q(Name__icontains=title_or_author_query) | Q(Location__icontains=title_or_author_query)).distinct()
    
    if min_cost:
        venues = venues.filter(Cost__gte=min_cost)

    if max_cost:
        venues = venues.filter(Cost__lte=max_cost)

    data = [{
        'Name': venue.Name,
        'Location': venue.Location,
        'Description': venue.Description,
        'Cost': venue.Cost,
        'Venue_images': [image.image.url for image in venue.Venue_image.all()],
        'id':venue.id
        
    } for venue in venues]


    # Return JSON response
    return JsonResponse({'venues': data})

#name chanage k sanga change garnye ho tei
def filterform(request):
    venues = Venues.objects.all()
    name_contains_query = request.GET.get('Name_contains')
    location_contains_query = request.GET.get('Location_exact')
    title_or_author_query = request.GET.get('Name_or_Location')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        venues = venues.filter(Name__icontains=name_contains_query)

    if location_contains_query != '' and location_contains_query is not None:
        venues = venues.filter(Location__icontains=location_contains_query)

    if title_or_author_query != '' and title_or_author_query is not None:
        venues = venues.filter(Q(Name__icontains=title_or_author_query) | Q(Location__icontains=title_or_author_query)).distinct()
    
    if min_cost:
        venues = venues.filter(Cost__gte=min_cost)

    if max_cost:
        venues = venues.filter(Cost__lte=max_cost)

    context = {
        'venues': venues,
        'categories':['Marriage','Birthday','Conference','Anniversary']
    }
    return render(request, "venues/filterform.html", context)


