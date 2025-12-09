from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Role & School', {'fields': ('role', 'school')}),
    )
    list_display = ('username', 'email', 'role', 'school', 'is_staff', 'is_active')
    list_filter = ('role', 'school', 'is_staff', 'is_active')

# Register your models here.
