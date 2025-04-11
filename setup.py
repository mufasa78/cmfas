from setuptools import setup

setup(
    name="cmfas",  # Changed to match repository name
    version="0.1.0",
    py_modules=["streamlit_app"],  # Specify the main module
    include_package_data=True,
    install_requires=[
        "streamlit>=1.30.0",
        "pandas>=2.0.0",
        "plotly>=5.15.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.5",
        "chinese-converter>=1.0.2",
        "numpy>=1.24.0",
        "email-validator>=2.0.0",
        "flask>=3.0.0",
        "flask-sqlalchemy>=3.0.0",
        "gunicorn>=20.0.0",
        "jieba>=0.42.1",
        "matplotlib>=3.0.0",
        "networkx>=3.0.0",
        "scikit-learn>=1.0.0",
        "werkzeug>=2.0.0",
    ],
)
