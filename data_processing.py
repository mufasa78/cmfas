import pandas as pd
import numpy as np
from sqlalchemy import func, desc
from app import db
from models import MedicinalMaterial, Prescription, EfficacyCategory
import io
import csv
import logging

logger = logging.getLogger(__name__)

def get_province_statistics():
    """
    Get statistics on the number of medicinal materials produced in each province
    
    Returns:
        dict: Dictionary with province names as keys and counts as values
    """
    results = db.session.query(
        MedicinalMaterial.province_origin, 
        func.count(MedicinalMaterial.id)
    ).group_by(MedicinalMaterial.province_origin).all()
    
    # Convert to dictionary for easier processing
    province_stats = {province: count for province, count in results if province}
    return province_stats

def get_material_usage_frequency():
    """
    Get the frequency of use of each medicinal material in all prescriptions
    
    Returns:
        list: List of dictionaries with material name and usage count
    """
    results = db.session.query(
        MedicinalMaterial.name, 
        MedicinalMaterial.usage_frequency
    ).order_by(desc(MedicinalMaterial.usage_frequency)).all()
    
    return [{"name": name, "value": count} for name, count in results]

def get_property_distribution():
    """
    Get the distribution of five properties (五性) of medicinal materials
    
    Returns:
        dict: Dictionary with property names as keys and counts as values
    """
    results = db.session.query(
        MedicinalMaterial.property,
        func.count(MedicinalMaterial.id)
    ).group_by(MedicinalMaterial.property).all()
    
    return {prop: count for prop, count in results if prop}

def get_flavor_distribution():
    """
    Get the distribution of five flavors (五味) of medicinal materials
    
    Returns:
        dict: Dictionary with flavor names as keys and counts as values
    """
    results = db.session.query(
        MedicinalMaterial.flavor,
        func.count(MedicinalMaterial.id)
    ).group_by(MedicinalMaterial.flavor).all()
    
    return {flavor: count for flavor, count in results if flavor}

def get_meridian_distribution():
    """
    Get the distribution of meridians (归经) of medicinal materials
    
    Returns:
        dict: Dictionary with meridian names as keys and counts as values
    """
    results = db.session.query(
        MedicinalMaterial.meridian,
        func.count(MedicinalMaterial.id)
    ).group_by(MedicinalMaterial.meridian).all()
    
    return {meridian: count for meridian, count in results if meridian}

def get_top_prescriptions_by_efficacy(efficacy_name, limit=10):
    """
    Get the top prescriptions for a specific efficacy
    
    Args:
        efficacy_name (str): Name of the efficacy category
        limit (int): Number of prescriptions to return
        
    Returns:
        list: List of prescription objects
    """
    category = EfficacyCategory.query.filter_by(name=efficacy_name).first()
    if not category:
        return []
    
    return category.prescriptions[:limit]

def get_top_materials_by_efficacy(efficacy_name, limit=10):
    """
    Get the top medicinal materials used in prescriptions for a specific efficacy
    
    Args:
        efficacy_name (str): Name of the efficacy category
        limit (int): Number of materials to return
        
    Returns:
        list: List of material names and their counts
    """
    category = EfficacyCategory.query.filter_by(name=efficacy_name).first()
    if not category:
        return []
    
    # Get all prescriptions in this category
    prescriptions = category.prescriptions
    
    # Count the materials used in these prescriptions
    material_counts = {}
    for prescription in prescriptions:
        for material in prescription.materials:
            material_counts[material.name] = material_counts.get(material.name, 0) + 1
    
    # Sort by count and take top N
    sorted_materials = sorted(material_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "count": count} for name, count in sorted_materials[:limit]]

def process_material_upload(file_data):
    """
    Process CSV upload for medicinal materials
    
    Args:
        file_data: File-like object containing CSV data
        
    Returns:
        tuple: (success_count, error_count, error_messages)
    """
    success_count = 0
    error_count = 0
    error_messages = []
    
    try:
        # Convert file data to string and create a StringIO object
        if isinstance(file_data, bytes):
            file_data = file_data.decode('utf-8')
        
        csv_data = io.StringIO(file_data)
        reader = csv.DictReader(csv_data)
        
        for row in reader:
            try:
                # Check if material already exists
                material = MedicinalMaterial.query.filter_by(name=row.get('name')).first()
                
                if material:
                    # Update existing material
                    material.pinyin = row.get('pinyin', material.pinyin)
                    material.english_name = row.get('english_name', material.english_name)
                    material.province_origin = row.get('province_origin', material.province_origin)
                    material.property = row.get('property', material.property)
                    material.flavor = row.get('flavor', material.flavor)
                    material.meridian = row.get('meridian', material.meridian)
                    material.description = row.get('description', material.description)
                else:
                    # Create new material
                    material = MedicinalMaterial(
                        name=row.get('name'),
                        pinyin=row.get('pinyin'),
                        english_name=row.get('english_name'),
                        province_origin=row.get('province_origin'),
                        property=row.get('property'),
                        flavor=row.get('flavor'),
                        meridian=row.get('meridian'),
                        description=row.get('description'),
                        usage_frequency=0
                    )
                    db.session.add(material)
                
                success_count += 1
            except Exception as e:
                error_count += 1
                error_messages.append(f"Error on row {success_count + error_count}: {str(e)}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error_count += 1
        error_messages.append(f"General error: {str(e)}")
    
    return success_count, error_count, error_messages

def process_prescription_upload(file_data):
    """
    Process CSV upload for prescriptions
    
    Args:
        file_data: File-like object containing CSV data
        
    Returns:
        tuple: (success_count, error_count, error_messages)
    """
    success_count = 0
    error_count = 0
    error_messages = []
    
    try:
        # Convert file data to string and create a StringIO object
        if isinstance(file_data, bytes):
            file_data = file_data.decode('utf-8')
        
        csv_data = io.StringIO(file_data)
        reader = csv.DictReader(csv_data)
        
        for row in reader:
            try:
                # Check if prescription already exists
                prescription = Prescription.query.filter_by(name=row.get('name')).first()
                
                if not prescription:
                    # Create new prescription
                    prescription = Prescription(
                        name=row.get('name'),
                        description=row.get('description'),
                        efficacy=row.get('efficacy'),
                        evolution_history={}
                    )
                    db.session.add(prescription)
                    db.session.flush()  # To get the prescription ID
                
                # Process the materials in this prescription
                materials_str = row.get('materials', '')
                if materials_str:
                    # Assuming materials are in format: "name1:amount1,name2:amount2"
                    materials_list = materials_str.split(',')
                    
                    for material_info in materials_list:
                        if ':' in material_info:
                            material_name, amount = material_info.split(':')
                            material = MedicinalMaterial.query.filter_by(name=material_name.strip()).first()
                            
                            if material:
                                # Check if already in prescription
                                if material not in prescription.materials:
                                    prescription.materials.append(material)
                                    
                                # Increment usage frequency
                                material.usage_frequency += 1
                            else:
                                error_messages.append(f"Material not found: {material_name}")
                
                # Process efficacy categories
                efficacy_cats = row.get('efficacy_categories', '')
                if efficacy_cats:
                    categories = efficacy_cats.split(',')
                    
                    for cat_name in categories:
                        cat_name = cat_name.strip()
                        category = EfficacyCategory.query.filter_by(name=cat_name).first()
                        
                        if not category:
                            # Create if it doesn't exist
                            category = EfficacyCategory(name=cat_name)
                            db.session.add(category)
                            db.session.flush()
                        
                        if category not in prescription.efficacy_categories:
                            prescription.efficacy_categories.append(category)
                
                success_count += 1
            except Exception as e:
                error_count += 1
                error_messages.append(f"Error on row {success_count + error_count}: {str(e)}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error_count += 1
        error_messages.append(f"General error: {str(e)}")
    
    return success_count, error_count, error_messages

def search_prescriptions(query_params):
    """
    Search prescriptions based on query parameters
    
    Args:
        query_params (dict): Dictionary of query parameters
        
    Returns:
        list: List of matching prescriptions
    """
    prescription_query = Prescription.query
    
    # Filter by name if provided
    if query_params.get('name'):
        prescription_query = prescription_query.filter(
            Prescription.name.ilike(f"%{query_params['name']}%")
        )
    
    # Filter by efficacy if provided
    if query_params.get('efficacy'):
        prescription_query = prescription_query.filter(
            Prescription.efficacy.ilike(f"%{query_params['efficacy']}%")
        )
    
    # Filter by material if provided
    if query_params.get('material'):
        material_name = query_params['material']
        prescription_query = prescription_query.join(
            Prescription.materials
        ).filter(
            MedicinalMaterial.name.ilike(f"%{material_name}%")
        )
    
    # Filter by efficacy category if provided
    if query_params.get('category'):
        category_name = query_params['category']
        prescription_query = prescription_query.join(
            Prescription.efficacy_categories
        ).filter(
            EfficacyCategory.name.ilike(f"%{category_name}%")
        )
    
    return prescription_query.all()
