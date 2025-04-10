"""
Translations for Chinese and English languages
"""

translations = {
    'en': {
        # Common elements
        'site_title': 'Chinese Medicine Prescription Analysis',
        'dashboard': 'Dashboard',
        'analytics': 'Analytics',
        'prescriptions': 'Prescriptions',
        'formula_optimization': 'Formula Optimization',
        'knowledge_graph': 'Knowledge Graph',
        'import_data': 'Import Data',
        'welcome': 'Welcome to the Chinese Medicine Prescription Analysis System',
        'welcome_description': 'This platform provides tools for analyzing traditional Chinese medicine prescriptions, visualizing medicinal material usage patterns, and optimizing formulations based on machine learning.',
        
        # Dashboard statistics
        'medicinal_materials': 'Medicinal Materials',
        'prescription_formulas': 'Prescription Formulas',
        'efficacy_categories': 'Efficacy Categories',
        'recent_prescriptions': 'Recent Prescriptions',
        'top_materials': 'Top Used Materials',
        'view_all': 'View All',
        'quick_analysis': 'Quick Analysis',
        'no_prescriptions': 'No prescriptions found. Add a prescription to get started.',
        'no_materials': 'No medicinal materials found. Import data to get started.',
        
        # Province stats page
        'province_stats': 'Province Statistics',
        'materials_by_province': 'Medicinal Materials by Province',
        
        # Material usage page
        'material_usage': 'Material Usage Statistics',
        'usage_frequency': 'Usage Frequency',
        'usage_distribution': 'Usage Distribution',
        
        # Property distribution page
        'property_distribution': 'Distribution of Properties, Flavors, and Meridians',
        
        # Prescription related
        'add_prescription': 'Add New Prescription',
        'search_prescriptions': 'Search Prescriptions',
        'prescription_name': 'Prescription Name',
        'efficacy': 'Efficacy',
        'actions': 'Actions',
        'material_name': 'Material Name',
        'property': 'Property',
        'flavor': 'Flavor',
        'usage': 'Usage Count',
        'top_prescriptions': 'Top Prescriptions by Efficacy'
    },
    'zh': {
        # Common elements
        'site_title': '中药处方分析系统',
        'dashboard': '仪表盘',
        'analytics': '分析',
        'prescriptions': '处方',
        'formula_optimization': '方剂优化',
        'knowledge_graph': '知识图谱',
        'import_data': '数据导入',
        'welcome': '欢迎使用中药处方分析系统',
        'welcome_description': '该平台提供分析传统中药处方、可视化药材使用模式以及基于机器学习优化配方的工具。',
        
        # Dashboard statistics
        'medicinal_materials': '药材',
        'prescription_formulas': '处方方剂',
        'efficacy_categories': '功效分类',
        'recent_prescriptions': '最近处方',
        'top_materials': '常用药材',
        'view_all': '查看全部',
        'quick_analysis': '快速分析',
        'no_prescriptions': '未找到处方。添加处方以开始使用。',
        'no_materials': '未找到药材。导入数据以开始使用。',
        
        # Province stats page
        'province_stats': '各省统计',
        'materials_by_province': '各省药材分布',
        
        # Material usage page
        'material_usage': '药材使用情况',
        'usage_frequency': '使用频率',
        'usage_distribution': '使用分布',
        
        # Property distribution page
        'property_distribution': '性味归经分布',
        
        # Prescription related
        'add_prescription': '添加新处方',
        'search_prescriptions': '搜索处方',
        'prescription_name': '处方名称',
        'efficacy': '功效',
        'actions': '操作',
        'material_name': '药材名称',
        'property': '性质',
        'flavor': '味道',
        'usage': '使用次数',
        'top_prescriptions': '按功效分类的常用处方'
    }
}

def get_text(key, lang='en', *args):
    """
    Get translated text for a given key and language
    
    Args:
        key (str): Translation key
        lang (str): Language code ('en' or 'zh')
        *args: Optional arguments for string formatting
    
    Returns:
        str: Translated text
    """
    if lang not in translations:
        lang = 'en'
    
    text = translations[lang].get(key, translations['en'].get(key, key))
    
    if args:
        try:
            text = text.format(*args)
        except:
            pass
    
    return text