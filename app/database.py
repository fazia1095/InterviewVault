from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file (will be created in the project root when first used)
SQLALCHEMY_DATABASE_URL = "sqlite:///./interviewvault.db"

# check_same_thread=False is required for SQLite when used with FastAPI,
# because FastAPI can handle requests using multiple threads,
# but SQLite by default only allows one thread to use a connection.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for creating new DB sessions.
# Each request will get its own session instance from this.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our future ORM models (models.py) will inherit from.
Base = declarative_base()