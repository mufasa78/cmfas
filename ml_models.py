import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import logging
from app import db
from models import MedicinalMaterial, Prescription, MaterialInteraction, FormulaOptimization

logger = logging.getLogger(__name__)

class PrescriptionClassifier:
    """
    A machine learning model for classifying prescriptions based on their efficacy.
    """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.material_encoder = None
        self.efficacy_encoder = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _prepare_data(self):
        """Prepare training data from the database"""
        # Get all prescriptions and their materials
        prescriptions = Prescription.query.all()
        
        if not prescriptions:
            logger.warning("No prescriptions found in database for training")
            return None, None
        
        # Get all unique materials
        materials = MedicinalMaterial.query.all()
        material_names = [m.name for m in materials]
        
        # Create feature vectors for each prescription
        X = []
        y = []
        
        for prescription in prescriptions:
            # Create binary feature vector (1 if material is in prescription, 0 otherwise)
            feature_vector = [1 if material.name in [m.name for m in prescription.materials] else 0 
                             for material in materials]
            
            X.append(feature_vector)
            y.append(prescription.efficacy)
        
        if not X or not y:
            logger.warning("Empty feature vectors or labels")
            return None, None
        
        # Convert to numpy arrays
        X = np.array(X)
        
        # One-hot encode the efficacy labels
        self.efficacy_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        y_encoded = self.efficacy_encoder.fit_transform(np.array(y).reshape(-1, 1))
        
        return X, y_encoded
    
    def train(self):
        """Train the model on prescription data"""
        X, y = self._prepare_data()
        
        if X is None or y is None:
            logger.warning("Unable to train model due to data preparation issues")
            return False
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Prescription classifier model trained successfully")
        return True
    
    def predict_efficacy(self, materials):
        """
        Predict the efficacy of a prescription based on its materials
        
        Args:
            materials (list): List of material names in the prescription
            
        Returns:
            str: Predicted efficacy
        """
        if not self.is_trained:
            success = self.train()
            if not success:
                return "Unable to predict due to training issues"
        
        # Get all unique materials
        all_materials = MedicinalMaterial.query.all()
        material_names = [m.name for m in all_materials]
        
        # Create feature vector
        feature_vector = [1 if material in materials else 0 for material in material_names]
        
        # Scale the feature vector
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # Predict
        prediction = self.model.predict(feature_vector_scaled)
        
        # Convert one-hot encoded prediction back to label
        predicted_efficacy = self.efficacy_encoder.inverse_transform(prediction)[0][0]
        
        return predicted_efficacy

class FormulaOptimizer:
    """
    A machine learning model for optimizing formulas based on symptoms and materials.
    """
    def __init__(self):
        self.material_profiles = {}
        self.prescription_profiles = {}
        self.interaction_matrix = None
        self._build_profiles()
    
    def _build_profiles(self):
        """Build profiles for materials and prescriptions"""
        # Get all materials and their properties
        materials = MedicinalMaterial.query.all()
        
        for material in materials:
            self.material_profiles[material.name] = {
                'property': material.property,
                'flavor': material.flavor,
                'meridian': material.meridian,
                'usage_frequency': material.usage_frequency
            }
        
        # Get all prescriptions and their efficacies
        prescriptions = Prescription.query.all()
        
        for prescription in prescriptions:
            material_names = [m.name for m in prescription.materials]
            self.prescription_profiles[prescription.name] = {
                'materials': material_names,
                'efficacy': prescription.efficacy
            }
        
        # Build interaction matrix
        self._build_interaction_matrix()
    
    def _build_interaction_matrix(self):
        """Build interaction matrix between materials"""
        interactions = MaterialInteraction.query.all()
        
        if not interactions:
            logger.warning("No material interactions found in database")
            return
        
        # Create a dictionary to store interaction scores
        interaction_dict = {}
        
        for interaction in interactions:
            mat1 = interaction.material1.name
            mat2 = interaction.material2.name
            
            # Assign score based on interaction type (simplified)
            score = 1.0  # default
            if interaction.interaction_type == 'synergistic':
                score = 2.0
            elif interaction.interaction_type == 'antagonistic':
                score = -1.0
            
            # Store both directions
            if mat1 not in interaction_dict:
                interaction_dict[mat1] = {}
            if mat2 not in interaction_dict:
                interaction_dict[mat2] = {}
            
            interaction_dict[mat1][mat2] = score
            interaction_dict[mat2][mat1] = score
        
        self.interaction_matrix = interaction_dict
    
    def optimize_formula(self, symptoms, base_formula=None):
        """
        Optimize a formula based on symptoms and optionally a base formula
        
        Args:
            symptoms (str): Description of symptoms
            base_formula (list, optional): List of material names to start with
            
        Returns:
            dict: Optimized formula with explanation
        """
        # Find prescriptions with similar efficacy to symptoms
        relevant_prescriptions = self._find_relevant_prescriptions(symptoms)
        
        if not relevant_prescriptions:
            return {
                "success": False,
                "message": "No relevant prescriptions found for the given symptoms"
            }
        
        # Start with base formula or most common materials from relevant prescriptions
        if base_formula:
            optimized_formula = base_formula.copy()
        else:
            # Get most common materials from relevant prescriptions
            all_materials = []
            for prescription in relevant_prescriptions:
                all_materials.extend(self.prescription_profiles[prescription]['materials'])
            
            # Count and get top materials
            material_counts = Counter(all_materials)
            optimized_formula = [material for material, _ in material_counts.most_common(5)]
        
        # Optimize the formula by adding/removing materials based on interactions
        optimized_formula = self._refine_formula(optimized_formula, symptoms)
        
        # Generate explanation
        explanation = self._generate_explanation(optimized_formula, symptoms)
        
        # Save the recommendation to database
        optimized_data = {
            'materials': optimized_formula,
            'based_on': [p for p in relevant_prescriptions[:3]]
        }
        
        formula_rec = FormulaOptimization(
            user_symptoms=symptoms,
            recommended_formula=optimized_data,
            explanation=explanation
        )
        
        db.session.add(formula_rec)
        db.session.commit()
        
        return {
            "success": True,
            "formula": optimized_formula,
            "explanation": explanation
        }
    
    def _find_relevant_prescriptions(self, symptoms):
        """Find prescriptions with efficacy relevant to symptoms"""
        relevant = []
        
        for name, profile in self.prescription_profiles.items():
            efficacy = profile['efficacy']
            
            # Simple keyword matching (could be improved with NLP)
            if any(keyword in symptoms.lower() for keyword in efficacy.lower().split()):
                relevant.append(name)
        
        return relevant
    
    def _refine_formula(self, formula, symptoms):
        """Refine formula by adding/removing materials based on interactions"""
        if not self.interaction_matrix:
            return formula
        
        # Calculate interaction scores for current formula
        current_score = self._calculate_interaction_score(formula)
        
        # Try adding materials to improve score
        potential_additions = []
        
        for material in self.material_profiles:
            if material not in formula:
                test_formula = formula + [material]
                new_score = self._calculate_interaction_score(test_formula)
                
                if new_score > current_score:
                    potential_additions.append((material, new_score - current_score))
        
        # Sort by improvement score and add top materials
        potential_additions.sort(key=lambda x: x[1], reverse=True)
        
        refined_formula = formula.copy()
        for material, _ in potential_additions[:2]:  # Add up to 2 new materials
            refined_formula.append(material)
        
        return refined_formula
    
    def _calculate_interaction_score(self, materials):
        """Calculate interaction score for a set of materials"""
        if not self.interaction_matrix:
            return 0
        
        score = 0
        
        # Look at all pairs of materials
        for i, mat1 in enumerate(materials):
            for mat2 in materials[i+1:]:
                if mat1 in self.interaction_matrix and mat2 in self.interaction_matrix.get(mat1, {}):
                    score += self.interaction_matrix[mat1][mat2]
        
        return score
    
    def _generate_explanation(self, formula, symptoms):
        """Generate explanation for the optimized formula"""
        explanation = f"Formula optimized for symptoms: {symptoms}\n\n"
        
        # Explain each material's purpose
        explanation += "Material properties:\n"
        for material in formula:
            if material in self.material_profiles:
                profile = self.material_profiles[material]
                explanation += f"- {material}: {profile.get('property', 'N/A')} in nature, " \
                               f"{profile.get('flavor', 'N/A')} in flavor, " \
                               f"affects {profile.get('meridian', 'N/A')} meridian\n"
        
        # Explain interactions if available
        if self.interaction_matrix:
            explanation += "\nKey material interactions:\n"
            interactions_explained = 0
            
            for i, mat1 in enumerate(formula):
                for mat2 in formula[i+1:]:
                    if mat1 in self.interaction_matrix and mat2 in self.interaction_matrix.get(mat1, {}):
                        score = self.interaction_matrix[mat1][mat2]
                        interaction_type = "synergistic" if score > 0 else "antagonistic" if score < 0 else "neutral"
                        explanation += f"- {mat1} and {mat2}: {interaction_type} interaction\n"
                        interactions_explained += 1
                        
                        # Limit to a few key interactions
                        if interactions_explained >= 3:
                            break
                
                if interactions_explained >= 3:
                    break
        
        return explanation

class MaterialClusterer:
    """
    A machine learning model for clustering medicinal materials based on their properties.
    """
    def __init__(self):
        self.model = KMeans(n_clusters=5, random_state=42)
        self.pca = PCA(n_components=2)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = ['property_encoded', 'flavor_encoded', 'meridian_encoded', 'usage_frequency']
    
    def _prepare_data(self):
        """Prepare training data from the database"""
        # Get all materials
        materials = MedicinalMaterial.query.all()
        
        if not materials:
            logger.warning("No materials found in database for clustering")
            return None, None
        
        # Create pandas DataFrame
        data = []
        for material in materials:
            data.append({
                'name': material.name,
                'property': material.property or 'unknown',
                'flavor': material.flavor or 'unknown',
                'meridian': material.meridian or 'unknown',
                'usage_frequency': material.usage_frequency or 0
            })
        
        df = pd.DataFrame(data)
        
        # Encode categorical features
        for col in ['property', 'flavor', 'meridian']:
            # Simple label encoding
            unique_values = df[col].unique()
            value_map = {val: i for i, val in enumerate(unique_values)}
            df[f'{col}_encoded'] = df[col].map(value_map)
        
        # Fill NaN values
        for col in self.feature_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Check if required columns exist
        missing_cols = [col for col in self.feature_columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Missing columns in data: {missing_cols}")
            return None, None
        
        return df, df[self.feature_columns].values
    
    def train(self):
        """Train the clustering model on material data"""
        df, X = self._prepare_data()
        
        if X is None or df is None:
            logger.warning("Unable to train model due to data preparation issues")
            return None
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(X_scaled)
        self.is_trained = True
        
        # Apply PCA for visualization
        pca_result = self.pca.fit_transform(X_scaled)
        
        # Add results to DataFrame
        df['cluster'] = self.model.labels_
        df['pca_x'] = pca_result[:, 0]
        df['pca_y'] = pca_result[:, 1]
        
        logger.info("Material clustering model trained successfully")
        return df
    
    def get_cluster_data(self):
        """Get clustering results for visualization"""
        if not self.is_trained:
            df = self.train()
            if df is None:
                return {"success": False, "message": "Failed to train clustering model"}
        else:
            df, X = self._prepare_data()
            X_scaled = self.scaler.transform(X)
            df['cluster'] = self.model.predict(X_scaled)
            pca_result = self.pca.transform(X_scaled)
            df['pca_x'] = pca_result[:, 0]
            df['pca_y'] = pca_result[:, 1]
        
        # Prepare data for visualization
        result = []
        for cluster_id in df['cluster'].unique():
            cluster_df = df[df['cluster'] == cluster_id]
            
            # Get common properties in this cluster
            common_properties = cluster_df['property'].value_counts().index[0] if not cluster_df.empty else "Unknown"
            common_flavors = cluster_df['flavor'].value_counts().index[0] if not cluster_df.empty else "Unknown"
            
            cluster_data = {
                'cluster_id': int(cluster_id),
                'common_properties': common_properties,
                'common_flavors': common_flavors,
                'materials': []
            }
            
            # Add material points
            for _, row in cluster_df.iterrows():
                cluster_data['materials'].append({
                    'name': row['name'],
                    'x': float(row['pca_x']),
                    'y': float(row['pca_y']),
                    'usage_frequency': int(row['usage_frequency'])
                })
            
            result.append(cluster_data)
        
        return {
            "success": True,
            "clusters": result
        }
