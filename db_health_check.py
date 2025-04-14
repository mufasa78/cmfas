"""
Database health check utility
This script tests the database connection and reports any issues
"""
import os
import sys
import logging
from sqlalchemy import create_engine, text, inspect
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    # Use the provided Neon PostgreSQL database
    DB_URL = "postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def check_database_connection():
    """Test the database connection and report any issues"""
    logger.info("Testing database connection...")
    
    try:
        # Configure SQLAlchemy engine with proper connection pooling for Neon PostgreSQL
        engine = create_engine(
            DB_URL,
            connect_args={
                'connect_timeout': 30,  # Longer timeout for initial connection
                'keepalives': 1,        # Enable keepalives
                'keepalives_idle': 30,  # Send keepalive every 30 seconds
                'keepalives_interval': 10,  # Retry interval
                'keepalives_count': 5   # Number of retries
            },
            pool_pre_ping=True,         # Verify connections before using them
            pool_recycle=300,           # Recycle connections every 5 minutes
            pool_size=5,                # Limit pool size for Neon's connection pooler
            max_overflow=10             # Allow up to 10 overflow connections
        )
        
        # Test basic connection
        with engine.connect() as conn:
            logger.info("Testing basic connection...")
            result = conn.execute(text("SELECT 1"))
            value = result.scalar()
            logger.info(f"Basic connection test result: {value}")
            
            # Check if we can get the current timestamp from the database
            logger.info("Testing timestamp retrieval...")
            result = conn.execute(text("SELECT NOW()"))
            db_time = result.scalar()
            logger.info(f"Database timestamp: {db_time}")
            
            # Check database size
            logger.info("Checking database size...")
            result = conn.execute(text("""
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """))
            db_size = result.scalar()
            logger.info(f"Database size: {db_size}")
            
            # Get table information
            logger.info("Getting table information...")
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"Tables in database: {', '.join(tables)}")
            
            # Check user table
            if 'user' in tables:
                logger.info("Checking user table...")
                result = conn.execute(text("SELECT COUNT(*) FROM \"user\""))
                user_count = result.scalar()
                logger.info(f"User count: {user_count}")
                
                # Check user_preference table
                if 'user_preference' in tables:
                    logger.info("Checking user_preference table...")
                    result = conn.execute(text("SELECT COUNT(*) FROM user_preference"))
                    pref_count = result.scalar()
                    logger.info(f"User preference count: {pref_count}")
                    
                    # Check if counts match
                    if user_count != pref_count:
                        logger.warning(f"User count ({user_count}) does not match preference count ({pref_count})")
            
            # Check activity_log table
            if 'activity_log' in tables:
                logger.info("Checking activity_log table...")
                result = conn.execute(text("SELECT COUNT(*) FROM activity_log"))
                log_count = result.scalar()
                logger.info(f"Activity log count: {log_count}")
            
            logger.info("All database tests completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return False

if __name__ == "__main__":
    success = check_database_connection()
    sys.exit(0 if success else 1)
