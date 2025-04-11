"""
Streamlit configuration helper
This file is used to configure Streamlit for deployment
"""
import os

# Set environment variables for Streamlit
os.environ["STREAMLIT_DEPLOYMENT"] = "true"

# Print deployment message
print("Streamlit deployment configuration loaded")
