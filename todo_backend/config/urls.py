"""
URL configuration for config project.

Routes:
- /admin/ Django admin
- /auth/ authentication endpoints (register, login, refresh, logout, me)
- /api/todos/ CRUD endpoints for todos (JWT protected)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('todos.auth_urls')),
    path('api/', include('todos.urls')),
]
