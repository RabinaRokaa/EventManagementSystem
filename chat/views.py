from django.shortcuts import render

# Create your views here.
def chat(req):
    return render (req, "chat/chat.html")

def chatinside(req):
    return render (req, "chat/chat.html")
