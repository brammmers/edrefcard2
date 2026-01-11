#!/usr/bin/env python3
"""
EDRefCard Scripts Package

This package provides the core functionality for generating Elite: Dangerous
reference cards from controller bindings files.

The package is organized into the following modules:
- models: Core data models (Config, Mode, Errors)
- parser: XML parsing and form handling
- renderer: Image generation
- styles: Styling constants
- utils: Utility functions

For backwards compatibility, all public symbols are also available directly
from this package or from the bindings module.
"""

__version__ = '2.1.0'

# Re-export from submodules for backwards compatibility
from .models import Config, Mode, Errors
from .utils import getFontPath, transKey, logError
from .parser import (
    parseBindings, 
    parseForm, 
    parseFormData, 
    determineMode, 
    saveReplayInfo, 
    parseLocalFile,
    isRedundantSpecialisation,
    controllerNames,
)
from .renderer import (
    createKeyboardImage,
    appendKeyboardImage,
    createHOTASImage,
    createBlockImage,
    writeText,
    layoutText,
    calculateBestFitFontSize,
    calculateBestFontSize,
)

# Import data
from .bindingsData import supportedDevices, hotasDetails
from .controlsData import controls

# Import styles (may fail if wand not available)
try:
    from .styles import groupStyles, categoryStyles, ModifierStyles
except ImportError:
    groupStyles = None
    categoryStyles = None
    ModifierStyles = None

__all__ = [
    '__version__',
    # Models
    'Config',
    'Mode', 
    'Errors',
    # Parser
    'parseBindings',
    'parseForm',
    'parseFormData',
    'determineMode',
    'saveReplayInfo',
    'parseLocalFile',
    'isRedundantSpecialisation',
    'controllerNames',
    # Renderer
    'createKeyboardImage',
    'appendKeyboardImage',
    'createHOTASImage',
    'createBlockImage',
    'writeText',
    'layoutText',
    'calculateBestFitFontSize',
    'calculateBestFontSize',
    # Utils
    'getFontPath',
    'transKey',
    'logError',
    # Data
    'supportedDevices',
    'hotasDetails',
    'controls',
    # Styles
    'groupStyles',
    'categoryStyles',
    'ModifierStyles',
]
