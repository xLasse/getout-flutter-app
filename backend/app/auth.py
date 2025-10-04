import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .db import get_db
from .models import User, RefreshToken
from .schemas import UserCreate, UserOut, Token, TokenRefresh, MessageResponse
from .security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    decode_token,
    get_current_user,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Add rate limit exception handler
router.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role="user",
        is_active=True
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logging.info(f"New user registered: {user_data.email}")
        return db_user
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logging.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(sub=str(user.id))
    
    # Store refresh token in database
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    
    try:
        db.add(db_refresh_token)
        db.commit()
        logging.info(f"User logged in: {user.email}")
    except Exception as e:
        logging.error(f"Failed to store refresh token: {e}")
        # Continue without refresh token if storage fails
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    try:
        payload = decode_token(token_data.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if refresh token exists and is not revoked
        db_refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == token_data.refresh_token,
            RefreshToken.user_id == int(user_id),
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        if not db_refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # Get user
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        logging.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )


@router.get("/me", response_model=UserOut)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile information."""
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout(
    token_data: TokenRefresh,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user by revoking refresh token."""
    try:
        # Revoke the refresh token
        db_refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == token_data.refresh_token,
            RefreshToken.user_id == current_user.id
        ).first()
        
        if db_refresh_token:
            db_refresh_token.revoked = True
            db.commit()
        
        logging.info(f"User logged out: {current_user.email}")
        return MessageResponse(message="Successfully logged out")
        
    except Exception as e:
        logging.error(f"Logout failed: {e}")
        return MessageResponse(message="Logout completed")


@router.post("/revoke-all-tokens", response_model=MessageResponse)
async def revoke_all_tokens(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke all refresh tokens for the current user."""
    try:
        db.query(RefreshToken).filter(
            RefreshToken.user_id == current_user.id,
            RefreshToken.revoked == False
        ).update({"revoked": True})
        db.commit()
        
        logging.info(f"All tokens revoked for user: {current_user.email}")
        return MessageResponse(message="All tokens revoked successfully")
        
    except Exception as e:
        logging.error(f"Failed to revoke tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke tokens"
        )
