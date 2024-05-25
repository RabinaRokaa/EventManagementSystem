from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render

from django.db.models import Count

from django.http import JsonResponse

def chat(req):
    # Get the currently logged-in user
    current_user = req.user

    # Exclude the currently logged-in user and superusers
    users = User.objects.filter(is_superuser=False).exclude(username=current_user.username)

    # Subquery to annotate each user with the count of associated messages
    users_with_messages = User.objects.annotate(message_count=Count('message'))

    # Filter users to only those who have at least one message
    users_with_messages = users_with_messages.filter(message_count__gt=0)

    receiver_username = req.GET.get('message_to')
    messages = Message.objects.filter(Q(user__username=receiver_username) | Q(messaged_to__username=receiver_username))

    return render(req, "chat/chat.html", {'messages': messages, 'users': users_with_messages})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Message


def chat_api(request):
    # Get the currently logged-in user
    current_user = request.user

    # Exclude the currently logged-in user and superusers
    users = User.objects.filter(is_superuser=False).exclude(username=current_user.username)

    # Subquery to annotate each user with the count of associated messages
    users_with_messages = users.annotate(message_count=Count('message'))

    # Filter users to only those who have at least one message
    users_with_messages = users_with_messages.filter(message_count__gt=0)

    # Get the receiver's username from the GET parameters
    receiver_username = request.GET.get('message_to')
    
    # Fetch messages where the current user or the receiver is involved
    messages = Message.objects.filter(
        Q(user__username=receiver_username) | Q(messaged_to__username=receiver_username)
    ).select_related('user')

    # Serialize messages to JSON-compatible format
    messages_list = []
    for message in messages:
        messages_list.append({
            'username': message.user.username,
            'message': message.message,
        })

    return JsonResponse({'messages': messages_list, 'users': list(users_with_messages.values('username'))})





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
        
        receiver_username =data.get('receiver', '')

        if message:
            if receiver_username:
                receivers = User.objects.filter(username=receiver_username)
                if receivers.exists():
                    # If multiple users found, take the first one
                    receiver = receivers.first()
                    # if receiver.is_superuser:
                    #     sender, receiver = sender, receiver
                    # else:
                    #     sender, receiver = receiver, sender
                else:
                    return JsonResponse({'status': 'error', 'message': 'Receiver not found'})
           

           
            senders = User.objects.filter(username=request.user.username)
            if senders.exists():
                    # If multiple users found, take the first one
                    senders = senders.first()
                    if senders.is_superuser:
                        sender=User.objects.filter(username='admin')
                        sender=sender.first()

            Message.objects.create(user=sender, message=message, messaged_to=receiver)

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
