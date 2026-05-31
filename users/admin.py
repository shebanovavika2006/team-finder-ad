from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name", "phone")
    list_filter = ("is_staff", "is_active", "date_joined")
    
    fieldsets = UserAdmin.fieldsets + (
        (
            "Профиль участника",
            {"fields": ("phone", "github_url", "avatar", "about")},
        ),
    )
