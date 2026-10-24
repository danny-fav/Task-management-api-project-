
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Convert task records to API responses and validate incoming data."""

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
