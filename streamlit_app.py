"""
Entry point for Streamlit Cloud deployment
This file imports from the cmfas package to ensure proper package structure
"""
import sys
import os

# Print debug information
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print(f"Python path: {sys.path}")

# Add the current directory to the Python path to help with imports
sys.path.insert(0, os.getcwd())

# Try different import strategies
try:
    # First, try to import from the package
    import cmfas
    from cmfas.streamlit_app import main
    print("Successfully imported from cmfas package")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error importing main app: {e}")
    print("Trying fallback app...")

    try:
        # Try to import the fallback app
        from cmfas.fallback_app import fallback_main
        print("Successfully imported fallback app")

        if __name__ == "__main__":
            fallback_main()

    except ImportError as e2:
        # If all else fails, create a minimal Streamlit app inline
        print(f"Error importing fallback app: {e2}")
        print("Using inline minimal app")

        import streamlit as st

        st.set_page_config(page_title="CMFAS - Error", page_icon="🌿")
        st.title("Chinese Medicine Formula Analysis System - Error")
        st.error("Failed to load the application")

        st.write(f"Main import error: {e}")
        st.write(f"Fallback import error: {e2}")

        st.header("System Information")
        st.write(f"Python version: {sys.version}")
        st.write(f"Current directory: {os.getcwd()}")
        st.write(f"Files in directory: {os.listdir('.')}")

        if os.path.exists('cmfas'):
            st.write(f"cmfas directory exists, contents: {os.listdir('cmfas')}")
        else:
            st.write("cmfas directory does not exist")