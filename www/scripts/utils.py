#!/usr/bin/env python3
"""
EDRefCard Utils Module

This module contains utility functions used across the application.
"""

import os
import sys
import re

def slugify(text):
    """Convert text to a URL-friendly slug.
    
    Args:
        text: Input string
        
    Returns:
        Slugified string (lowercase, alphanumeric and hyphens only)
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Key translation map for displaying keyboard keys.
# Labels must stay plain text: the card font (Exo 2) has no arrow or keycap
# symbols, and a missing glyph is drawn as an empty key (the Shift, Tab,
# Space, arrow... keys were blank from December 2025 to November 2026).
# Left and right modifiers are different keys in Elite: Dangerous, so they
# keep their side, as on the original site.
keymap = {
    'Key_LeftShift': 'Left Shift',
    'Key_RightShift': 'Right Shift',
    'Key_LeftAlt': 'Left Alt',
    'Key_RightAlt': 'Right Alt',
    'Key_LeftControl': 'Left Ctrl',
    'Key_RightControl': 'Right Ctrl',
    'Key_LeftBracket': '[',
    'Key_RightBracket': ']',
    'Key_SemiColon': ';',
    'Key_Apostrophe': "'",
    'Key_BackSlash': '\\',
    'Key_Comma': ',',
    'Key_Period': '.',
    'Key_Slash': '/',
    'Key_Equals': '=',
    'Key_Minus': '-',
    'Key_Grave': '`',
    'Key_Tab': 'Tab',
    'Key_CapsLock': 'Caps Lock',
    'Key_Return': 'Return',
    'Key_Backspace': 'Backspace',
    'Key_Space': 'Space',
    'Key_Escape': 'Esc',
    'Key_Delete': 'Del',
    'Key_Insert': 'Ins',
    'Key_Home': 'Home',
    'Key_End': 'End',
    'Key_PageUp': 'PgUp',
    'Key_PageDown': 'PgDn',
    'Key_UpArrow': 'Up',
    'Key_DownArrow': 'Down',
    'Key_LeftArrow': 'Left',
    'Key_RightArrow': 'Right',
    'Key_LessThan': '<',
    'Key_GreaterThan': '>',
    'Key_LeftParenthesis': '(',
    'Key_RightParenthesis': ')',
    'Key_Plus': '+',
    'Key_Hash': '#',
    'Key_Numpad_0': 'Num0',
    'Key_Numpad_1': 'Num1',
    'Key_Numpad_2': 'Num2',
    'Key_Numpad_3': 'Num3',
    'Key_Numpad_4': 'Num4',
    'Key_Numpad_5': 'Num5',
    'Key_Numpad_6': 'Num6',
    'Key_Numpad_7': 'Num7',
    'Key_Numpad_8': 'Num8',
    'Key_Numpad_9': 'Num9',
    'Key_Numpad_Divide': 'Num/',
    'Key_Numpad_Multiply': 'Num*',
    'Key_Numpad_Subtract': 'Num-',
    'Key_Numpad_Add': 'Num+',
    'Key_Numpad_Enter': 'Num Enter',
    'Key_Numpad_Decimal': 'Num.',
    'Key_Numpad_Period': 'Num.',
    'Key_Numpad_Comma': 'Num,',
    'Key_Numpad_Equals': 'Num=',
    'Key_NumLock': 'NumLk',
    'Key_ScrollLock': 'ScrLk',
    'Key_Pause': 'Pause',
    'Key_PrintScreen': 'PrtSc',
}


def getFontPath(weight, style):
    """Get the path to a font file.
    
    Args:
        weight: Font weight ('Regular', 'Bold', 'SemiBold', etc.)
        style: Font style ('Normal', 'Italic')
        
    Returns:
        Relative path to the font file
    """
    if style == 'Normal':
        style = ''
    if weight == 'Regular' and style != '':
        weight = ''
    return '../fonts/Exo2.0-%s%s.otf' % (weight, style)


def transKey(key):
    """Translate a key code to a displayable string.
    
    Args:
        key: Key code string (e.g., 'Key_A', 'Key_Comma')
        
    Returns:
        Human-readable key name or symbol
    """
    if key is None:
        return None
    trans = keymap.get(key)
    if trans is None:
        trans = key.replace('Key_', '')
    return trans


RECENT_ERRORS: list[str] = []

# error.log lives in the persistent volume and was never trimmed. Past this
# size it is moved to error.log.1 (one generation kept, so at most twice
# this amount on disk).
ERROR_LOG_MAX_BYTES = 5 * 1024 * 1024

def logError(message):
    """Log an error message to stderr and a persistent file.
    
    Args:
        message: The error message to log
    """
    sys.stderr.write("EDRefCard: " + message)
    
    # Keep last 20 errors in memory
    global RECENT_ERRORS
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}\n"
    
    RECENT_ERRORS.append(f"[{timestamp}] {message}")
    if len(RECENT_ERRORS) > 50:
        RECENT_ERRORS.pop(0)

    # Persist to file in configs (which is a volume)
    try:
        from scripts.models import Config
        log_path = Config.configsPath() / 'error.log'
        try:
            if log_path.stat().st_size > ERROR_LOG_MAX_BYTES:
                os.replace(log_path, log_path.with_name('error.log.1'))
        except OSError:
            pass  # no log yet, or another worker rotated it first
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(formatted_msg)
    except Exception as e:
        sys.stderr.write(f"Failed to log to file: {e}\n")
