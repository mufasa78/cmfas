from app import db
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables for many-to-many relationships
prescription_material = db.Table(
    'prescription_material',
    db.Column('prescription_id', db.Integer, db.ForeignKey('prescription.id')),
    db.Column('material_id', db.Integer, db.ForeignKey('medicinal_material.id')),
    db.Column('amount', db.String(50)),  # Amount of the material in the prescription
    db.Column('unit', db.String(20))     # Unit of measurement
)

# Model for medicinal material
class MedicinalMaterial(db.Model):
    __tablename__ = 'medicinal_material'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    pinyin = db.Column(db.String(100))
    english_name = db.Column(db.String(200))
    province_origin = db.Column(db.String(50))  # Province where the material originates

    # Five properties (五性): cold, hot, warm, cool, neutral
    property = db.Column(db.String(20))

    # Five flavors (五味): sour, bitter, sweet, spicy, salty
    flavor = db.Column(db.String(100))  # Increased size to handle combined flavors

    # Meridian tropism (归经): which organ/meridian the herb affects
    meridian = db.Column(db.String(100))

    description = db.Column(db.Text)
    usage_frequency = db.Column(db.Integer, default=0)  # How often the material is used in prescriptions

    # Relationship to prescriptions
    prescriptions = db.relationship('Prescription', secondary=prescription_material, back_populates='materials')

    def __repr__(self):
        return f"<MedicinalMaterial {self.name}>"

# Model for prescription (formula)
class Prescription(db.Model):
    __tablename__ = 'prescription'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    efficacy = db.Column(db.String(200))  # What the prescription treats

    # Store the evolution history as JSON
    evolution_history = db.Column(JSONB)

    # Relationship to medicinal materials
    materials = db.relationship('MedicinalMaterial', secondary=prescription_material, back_populates='prescriptions')

    # Metadata
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Prescription {self.name}>"

# Model for efficacy categories
class EfficacyCategory(db.Model):
    __tablename__ = 'efficacy_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    # Prescriptions in this category
    prescriptions = db.relationship('Prescription',
                                    secondary='prescription_efficacy',
                                    back_populates='efficacy_categories')

    def __repr__(self):
        return f"<EfficacyCategory {self.name}>"

# Association table for prescriptions and efficacy categories
prescription_efficacy = db.Table(
    'prescription_efficacy',
    db.Column('prescription_id', db.Integer, db.ForeignKey('prescription.id')),
    db.Column('efficacy_category_id', db.Integer, db.ForeignKey('efficacy_category.id'))
)

# Add the relationship to Prescription model
Prescription.efficacy_categories = db.relationship('EfficacyCategory',
                                                  secondary='prescription_efficacy',
                                                  back_populates='prescriptions')

# Model for storing ML model results
class FormulaOptimization(db.Model):
    __tablename__ = 'formula_optimization'

    id = db.Column(db.Integer, primary_key=True)
    user_symptoms = db.Column(db.Text)
    recommended_formula = db.Column(JSONB)  # Stores the optimized formula as JSON
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<FormulaOptimization {self.id}>"

# Model for material interactions (knowledge graph data)
class MaterialInteraction(db.Model):
    __tablename__ = 'material_interaction'

    id = db.Column(db.Integer, primary_key=True)
    material1_id = db.Column(db.Integer, db.ForeignKey('medicinal_material.id'))
    material2_id = db.Column(db.Integer, db.ForeignKey('medicinal_material.id'))
    interaction_type = db.Column(db.String(50))  # e.g., synergistic, antagonistic, etc.
    description = db.Column(db.Text)

    # Relationships
    material1 = db.relationship('MedicinalMaterial', foreign_keys=[material1_id])
    material2 = db.relationship('MedicinalMaterial', foreign_keys=[material2_id])

    def __repr__(self):
        return f"<MaterialInteraction {self.material1.name}-{self.material2.name}>"

# Model for data import logs
class DataImport(db.Model):
    __tablename__ = 'data_import'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    import_type = db.Column(db.String(50))  # What kind of data was imported
    rows_imported = db.Column(db.Integer)
    import_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20))  # success, error, etc.
    error_message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<DataImport {self.import_type} - {self.filename}>"

# Helper functions for token generation
def generate_uuid():
    """Generate a UUID string"""
    return str(uuid4())


# User model for authentication
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)

    # User preferences
    preferences = db.Column(JSONB, default=lambda: {'language': 'zh', 'theme': 'light'})

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# User activity log
class UserActivity(db.Model):
    __tablename__ = 'user_activity'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100), nullable=False)  # login, logout, register, etc.
    details = db.Column(db.Text, nullable=True)  # Additional details about the action
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6 address
    user_agent = db.Column(db.String(255), nullable=True)  # Browser/client info
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to user
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))

    def __repr__(self):
        return f"<UserActivity {self.action} by {self.user_id} at {self.timestamp}>"
