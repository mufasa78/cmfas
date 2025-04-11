"""
Fallback Streamlit application for Chinese Medicine Prescription Analysis System
This is a minimal version that will be used if the main app fails to load
"""
import streamlit as st
import os
import sys

def fallback_main():
    """Fallback main function that displays diagnostic information"""
    st.set_page_config(
        page_title="CMFAS - Diagnostic Mode",
        page_icon="🌿",
        layout="wide"
    )
    
    st.title("Chinese Medicine Formula Analysis System - Diagnostic Mode")
    st.warning("The application is running in diagnostic mode due to package loading issues.")
    
    st.header("System Information")
    st.write(f"Python version: {sys.version}")
    st.write(f"Current directory: {os.getcwd()}")
    
    # Display files in current directory
    st.subheader("Files in current directory")
    files = os.listdir('.')
    st.write(files)
    
    # Display Python path
    st.subheader("Python path")
    st.write(sys.path)
    
    # Check for cmfas directory
    st.subheader("CMFAS package")
    if os.path.exists('cmfas'):
        st.write(f"cmfas directory exists, contents: {os.listdir('cmfas')}")
    else:
        st.error("cmfas directory does not exist")
    
    # Display environment variables
    st.subheader("Environment Variables")
    env_vars = {key: value for key, value in os.environ.items() if not key.startswith('_')}
    st.write(env_vars)
    
    st.header("Troubleshooting Steps")
    st.markdown("""
    1. Check that the cmfas package is properly installed
    2. Verify that all required dependencies are installed
    3. Check the Python path to ensure the package can be found
    4. Review the package structure to ensure it follows Python conventions
    """)

if __name__ == "__main__":
    fallback_main()
