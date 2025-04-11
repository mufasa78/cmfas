"""
Main Streamlit application for CMFAS (Chinese Medicine Formula Analysis System)
"""
import streamlit as st
import os
import sys

def main():
    st.set_page_config(
        page_title="Chinese Medicine Prescription Analysis",
        page_icon="🌿",
        layout="wide"
    )
    
    st.title("Chinese Medicine Prescription Analysis System")
    st.write("Welcome to the Chinese Medicine Prescription Analysis System")
    
    # Print debug information
    st.write(f"Python version: {sys.version}")
    st.write(f"Current directory: {os.getcwd()}")
    st.write(f"Files in directory: {os.listdir('.')}")
    
    st.success("Application loaded successfully!")

if __name__ == "__main__":
    main()