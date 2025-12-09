from rest_framework import serializers
from .models import Task

# PUBLIC_INTERFACE
class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model covering all fields."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
