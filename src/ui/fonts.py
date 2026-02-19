"""
Font Management Module
"""
import tkinter as tk
from tkinter import font

# List of suitable fonts (in priority order)
_FONT_CANDIDATES = [
    'Tahoma',
    'DejaVu Sans',
    'Noto Sans Arabic',
    'Noto Naskh Arabic',
    'Vazir',
    'XB Zar',
    'B Nazanin',
    'Arial Unicode MS',
    'Arial',
    'Sans'
]

# Cache selected font
_selected_font = None


def get_persian_font(size=10, weight='normal'):
    """
    Find and return suitable font
    
    Args:
        size: Font size
        weight: Font weight ('normal' or 'bold')
    
    Returns:
        Font tuple (font name, size, weight)
    """
    global _selected_font
    
    # If font already selected, use it
    if _selected_font:
        return (_selected_font, size, weight)
    
    # Try to find suitable font
    try:
        # Get list of available fonts (requires root window)
        available_fonts = [f.lower() for f in font.families()]
        
        # Find first available font
        for font_name in _FONT_CANDIDATES:
            if font_name.lower() in available_fonts:
                _selected_font = font_name
                return (font_name, size, weight)
    except RuntimeError:
        # If root window doesn't exist, use default font
        pass
    
    # If no font found, use Tahoma (system will substitute if not available)
    _selected_font = 'Tahoma'
    return ('Tahoma', size, weight)


def get_font_config(size=10, weight='normal'):
    """Return font configuration as tuple"""
    return get_persian_font(size, weight)
