"""
Simple health check script for Streamlit Cloud deployment
"""
import os
import sys
import platform
import streamlit as st

def main():
    st.set_page_config(page_title="Health Check", page_icon="✅")
    
    st.title("Streamlit Cloud Health Check")
    
    # System information
    st.header("System Information")
    system_info = {
        "Python Version": sys.version,
        "Platform": platform.platform(),
        "Working Directory": os.getcwd(),
        "Files in Directory": ", ".join(os.listdir(".")),
    }
    
    for key, value in system_info.items():
        st.text(f"{key}: {value}")
    
    # Environment variables (excluding sensitive ones)
    st.header("Environment Variables")
    env_vars = {k: v for k, v in os.environ.items() 
                if not any(sensitive in k.lower() for sensitive in 
                          ["key", "secret", "password", "token", "auth"])}
    
    for key, value in env_vars.items():
        st.text(f"{key}: {value}")
    
    # Package information
    st.header("Installed Packages")
    try:
        import pkg_resources # type: ignore
        packages = sorted([f"{pkg.key}=={pkg.version}" 
                          for pkg in pkg_resources.working_set])
        st.code("\n".join(packages))
    except Exception as e:
        st.error(f"Error getting package information: {e}")
    
    # Database connection test
    st.header("Database Connection Test")
    try:
        from sqlalchemy import create_engine, text
        
        # Get database URL from environment (with fallback)
        db_url = os.environ.get(
            "DATABASE_URL", 
            "postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
        )
        
        # Mask password in display
        display_url = db_url
        if "@" in display_url and ":" in display_url.split("@")[0]:
            parts = display_url.split("@")
            user_pass = parts[0].split(":")
            masked_url = f"{user_pass[0]}:****@{parts[1]}"
            display_url = masked_url
            
        st.text(f"Database URL: {display_url}")
        
        # Try to connect
        engine = create_engine(db_url, connect_args={'connect_timeout': 10})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            st.success(f"Database connection successful: {result.scalar()}")
    except Exception as e:
        st.error(f"Database connection error: {e}")
    
    st.success("Health check completed!")

if __name__ == "__main__":
    main()
