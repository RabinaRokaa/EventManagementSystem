from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_login','is_active', 'is_superuser')

# Register the custom admin class with the User model
# admin.site.unregister(User)  # Unregister the built-in User admin
admin.site.register(User, UserAdmin)  # Register the custom admin

