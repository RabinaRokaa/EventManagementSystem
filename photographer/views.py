from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from .models import photographer
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from .models import  ImageFile
from .forms import PhotographerForm
from .models import ImageFile
from django.contrib import messages

from django.core.serializers import serialize

# Create your views here.
def photographer_list(request):
    photographers = photographer.objects.all()  #fetch photographerss from the database
    return render(request, 'photographer/Photographerlist.html', {'photographers': photographers})


def addphotographer(request):
    if request.method == 'POST':
        form = PhotographerForm(request.POST, request.FILES)
        if form.is_valid():
            photographer = form.save(commit=False)  # Save the form data without committing to the database yet
            photographer.save()  # Save the photographers instance to get an ID
            
            # Handle multiple uploaded files and associate them with the photographers
            for image in request.FILES.getlist('Photographer_image'):
                image_instance = ImageFile.objects.create(image=image)
                photographer.Photographer_image.add(image_instance)
            return HttpResponse('<script>alert("photographer added successfully!"); window.location.href = "/photographer_list";</script>')  # Redirect to a success page
    else:
        form = PhotographerForm()
    return render(request, "photographer/addphotographer.html" , {'form': form})
    


def update_photographer(request, photographer_id):
    from django.conf import settings

    photographers = get_object_or_404(photographer, pk=photographer_id)

    if request.method == 'POST':
        form = PhotographerForm(request.POST, request.FILES, instance=photographers)
        if form.is_valid():
            photographers = form.save(commit=False)
            photographers.save()

            # Clear existing images associated with the photographers
            # photographers.Photographer_image.clear()

            # Handle multiple uploaded files and associate them with the photographers
            for image in request.FILES.getlist('Photographer_image'):
                image_instance = ImageFile.objects.create(image=image)
                photographers.Photographer_image.add(image_instance)

            return HttpResponse('<script>alert("photographers updated successfully!"); window.location.href = "/photographer_list";</script>')  # Redirect to a success page or wherever you want
    else:
        form = PhotographerForm(instance=photographers)
    
        # Fetch image URLs associated with the photographers
    image_urls = [request.build_absolute_uri(settings.MEDIA_URL + str(image.image)) for image in photographers.Photographer_image.all()]
    return render(request, "photographer/update_photographer.html", {'form': form, 'photographers': photographers,'image_urls': image_urls})

from django.http import JsonResponse

def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ImageFile, pk=image_id)
        image.delete()
        return JsonResponse({'message': 'Image deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request m ethod'}, status=400)
    
from django.contrib import messages
from django.http import HttpResponse

def delete_photographer(request, photographer_id):
    photographers = get_object_or_404(photographer, id=photographer_id)
    if request.method == 'GET':
        photographers.delete()
        return redirect('/photographer_list')
    




# def delete_photographer(request, photographer_id):
#     photographers = get_object_or_404(photographer, id=photographer_id)
#     if request.method == 'POST':
#         photographers.delete()
#         messages.success(request, 'Photographer deleted successfully.')
#         return HttpResponseRedirect('/photographer_list')  # Redirect to photographers list page after delete
    
#     return render(request, "photographer/delete_photographer.html", {'photographers': photographers})


# def delete_photographer(request, photographer_id):
#     photographers = get_object_or_404(photographer, id= photographer_id)
#     if request.method == 'POST':
#         photographers.delete()
#         return HttpResponseRedirect('/photographer_list')  # Redirect to photographers list page after delete
    
#     return render(request, "photographer/delete_photographer.html", {'photographers': photographers})



 
# pass id attribute from urls
#for showing one respective photographers in admin view through id we have to pass id
def view_photographer(request, id):
   
    # Fetch the photographers with the given ID from the database(euta photographers click garda tesko matra data display garna)
    photographers = get_object_or_404(photographer, id=id)
    
    # Render the template with the photographers data
    return render(request, "photographer/view_photographer.html", {'photographers': photographers})   



def photographers(req):
    photographers = photographer.objects.all()  #fetch photographers from the database
    print('lol')
    return render(req, 'photographer/photographers.html', {'photographers': photographers})

def explorephotographer(request, id):
    # Fetch the photographers with the given ID from the database(euta photographers click garda tesko matra data display garna)
    photographers = get_object_or_404(photographer, id=id)
    
    # Render the template with the photographers data
    return render(request, 'photographer/explorephotographer.html', {'photographer': photographers})


@require_GET
def search_photographer(request):
    searched = request.GET.get('searched', '')
    
    # Search through Name, Location, and Cost fields
    photographers = photographer.objects.filter(
        Q(Username__icontains=searched) | 
        Q(Cost__icontains=searched)
    ).prefetch_related('Photographer_image')

    # Serialize Photographer data including the paths of multiple images
    Photographers_data = []
    for photo in photographers:
        Photographer_data = {
            'id': photo.id,
            'Name': photo.Username,
            'Cost': photo.Cost,
            # Retrieve paths of associated images
            'Photographer_images': [image.image.url for image in photo.Photographer_image.all()]
        }
        Photographers_data.append(Photographer_data)

    # Return JSON response
    return JsonResponse({'Photographer': Photographers_data})


from django.http import JsonResponse
from django.db.models import Q
from .models import photographer  # Assuming your model is named 'Photographer'

@require_GET
def filter_photographers(request):
    photographers = photographer.objects.all()
    name_contains_query = request.GET.get('Name_contains')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        photographers = photographers.filter(Username__icontains=name_contains_query)

    if min_cost:
        photographers = photographers.filter(Cost__gte=min_cost)

    if max_cost:
        photographers = photographers.filter(Cost__lte=max_cost)

    data = [{
        'Name': photographer.Username,
        # 'Description': photographer.Description,
        'Cost': photographer.Cost,
        'Photographer_images': [image.image.url for image in photographer.Photographer_image.all()],
        'id': photographer.id
    } for photographer in photographers]
 
    return JsonResponse({'photographers': data})
