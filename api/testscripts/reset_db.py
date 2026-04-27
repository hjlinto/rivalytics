import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
# Import models to ensure they are registered with SQLAlchemy
from models import Hero, TeamUp


def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)

    print("Database reset complete.")


if __name__ == "__main__":
    confirm = input("This will delete all local data. Type RESET to continue: ")

    if confirm == "RESET":
        reset_database()
    else:
        print("Reset cancelled.")