from django.contrib import admin
from .models import TodoItem, TodoCategory, TodoTag


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Task Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(TodoCategory)
class TodoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


@admin.register(TodoTag)
class TodoTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
