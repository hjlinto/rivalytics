"""
Database configuration for the Rivalytics backend.

This module owns SQLAlchemy engine creation, session factory setup, and the
shared declarative base used by ORM models. Environment variables are loaded
from the backend `.env` file for local development.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# backend/app/db/database.py -> backend/.env
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=BACKEND_DIR / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")


# SQLAlchemy engine used by the application to connect to the configured database.
engine = create_engine(DATABASE_URL)


# Session factory used by FastAPI dependencies and backend scripts.
SessionLocal = sessionmaker(bind=engine)


# Shared base class for all SQLAlchemy ORM models.
Base = declarative_base()