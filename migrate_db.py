"""
Script to migrate the database schema
"""
from app import app, db
from sqlalchemy import text

def migrate_db():
    """Migrate the database schema to add missing columns"""
    with app.app_context():
        try:
            print("Checking if user table exists...")
            result = db.session.execute(text("SELECT to_regclass('user')"))
            user_table_exists = result.scalar() is not None
            
            if user_table_exists:
                print("User table exists. Checking columns...")
                
                # Check if is_admin column exists
                result = db.session.execute(text(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'user' AND column_name = 'is_admin'"
                ))
                is_admin_exists = result.scalar() is not None
                
                if not is_admin_exists:
                    print("Adding is_admin column...")
                    db.session.execute(text(
                        "ALTER TABLE \"user\" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"
                    ))
                    print("is_admin column added.")
                else:
                    print("is_admin column already exists.")
                
                # Check if is_active column exists
                result = db.session.execute(text(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'user' AND column_name = 'is_active'"
                ))
                is_active_exists = result.scalar() is not None
                
                if not is_active_exists:
                    print("Adding is_active column...")
                    db.session.execute(text(
                        "ALTER TABLE \"user\" ADD COLUMN is_active BOOLEAN DEFAULT TRUE"
                    ))
                    print("is_active column added.")
                else:
                    print("is_active column already exists.")
                
                # Check if preferences column exists
                result = db.session.execute(text(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'user' AND column_name = 'preferences'"
                ))
                preferences_exists = result.scalar() is not None
                
                if not preferences_exists:
                    print("Adding preferences column...")
                    db.session.execute(text(
                        "ALTER TABLE \"user\" ADD COLUMN preferences JSONB DEFAULT '{\"language\": \"zh\", \"theme\": \"light\"}'"
                    ))
                    print("preferences column added.")
                else:
                    print("preferences column already exists.")
                
                # Check if last_login column exists
                result = db.session.execute(text(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'user' AND column_name = 'last_login'"
                ))
                last_login_exists = result.scalar() is not None
                
                if not last_login_exists:
                    print("Adding last_login column...")
                    db.session.execute(text(
                        "ALTER TABLE \"user\" ADD COLUMN last_login TIMESTAMP WITH TIME ZONE"
                    ))
                    print("last_login column added.")
                else:
                    print("last_login column already exists.")
                
                # Commit all changes
                db.session.commit()
                print("Database migration completed successfully.")
            else:
                print("User table does not exist. Creating all tables...")
                db.create_all()
                print("All tables created.")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_db()
