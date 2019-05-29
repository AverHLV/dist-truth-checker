from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TextsAdmin


@admin.register(TextsAdmin)
class StaffAdmin(UserAdmin):
    model = TextsAdmin
    list_display = 'username', 'is_active', 'is_staff', 'is_superuser'
    search_fields = 'username',
    ordering = '-date_joined',


StaffAdmin.fieldsets += ('StaffAdmin fields', {'fields': ('token',)}),
