from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'task_count']

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'done', 'due_date', 'category', 'created_at', 'short_description']
    list_filter = ['priority', 'done', 'category', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    list_editable = ['done']
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Task Details', {
            'fields': ['title', 'description', 'priority', 'due_date', 'category']
        }),
        ('Status', {
            'fields': ['done']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def short_description(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '—'
    short_description.short_description = 'Description'

    @admin.action(description='Mark selected tasks as done')
    def mark_done(self, request, queryset):
        updated = queryset.update(done=True)
        self.message_user(request, f'{updated} task(s) marked as done.')

    @admin.action(description='Mark selected tasks as pending')
    def mark_pending(self, request, queryset):
        updated = queryset.update(done=False)
        self.message_user(request, f'{updated} task(s) marked as pending.')

    actions = ['mark_done', 'mark_pending']
