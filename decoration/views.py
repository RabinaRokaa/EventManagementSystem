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
    if request.method == 'POST':
        decorations.delete()
        return HttpResponseRedirect('/decoration_list')  # Redirect to decorations list page after delete
    return render(request, "decoration/delete_decoration.html", {'decorations': decorations})



 
# pass id attribute from urls
#for showing one respective decorations in admin view through id we have to pass id
def view_decoration(request, id):
   
    # Fetch the decorations with the given ID from the database(euta decorations click garda tesko matra data display garna)
    decorations = get_object_or_404(decoration, id=id)
    
    # Render the template with the decorations data
    return render(request, "decoration/view_decoration.html", {'decorations': decorations})    