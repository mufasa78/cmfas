import csv
import os
from datetime import datetime
from app import app, db
from models import MedicinalMaterial, DataImport

def import_medicinal_materials(file_path):
    """Import medicinal materials from CSV file"""
    success_count = 0
    error_count = 0
    error_messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Check if the material already exists
                    existing = MedicinalMaterial.query.filter_by(name=row['name']).first()
                    if existing:
                        error_count += 1
                        error_messages.append(f"Material '{row['name']}' already exists")
                        continue
                    
                    # Create new material
                    material = MedicinalMaterial(
                        name=row['name'],
                        pinyin=row['pinyin'],
                        english_name=row['english_name'],
                        province_origin=row['province_origin'],
                        property=row['property'],
                        flavor=row['flavor'],
                        meridian=row['meridian'],
                        description=row['description'],
                        usage_frequency=0  # Will be updated when prescriptions are imported
                    )
                    
                    db.session.add(material)
                    db.session.commit()
                    success_count += 1
                    print(f"Imported material {success_count}: {row['name']}")
                except Exception as e:
                    db.session.rollback()
                    error_count += 1
                    error_messages.append(f"Error processing material '{row.get('name', 'unknown')}': {str(e)}")
                    
        # Log the import
        log_import('medicinal_materials.csv', 'Medicinal Materials', success_count, error_count, error_messages)
        
        return success_count, error_count, error_messages
    except Exception as e:
        error_message = f"Error opening or reading file: {str(e)}"
        log_import('medicinal_materials.csv', 'Medicinal Materials', 0, 1, [error_message])
        return 0, 1, [error_message]

def log_import(filename, import_type, success_count, error_count, error_messages):
    """Log the import in the database"""
    status = "success" if error_count == 0 else "partial" if success_count > 0 else "error"
    error_message = "\n".join(error_messages) if error_messages else None
    
    import_log = DataImport(
        filename=filename,
        import_type=import_type,
        rows_imported=success_count,
        import_date=datetime.utcnow(),
        status=status,
        error_message=error_message
    )
    
    try:
        db.session.add(import_log)
        db.session.commit()
    except:
        db.session.rollback()
        print("Error logging import")

def main():
    with app.app_context():
        # Import the data
        materials_path = os.path.join('data', 'medicinal_materials.csv')
        
        print("Importing medicinal materials...")
        m_success, m_error, m_messages = import_medicinal_materials(materials_path)
        print(f"Successfully imported {m_success} materials with {m_error} errors")
        
        # Print any errors
        if m_messages:
            print("Medicinal material import errors:")
            for msg in m_messages:
                print(f"- {msg}")

if __name__ == "__main__":
    main()