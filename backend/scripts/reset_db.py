"""
Utility script for rebuilding the Rivalytics database.

This script drops all existing tables and recreates the schema using the
current SQLAlchemy model definitions.

Warning:
    Running this script will permanently delete all data stored in the
    configured database.
"""

from backend.app.db.database import Base, engine

# Import models so SQLAlchemy registers them before create_all().
from backend.app.models import Hero, TeamUp  # noqa: F401


def reset_database() -> None:
    """
    Drop all database tables and recreate the schema.
    """

    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)

    print("Database reset complete.")


if __name__ == "__main__":
    confirmation = input(
        "This will delete all database data. Type RESET to continue: "
    )

    if confirmation == "RESET":
        reset_database()
    else:
        print("Reset cancelled.")