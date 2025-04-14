"""
Streamlit application for Chinese Medicine Prescription Analysis System
This is a flat version for direct deployment on Streamlit Cloud
"""
import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime, timedelta, timezone
# Import dummy authentication functions
from dummy_auth import (register_user, login_user, logout_user, verify_email,
                      request_password_reset, reset_password, update_user_preferences,
                      log_user_activity, get_user_activity_logs, is_valid_email, generate_token)

# Print debug information
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print(f"Python path: {sys.path}")

# Handle potential import errors gracefully
try:
    import plotly.express as px
    from sqlalchemy import create_engine, text
except ImportError as e:
    if 'language' in st.session_state and st.session_state.language == 'zh':
        st.error(f"导入所需包时出错：{e}")
        st.info("请检查您的requirements.txt文件并确保所有依赖项已安装。")
    else:
        st.error(f"Error importing required packages: {e}")
        st.info("Please check your requirements.txt file and make sure all dependencies are installed.")

# Database configuration
DB_URL = "postgresql://neondb_owner:npg_Bnf7usLCGcZ5@ep-holy-tree-a5vv7bmk-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Flag to check if we're in a health check
is_health_check = os.environ.get("STREAMLIT_HEALTH_CHECK", "false").lower() == "true"

# Set page configuration
st.set_page_config(
    page_title="中药处方分析系统 | Chinese Medicine Prescription Analysis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Chinese Medicine Prescription Analysis System"
    }
)

# Custom CSS for light mode and sidebar positioning
st.markdown('''
<style>
    /* Light mode styling */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Ensure text is visible on light background */
    .stSelectbox, .stMultiselect, .stSlider, .stRadio > div > div > label, .stCheckbox > div > div > label {
        color: #31333F !important;
    }

    /* Ensure dropdown styling for light mode */
    .stSelectbox > div > div > div, .stMultiselect > div > div > div {
        color: #31333F !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CCC !important;
    }

    /* Dropdown options in light mode */
    .stSelectbox > div > div > div > ul > li, .stMultiselect > div > div > div > ul > li {
        color: #31333F !important;
        background-color: #FFFFFF !important;
    }

    /* Highlight selected dropdown option */
    .stSelectbox > div > div > div > ul > li:hover, .stMultiselect > div > div > div > ul > li:hover {
        background-color: #F0F2F6 !important;
    }

    /* Text inputs in light mode */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        color: #31333F !important;
        border: 1px solid #CCC !important;
    }

    /* Button styling for light mode */
    .stButton > button {
        color: #31333F !important;
        border-color: #CCC !important;
        background-color: #FFFFFF !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        border-color: #4CAF50 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transform: translateY(-1px) !important;
    }

    /* Sidebar specific button styling */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }

    /* Sidebar subheader styling */
    section[data-testid="stSidebar"] h3 {
        font-size: 1rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.75rem !important;
        color: #4CAF50 !important;
    }

    /* Sidebar styling - allowing main content to adjust */
    section[data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
        height: 100vh !important;
        padding-top: 1.5rem !important;
        box-shadow: 2px 0px 5px rgba(0,0,0,0.1) !important;
        overflow: hidden !important;
        min-width: 250px !important;
    }

    /* Ensure sidebar toggle button is visible */
    button[kind="header"] {
        z-index: 999 !important;
    }

    /* Make the sidebar content scrollable */
    section[data-testid="stSidebar"] > div {
        height: 100% !important;
        overflow-y: auto !important;
    }

    /* Hide the sidebar's scrollbar for cleaner look */
    section[data-testid="stSidebar"] > div::-webkit-scrollbar {
        width: 6px !important;
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] > div::-webkit-scrollbar-thumb {
        background-color: rgba(0,0,0,0.1) !important;
        border-radius: 3px !important;
    }

    /* Sidebar header styling */
    section[data-testid="stSidebar"] .stImage {
        text-align: center !important;
        margin: 0 auto 1rem auto !important;
        display: block !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.3rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
    }

    /* Improve radio button styling for navigation */
    section[data-testid="stSidebar"] .stRadio > div {
        padding: 0.25rem 0 !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > div > label {
        padding: 0.75rem 1rem !important;
        border-radius: 6px !important;
        width: 100% !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 4px !important;
        border-left: 3px solid transparent !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > div > label:hover {
        background-color: rgba(151, 166, 195, 0.15) !important;
        transform: translateX(2px) !important;
    }

    section[data-testid="stSidebar"] .stRadio > div > div > label[data-baseweb="radio"] > div:first-child {
        margin-right: 10px !important;
    }

    /* Selected radio button styling */
    section[data-testid="stSidebar"] .stRadio > div > div > label[aria-checked="true"] {
        background-color: rgba(151, 166, 195, 0.25) !important;
        font-weight: 600 !important;
        border-left: 3px solid #4CAF50 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }

    /* Hide radio button circles for cleaner navigation */
    section[data-testid="stSidebar"] .stRadio > div > div > label > div:first-child {
        display: none !important;
    }

    /* Divider styling */
    section[data-testid="stSidebar"] hr {
        margin: 1rem 0 !important;
    }

    /* Status indicator styling */
    section[data-testid="stSidebar"] p {
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Info box styling */
    section[data-testid="stSidebar"] .stAlert {
        padding: 0.5rem !important;
        font-size: 0.8rem !important;
    }

    /* Adjust main content to work with collapsible sidebar */
    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Ensure content is properly spaced */
    .main {
        padding: 0 !important;
    }
</style>
''', unsafe_allow_html=True)

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
        'count_column': 'Count',
        'note': 'Note: This is a Streamlit version of the application for cloud deployment. For full functionality, use the Flask application.',
        'health_check_ok': 'Health check: OK',
        'materials_by_province': 'Materials by Province',
        'province_origin_description': 'Province of Origin',
        'usage_frequency': 'Usage Frequency',
        'usage_distribution': 'Usage Distribution',
        'meridian_label': 'Meridian',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'username': 'Username',
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'login_success': 'Login successful',
        'login_failed': 'Login failed. Please check your username and password.',
        'register_success': 'Registration successful. You can now log in.',
        'register_failed': 'Registration failed. Please try again.',
        'passwords_not_match': 'Passwords do not match',
        'email_invalid': 'Invalid email address',
        'username_exists': 'Username already exists',
        'email_exists': 'Email already exists',
        'profile': 'Profile',
        'welcome_user': 'Welcome, {}',
        'verify_email': 'Verify Email',
        'email_verification': 'Email Verification',
        'verification_sent': 'Verification email sent. Please check your inbox.',
        'verification_success': 'Email verified successfully.',
        'verification_failed': 'Email verification failed.',
        'reset_password': 'Reset Password',
        'forgot_password': 'Forgot Password?',
        'reset_password_sent': 'Password reset instructions sent to your email.',
        'reset_password_success': 'Password reset successfully.',
        'reset_password_failed': 'Password reset failed.',
        'new_password': 'New Password',
        'confirm_new_password': 'Confirm New Password',
        'submit': 'Submit',
        'preferences': 'Preferences',
        'theme': 'Theme',
        'light': 'Light',
        'notifications': 'Notifications',
        'enable_notifications': 'Enable Notifications',
        'save_preferences': 'Save Preferences',
        'preferences_saved': 'Preferences saved successfully.',
        'activity_log': 'Activity Log',
        'action': 'Action',
        'timestamp': 'Timestamp',
        'details': 'Details',
        'no_activity': 'No activity recorded yet.'
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
        'count_column': '数量',
        'note': '注意：这是用于云部署的Streamlit版本应用程序。要获得完整功能，请使用Flask应用程序。',
        'health_check_ok': '健康检查：正常',
        'materials_by_province': '各省药材分布',
        'province_origin_description': '原产省份',
        'usage_frequency': '使用频率',
        'usage_distribution': '使用分布',
        'meridian_label': '归经',
        'login': '登录',
        'register': '注册',
        'logout': '退出登录',
        'username': '用户名',
        'email': '电子邮箱',
        'password': '密码',
        'confirm_password': '确认密码',
        'login_success': '登录成功',
        'login_failed': '登录失败。请检查您的用户名和密码。',
        'register_success': '注册成功。您现在可以登录。',
        'register_failed': '注册失败。请重试。',
        'passwords_not_match': '密码不匹配',
        'email_invalid': '无效的电子邮箱地址',
        'username_exists': '用户名已存在',
        'email_exists': '电子邮箱已存在',
        'profile': '个人资料',
        'welcome_user': '欢迎，{}',
        'verify_email': '验证邮箱',
        'email_verification': '邮箱验证',
        'verification_sent': '验证邮件已发送。请检查您的收件箱。',
        'verification_success': '邮箱验证成功。',
        'verification_failed': '邮箱验证失败。',
        'reset_password': '重置密码',
        'forgot_password': '忘记密码？',
        'reset_password_sent': '密码重置说明已发送到您的邮箱。',
        'reset_password_success': '密码重置成功。',
        'reset_password_failed': '密码重置失败。',
        'new_password': '新密码',
        'confirm_new_password': '确认新密码',
        'submit': '提交',
        'preferences': '偏好设置',
        'theme': '主题',
        'light': '浅色',
        'notifications': '通知',
        'enable_notifications': '启用通知',
        'save_preferences': '保存偏好设置',
        'preferences_saved': '偏好设置保存成功。',
        'activity_log': '活动日志',
        'action': '操作',
        'timestamp': '时间戳',
        'details': '详情',
        'no_activity': '尚未记录活动。'
    }
}

def get_text(key):
    """Get translated text based on current language"""
    lang = st.session_state.language
    return translations[lang].get(key, key)

# Connect to database
@st.cache_resource(ttl=300)  # Cache for 5 minutes
def get_engine():
    # Skip actual database connection during health checks
    if is_health_check:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.info("检测到健康检查 - 跳过数据库连接")
        else:
            st.info("Health check detected - skipping database connection")
        return None

    if not DB_URL:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error("数据库连接字符串未设置")
        else:
            st.error("Database connection string not set")
        return None

    try:
        # Configure SQLAlchemy engine with proper connection pooling for Neon PostgreSQL
        engine = create_engine(
            DB_URL,
            connect_args={
                'connect_timeout': 30,  # Longer timeout for initial connection
                'keepalives': 1,        # Enable keepalives
                'keepalives_idle': 30,  # Send keepalive every 30 seconds
                'keepalives_interval': 10,  # Retry interval
                'keepalives_count': 5   # Number of retries
            },
            pool_pre_ping=True,         # Verify connections before using them
            pool_recycle=300,           # Recycle connections every 5 minutes
            pool_size=5,                # Limit pool size for Neon's connection pooler
            max_overflow=10             # Allow up to 10 overflow connections
        )

        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.success("数据库连接成功")
        else:
            st.success("Database connected successfully")

        return engine
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"数据库连接错误：{e}")
        else:
            st.error(f"Database connection error: {e}")
        return None

# Database helper functions
def get_total_materials():
    engine = get_engine()
    if not engine:
        return 0
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT COUNT(*) FROM medicinal_material"))
            return result.scalar()
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询药材时出错：{e}")
        else:
            st.error(f"Error querying materials: {e}")
        return 0

def get_total_prescriptions():
    engine = get_engine()
    if not engine:
        return 0
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT COUNT(*) FROM prescription"))
            return result.scalar()
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询处方时出错：{e}")
        else:
            st.error(f"Error querying prescriptions: {e}")
        return 0

def get_total_efficacy_categories():
    engine = get_engine()
    if not engine:
        return 0
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT COUNT(*) FROM efficacy_category"))
            return result.scalar()
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询功效类别时出错：{e}")
        else:
            st.error(f"Error querying efficacy categories: {e}")
        return 0

def get_recent_prescriptions(limit=5):
    engine = get_engine()
    if not engine:
        return []
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text(f"""
                SELECT id, name, efficacy, created_at
                FROM prescription
                ORDER BY created_at DESC
                LIMIT {limit}
            """))
            # Convert rows to dictionaries using _mapping attribute
            return [dict(row._mapping) for row in result]
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询最近处方时出错：{e}")
        else:
            st.error(f"Error querying recent prescriptions: {e}")
        return []

def get_top_materials(limit=5):
    engine = get_engine()
    if not engine:
        return []
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text(f"""
                SELECT id, name, property, flavor, usage_frequency
                FROM medicinal_material
                ORDER BY usage_frequency DESC
                LIMIT {limit}
            """))
            # Convert rows to dictionaries using _mapping attribute
            return [dict(row._mapping) for row in result]
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询热门药材时出错：{e}")
        else:
            st.error(f"Error querying top materials: {e}")
        return []

def get_province_statistics():
    engine = get_engine()
    if not engine:
        return {}
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT province_origin, COUNT(*) as count
                FROM medicinal_material
                WHERE province_origin IS NOT NULL AND province_origin != ''
                GROUP BY province_origin
                ORDER BY count DESC
            """))
            return {row[0]: row[1] for row in result}
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询省份统计时出错：{e}")
        else:
            st.error(f"Error querying province statistics: {e}")
        return {}

def get_material_usage_frequency(limit=20):
    engine = get_engine()
    if not engine:
        return []
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text(f"""
                SELECT name, usage_frequency
                FROM medicinal_material
                ORDER BY usage_frequency DESC
                LIMIT {limit}
            """))
            # Convert rows to dictionaries using _mapping attribute
            return [dict(row._mapping) for row in result]
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询药材使用频率时出错：{e}")
        else:
            st.error(f"Error querying material usage frequency: {e}")
        return []

def get_property_distribution():
    engine = get_engine()
    if not engine:
        return {}
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT property, COUNT(*) as count
                FROM medicinal_material
                WHERE property IS NOT NULL AND property != ''
                GROUP BY property
                ORDER BY count DESC
            """))
            return {row[0]: row[1] for row in result}
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询性质分布时出错：{e}")
        else:
            st.error(f"Error querying property distribution: {e}")
        return {}

def get_flavor_distribution():
    engine = get_engine()
    if not engine:
        return {}
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT flavor, COUNT(*) as count
                FROM medicinal_material
                WHERE flavor IS NOT NULL AND flavor != ''
                GROUP BY flavor
                ORDER BY count DESC
            """))
            return {row[0]: row[1] for row in result}
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询味道分布时出错：{e}")
        else:
            st.error(f"Error querying flavor distribution: {e}")
        return {}

def get_meridian_distribution():
    engine = get_engine()
    if not engine:
        return {}
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT meridian, COUNT(*) as count
                FROM medicinal_material
                WHERE meridian IS NOT NULL AND meridian != ''
                GROUP BY meridian
                ORDER BY count DESC
            """))
            return {row[0]: row[1] for row in result}
    except Exception as e:
        if 'language' in st.session_state and st.session_state.language == 'zh':
            st.error(f"查询归经分布时出错：{e}")
        else:
            st.error(f"Error querying meridian distribution: {e}")
        return {}

# Authentication functions are now imported from dummy_auth.py

# Login and logout functions are now imported from dummy_auth.py

# Email verification and password reset functions are now imported from dummy_auth.py

# All authentication-related functions are now imported from dummy_auth.py

# Navigation and UI components
def sidebar():
    with st.sidebar:
        # App header
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://raw.githubusercontent.com/streamlit/streamlit/master/lib/streamlit/static/leaf-green.png", width=50)
        with col2:
            st.title(get_text('title'))

        # Language switcher
        lang_col1, lang_col2 = st.columns([3, 1])
        with lang_col1:
            st.write(f"🌐 {get_text('language').split(' | ')[0]}")
        with lang_col2:
            if st.button("🔄", help="Switch language"):
                change_language()

        st.divider()

        # User authentication section
        if 'is_authenticated' not in st.session_state:
            st.session_state.is_authenticated = False

        if st.session_state.is_authenticated:
            # User is logged in
            st.success(f"👤 {get_text('welcome_user').format(st.session_state.username)}")
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🚪", help=get_text('logout')):
                    logout_user()
                    st.rerun()
        else:
            # User is not logged in - show tabs for login and registration
            login_tab, register_tab = st.tabs([f"🔑 {get_text('login')}", f"📝 {get_text('register')}"])

            with login_tab:
                login_form = st.form("login_form")
                username = login_form.text_input(get_text('username'))
                password = login_form.text_input(get_text('password'), type="password")
                login_submit = login_form.form_submit_button(f"🔓 {get_text('login')}")

                if login_submit:
                    if username and password:
                        success, error = login_user(username, password)
                        if success:
                            st.success(get_text('login_success'))
                            st.rerun()
                        else:
                            st.error(get_text('login_failed'))
                    else:
                        st.warning(get_text('login_failed'))

            with register_tab:
                register_form = st.form("register_form")
                new_username = register_form.text_input(get_text('username'))
                new_email = register_form.text_input(get_text('email'))
                new_password = register_form.text_input(get_text('password'), type="password")
                confirm_password = register_form.text_input(get_text('confirm_password'), type="password")
                register_submit = register_form.form_submit_button(f"✅ {get_text('register')}")

                if register_submit:
                    if not new_username or not new_email or not new_password or not confirm_password:
                        st.warning(get_text('register_failed'))
                    elif new_password != confirm_password:
                        st.error(get_text('passwords_not_match'))
                    elif not is_valid_email(new_email):
                        st.error(get_text('email_invalid'))
                    else:
                        success, error = register_user(new_username, new_email, new_password)
                        if success:
                            st.success(get_text('register_success'))
                        else:
                            if error == "username_exists":
                                st.error(get_text('username_exists'))
                            elif error == "email_exists":
                                st.error(get_text('email_exists'))
                            else:
                                st.error(get_text('register_failed'))

        st.divider()

        # Navigation with icons
        st.subheader("📊 Navigation")

        # Define pages with icons
        pages = {
            'dashboard': f"🏠 {get_text('dashboard')}",
            'province_stats': f"🗺️ {get_text('province_stats')}",
            'material_stats': f"🌿 {get_text('material_stats')}",
            'property_distribution': f"⚖️ {get_text('property_dist')}",
            'top_prescriptions': f"📋 {get_text('top_prescriptions')}",
            'formula_optimization': f"🧪 {get_text('formula_optimization')}",
            'knowledge_graph': f"🔍 {get_text('knowledge_graph')}"
        }

        # Add profile page if user is authenticated
        if st.session_state.is_authenticated:
            pages['profile'] = f"👤 {get_text('profile')}"

        selection = st.radio("", list(pages.values()))

        # Map selection back to page key
        for key, value in pages.items():
            if value == selection:
                st.session_state.page = key
                break

        # System status section
        st.divider()
        st.subheader("💻 System Status")

        # Database status
        engine = get_engine()
        status = get_text('connected') if engine else get_text('not_connected')
        status_color = "green" if engine else "red"
        st.write(f"🔌 {get_text('db_status')}: :{status_color}[{status}]")

        # Note about Streamlit version
        st.info(f"ℹ️ {get_text('note')}")

        # Add a small footer
        st.divider()
        st.caption("© 2025 Chinese Medicine Analysis System")
        st.caption("v1.0.0")


def dashboard_page():
    st.header(get_text('dashboard'))

    st.write(f"### {get_text('welcome')}")
    st.write(get_text('description'))

    # Add a health check indicator
    if is_health_check:
        st.success(get_text('health_check_ok'))

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
        # Update axis labels
        fig.update_layout(
            xaxis_title=get_text('province_origin_description'),
            yaxis_title=get_text('count_column')
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
        # Update axis labels
        fig.update_layout(
            xaxis_title=get_text('material_name'),
            yaxis_title=get_text('usage')
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

        # Create a pie chart for the top 10
        top_10 = df.head(10).copy()
        others_label = '其他' if st.session_state.language == 'zh' else 'Others'
        others = pd.DataFrame([{'name': others_label, 'usage_frequency': df.iloc[10:]['usage_frequency'].sum()}])
        pie_data = pd.concat([top_10, others])

        fig = px.pie(
            pie_data,
            values='usage_frequency',
            names='name',
            title=get_text('usage_distribution')
        )
        # Update labels
        fig.update_traces(textinfo='percent+label')

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
        if st.session_state.language == 'zh':
            tab1, tab2, tab3 = st.tabs(["五性", "五味", "归经"])
        else:
            tab1, tab2, tab3 = st.tabs(["Five Properties", "Five Flavors", "Meridian Tropism"])

        with tab1:
            if properties:
                df = pd.DataFrame(list(properties.items()), columns=['Property', 'Count'])
                fig = px.pie(
                    df,
                    values='Count',
                    names='Property',
                    title="五性分布" if st.session_state.language == 'zh' else "Five Properties Distribution"
                )
                # Update labels
                fig.update_traces(textinfo='percent+label')
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
                    title="五味分布" if st.session_state.language == 'zh' else "Five Flavors Distribution"
                )
                # Update labels
                fig.update_traces(textinfo='percent+label')
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
                    title="归经分布" if st.session_state.language == 'zh' else "Meridian Distribution"
                )
                # Update axis labels
                fig.update_layout(
                    xaxis_title=get_text('meridian_label'),
                    yaxis_title=get_text('count_column')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(get_text('no_data'))
    else:
        st.info(get_text('no_data'))

def top_prescriptions_page():
    st.header(get_text('top_prescriptions'))
    if st.session_state.language == 'zh':
        st.write("⚠️ 此功能在Streamlit版本中受限。请使用Flask应用程序获取完整功能。")
    else:
        st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

def formula_optimization_page():
    st.header(get_text('formula_optimization'))
    if st.session_state.language == 'zh':
        st.write("⚠️ 此功能在Streamlit版本中受限。请使用Flask应用程序获取完整功能。")
    else:
        st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

def knowledge_graph_page():
    st.header(get_text('knowledge_graph'))
    if st.session_state.language == 'zh':
        st.write("⚠️ 此功能在Streamlit版本中受限。请使用Flask应用程序获取完整功能。")
    else:
        st.write("⚠️ This feature is limited in the Streamlit version. Please use the Flask application for full functionality.")

def profile_page():
    st.header(get_text('profile'))

    if not st.session_state.is_authenticated:
        st.warning(get_text('login_failed'))
        return

    # Display basic profile information without database
    st.subheader(get_text('username'))
    st.write(st.session_state.username)

    st.subheader(get_text('user_id'))
    st.write(st.session_state.user_id)

    # Note about dummy authentication
    st.info("This is using dummy authentication for demonstration purposes.")

    # Add language preference option
    st.subheader(get_text('preferences'))
    language_options = {"en": "English", "zh": "中文"}
    selected_language = st.selectbox(
        get_text('language'),
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=0 if st.session_state.get('language', 'en') == "en" else 1
    )

    # Save preferences button
    if st.button(get_text('save_preferences')):
        success, _ = update_user_preferences(
            st.session_state.user_id,
            language=selected_language
        )

        if success:
            st.success(get_text('preferences_saved'))
            # Update session state
            st.session_state.language = selected_language
            st.rerun()

# Main application
def main():
    # Special handling for health checks
    if is_health_check:
        if st.session_state.language == 'zh':
            st.success("健康检查通过")
        else:
            st.success("Health check passed")
        return

    # Display a message for Streamlit Cloud deployment
    is_deployment = os.environ.get("STREAMLIT_DEPLOYMENT", "false").lower() == "true"
    if is_deployment:
        if st.session_state.language == 'zh':
            st.info("⚠️ 此应用程序在Streamlit Cloud上运行。某些功能可能受限。")
        else:
            st.info("⚠️ This application is running on Streamlit Cloud. Some features may be limited.")

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'

    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Handle URL parameters for email verification and password reset
    params = st.query_params

    # Email verification
    if 'verify' in params:
        verification_token = params['verify'][0]
        success, _ = verify_email(verification_token)

        if success:
            st.success(get_text('verification_success'))
        else:
            st.error(get_text('verification_failed'))

        # Remove the parameter from URL
        params.clear()

    # Password reset
    if 'reset' in params:
        reset_token = params['reset'][0]

        # Show password reset form
        st.title(get_text('reset_password'))

        with st.form("reset_password_form"):
            new_password = st.text_input(get_text('new_password'), type="password")
            confirm_password = st.text_input(get_text('confirm_new_password'), type="password")
            submit = st.form_submit_button(get_text('submit'))

            if submit:
                if not new_password or not confirm_password:
                    st.error(get_text('reset_password_failed'))
                elif new_password != confirm_password:
                    st.error(get_text('passwords_not_match'))
                else:
                    success, _ = reset_password(reset_token, new_password)
                    if success:
                        st.success(get_text('reset_password_success'))
                        # Remove the parameter from URL
                        params.clear()
                    else:
                        st.error(get_text('reset_password_failed'))

        # Skip the rest of the UI when showing the reset form
        return

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
    elif st.session_state.page == 'profile':
        profile_page()

if __name__ == "__main__":
    main()