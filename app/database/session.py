from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create a database engine with professional connection pooling settings
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Automatically reconnect if the database connection drops
    pool_size=10,            # Maintain a pool of 10 connections
    max_overflow=20,         # Allow up to 20 additional connections during traffic spikes
    pool_timeout=30          # Timeout after 30 seconds if a connection is not available
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
