"""
Script to create an admin user for the Flask application
"""
import os
import sys
from app import app, db
from models import User
from datetime import datetime, timezone

def create_admin_user(username, email, password):
    """Create an admin user"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                print(f"Error: Username '{username}' already exists.")
            else:
                print(f"Error: Email '{email}' already exists.")
            return False
        
        # Create new admin user
        user = User(
            username=username,
            email=email,
            is_admin=True,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        user.set_password(password)
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully.")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)
