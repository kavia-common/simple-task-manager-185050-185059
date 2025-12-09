from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""
    list_display = ("id", "title", "completed", "due_date", "created_at", "updated_at")
    list_filter = ("completed", "due_date", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
