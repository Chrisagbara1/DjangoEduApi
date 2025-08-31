
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {"fields": ("is_teacher", "bio", "profile_picture")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra", {"fields": ("is_teacher",)}),
    )
