"""
Simple script to create an admin user
"""
from app import app, db
from models import User
from datetime import datetime, timezone

def create_admin():
    """Create an admin user"""
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username="admin").first()
        
        if admin:
            print("Admin user already exists.")
            return
        
        # Create new admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        admin.set_password("password123")
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user created successfully.")

if __name__ == "__main__":
    create_admin()
