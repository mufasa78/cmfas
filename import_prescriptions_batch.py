import csv
import os
import sys
from datetime import datetime
from app import app, db
from models import MedicinalMaterial, Prescription, EfficacyCategory, DataImport

def import_prescriptions_batch(file_path, start_row, batch_size):
    """Import a batch of prescriptions from CSV file"""
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
                    # Check if the prescription already exists
                    existing = Prescription.query.filter_by(name=row['name']).first()
                    if existing:
                        error_count += 1
                        error_messages.append(f"Prescription '{row['name']}' already exists")
                        continue
                    
                    # Create new prescription
                    prescription = Prescription(
                        name=row['name'],
                        description=row['description'],
                        efficacy=row['efficacy'],
                        evolution_history={},
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    
                    # Process materials
                    if 'materials' in row:
                        material_list = row['materials'].split(',')
                        for material_item in material_list:
                            if ':' in material_item:
                                material_name = material_item.split(':')[0].strip()
                            else:
                                material_name = material_item.strip()
                                
                            if material_name:
                                material = MedicinalMaterial.query.filter_by(name=material_name).first()
                                if material:
                                    prescription.materials.append(material)
                                    # Increment usage frequency
                                    material.usage_frequency += 1
                                else:
                                    error_messages.append(f"Material '{material_name}' not found for prescription '{row['name']}'")
                    
                    # Process efficacy categories
                    if 'efficacy_categories' in row:
                        categories = row['efficacy_categories'].split(',')
                        for category_name in categories:
                            category_name = category_name.strip()
                            if category_name:
                                category = EfficacyCategory.query.filter_by(name=category_name).first()
                                if not category:
                                    category = EfficacyCategory(name=category_name)
                                    db.session.add(category)
                                prescription.efficacy_categories.append(category)
                    
                    db.session.add(prescription)
                    db.session.commit()
                    success_count += 1
                    actual_row = start_row + i + 1  # +1 for header row
                    print(f"Imported prescription at row {actual_row}: {row['name']}")
                except Exception as e:
                    db.session.rollback()
                    error_count += 1
                    error_messages.append(f"Error processing prescription '{row.get('name', 'unknown')}': {str(e)}")
            
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
    batch_size = 25  # Import 25 prescriptions at a time
    
    if len(sys.argv) < 2:
        print("Usage: python import_prescriptions_batch.py <start_row>")
        return
    
    try:
        start_row = int(sys.argv[1])
    except ValueError:
        print("Start row must be an integer")
        return
    
    with app.app_context():
        # Import the batch
        prescriptions_path = os.path.join('data', 'prescriptions.csv')
        
        print(f"Importing prescriptions batch starting at row {start_row}...")
        p_success, p_error, p_messages, is_complete = import_prescriptions_batch(
            prescriptions_path, start_row, batch_size
        )
        print(f"Successfully imported {p_success} prescriptions with {p_error} errors")
        
        # Print any errors
        if p_messages:
            print("Errors:")
            for msg in p_messages:
                print(f"- {msg}")
        
        if not is_complete:
            next_start = start_row + batch_size
            print(f"Batch complete. To import the next batch, run: python import_prescriptions_batch.py {next_start}")
        else:
            print("All prescriptions have been imported.")
            log_import('prescriptions.csv', 'Prescriptions (Batched)', p_success, p_error, p_messages)

if __name__ == "__main__":
    main()