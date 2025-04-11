import streamlit as st

st.set_page_config(
    page_title="Chinese Medicine Prescription Analysis",
    page_icon="🌿",
    layout="wide"
)

st.title("Chinese Medicine Formula Analysis System")
st.write("This is a simple test app to verify deployment.")

st.success("If you can see this, the app is working correctly!")

# Display some debug information
import os
import sys

st.write("## Debug Information")
st.write(f"Python version: {sys.version}")
st.write(f"Current directory: {os.getcwd()}")
st.write(f"Files in directory: {os.listdir('.')}")
st.write(f"Python path: {sys.path}")

# Try to import some key packages
try:
    import pandas as pd
    import plotly.express as px
    from sqlalchemy import create_engine
    st.write("## Package Import Test")
    st.write("✅ pandas imported successfully")
    st.write("✅ plotly.express imported successfully")
    st.write("✅ sqlalchemy imported successfully")
except ImportError as e:
    st.error(f"Error importing packages: {e}")
