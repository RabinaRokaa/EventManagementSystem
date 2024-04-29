from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import feedback

def contact_us(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Save the feedback to the database
        feedback.objects.create(username=username, email=email, message=message)

        # Display success message or redirect to a success page
        return render(request, 'contact_success.html')

    return render(request, 'contact.html')

