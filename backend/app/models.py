from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="user")  # user, admin, moderator
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile_image_url = Column(String(500))
    bio = Column(Text)
    
    # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    created_events = relationship("Event", back_populates="creator", cascade="all, delete-orphan")
    
    # Create unique index on email
    __table_args__ = (
        Index('ix_users_email_unique', 'email', unique=True),
    )


class RefreshToken(Base):
    """Refresh token model for JWT token management."""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")


class Event(Base):
    """Event model for social event management."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(500))
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), default="social")  # social, sports, music, etc.
    is_public = Column(Boolean, default=True)
    max_attendees = Column(Integer, default=50)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="created_events")
    attendees = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")


class EventAttendee(Base):
    """Event attendee relationship model."""
    __tablename__ = "event_attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="attending")  # attending, maybe, declined
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    event = relationship("Event", back_populates="attendees")
    user = relationship("User")
    
    # Unique constraint on event_id and user_id
    __table_args__ = (
        Index('ix_event_attendees_unique', 'event_id', 'user_id', unique=True),
    )


class Friendship(Base):
    """Friendship model for social connections."""
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, declined, blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id])
    addressee = relationship("User", foreign_keys=[addressee_id])
    
    # Unique constraint to prevent duplicate friendship requests
    __table_args__ = (
        Index('ix_friendships_unique', 'requester_id', 'addressee_id', unique=True),
    )


class ChatMessage(Base):
    """Chat message model for user communication."""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, image, system
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
