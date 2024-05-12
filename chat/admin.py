from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'messaged_to', 'message', 'date')
    search_fields = ('user__username', 'messaged_to__username', 'message')
