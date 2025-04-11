"""
CMFAS package initialization
Chinese Medicine Formula Analysis System
"""
__version__ = "0.1.0"

# Import main components to make them available at package level
try:
    from .streamlit_app import main
except ImportError as e:
    print(f"Warning: Could not import streamlit_app module: {e}")
