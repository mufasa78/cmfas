"""
Streamlit application for Chinese Medicine Prescription Analysis System
This allows for deployment on Streamlit Cloud
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sqlalchemy import create_engine
import os
from chinese_converter import to_simplified, to_traditional
import json

# Database configuration
DB_URL = os.environ.get("DATABASE_URL")

# Set page configuration
st.set_page_config(
    page_title="中药处方分析系统 | Chinese Medicine Prescription Analysis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language selection
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # Default to Chinese

def change_language():
    st.session_state.language = 'en' if st.session_state.language == 'zh' else 'zh'

# Translations
translations = {
    'en': {
        'title': 'Chinese Medicine Prescription Analysis System',
        'language': 'Language: English | 语言：中文',
        'dashboard': 'Dashboard',
        'analytics': 'Analytics',
        'province_stats': 'Province Statistics',
        'material_stats': 'Material Usage',
        'property_dist': 'Property Distribution',
        'top_prescriptions': 'Top Prescriptions',
        'formula_optimization': 'Formula Optimization',
        'knowledge_graph': 'Knowledge Graph',
        'welcome': 'Welcome to the Chinese Medicine Prescription Analysis System',
        'description': 'This platform provides tools for analyzing traditional Chinese medicine prescriptions, visualizing medicinal material usage patterns, and optimizing formulations based on machine learning.',
        'db_status': 'Database Status',
        'connected': 'Connected',
        'not_connected': 'Not Connected',
        'total_materials': 'Total Medicinal Materials',
        'total_prescriptions': 'Total Prescriptions',
        'total_efficacies': 'Total Efficacy Categories', 
        'recent_prescriptions': 'Recent Prescriptions',
        'top_materials': 'Top Used Materials',
        'no_data': 'No data available. Please import data first.',
        'material_name': 'Material Name',
        'property': 'Property',
        'flavor': 'Flavor',
        'usage': 'Usage Count',
        'prescription_name': 'Prescription Name',
        'efficacy': 'Efficacy',
        'actions': 'Actions',
        'view': 'View',
        'note': 'Note: This is a Streamlit version of the application for cloud deployment. For full functionality, use the Flask application.'
    },
    'zh': {
        'title': '中药处方分析系统',
        'language': '语言：中文 | Language: English',
        'dashboard': '仪表盘',
        'analytics': '分析',
        'province_stats': '各省统计',
        'material_stats': '药材使用情况',
        'property_dist': '性味归经分布',
        'top_prescriptions': '按功效分类的常用处方',
        'formula_optimization': '方剂优化',
        'knowledge_graph': '知识图谱',
        'welcome': '欢迎使用中药处方分析系统',
        'description': '该平台提供分析传统中药处方、可视化药材使用模式以及基于机器学习优化配方的工具。',
        'db_status': '数据库状态',
        'connected': '已连接',
        'not_connected': '未连接',
        'total_materials': '药材总数',
        'total_prescriptions': '处方总数',
        'total_efficacies': '功效类别总数',
        'recent_prescriptions': '最近处方',
        'top_materials': '常用药材',
        'no_data': '暂无数据。请先导入数据。',
        'material_name': '药材名称',
        'property': '性质',
        'flavor': '味道',
        'usage': '使用次数',
        'prescription_name': '处方名称',
        'efficacy': '功效',
        'actions': '操作',
        'view': '查看',
        'note': '注意：这是用于云部署的Streamlit版本应用程序。要获得完整功能，请使用Flask应用程序。'
    }
}

def get_text(key):
    """Get translated text based on current language"""
    lang = st.session_state.language
    return translations[lang].get(key, key)

# Connect to database
@st.cache_resource
def get_connection():
    if not DB_URL:
        return None
    try:
        engine = create_engine(DB_URL)
        connection = engine.connect()
        return connection
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Database helper functions
def get_total_materials():
    conn = get_connection()
    if not conn:
        return 0
    try:
        result = conn.execute("SELECT COUNT(*) FROM medicinal_material")
        return result.fetchone()[0]
    except:
        return 0
    finally:
        conn.close()

def get_total_prescriptions():
    conn = get_connection()
    if not conn:
        return 0
    try:
        result = conn.execute("SELECT COUNT(*) FROM prescription")
        return result.fetchone()[0]
    except:
        return 0
    finally:
        conn.close()

def get_total_efficacy_categories():
    conn = get_connection()
    if not conn:
        return 0
    try:
        result = conn.execute("SELECT COUNT(*) FROM efficacy_category")
        return result.fetchone()[0]
    except:
        return 0
    finally:
        conn.close()

def get_recent_prescriptions(limit=5):
    conn = get_connection()
    if not conn:
        return []
    try:
        result = conn.execute(f"""
            SELECT id, name, efficacy, created_at 
            FROM prescription 
            ORDER BY created_at DESC 
            LIMIT {limit}
        """)
        return [dict(row) for row in result]
    except:
        return []
    finally:
        conn.close()

def get_top_materials(limit=5):
    conn = get_connection()
    if not conn:
        return []
    try:
        result = conn.execute(f"""
            SELECT id, name, property, flavor, usage_frequency 
            FROM medicinal_material 
            ORDER BY usage_frequency DESC 
            LIMIT {limit}
        """)
        return [dict(row) for row in result]
    except:
        return []
    finally:
        conn.close()

def get_province_statistics():
    conn = get_connection()
    if not conn:
        return {}
    try:
        result = conn.execute("""
            SELECT province_origin, COUNT(*) as count 
            FROM medicinal_material 
            WHERE province_origin IS NOT NULL AND province_origin != '' 
            GROUP BY province_origin 
            ORDER BY count DESC
        """)
        return {row[0]: row[1] for row in result}
    except:
        return {}
    finally:
        conn.close()

def get_material_usage_frequency(limit=20):
    conn = get_connection()
    if not conn:
        return []
    try:
        result = conn.execute(f"""
            SELECT name, usage_frequency 
            FROM medicinal_material 
            ORDER BY usage_frequency DESC 
            LIMIT {limit}
        """)
        return [dict(row) for row in result]
    except:
        return []
    finally:
        conn.close()

def get_property_distribution():
    conn = get_connection()
    if not conn:
        return {}
    try:
        result = conn.execute("""
            SELECT property, COUNT(*) as count 
            FROM medicinal_material 
            WHERE property IS NOT NULL AND property != '' 
            GROUP BY property 
            ORDER BY count DESC
        """)
        return {row[0]: row[1] for row in result}
    except:
        return {}
    finally:
        conn.close()

def get_flavor_distribution():
    conn = get_connection()
    if not conn:
        return {}
    try:
        result = conn.execute("""
            SELECT flavor, COUNT(*) as count 
            FROM medicinal_material 
            WHERE flavor IS NOT NULL AND flavor != '' 
            GROUP BY flavor 
            ORDER BY count DESC
        """)
        return {row[0]: row[1] for row in result}
    except:
        return {}
    finally:
        conn.close()

def get_meridian_distribution():
    conn = get_connection()
    if not conn:
        return {}
    try:
        result = conn.execute("""
            SELECT meridian, COUNT(*) as count 
            FROM medicinal_material 
            WHERE meridian IS NOT NULL AND meridian != '' 
            GROUP BY meridian 
            ORDER BY count DESC
        """)
        return {row[0]: row[1] for row in result}
    except:
        return {}
    finally:
        conn.close()

# Navigation and UI components
def sidebar():
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/streamlit/streamlit/master/lib/streamlit/static/leaf-green.png", width=50)
        st.title(get_text('title'))
        
        if st.button(get_text('language')):
            change_language()
        
        st.divider()
        
        # Navigation
        pages = {
            'dashboard': get_text('dashboard'),
            'province_stats': get_text('province_stats'),
            'material_stats': get_text('material_stats'),
            'property_distribution': get_text('property_dist'),
            'top_prescriptions': get_text('top_prescriptions'),
            'formula_optimization': get_text('formula_optimization'),
            'knowledge_graph': get_text('knowledge_graph')
        }
        
        selection = st.radio("", list(pages.values()))
        
        # Map selection back to page key
        for key, value in pages.items():
            if value == selection:
                st.session_state.page = key
                break
        
        # Database status
        conn = get_connection()
        status = get_text('connected') if conn else get_text('not_connected')
        status_color = "green" if conn else "red"
        st.divider()
        st.write(f"{get_text('db_status')}: :{status_color}[{status}]")
        
        # Note about Streamlit version
        st.divider()
        st.info(get_text('note'))

def dashboard_page():
    st.header(get_text('dashboard'))
    
    st.write(f"### {get_text('welcome')}")
    st.write(get_text('description'))
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(get_text('total_materials'), get_total_materials())
    with col2:
        st.metric(get_text('total_prescriptions'), get_total_prescriptions())
    with col3:
        st.metric(get_text('total_efficacies'), get_total_efficacy_categories())
    
    # Recent prescriptions and top materials
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('recent_prescriptions'))
        prescriptions = get_recent_prescriptions()
        if prescriptions:
            df = pd.DataFrame(prescriptions)
            df = df.rename(columns={
                'name': get_text('prescription_name'),
                'efficacy': get_text('efficacy')
            })
            st.dataframe(df[[get_text('prescription_name'), get_text('efficacy')]], use_container_width=True)
        else:
            st.info(get_text('no_data'))
    
    with col2:
        st.subheader(get_text('top_materials'))
        materials = get_top_materials()
        if materials:
            df = pd.DataFrame(materials)
            df = df.rename(columns={
                'name': get_text('material_name'),
                'property': get_text('property'),
                'flavor': get_text('flavor'),
                'usage_frequency': get_text('usage')
            })
            st.dataframe(df[[get_text('material_name'), get_text('property'), get_text('flavor'), get_text('usage')]], use_container_width=True)
        else:
            st.info(get_text('no_data'))

def province_stats_page():
    st.header(get_text('province_stats'))
    
    stats = get_province_statistics()
    if stats:
        # Create a dataframe for the chart
        df = pd.DataFrame(list(stats.items()), columns=['Province', 'Count'])
        
        # Create a bar chart
        fig = px.bar(
            df, 
            x='Province', 
            y='Count',
            color='Count',
            color_continuous_scale='Viridis',
            title=get_text('materials_by_province')
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the data table
        st.dataframe(df, use_container_width=True)
    else:
        st.info(get_text('no_data'))

def material_stats_page():
    st.header(get_text('material_stats'))
    
    usage_data = get_material_usage_frequency()
    if usage_data:
        # Create a dataframe for the chart
        df = pd.DataFrame(usage_data)
        
        # Create a bar chart
        fig = px.bar(
            df, 
            x='name', 
            y='usage_frequency',
            color='usage_frequency',
            color_continuous_scale='Viridis',
            title=get_text('usage_frequency')
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a pie chart for the top 10
        top_10 = df.head(10).copy()
        others = pd.DataFrame([{'name': 'Others', 'usage_frequency': df.iloc[10:]['usage_frequency'].sum()}])
        pie_data = pd.concat([top_10, others])
        
        fig = px.pie(
            pie_data, 
            values='usage_frequency', 
            names='name',
            title=get_text('usage_distribution')
        )
        
        # Display the pie chart
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(get_text('no_data'))

def property_distribution_page():
    st.header(get_text('property_dist'))
    
    properties = get_property_distribution()
    flavors = get_flavor_distribution()
    meridians = get_meridian_distribution()
    
    if properties or flavors or meridians:
        # Create tabs for different distributions
        tab1, tab2, tab3 = st.tabs(["五性", "五味", "归经"])
        
        with tab1:
            if properties:
                df = pd.DataFrame(list(properties.items()), columns=['Property', 'Count'])
                fig = px.pie(
                    df, 
                    values='Count', 
                    names='Property',
                    title="五性分布 (Five Properties Distribution)"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(get_text('no_data'))
        
        with tab2:
            if flavors:
                df = pd.DataFrame(list(flavors.items()), columns=['Flavor', 'Count'])
                fig = px.pie(
                    df, 
                    values='Count', 
                    names='Flavor',
                    title="五味分布 (Five Flavors Distribution)"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(get_text('no_data'))
        
        with tab3:
            if meridians:
                df = pd.DataFrame(list(meridians.items()), columns=['Meridian', 'Count'])
                fig = px.bar(
                    df, 
                    x='Meridian', 
                    y='Count',
                    color='Count',
                    color_continuous_scale='Viridis',
                    title="归经分布 (Meridian Distribution)"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(get_text('no_data'))
    else:
        st.info(get_text('no_data'))

def top_prescriptions_page():
    st.header(get_text('top_prescriptions'))
    st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

def formula_optimization_page():
    st.header(get_text('formula_optimization'))
    st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

def knowledge_graph_page():
    st.header(get_text('knowledge_graph'))
    st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

# Main application
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    
    # Show sidebar
    sidebar()
    
    # Display the selected page
    if st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'province_stats':
        province_stats_page()
    elif st.session_state.page == 'material_stats':
        material_stats_page()
    elif st.session_state.page == 'property_distribution':
        property_distribution_page()
    elif st.session_state.page == 'top_prescriptions':
        top_prescriptions_page()
    elif st.session_state.page == 'formula_optimization':
        formula_optimization_page()
    elif st.session_state.page == 'knowledge_graph':
        knowledge_graph_page()

if __name__ == "__main__":
    main()