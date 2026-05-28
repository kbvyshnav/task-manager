# tasks/admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = ['title', 'priority', 'done', 'created_at', 'short_description']

    # Sidebar filters
    list_filter = ['priority', 'done', 'created_at']

    # Search box — searches these fields
    search_fields = ['title', 'description']

    # Default ordering in list
    ordering = ['-created_at']

    # Make 'done' togglable directly in the list (no need to open the record)
    list_editable = ['done']

    # How many records per page
    list_per_page = 20

    # Read-only fields in the edit form
    readonly_fields = ['created_at', 'updated_at']

    # Organise fields in the edit form into sections
    fieldsets = [
        ('Task Details', {
            'fields': ['title', 'description', 'priority']
        }),
        ('Status', {
            'fields': ['done']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']  # collapsible section
        }),
    ]

   