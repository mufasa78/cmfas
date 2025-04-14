import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "chinese_medicine_analysis_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    # Use the provided Neon PostgreSQL database
    db_url = "postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    # Connection pooling settings
    "pool_size": 5,  # Limit pool size for Neon's connection pooler
    "max_overflow": 10,  # Allow up to 10 overflow connections
    "pool_timeout": 30,  # Timeout for getting a connection from the pool
    "pool_recycle": 300,  # Recycle connections every 5 minutes
    "pool_pre_ping": True,  # Verify connections before using them

    # Connection settings
    "connect_args": {
        "connect_timeout": 30,  # Longer timeout for initial connection
        "keepalives": 1,        # Enable keepalives
        "keepalives_idle": 30,  # Send keepalive every 30 seconds
        "keepalives_interval": 10,  # Retry interval
        "keepalives_count": 5   # Number of retries
    }
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set higher logging level for SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Initialize the app with the extension
db.init_app(app)

# Add template context processor to include language in all templates
@app.context_processor
def inject_language():
    from language import get_language
    from translations import get_text

    lang = get_language()
    return {
        'lang': lang,
        't': lambda key, *args: get_text(key, lang, *args)
    }

# No authentication code

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401

    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
