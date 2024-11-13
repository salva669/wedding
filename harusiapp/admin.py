# admin.py
from django.contrib import admin
from .models import UserType, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register the UserType model
admin.site.register(UserType)

# Register the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type']  # Display user type in list
    list_filter = ['user_type']  # Filter by user type
    search_fields = ['username', 'email']  # Enable search by username and email
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
