from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Database URL - using SQLite
DATABASE_URL = "postgresql://postgres.ussdbvkiiterzyhkeysq:Oy1SWHFJeXZF1c09@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

# Create SQLAlchemy engine with better configuration
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging in development
    pool_pre_ping=True,  # Verify connections before use
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

if "sqlite" in DATABASE_URL:
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))


# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def create_tables():
    """
    Create all database tables based on the models.
    This function should be called when the application starts.
    """
    # Import all models to ensure they are registered with Base

    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    This function is used as a FastAPI dependency to get a database session
    for each request and automatically close it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

