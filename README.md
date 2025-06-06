# Chinese Medicine Prescription Analysis System (CMFAS)

![Chinese Medicine](https://raw.githubusercontent.com/streamlit/streamlit/master/lib/streamlit/static/leaf-green.png)

A comprehensive platform for analyzing traditional Chinese medicine prescriptions, visualizing medicinal material usage patterns, and optimizing formulations using machine learning.

## 🌟 Features

- **Bilingual Support**: Full support for both English and Chinese languages
- **Dashboard**: Overview of key statistics and recent prescriptions
- **Province Statistics**: Visualization of medicinal materials by province
- **Material Usage Analysis**: Frequency and patterns of medicinal material usage
- **Property Distribution**: Analysis of the five properties (五性), five flavors (五味), and meridian tropism (归经)
- **Top Prescriptions**: Most commonly used prescriptions by efficacy category
- **Formula Optimization**: AI-powered recommendation system for optimizing prescriptions based on symptoms
- **Knowledge Graph**: Visual representation of relationships between medicinal materials and prescriptions
- **Data Import/Export**: Tools for importing and exporting prescription and material data

## 🚀 Deployment Options

This application can be deployed in two ways:

### 1. Flask Application (Full Features)

The Flask application provides the complete feature set with a rich user interface.

```bash
# Run with Flask development server
python main.py

# For production deployment on Unix-like systems
gunicorn main:app --bind 0.0.0.0:5000
```

### 2. Streamlit Application (Cloud-Ready)

The Streamlit version is optimized for cloud deployment with a simplified interface.

```bash
streamlit run streamlit_app.py
```

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap, ECharts, Plotly
- **Database**: PostgreSQL (Neon)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Natural Language Processing**: Jieba (for Chinese text processing)
- **Visualization**: Matplotlib, Plotly, NetworkX
- **Cloud Deployment**: Streamlit Cloud, Gunicorn

## 📊 Database Schema

The application uses a relational database with the following main models:

- **MedicinalMaterial**: Information about individual medicinal herbs and materials
- **Prescription**: Traditional formulas and their compositions
- **EfficacyCategory**: Categories of medicinal effects
- **MaterialInteraction**: Relationships between different materials
- **FormulaOptimization**: Results from the AI optimization system

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mufasa78/cmfas.git
   cd cmfas
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional):
   ```bash
   export DATABASE_URL="postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
   export SESSION_SECRET="your_secret_key"
   ```

5. Run the application:
   ```bash
   # Flask version
   python main.py

   # Streamlit version
   streamlit run streamlit_app.py
   ```

## 🌐 Accessing the Application

- **Flask**: http://localhost:5000
- **Streamlit**: http://localhost:8501

## 📝 Configuration

The application can be configured through environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for Flask sessions
- `STREAMLIT_DEPLOYMENT`: Set to "true" for Streamlit Cloud deployment
- `STREAMLIT_HEALTH_CHECK`: Set to "true" for health check mode

## 🧪 Testing

To run the health check for the Streamlit application:

```bash
python streamlit_health_check.py
```

## 📚 Data Sources

The system is designed to work with traditional Chinese medicine data from various sources. Sample data is included in the `data` directory.

## 🔄 Deployment Workflow

1. **Local Development**: Use Flask for development and testing
2. **Cloud Deployment**: Deploy the Streamlit version to Streamlit Cloud
3. **Production**: Deploy the Flask version with Gunicorn for production use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or support, please open an issue on the GitHub repository.
