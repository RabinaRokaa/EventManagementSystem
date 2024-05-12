from django.shortcuts import render
from django.db.models import Q

# Create your views here.
def chat(req):
    messages = Message.objects.filter(Q(user=req.user) | Q(messaged_to__username='admin'))
    for message in messages:
        print(message)
        print('hey')

    return render (req, "chat/chat.html" ,{'messages': messages})





def chatinside(req):
    messages = Message.objects.filter(messaged_to=req.user)

    return render (req, "chat/chat.html" ,{'messages': messages})
  


# views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt


import json

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sender = request.user
        message = data.get('message', '')
        receiver_username = 'admin'
        if message:
            if receiver_username:
                receivers = User.objects.filter(username=receiver_username)
                if receivers.exists():
                    # If multiple users found, take the first one
                    receiver = receivers.first()
                    if receiver.is_superuser:
                        sender, receiver = sender, receiver
                    else:
                        sender, receiver = receiver, sender
                else:
                    return JsonResponse({'status': 'error', 'message': 'Receiver not found'})
            else:
                receiver = User.objects.get(is_superuser=True)
            Message.objects.create(user=sender, message=message, messaged_to=receiver)

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




