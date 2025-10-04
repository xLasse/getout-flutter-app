import os
import logging
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to SQLite if no DATABASE_URL is provided
if not DATABASE_URL:
    DATABASE_URL = "sqlite:////home/site/wwwroot/app.db"
    logging.info("Using SQLite fallback database")

# Create engine
def get_engine(url: str = DATABASE_URL) -> Engine:
    """Create and return SQLAlchemy engine."""
    try:
        if url.startswith("sqlite"):
            engine = create_engine(
                url,
                connect_args={"check_same_thread": False},
                echo=False
            )
        else:
            engine = create_engine(url, echo=False)
        
        logging.info(f"Database engine created successfully")
        return engine
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        # Fallback to in-memory SQLite
        logging.info("Falling back to in-memory SQLite database")
        return create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            echo=False
        )

# Create engine instance
engine = get_engine()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
