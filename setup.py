from setuptools import setup, find_packages # type: ignore

setup(
    name="cmfas",
    version="0.1.0",
    packages=["cmfas"],
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0.0",
        "pandas>=1.0.0",
        "plotly>=5.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
    ],
    python_requires=">=3.9",
)
