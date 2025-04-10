from app import app, db

def clear_data():
    """Clear existing data in the database"""
    try:
        print("Clearing existing data...")
        
        # Clear relationships first
        db.session.execute(db.text('DELETE FROM prescription_material'))
        db.session.execute(db.text('DELETE FROM prescription_efficacy'))
        
        # Delete records
        db.session.execute(db.text('DELETE FROM data_import'))
        db.session.execute(db.text('DELETE FROM formula_optimization'))
        db.session.execute(db.text('DELETE FROM material_interaction'))
        db.session.execute(db.text('DELETE FROM prescription'))
        db.session.execute(db.text('DELETE FROM efficacy_category'))
        db.session.execute(db.text('DELETE FROM medicinal_material'))
        
        db.session.commit()
        print("Data cleared successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing data: {str(e)}")

if __name__ == "__main__":
    with app.app_context():
        clear_data()