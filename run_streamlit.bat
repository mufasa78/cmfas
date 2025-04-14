@echo off
echo Starting Streamlit server...
python -m streamlit run streamlit_app.py --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
echo Streamlit server stopped.
pause
