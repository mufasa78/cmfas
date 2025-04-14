"""
Script to reset the database by dropping and recreating all tables
"""
from app import app, db

def reset_db():
    """Reset the database by dropping and recreating all tables"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Database reset successfully.")

if __name__ == "__main__":
    reset_db()
