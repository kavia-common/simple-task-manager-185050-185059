from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer, UserSerializer
from .schemas import (
    RegisterRequest,
    UserModel,
    LogoutRequest,
    TodoCreate,
    TodoUpdate,
)

User = get_user_model()


class IsOwner(permissions.BasePermission):
    """Allow access only to object's owner."""

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "user") and obj.user == request.user


class TodoViewSet(viewsets.ModelViewSet):
    """
    PUBLIC_INTERFACE
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Return todos belonging to the current authenticated user only."""
        return Todo.objects.filter(user=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        # Validate with Pydantic first
        try:
            payload = TodoCreate(**request.data)
        except Exception as e:
            return Response({"detail": "Invalid request", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=payload.model_dump())
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request: Request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Validate with Pydantic first
        try:
            payload = TodoUpdate(**request.data)
        except Exception as e:
            return Response({"detail": "Invalid request", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=payload.model_dump(exclude_unset=True), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request: Request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        # list/retrieve/update/destroy all require authentication; object level checked by IsOwner
        return super().get_permissions()


# PUBLIC_INTERFACE
class JWTLoginView(TokenObtainPairView):
    """Obtain JWT access and refresh tokens for valid credentials."""
    # default serializer is fine from SimpleJWT


# PUBLIC_INTERFACE
class JWTRefreshView(TokenRefreshView):
    """Refresh JWT access token using a valid refresh token."""
    # default serializer is fine from SimpleJWT


# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request: Request):
    """
    Register a new user.

    Request body (Pydantic: RegisterRequest):
    - username: string
    - email: string (optional)
    - password: string
    - password_confirm: string

    Returns (Pydantic: UserModel):
    - 201 with user info
    """
    try:
        payload = RegisterRequest(**request.data)
    except Exception as e:
        return Response({"detail": "Invalid request", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterSerializer(data=payload.model_dump())
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserModel(**UserSerializer(user).data).model_dump(), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request: Request):
    """
    Get current authenticated user info.

    Returns (Pydantic: UserModel)
    """
    return Response(UserModel(**UserSerializer(request.user).data).model_dump(), status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request: Request):
    """
    Logout by blacklisting the provided refresh token (if present).
    Send JSON body: {"refresh": "<refresh_token>"}.
    If no refresh is provided, this is a no-op for stateless JWT.

    Request body (Pydantic: LogoutRequest)
    """
    try:
        payload = LogoutRequest(**request.data)
    except Exception as e:
        return Response({"detail": "Invalid request", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if payload.refresh:
        try:
            token = RefreshToken(payload.refresh)
            token.blacklist()  # will work only if blacklist app is added, else ignore
        except Exception:
            # Return 200 even if blacklisting is not configured to avoid leaking info.
            pass
    return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
