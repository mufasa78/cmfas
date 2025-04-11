"""
Entry point for Streamlit Cloud deployment
This file imports from the cmfas package to ensure proper package structure
"""
try:
    # Try to import from the cmfas package
    from cmfas.streamlit_app import main

    # Print debug information
    import sys
    import os
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    print(f"Python path: {sys.path}")

    if __name__ == "__main__":
        main()
except ImportError as e:
    # If import fails, show error and debug information
    import streamlit as st
    import sys
    import os

    st.error(f"Error importing from cmfas package: {e}")
    st.write(f"Python version: {sys.version}")
    st.write(f"Current directory: {os.getcwd()}")
    st.write(f"Files in directory: {os.listdir('.')}")
    st.write(f"Python path: {sys.path}")