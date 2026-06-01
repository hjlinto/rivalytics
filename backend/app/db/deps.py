"""
Database dependencies for the Rivalytics backend.

This module contains FastAPI dependency functions that provide access to
database resources during request processing.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for the lifetime of a request.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()