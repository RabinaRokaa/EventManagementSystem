from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
         # Return JavaScript alert response
        return HttpResponse('<script>alert("Your profile has been updated successfully!"); window.location.href = "/contact/";</script>')

    return render(request, 'loginAuthentication/contact.html')

# Create your views here.
def feedback_list(request):
    feedbacks = feedback.objects.all()  #fetch photographerss from the database
    return render(request, 'loginAuthentication/feedback.html', {'feedbacks': feedbacks})


def contact_us_api(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Save the feedback to the database
        feedback.objects.create(username=username, email=email, message=message)

        # Return JSON response
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
