"""
Script to create an admin user directly in the database
"""
import os
import sys
from app import app, db
from models import User
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
import json

def create_admin_user_direct(username, email, password):
    """Create an admin user directly in the database"""
    with app.app_context():
        try:
            # Create SQL to insert user
            password_hash = generate_password_hash(password)
            preferences = json.dumps({'language': 'zh', 'theme': 'light'})
            created_at = datetime.now(timezone.utc).isoformat()

            # Execute raw SQL using text
            from sqlalchemy import text
            sql = text("""
            INSERT INTO "user" (username, email, password_hash, is_active, is_admin, created_at, preferences)
            VALUES (:username, :email, :password_hash, TRUE, TRUE, :created_at, :preferences)
            ON CONFLICT (username) DO NOTHING
            RETURNING id
            """)

            result = db.session.execute(sql, {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'created_at': created_at,
                'preferences': preferences
            })

            user_id = result.scalar()

            if user_id:
                db.session.commit()
                print(f"Admin user '{username}' created successfully with ID {user_id}.")
                return True
            else:
                print(f"User '{username}' already exists.")
                return False

        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin_direct.py <username> <email> <password>")
        sys.exit(1)

    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]

    create_admin_user_direct(username, email, password)
