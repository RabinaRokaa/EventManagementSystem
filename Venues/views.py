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
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from .models import Reviews


def venues(req):
    venues = Venues.objects.all()  #fetch venues from the database
    print('lol')
    return render(req, 'venues/venue.html', {'venues': venues})

@csrf_exempt
def explorevenue(request, id):
    if request.GET.get("Name",0):
        venue=Venues.objects.get(Name=request.GET.get('Name'))
    else:
    # Fetch the venue with the given ID from the database(euta venue click garda tesko matra data display garna)
        venue = get_object_or_404(Venues, id=id)
        condition1 = Q(status=True) & Q(venue_name=venue.Name)
        reviews=""
        try:
            if request.user:  # Check if the user is logged in
                print("user")
                condition2 = Q(user=request.user) & Q(venue_name=venue.Name)
                reviews = Reviews.objects.filter(condition1 | condition2)
                return render(request, 'venues/explorevenue.html', {'venue': venue, 'reviews': reviews})
            else:
                reviews = Reviews.objects.filter(condition1)
                return render(request, 'venues/explorevenue.html', {'venue': venue, 'reviews': reviews})
        except Exception as e:
            return render(request, 'venues/explorevenue.html', {'venue': venue,'reviews':reviews})
        


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
        print("helloo")
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
    if request.method == 'GET':
        venue.delete()
        return redirect('/venue_list')  # Redirect to venue list page after delete
    # return render(request, 'Venues/delete_venue.html', {'venue': venue})

























 
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


import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import numpy as np


def review_store(request):
    status=True
    sentences = [
        # Positive and Negative Reviews about Venues
        "The wedding venue was absolutely beautiful and spacious, perfect for our big day.", # Positive
        "I booked this venue for my birthday party and it was a great choice, very accommodating staff.", # Positive
        "The location was convenient, but the venue itself was not well-maintained.", # Negative
        "Our event at this venue was fantastic; the facilities were top-notch.", # Positive
        "Not satisfied with the venue as it was too small for the number of guests we had.", # Negative
        # Positive and Negative Reviews about Decoration
        "The decorations were stunning and exceeded our expectations.", # Positive
        "I loved the birthday decorations, they were colorful and vibrant.", # Positive
        "The wedding decor was elegant and added a special touch to our celebration.", # Positive
        "Decorations were okay, but I expected more given the price we paid.", # Negative
        "Disappointed with the decorations, they were not as described in the catalog.", # Negative
        # Positive and Negative Reviews about Photography
        "The photographer captured every special moment beautifully.", # Positive
        "Very happy with the birthday photos, the photographer did an amazing job.", # Positive
        "Our wedding pictures turned out great, very professional work.", # Positive
        "The photographer was late and missed some important shots.", # Negative
        "Photos were average, expected better quality for the price.", # Negative
    # Venue Reviews (Positive and Negative)
        "The venue was perfect for our small, intimate wedding. Everything was flawless.",  # Positive
        "The venue staff were rude and unhelpful. I would not recommend this place.",  # Negative
        "Our birthday celebration at the venue was fantastic! Great service and ambiance.",  # Positive
        "The venue was too expensive for the services provided. Not worth it.",  # Negative
        "Beautiful venue with excellent facilities. We had an amazing time.",  # Positive
        # Decoration Reviews (Positive and Negative)
        "The decorations were creative and unique, adding a magical touch to our wedding.",  # Positive
        "I was very disappointed with the decorations. They looked cheap and tacky.",  # Negative
        "The birthday party decorations were spot on, exactly what we wanted.",  # Positive
        "The decor was underwhelming and didn't match our expectations.",  # Negative
        "Stunning decorations that made our event truly special.",  # Positive
        # Photography Reviews (Positive and Negative)
        "The photographer was very professional and captured beautiful moments.",  # Positive
        "I did not like the photos at all. The photographer missed many key moments.",  # Negative
        "The photography services were top-notch. Highly recommend!",  # Positive
        "The photos were blurry and not well-composed. Very disappointed.",  # Negative
        "Fantastic photographer who made us feel comfortable and took amazing shots.",  # Positive
        # Venue Reviews (Positive and Negative)
        "The venue in Kathmandu was perfect for our traditional wedding. Highly recommend!",  # Positive
        "The venue in Pokhara was disappointing, the staff were not cooperative.",  # Negative
        "Our birthday party at the Bhaktapur venue was fantastic, the ambiance was great.",  # Positive
        "The venue in Lalitpur was too expensive and not well-maintained.",  # Negative
        "Beautiful venue in Chitwan with excellent facilities. We had an amazing time.",  # Positive
        # Decoration Reviews (Positive and Negative)
        "The decorations for our wedding in Patan were stunning and exceeded our expectations.",  # Positive
        "The decorations at the birthday party in Butwal were very disappointing, not as advertised.",  # Negative
        "The decorations in Biratnagar were perfect, exactly what we wanted for our celebration.",  # Positive
        "The decor for the event in Dharan was underwhelming and didn't match our expectations.",  # Negative
        "Amazing decorations in Janakpur that made our event truly special.",  # Positive
        # Photography Reviews (Positive and Negative)
        "The photographer in Kathmandu captured beautiful moments at our wedding.",  # Positive
        "I did not like the photos from the photographer in Pokhara. They missed many key moments.",  # Negative
        "The photography services in Patan were top-notch. Highly recommend!",  # Positive
        "The photos from the Bhaktapur photographer were blurry and not well-composed.",  # Negative
        "Fantastic photographer in Lalitpur who made us feel comfortable and took amazing shots.",  # Positive

        # Venue Reviews (Positive and Negative)
        "The wedding venue had a beautiful view of the Himalayas, making our special day unforgettable.",  # Positive
        "The venue was too small for our guest list and the parking was inadequate.",  # Negative
        "Our event at the traditional Newari venue was fantastic, and the cultural ambiance was a big hit.",  # Positive
        "The venue was expensive but lacked the promised amenities, very disappointing.",  # Negative
        "The riverside venue provided a serene environment perfect for our celebration.",  # Positive
        # Decoration Reviews (Positive and Negative)
        "The wedding decorations were stunning, especially the floral arrangements with marigolds.",  # Positive
        "The decorations were poorly executed and looked nothing like the catalog pictures.",  # Negative
        "The traditional Nepali decor with diyas and flowers added a magical touch to our event.",  # Positive
        "We found the decorations very basic and not worth the money we spent.",  # Negative
        "The intricate decorations with traditional motifs made our event truly special.",  # Positive
        # Photography Reviews (Positive and Negative)
        "The photographer captured the essence of our wedding ceremony with beautiful candid shots.",  # Positive
        "We were unhappy with the photographer as they missed several key moments of the event.",  # Negative
        "The photographer did an excellent job capturing the cultural rituals and emotions.",  # Positive
        "The photos were overexposed and poorly framed, not what we expected.",  # Negative
        "Amazing photography! The photographer really understood how to capture the traditional dances.",  # Positive
        # Venue Reviews (Positive and Negative)
        "The wedding venue had a beautiful view of the Himalayas, making our special day unforgettable.",  # Positive
        "The venue was too small for our guest list and the parking was inadequate.",  # Negative
        "Our event at the traditional Newari venue was fantastic, and the cultural ambiance was a big hit.",  # Positive
        "The venue was expensive but lacked the promised amenities, very disappointing.",  # Negative
        "The riverside venue provided a serene environment perfect for our celebration.",  # Positive
        "The venue's traditional architecture added a unique charm to our event.",  # Positive
        "The venue had poor lighting and sound system which ruined the experience.",  # Negative
        "We loved the outdoor setup at the venue, it was perfect for our wedding photos.",  # Positive
        "The venue was not clean and the service was below average.",  # Negative
        "The venue had a beautiful garden that was perfect for our evening party.",  # Positive
        # Decoration Reviews (Positive and Negative)
        "The wedding decorations were stunning, especially the floral arrangements with marigolds.",  # Positive
        "The decorations were poorly executed and looked nothing like the catalog pictures.",  # Negative
        "The traditional Nepali decor with diyas and flowers added a magical touch to our event.",  # Positive
        "We found the decorations very basic and not worth the money we spent.",  # Negative
        "The intricate decorations with traditional motifs made our event truly special.",  # Positive
        "The decorator did a fantastic job with the mandap, it looked spectacular.",  # Positive
        "The decorations were not done on time, causing a lot of stress before the event.",  # Negative
        "The use of colorful drapes and lights made the venue look vibrant and festive.",  # Positive
        "The decorations were overpriced and did not meet our expectations.",  # Negative
        "The floral arrangements were fresh and beautifully arranged.",  # Positive
        # Photography Reviews (Positive and Negative)
        "The photographer captured the essence of our wedding ceremony with beautiful candid shots.",  # Positive
        "We were unhappy with the photographer as they missed several key moments of the event.",  # Negative
        "The photographer did an excellent job capturing the cultural rituals and emotions.",  # Positive
        "The photos were overexposed and poorly framed, not what we expected.",  # Negative
        "Amazing photography! The photographer really understood how to capture the traditional dances.",  # Positive
        "The photographer was very professional and made everyone feel comfortable.",  # Positive
        "The photos were delivered late and the quality was not good.",  # Negative
        "We loved the pre-wedding shoot, the photographer chose beautiful locations.",  # Positive
        "The photographer did not listen to our requests and missed important shots.",  # Negative
        "Excellent service! The photographer captured every special moment perfectly.",# Positive

        # Venue Reviews (Positive and Negative)
        "The venue's outdoor garden was beautifully decorated with colorful lights, creating a magical atmosphere.",  # Positive
        "We were disappointed with the venue's management; they were unorganized and seemed overwhelmed.",  # Negative
        "The venue's traditional architecture and intricate woodwork added a touch of elegance to our event.",  # Positive
        "The venue's bathrooms were dirty and poorly maintained, which was very off-putting.",  # Negative
        "The venue's location in the heart of the city made it easily accessible for all our guests.",  # Positive
        "The venue's banquet hall was too small for our event, and many of our guests had to stand.",  # Negative
        "The venue's staff were courteous and attentive, ensuring that all our needs were met throughout the event.",  # Positive
        "The venue's air conditioning system was malfunctioning, making it uncomfortably hot for our guests.",  # Negative
        "The venue's rooftop terrace offered breathtaking views of the city skyline, creating a memorable experience.",  # Positive
        "The venue's parking lot was chaotic and poorly managed, causing confusion and delays for our guests.",  # Negative
    
        # Decoration Reviews (Positive and Negative)
        "The decorator's attention to detail was impeccable, and the decorations were absolutely stunning.",  # Positive
        "We were dissatisfied with the decorator's work; the decorations were lackluster and uninspired.",  # Negative
        "The traditional Nepali decorations infused our event with culture and heritage, making it truly special.",  # Positive
        "The decorations were not set up according to our specifications, and several items were missing.",  # Negative
        "The decorator's creative use of flowers and fabrics transformed the venue into a fairytale setting.",  # Positive
        "We were disappointed with the decorator's lack of professionalism and poor communication.",  # Negative
        "The decorations created a festive and celebratory atmosphere that our guests loved.",  # Positive
        "The decorations were overpriced, and we felt like we didn't get value for our money.",  # Negative
        "The decorator went above and beyond to ensure that every corner of the venue was beautifully decorated.",  # Positive
        "We regretted hiring the decorator as the decorations did not meet our expectations.",  # Negative
    
        # Photography Reviews (Positive and Negative)
        "The photographer's creative eye and technical skill resulted in breathtakingly beautiful photos.",  # Positive
        "We were dissatisfied with the photographer's work; the photos were poorly composed and unflattering.",  # Negative
        "The photographer was professional and unobtrusive, capturing candid moments without being intrusive.",  # Positive
        "The photographer missed several key moments of our event, leaving us disappointed.",  # Negative
        "We were thrilled with the photographer's ability to capture the emotion and energy of our event.",  # Positive
        "The photographer was rude and demanding, making everyone feel uncomfortable during the shoot.",  # Negative
        "The photographer's use of light and shadow created dramatic and visually striking images.",  # Positive
        "We felt like the photographer rushed through the shoot, resulting in subpar photos.",  # Negative
        "The photographer's friendly and approachable demeanor put everyone at ease during the shoot.",  # Positive
        "We were disappointed with the photographer's lack of professionalism and attention to detail.",  # Negative
        # Positive Reviews
        "Our event was truly memorable, thanks to the excellent service and attention to detail.",
        "We had a fantastic experience; everything exceeded our expectations!",
        "The ambiance was perfect, creating a magical atmosphere for our celebration.",
        "The staff were friendly and attentive, making sure that every guest felt welcome.",
        "Our event went smoothly, and we couldn't be happier with how everything turned out.",
        
        # Negative Reviews
        "We were disappointed with our experience; there were several issues that were not addressed.",
        "The service was below par, and we encountered several problems throughout the event.",
        "The lack of organization and communication made our experience frustrating and stressful.",
        "We regretted choosing this service; it did not live up to our expectations.",
        "Overall, our experience was disappointing, and we would not recommend it to others.",
        "Our experience exceeded our expectations; everything was perfect from start to finish.",
        "We were impressed by the level of professionalism and attention to detail.",
        "The atmosphere was lively, and everyone had a great time at our event.",
        "The service was impeccable, and the staff went above and beyond to ensure our satisfaction.",
        "We had an amazing experience and would highly recommend it to others.",
        
        # Negative Reviews
        "Our experience was disappointing; there were too many issues that detracted from our enjoyment.",
        "We encountered several problems throughout our event, which left us feeling frustrated.",
        "The lack of coordination and communication made our experience less enjoyable.",
        "We were dissatisfied with the service; it did not meet our expectations.",
        "Overall, our experience fell short of what was promised, and we left feeling disappointed.",
        # Positive Reviews
        "Our experience was simply outstanding; every detail was meticulously taken care of.",
        "We were blown away by the exceptional service and hospitality.",
        "The ambiance was perfect, creating a warm and inviting atmosphere.",
        "The staff were attentive and friendly, ensuring that our event ran smoothly.",
        "Our event was a resounding success, thanks to the top-notch service and attention to detail.",
        
        # Negative Reviews
        "Our experience was marred by multiple issues; it was far from what we expected.",
        "We encountered numerous problems throughout our event, leaving us feeling disappointed.",
        "The lack of professionalism and coordination made our experience frustrating.",
        "We were unsatisfied with the overall service and quality of our experience.",
        "Our experience did not meet our expectations, and we left feeling dissatisfied.",

        "The venue was poorly maintained, with dirty carpets and broken furniture.",
        "We were disappointed with the venue's lack of parking facilities, which caused inconvenience for our guests.",
        "The venue's air conditioning system was faulty, and it was uncomfortably hot throughout the event.",
        "The staff at the venue were unprofessional and rude, making our experience unpleasant.",
        "We encountered several issues with the venue's sound system, which affected the quality of our event.",
        "The venue's location was inconvenient, and many of our guests struggled to find it.",
        "The venue's bathrooms were dirty and poorly maintained, which left a negative impression on our guests.",
        "We regretted choosing this venue; it did not meet our expectations, and we had a disappointing experience.",
        "The venue's lighting was inadequate, and it made the atmosphere dull and uninviting.",
        "The management at the venue was disorganized, and they failed to address our concerns effectively.",


        "We were extremely disappointed with the photographer's work; the photos were blurry and poorly composed.",
        "The photographer arrived late to our event, causing us to miss out on capturing important moments.",
        "We regretted hiring this photographer; they were unprofessional and made our guests feel uncomfortable.",
        "The quality of the photos we received was subpar, and they did not meet our expectations.",
        "The photographer did not listen to our requests and failed to capture the key moments of our event.",
        "We encountered several issues with the photographer's communication and responsiveness.",
        "The photos we received were overexposed and washed out, making them unusable.",
        "We had a terrible experience with this photographer, and we would not recommend them to others.",
        "The photographer's lack of creativity and attention to detail was evident in the photos we received.",
        "Overall, our experience with this photographer was disappointing, and we were left feeling unsatisfied.",
    ]

    # Tokenize and pad the sentences
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(sentences)

    # Load the saved model
    loaded_model = load_model('./sentiment_analysis_model.h5')

    # Make predictions on new sentences
    new_sentences = [request.GET.get('message',"hello")]
    print(new_sentences)
    new_sequences = tokenizer.texts_to_sequences(new_sentences)
    new_padded_sequences = pad_sequences(new_sequences, maxlen=100)

    predictions = loaded_model.predict(new_padded_sequences)

    # Print predictions
    for i, sentence in enumerate(new_sentences):
        print(predictions[i][0])
        if predictions[i][0] >= 0.5:
            status=True
        else:
            status=False

    user = request.user
    message = request.GET.get('message')
    rating = int(request.GET.get('rating'))
    venue_name = request.GET.get('Name')
    status = status  # You should define how 'status' is set

    # Attempt to find an existing review by this user for the given venue_name
    review, created = Reviews.objects.update_or_create(
        user=user,
        venue_name=venue_name,
        defaults={
            'message': message,
            'rating': rating,
            'status': status
        }
    )
    return JsonResponse(
        {
            'status':1
        }
    )
    

