import networkx as nx
import json
from app import db
from models import MedicinalMaterial, Prescription, MaterialInteraction

def build_knowledge_graph():
    """
    Build a knowledge graph of Chinese medicine materials and prescriptions
    
    Returns:
        dict: Graph data in a format suitable for visualization
    """
    # Create a NetworkX graph
    G = nx.Graph()
    
    # Add nodes for materials
    materials = MedicinalMaterial.query.all()
    for material in materials:
        G.add_node(f"m_{material.id}", 
                  name=material.name,
                  type="material",
                  property=material.property,
                  flavor=material.flavor,
                  meridian=material.meridian)
    
    # Add nodes for prescriptions
    prescriptions = Prescription.query.all()
    for prescription in prescriptions:
        G.add_node(f"p_{prescription.id}", 
                  name=prescription.name,
                  type="prescription",
                  efficacy=prescription.efficacy)
    
    # Add edges between prescriptions and materials
    for prescription in prescriptions:
        for material in prescription.materials:
            G.add_edge(f"p_{prescription.id}", f"m_{material.id}", type="contains")
    
    # Add edges between materials (interactions)
    interactions = MaterialInteraction.query.all()
    for interaction in interactions:
        G.add_edge(f"m_{interaction.material1_id}", 
                  f"m_{interaction.material2_id}", 
                  type=interaction.interaction_type,
                  description=interaction.description)
    
    # Convert to a format suitable for visualization (D3.js)
    nodes = []
    for node, data in G.nodes(data=True):
        node_type = data['type']
        node_data = {
            'id': node,
            'name': data['name'],
            'type': node_type
        }
        
        # Add type-specific attributes
        if node_type == 'material':
            node_data.update({
                'property': data.get('property', ''),
                'flavor': data.get('flavor', ''),
                'meridian': data.get('meridian', '')
            })
        elif node_type == 'prescription':
            node_data.update({
                'efficacy': data.get('efficacy', '')
            })
        
        nodes.append(node_data)
    
    links = []
    for source, target, data in G.edges(data=True):
        links.append({
            'source': source,
            'target': target,
            'type': data.get('type', ''),
            'description': data.get('description', '')
        })
    
    return {
        'nodes': nodes,
        'links': links
    }

def get_material_subgraph(material_id):
    """
    Get a subgraph centered on a specific material
    
    Args:
        material_id (int): ID of the material
        
    Returns:
        dict: Subgraph data
    """
    # Get the full graph
    full_graph = build_knowledge_graph()
    
    # Find the material node
    material_node_id = f"m_{material_id}"
    
    # Create a new graph with just the material and its immediate connections
    nodes = []
    links = []
    
    # Find the material node
    material_node = None
    for node in full_graph['nodes']:
        if node['id'] == material_node_id:
            material_node = node
            nodes.append(node)
            break
    
    if not material_node:
        return {'nodes': [], 'links': []}
    
    # Find immediate connections
    connected_node_ids = set()
    for link in full_graph['links']:
        if link['source'] == material_node_id:
            connected_node_ids.add(link['target'])
            links.append(link)
        elif link['target'] == material_node_id:
            connected_node_ids.add(link['source'])
            links.append(link)
    
    # Add connected nodes
    for node in full_graph['nodes']:
        if node['id'] in connected_node_ids:
            nodes.append(node)
    
    return {
        'nodes': nodes,
        'links': links
    }

def get_prescription_subgraph(prescription_id):
    """
    Get a subgraph centered on a specific prescription
    
    Args:
        prescription_id (int): ID of the prescription
        
    Returns:
        dict: Subgraph data
    """
    # Get the full graph
    full_graph = build_knowledge_graph()
    
    # Find the prescription node
    prescription_node_id = f"p_{prescription_id}"
    
    # Create a new graph with just the prescription and its materials
    nodes = []
    links = []
    
    # Find the prescription node
    prescription_node = None
    for node in full_graph['nodes']:
        if node['id'] == prescription_node_id:
            prescription_node = node
            nodes.append(node)
            break
    
    if not prescription_node:
        return {'nodes': [], 'links': []}
    
    # Find materials in this prescription
    material_node_ids = set()
    for link in full_graph['links']:
        if link['source'] == prescription_node_id and link['type'] == 'contains':
            material_node_ids.add(link['target'])
            links.append(link)
        elif link['target'] == prescription_node_id and link['type'] == 'contains':
            material_node_ids.add(link['source'])
            links.append(link)
    
    # Add material nodes
    for node in full_graph['nodes']:
        if node['id'] in material_node_ids:
            nodes.append(node)
    
    # Add interactions between materials
    for link in full_graph['links']:
        if (link['source'] in material_node_ids and link['target'] in material_node_ids):
            links.append(link)
    
    return {
        'nodes': nodes,
        'links': links
    }

def get_related_prescriptions(material_ids):
    """
    Find prescriptions that contain all of the given materials
    
    Args:
        material_ids (list): List of material IDs
        
    Returns:
        list: List of prescription objects
    """
    if not material_ids:
        return []
    
    # Convert to set for faster lookups
    material_ids = set(material_ids)
    
    # Get all prescriptions
    prescriptions = Prescription.query.all()
    
    # Filter prescriptions containing all the materials
    related_prescriptions = []
    for prescription in prescriptions:
        material_ids_in_prescription = {material.id for material in prescription.materials}
        if material_ids.issubset(material_ids_in_prescription):
            related_prescriptions.append(prescription)
    
    return related_prescriptions
