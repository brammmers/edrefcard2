#!/usr/bin/env python3
"""
EDRefCard Styles Module

This module contains styling constants for rendering reference cards,
including colors and fonts for different control groups and categories.
"""

from wand.color import Color

from .utils import getFontPath


# Command group styling - used when styling by group type
# Colours are aligned with clockbrain's PR #39 (Material Design palette).
groupStyles = {
    'General':    {'Color': Color('#26A69A'), 'Font': getFontPath('Regular', 'Normal')},  # Teal 400
    'Misc':       {'Color': Color('#FFCA28'), 'Font': getFontPath('Regular', 'Normal')},  # Amber 400
    'Modifier':   {'Color': Color('#78909C'), 'Font': getFontPath('Bold',    'Normal')},  # Blue Grey 400
    'Galaxy map': {'Color': Color('#26C6DA'), 'Font': getFontPath('Regular', 'Normal')},  # Cyan 400
    'Holo-Me':    {'Color': Color('#AB47BC'), 'Font': getFontPath('Regular', 'Normal')},  # Purple 400
    'Multicrew':  {'Color': Color('#EC407A'), 'Font': getFontPath('Bold',    'Normal')},  # Pink 400
    'Fighter':    {'Color': Color('#42A5F5'), 'Font': getFontPath('Regular', 'Normal')},  # Blue 400
    'Camera':     {'Color': Color('#FF7043'), 'Font': getFontPath('Regular', 'Normal')},  # Deep Orange 400
    'Head look':  {'Color': Color('#EF5350'), 'Font': getFontPath('Regular', 'Normal')},  # Red 400
    'Ship':       {'Color': Color('#66BB6A'), 'Font': getFontPath('Regular', 'Normal')},  # Green 400
    'SRV':        {'Color': Color('#29B6F6'), 'Font': getFontPath('Regular', 'Normal')},  # Light Blue 400
    'Scanners':   {'Color': Color('#D4E157'), 'Font': getFontPath('Regular', 'Normal')},  # Lime 400
    'UI':         {'Color': Color('#FFA726'), 'Font': getFontPath('Regular', 'Normal')},  # Orange 400
    'OnFoot':     {'Color': Color('#F48FB1'), 'Font': getFontPath('Regular', 'Normal')},  # Pink 200
    'Settlement': {'Color': Color('#9C27B0'), 'Font': getFontPath('Regular', 'Normal')},  # Purple 500
}

# Command category styling - used when styling by category
categoryStyles = {
    'General':    {'Color': Color('#42A5F5'), 'Font': getFontPath('Regular', 'Normal')},  # Blue 400
    'Combat':     {'Color': Color('#EF5350'), 'Font': getFontPath('Regular', 'Normal')},  # Red 400
    'Social':     {'Color': Color('#66BB6A'), 'Font': getFontPath('Regular', 'Normal')},  # Green 400
    'Navigation': {'Color': Color('#78909C'), 'Font': getFontPath('Regular', 'Normal')},  # Blue Grey 400
    'UI':         {'Color': Color('#FFA726'), 'Font': getFontPath('Regular', 'Normal')},  # Orange 400
}


class ModifierStyles:
    """Styling for modifier keys.
    
    Modifiers are numbered and each gets a distinct color to help
    users quickly identify which modifier is needed for each binding.
    """
    
    styles = [
        {'Color': Color('Black'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('Crimson'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('ForestGreen'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('DarkSlateBlue'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('DarkOrange'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('DarkOrchid'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('SteelBlue'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('Sienna'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('IndianRed'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('CornflowerBlue'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('OliveDrab'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('MediumPurple'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('DarkSalmon'), 'Font': getFontPath('Regular', 'Normal')},
        {'Color': Color('LightSlateGray'), 'Font': getFontPath('Regular', 'Normal')},
    ]

    @staticmethod
    def index(num):
        """Get the style for a modifier number.
        
        Args:
            num: The modifier number (wraps around if > len(styles))
            
        Returns:
            Style dictionary with 'Color' and 'Font' keys
        """
        i = num % len(ModifierStyles.styles)
        return ModifierStyles.styles[i]
