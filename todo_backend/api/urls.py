from django.urls import path
from .views import (
    health,
    tasks_list_create,
    tasks_detail,
    tasks_toggle_complete,
)

urlpatterns = [
    path('health/', health, name='Health'),

    # Task endpoints
    path('tasks/', tasks_list_create, name='tasks-list'),
    path('tasks/<int:pk>/', tasks_detail, name='tasks-detail'),
    path('tasks/<int:pk>/toggle-complete/', tasks_toggle_complete, name='tasks-toggle-complete'),
]
