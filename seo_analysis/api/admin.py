from django.contrib import admin
from .models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    readonly_fields = 'created', 'message_id'
    search_fields = 'message_id', 'cleared_text'
    ordering = '-created',
    list_filter = 'created',
