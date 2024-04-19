from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from .models import decoration
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from .models import  ImageFile
from .forms import DecorationForm
from .models import ImageFile

from django.core.serializers import serialize

# Create your views here.
def decoration_list(request):
    decorations = decoration.objects.all()  #fetch decorationss from the database
    return render(request, 'decoration/decoration_list.html', {'decorations': decorations})

from django.shortcuts import redirect

# def adddecoration(request):
#     if request.method == 'POST':
#         form = DecorationForm(request.POST, request.FILES)
#         if form.is_valid():
#             decoration = form.save()  # Save the form data to the database
#             print(decoration)
           
#             # Handle multiple uploaded files and associate them with the decoration
#             for image in request.FILES.getlist('Decoration_image'):
#                 image_instance = ImageFile.objects.create(image=image)
#                 decoration.Decoration_image.add(image_instance)
            
#             return redirect('decoration_list')  # Redirect to a success page
#     else:
#         form = DecorationForm()
#     return render(request, "decoration/adddecoration.html", {'form': form})

def adddecoration(request):
    if request.method == 'POST':
        form = DecorationForm(request.POST, request.FILES)
        if form.is_valid():
            decoration = form.save(commit=False)  # Save the form data without committing to the database yet
            decoration.save()  # Save the decorations instance to get an ID
            
            # Handle multiple uploaded files and associate them with the decorations
            for image in request.FILES.getlist('Decoration_image'):
                image_instance = ImageFile.objects.create(image=image)
                decoration.Decoration_image.add(image_instance)
            return HttpResponse('<script>alert("Decoration added successfully!"); window.location.href = "/decoration_list";</script>')  # Redirect to a success page
    else:
        form = DecorationForm()
    return render(request, "decoration/adddecoration.html" , {'form': form})
    
from django.shortcuts import render, redirect, get_object_or_404
# from .forms import VenuesForm
from .models import ImageFile

# def update_venue(request, venue_id):
#     from django.conf import settings

#     venue = get_object_or_404(decoration, pk=venue_id)

#     if request.method == 'POST':
#         form = VenuesForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             venue = form.save(commit=False)
#             venue.save()

#             # Clear existing images associated with the venue
#             # venue.Venue_image.clear()

#             # Handle multiple uploaded files and associate them with the venue
#             for image in request.FILES.getlist('Venue_image'):
#                 image_instance = ImageFile.objects.create(image=image)
#                 venue.Venue_image.add(image_instance)

#             return HttpResponse('<script>alert("Venue updated successfully!"); window.location.href = "/venue_list";</script>')  # Redirect to a success page or wherever you want
#     else:
#         form = VenuesForm(instance=venue)
    
#         # Fetch image URLs associated with the venue
#     image_urls = [request.build_absolute_uri(settings.MEDIA_URL + str(image.image)) for image in venue.Venue_image.all()]


#     return render(request, "Venues/venue_update.html", {'form': form, 'venue': venue,'image_urls': image_urls})



def update_decoration(request, decoration_id):
    from django.conf import settings

    decorations = get_object_or_404(decoration, pk=decoration_id)

    if request.method == 'POST':
        form = DecorationForm(request.POST, request.FILES, instance=decorations)
        if form.is_valid():
            decorations = form.save(commit=False)
            decorations.save()

            # Clear existing images associated with the decorations
            # decorations.Decoration_image.clear()

            # Handle multiple uploaded files and associate them with the decorations
            for image in request.FILES.getlist('Decoration_image'):
                image_instance = ImageFile.objects.create(image=image)
                decorations.Decoration_image.add(image_instance)

            return HttpResponse('<script>alert("decorations updated successfully!"); window.location.href = "/decoration_list";</script>')  # Redirect to a success page or wherever you want
    else:
        form = DecorationForm(instance=decorations)
    
        # Fetch image URLs associated with the decorations
    image_urls = [request.build_absolute_uri(settings.MEDIA_URL + str(image.image)) for image in decorations.Decoration_image.all()]

    return render(request, "decoration/update_decoration.html", {'form': form, 'decorations': decorations,'image_urls': image_urls})

from django.http import JsonResponse

def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ImageFile, pk=image_id)
        image.delete()
        return JsonResponse({'message': 'Image deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    


def delete_decoration(request, id):
    decorations = get_object_or_404(decoration, id= id)
    if request.method == 'GET':
        decorations.delete()
        return redirect('/decoration_list')  # Redirect to decorations list page after delete
    



 
# pass id attribute from urls
#for showing one respective decorations in admin view through id we have to pass id
def view_decoration(request, id):
   
    # Fetch the decorations with the given ID from the database(euta decorations click garda tesko matra data display garna)
    decorations = get_object_or_404(decoration, id=id)
    
    # Render the template with the decorations data
    return render(request, "decoration/view_decoration.html", {'decorations': decorations})    



def decorations(req):
    decorations = decoration.objects.all()  #fetch decorations from the database
    print('lol')
    return render(req, 'decoration/decorations.html', {'decorations': decorations})

def exploredecoration(request, id):
    # Fetch the venue with the given ID from the database(euta venue click garda tesko matra data display garna)
    decorations = get_object_or_404(decoration, id=id)
    
    # Render the template with the venue data
    return render(request, 'decoration/exploredecoration.html', {'decoration': decorations})

from django.http import JsonResponse
from django.db.models import Q
from .models import decoration  # Assuming your model is named 'Decoration'

@require_GET
def search_decoration(request):
    searched = request.GET.get('searched', '')
    
    # Search through Name, Location, and Cost fields
    decorations = decoration.objects.filter(
        Q(Name__icontains=searched) |  
        Q(Cost__icontains=searched)
    ).prefetch_related('Decoration_image')

    # Serialize decoration data including the paths of multiple images
    decorations_data = []
    for decor in decorations:
        decoration_data = {
            'id': decor.id,
            'Name': decor.Name,
            'Type': decor.Type,
            'Description': decor.Description,
            'Cost': decor.Cost,
            # Retrieve paths of associated images
            'decoration_images': [image.image.url for image in decor.Decoration_image.all()]
        }
        decorations_data.append(decoration_data)

    # Return JSON response containing all decoration data
    return JsonResponse({'decorations': decorations_data})


from django.http import JsonResponse
from django.db.models import Q
from .models import decoration
@require_GET
def filter_decorations(request):
    decorations = decoration.objects.all()
    name_contains_query = request.GET.get('Name_contains')
   
    # title_or_author_query = request.GET.get('Name_or_Location')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        decorations = decorations.filter(Name__icontains=name_contains_query)

    # if location_contains_query != '' and location_contains_query is not None:
    #     decorations = decorations.filter(Location__icontains=location_contains_query)

    # if title_or_author_query != '' and title_or_author_query is not None:
    #     decorations = decorations.filter(Q(Name__icontains=title_or_author_query) | Q(Location__icontains=title_or_author_query)).distinct()
    
    if min_cost:
        decorations = decorations.filter(Cost__gte=min_cost)

    if max_cost:
        decorations = decorations.filter(Cost__lte=max_cost)

    data = [{
        'Name': decoration.Name,        
        'Description': decoration.Description,
        'Cost': decoration.Cost,
        'decoration_images': [image.image.url for image in decoration.Decoration_image.all()],
        'id':decoration.id
        
    } for decoration in decorations]


    # Return JSON response
    return JsonResponse({'decorations': data})
