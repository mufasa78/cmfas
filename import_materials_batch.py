import csv
import os
import sys
from datetime import datetime
from app import app, db
from models import MedicinalMaterial, DataImport

def import_medicinal_materials_batch(file_path, start_row, batch_size):
    """Import a batch of medicinal materials from CSV file"""
    success_count = 0
    error_count = 0
    error_messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            end_row = min(start_row + batch_size, len(rows))
            batch_rows = rows[start_row:end_row]
            
            for i, row in enumerate(batch_rows):
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
                    actual_row = start_row + i + 1  # +1 for header row
                    print(f"Imported material at row {actual_row}: {row['name']}")
                except Exception as e:
                    db.session.rollback()
                    error_count += 1
                    error_messages.append(f"Error processing material '{row.get('name', 'unknown')}': {str(e)}")
            
            return success_count, error_count, error_messages, end_row >= len(rows)
    except Exception as e:
        error_message = f"Error opening or reading file: {str(e)}"
        return 0, 1, [error_message], True

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
    batch_size = 50  # Import 50 materials at a time (increased from 25)
    
    if len(sys.argv) < 2:
        print("Usage: python import_materials_batch.py <start_row>")
        return
    
    try:
        start_row = int(sys.argv[1])
    except ValueError:
        print("Start row must be an integer")
        return
    
    with app.app_context():
        # Import the batch
        materials_path = os.path.join('data', 'medicinal_materials.csv')
        
        print(f"Importing medicinal materials batch starting at row {start_row}...")
        m_success, m_error, m_messages, is_complete = import_medicinal_materials_batch(
            materials_path, start_row, batch_size
        )
        print(f"Successfully imported {m_success} materials with {m_error} errors")
        
        # Print any errors
        if m_messages:
            print("Errors:")
            for msg in m_messages:
                print(f"- {msg}")
        
        if not is_complete:
            next_start = start_row + batch_size
            print(f"Batch complete. To import the next batch, run: python import_materials_batch.py {next_start}")
        else:
            print("All materials have been imported.")
            log_import('medicinal_materials.csv', 'Medicinal Materials (Batched)', m_success, m_error, m_messages)

if __name__ == "__main__":
    main()