from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Task
from .serializers import TaskSerializer


@swagger_auto_schema(
    method="get",
    operation_summary="Health check",
    operation_description="Simple endpoint to verify the API is running.",
    responses={200: openapi.Response(description="Healthy response")},
    tags=["health"],
)
@api_view(["GET"])
def health(request):
    """Health check endpoint returning a simple JSON payload."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_summary="List Tasks",
    operation_description="Retrieve the list of all tasks.",
    responses={200: TaskSerializer(many=True)},
    tags=["tasks"],
)
@swagger_auto_schema(
    method="post",
    operation_summary="Create Task",
    operation_description="Create a new task.",
    request_body=TaskSerializer,
    responses={201: TaskSerializer()},
    tags=["tasks"],
)
@api_view(["GET", "POST"])
def tasks_list_create(request):
    """
    List all tasks or create a new task.

    GET: Returns a list of tasks.
    POST: Creates a new task with the provided data.
    """
    if request.method == "GET":
        queryset = Task.objects.all().order_by("-created_at")
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve Task",
    operation_description="Retrieve a single task by ID.",
    responses={200: TaskSerializer()},
    tags=["tasks"],
)
@swagger_auto_schema(
    method="put",
    operation_summary="Update Task",
    operation_description="Update a task by replacing all fields.",
    request_body=TaskSerializer,
    responses={200: TaskSerializer()},
    tags=["tasks"],
)
@swagger_auto_schema(
    method="patch",
    operation_summary="Partial Update Task",
    operation_description="Partially update fields of a task.",
    request_body=TaskSerializer(partial=True),
    responses={200: TaskSerializer()},
    tags=["tasks"],
)
@swagger_auto_schema(
    method="delete",
    operation_summary="Delete Task",
    operation_description="Delete the specified task.",
    responses={204: "No Content"},
    tags=["tasks"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def tasks_detail(request, pk: int):
    """
    Retrieve, update, partially update, or delete a task.

    Path parameters:
    - pk: The ID of the task.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = TaskSerializer(task, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="post",
    operation_summary="Toggle Task Completion",
    operation_description="Toggle the 'completed' state of the specified task.",
    responses={200: TaskSerializer()},
    tags=["tasks"],
)
@api_view(["POST"])
def tasks_toggle_complete(request, pk: int):
    """
    Toggle the completed flag for a given task.

    Path parameters:
    - pk: The ID of the task to toggle.
    """
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save(update_fields=["completed", "updated_at"])
    serializer = TaskSerializer(task)
    return Response(serializer.data)
