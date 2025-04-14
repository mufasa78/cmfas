"""
Script to initialize the database tables
"""
from app import app, db
from models import User, UserActivity, MedicinalMaterial, Prescription, EfficacyCategory, FormulaOptimization, DataImport

def init_db():
    """Initialize the database by creating all tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
