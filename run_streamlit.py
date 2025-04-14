import os
import subprocess
import sys

def run_streamlit():
    """Run Streamlit with stable settings"""
    print("Starting Streamlit server...")
    
    # Get the Python executable path
    python_exe = sys.executable
    
    # Command to run Streamlit
    cmd = [
        python_exe,
        "-m",
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ]
    
    # Run the command
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
            
        # Wait for the process to complete
        process.wait()
        
        print("Streamlit server stopped.")
        return process.returncode
    
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_streamlit())
