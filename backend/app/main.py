import os
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .auth import router as auth_router
from .db import get_engine, SessionLocal
from .models import Base


def app_version() -> str:
    """Get application version from environment variable."""
    return os.getenv("APP_VERSION", "dev")


def setup_logging() -> None:
    """Setup logging configuration."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    setup_logging()
    
    app = FastAPI(
        title="GetOut API",
        description="Backend API for GetOut social event management app",
        version=app_version(),
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS Configuration
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # GZip Middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Trusted Host Middleware (optional)
    trusted_hosts = os.getenv("TRUSTED_HOSTS")
    if trusted_hosts:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=trusted_hosts.split(",")
        )
    
    # Create database tables
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.warning(f"Database initialization warning: {e}")
    
    # Include routers
    app.include_router(auth_router)
    
    # Health endpoints
    @app.get("/")
    async def root():
        """Root endpoint with service information."""
        return {
            "service": "GetOut API",
            "version": app_version(),
            "status": "running",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "ok"}
    
    @app.get("/livez")
    async def liveness():
        """Liveness probe endpoint."""
        return {"live": "ok"}
    
    @app.get("/readyz")
    async def readiness():
        """Readiness probe endpoint."""
        return {"ready": "ok"}
    
    # Protected example routes
    from fastapi import Depends
    from .security import get_current_user, require_roles
    from .schemas import UserOut
    
    @app.get("/users/me", response_model=UserOut)
    async def get_current_user_info(current_user = Depends(get_current_user)):
        """Get current user information."""
        return current_user
    
    @app.get("/admin/ping")
    async def admin_ping(current_user = Depends(require_roles("admin"))):
        """Admin-only endpoint."""
        return {"message": "Admin access granted", "user": current_user.email}
    
    return app


# Global app instance for Gunicorn
app = create_app()
