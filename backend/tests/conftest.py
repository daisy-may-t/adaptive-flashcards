import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.database import Base, get_db
from app.main import app


# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Share same connection across threads in tests
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables once at module load
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    """
    Override the database dependency for tests.
    
    Yields:
        Session: A database session for testing
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency globally for all tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Provide a test client with a clean database for each test.
    
    The database is cleared before each test to ensure test isolation.
    
    Yields:
        TestClient: A test client for making API requests
    """
    # Clear all data before each test
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
    
    with TestClient(app) as test_client:
        yield test_client
