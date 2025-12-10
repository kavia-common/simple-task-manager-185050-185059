from django.urls import path
from rest_framework.permissions import AllowAny
from . import views

urlpatterns = [
    path('register', views.register, name='auth-register'),
    path('login', views.JWTLoginView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('refresh', views.JWTRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('logout', views.logout, name='auth-logout'),
    path('me', views.me, name='auth-me'),
]
