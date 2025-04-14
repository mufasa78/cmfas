"""
Script to check the database schema
"""
from app import app, db
from models import User

def check_schema():
    """Check the database schema"""
    with app.app_context():
        # Print User table columns
        print("User table columns:")
        for column in User.__table__.columns:
            print(f"  - {column.name}: {column.type}")

if __name__ == "__main__":
    check_schema()
