
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configure task records in Django Admin."""

    list_display = ("title", "user", "status", "due_date", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
