"""
Language utilities for the application
"""
from flask import request, session
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
    if not text or not isinstance(text, str):
        return text
        
    try:
        if to_type == 'simplified':
            return to_simplified(text)
        else:
            return to_traditional(text)
    except Exception as e:
        print(f"Error converting Chinese text: {e}")
        return text