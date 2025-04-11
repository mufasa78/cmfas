"""
Health check script for Streamlit Cloud
This script sets the STREAMLIT_HEALTH_CHECK environment variable to true
and then runs the main streamlit app.
"""
import os
import subprocess
import sys

# Set environment variable for health check
os.environ["STREAMLIT_HEALTH_CHECK"] = "true"

# Run the streamlit app
subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
