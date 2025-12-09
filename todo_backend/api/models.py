from django.db import models


class Task(models.Model):
    """
    Task model representing a to-do item with title, optional description,
    completion status, and timestamps.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Set on create
    updated_at = models.DateTimeField(auto_now=True)      # Set on each save

    def __str__(self) -> str:
        return f"{self.title} ({'done' if self.completed else 'pending'})"
