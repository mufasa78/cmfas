"""
Streamlit application for Chinese Medicine Prescription Analysis System
"""
import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Print debug information
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

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

if __name__ == "__main__":
    main()