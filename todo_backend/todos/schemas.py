from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# PUBLIC_INTERFACE
class RegisterRequest(BaseModel):
    """Schema for user registration request body."""
    username: str = Field(..., description="Unique username for the new user", min_length=1)
    email: Optional[EmailStr] = Field(None, description="Optional email address")
    password: str = Field(..., description="Password for the new user", min_length=1)
    password_confirm: str = Field(..., description="Confirmation password", min_length=1)


# PUBLIC_INTERFACE
class UserModel(BaseModel):
    """Schema for returning minimal user profile info."""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: Optional[EmailStr] = Field(None, description="Email address")


# PUBLIC_INTERFACE
class AuthTokens(BaseModel):
    """Schema for JWT tokens response."""
    access: str = Field(..., description="Access token")
    refresh: str = Field(..., description="Refresh token")


# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    """Schema for login request body."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


# PUBLIC_INTERFACE
class RefreshRequest(BaseModel):
    """Schema for refresh request body."""
    refresh: str = Field(..., description="Refresh token")


# PUBLIC_INTERFACE
class LogoutRequest(BaseModel):
    """Schema for logout request body. Providing refresh enables blacklisting if configured."""
    refresh: Optional[str] = Field(None, description="Refresh token to blacklist")


# PUBLIC_INTERFACE
class TodoCreate(BaseModel):
    """Schema for creating a todo."""
    title: str = Field(..., description="Short title for the task", min_length=1, max_length=255)
    description: Optional[str] = Field("", description="Details about the task")
    completed: Optional[bool] = Field(False, description="Initial completion state")


# PUBLIC_INTERFACE
class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = Field(None, description="Updated title", max_length=255)
    description: Optional[str] = Field(None, description="Updated details")
    completed: Optional[bool] = Field(None, description="Updated completion state")
