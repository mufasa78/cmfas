"""
Language utilities for the application
"""
from flask import session
from chinese_converter import to_simplified, to_traditional

def get_language():
    """
    Get the current language from session or default to English
    
    Returns:
        str: Language code ('en' or 'zh')
    """
    return session.get('language', 'en')

def set_language(lang):
    """
    Set the current language in session
    
    Args:
        lang (str): Language code ('en' or 'zh')
    """
    if lang in ['en', 'zh']:
        session['language'] = lang

def convert_chinese(text, to_type='simplified'):
    """
    Convert Chinese text between simplified and traditional
    
    Args:
        text (str): Chinese text to convert
        to_type (str): 'simplified' or 'traditional'
        
    Returns:
        str: Converted text
    """
    if not text:
        return text
    
    try:
        if to_type == 'simplified':
            return to_simplified(text)
        elif to_type == 'traditional':
            return to_traditional(text)
        else:
            return text
    except Exception as e:
        # Log error
        print(f"Error converting text: {e}")
        return text