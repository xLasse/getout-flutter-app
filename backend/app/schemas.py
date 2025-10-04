from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserCreate(BaseModel):
    """Schema for user creation."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None


class UserOut(BaseModel):
    """Schema for user output (without sensitive data)."""
    id: int
    email: str
    role: str
    is_active: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication Schemas
class LoginIn(BaseModel):
    """Schema for login input (OAuth2 convention)."""
    username: str  # Email address
    password: str


class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: int


class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    refresh_token: str


# Event Schemas
class EventCreate(BaseModel):
    """Schema for event creation."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: datetime
    location: Optional[str] = None
    category: str = "social"
    is_public: bool = True
    max_attendees: int = Field(default=50, ge=1, le=1000)
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    """Schema for event updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    category: Optional[str] = None
    is_public: Optional[bool] = None
    max_attendees: Optional[int] = Field(None, ge=1, le=1000)
    image_url: Optional[str] = None


class EventOut(BaseModel):
    """Schema for event output."""
    id: int
    title: str
    description: Optional[str] = None
    event_date: datetime
    location: Optional[str] = None
    creator_id: int
    category: str
    is_public: bool
    max_attendees: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    attendee_count: int = 0
    is_attending: bool = False
    
    class Config:
        from_attributes = True


# Event Attendee Schemas
class EventAttendeeCreate(BaseModel):
    """Schema for joining an event."""
    status: str = "attending"  # attending, maybe, declined


class EventAttendeeOut(BaseModel):
    """Schema for event attendee output."""
    id: int
    event_id: int
    user_id: int
    status: str
    joined_at: datetime
    user: UserOut
    
    class Config:
        from_attributes = True


# Friendship Schemas
class FriendshipCreate(BaseModel):
    """Schema for creating friendship request."""
    addressee_id: int


class FriendshipUpdate(BaseModel):
    """Schema for updating friendship status."""
    status: str  # accepted, declined, blocked


class FriendshipOut(BaseModel):
    """Schema for friendship output."""
    id: int
    requester_id: int
    addressee_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    requester: UserOut
    addressee: UserOut
    
    class Config:
        from_attributes = True


# Chat Message Schemas
class ChatMessageCreate(BaseModel):
    """Schema for creating chat message."""
    receiver_id: int
    content: str = Field(..., min_length=1, max_length=1000)
    message_type: str = "text"


class ChatMessageOut(BaseModel):
    """Schema for chat message output."""
    id: int
    sender_id: int
    receiver_id: int
    content: str
    message_type: str
    is_read: bool
    created_at: datetime
    sender: UserOut
    receiver: UserOut
    
    class Config:
        from_attributes = True


# Response Schemas
class MessageResponse(BaseModel):
    """Generic message response schema."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    error_code: Optional[str] = None
