"""
FastAPI application entrypoint for the Rivalytics backend.

This module owns application setup: FastAPI initialization, middleware
configuration, database table creation, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db.database import Base, engine
from backend.app.routes.recommendations import router as meta_router


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Rivalytics API", version="0.1.0")


# Allow the local Next.js frontend to call the FastAPI backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes.
app.include_router(meta_router)