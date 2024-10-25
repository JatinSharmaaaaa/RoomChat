from django.contrib import admin # type: ignore

# Register your models here.
# admin.py
from .models import Room, Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content', 'timestamp')
    list_filter = ('room', 'timestamp')
    search_fields = ('content', 'user__username', 'room__name')
    date_hierarchy = 'timestamp'