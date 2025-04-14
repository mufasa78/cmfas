"""
Script to update the database schema with the User table
"""
import os
from sqlalchemy import create_engine, text

# Database configuration
DB_URL = "postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def update_schema():
    """Update the database schema to include the User table and related tables"""
    try:
        # Connect to the database
        engine = create_engine(DB_URL)

        with engine.connect() as conn:
            # Check if the user table already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'user'
                )
            """))
            user_table_exists = result.scalar()

            # Update user table if it exists, otherwise create it
            if user_table_exists:
                print("User table exists, updating schema...")

                # Check if columns need to be added
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'user' AND column_name = 'is_email_verified'
                """))
                has_email_verified = result.fetchone() is not None

                if not has_email_verified:
                    print("Adding new columns to user table...")
                    conn.execute(text("""
                        ALTER TABLE "user"
                        ADD COLUMN is_email_verified BOOLEAN DEFAULT FALSE,
                        ADD COLUMN email_verification_token VARCHAR(100),
                        ADD COLUMN email_token_expiry TIMESTAMP,
                        ADD COLUMN role VARCHAR(20) DEFAULT 'user',
                        ADD COLUMN reset_password_token VARCHAR(100),
                        ADD COLUMN reset_token_expiry TIMESTAMP,
                        ADD COLUMN last_login TIMESTAMP
                    """))
            else:
                # Create the user table
                print("Creating user table...")
                conn.execute(text("""
                    CREATE TABLE "user" (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(64) UNIQUE NOT NULL,
                        email VARCHAR(120) UNIQUE NOT NULL,
                        password_hash VARCHAR(128) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        is_email_verified BOOLEAN DEFAULT FALSE,
                        email_verification_token VARCHAR(100),
                        email_token_expiry TIMESTAMP,
                        role VARCHAR(20) DEFAULT 'user',
                        reset_password_token VARCHAR(100),
                        reset_token_expiry TIMESTAMP,
                        created_at TIMESTAMP DEFAULT NOW(),
                        last_login TIMESTAMP
                    )
                """))

                # Create indexes
                conn.execute(text('CREATE INDEX ix_user_username ON "user" (username)'))
                conn.execute(text('CREATE INDEX ix_user_email ON "user" (email)'))

            # Check if user_preference table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'user_preference'
                )
            """))
            preference_table_exists = result.scalar()

            if not preference_table_exists:
                print("Creating user_preference table...")
                conn.execute(text("""
                    CREATE TABLE user_preference (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                        default_language VARCHAR(10) DEFAULT 'zh',
                        theme VARCHAR(20) DEFAULT 'light',
                        notification_enabled BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                """))

            # Check if activity_log table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'activity_log'
                )
            """))
            activity_log_table_exists = result.scalar()

            if not activity_log_table_exists:
                print("Creating activity_log table...")
                conn.execute(text("""
                    CREATE TABLE activity_log (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                        action VARCHAR(100) NOT NULL,
                        details TEXT,
                        ip_address VARCHAR(45),
                        user_agent VARCHAR(255),
                        timestamp TIMESTAMP DEFAULT NOW()
                    )
                """))
                conn.execute(text('CREATE INDEX ix_activity_log_user_id ON activity_log (user_id)'))
                conn.execute(text('CREATE INDEX ix_activity_log_timestamp ON activity_log (timestamp)'))

            conn.commit()
            print("Database schema updated successfully")
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_schema()
