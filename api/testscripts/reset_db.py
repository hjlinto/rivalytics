import os
import sys

# Add the parent directory to the system path to allow imports from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import Base, engine
import api.models



def reset_database():
    """Drops all tables and recreates them.
    """
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)

    print("Database reset complete.")

# This script can be run directly to reset the local database.
if __name__ == "__main__":
    confirm = input("This will delete all local data. Type RESET to continue: ")

    if confirm == "RESET":
        reset_database()
    else:
        print("Reset cancelled.")