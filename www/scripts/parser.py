#!/usr/bin/env python3
"""
EDRefCard Parser Module

This module contains functions for parsing Elite: Dangerous bindings files
and form data.
"""

import html
from collections import OrderedDict

from lxml import etree

from .utils import logError
from .mapping_runtime import mapping_software_warning

# Import data files
try:
    from .bindingsData import supportedDevices
except ImportError:  # pragma: no cover
    from bindingsData import supportedDevices

try:
    from .controlsData import controls
except ImportError:  # pragma: no cover
    from controlsData import controls


# Display group form field to name mapping
DISPLAY_GROUP_FIELDS = {
    'showgalaxymap': 'Galaxy map',
    'showheadlook': 'Head look',
    'showsrv': 'SRV',
    'showscanners': 'Scanners',
    'showship': 'Ship',
    'showui': 'UI',
    'showfighter': 'Fighter',
    'showonfoot': 'OnFoot',
    'showmulticrew': 'Multicrew',
    'showcamera': 'Camera',
    'showsettlement': 'Settlement',
    'showcommandercreator': 'Holo-Me',
    'showmisc': 'Misc',
}

# Every display group, for callers without a form (API, batch import).
# Single source of truth: hand-written copies drifted ('On Foot' instead of
# 'OnFoot', 'Settlement' forgotten) and silently dropped those bindings.
ALL_DISPLAY_GROUPS = tuple(DISPLAY_GROUP_FIELDS.values())


def parseFormData(form_data):
    """Parse form data from Flask request.form (dict-like object).
    
    This is a Flask-compatible version that works with dict-like objects.
    
    Args:
        form_data: A dict-like object (e.g., Flask's request.form)
    
    Returns:
        List of display groups to show
    """
    displayGroups = []
    for field, group in DISPLAY_GROUP_FIELDS.items():
        if form_data.get(field):
            displayGroups.append(group)
    return displayGroups


def parseBindings(runId, xml, displayGroups, errors):
    """Parse an Elite: Dangerous bindings XML file.
    
    This is the main parsing function that extracts controller bindings
    from the game's .binds XML format.
    
    Args:
        runId: Configuration run identifier
        xml: XML string content of the binds file
        displayGroups: List of groups to include in output
        errors: Errors object to populate with any errors
    
    Returns:
        Tuple of (physicalKeys, modifiers, devices)
    """
    try:
        from .bindingsData import apply_legacy_device_aliases
        from . import database
        apply_legacy_device_aliases(database.list_legacy_device_aliases())
    except Exception:
        # Parsing remains available in standalone tools and unit tests before
        # the application database has been initialized.
        pass

    parser = etree.XMLParser(encoding='utf-8', resolve_entities=False)
    
    try:
        tree = etree.fromstring(bytes(xml, 'utf-8'), parser=parser)
    except SyntaxError as e:
        errors.errors = '''<h3>There was a problem parsing the file you supplied.</h3>
        <p>%s.</p>
        <p>Possibly you submitted the wrong file, or hand-edited it and made a mistake.</p>''' % html.escape(str(e), quote=True)
        xml = '<root></root>'
        tree = etree.fromstring(bytes(xml, 'utf-8'), parser=parser)
    
    physicalKeys = {}
    modifiers = {}
    hotasModifierNum = 1
    keyboardModifierNum = 101
    devices = {}

    # Device detection
    hasT16000MThrottle = len(tree.findall(".//*[@Device='T16000MTHROTTLE']")) > 0
    
    # VPC MongoosT-50CM3 Throttle 32 Button mode detection
    vpcCM3Throttle32buttonmode = False
    if len(tree.findall(".//*[@Device='33448197']")) > 0:
        vpcCM3Throttle32buttonmode = len(tree.findall(".//*[@DeviceIndex='2']")) > 0
    if len(tree.findall(".//*[@Device='33440197']")) > 0:
        vpcCM3Throttle32buttonmode = len(tree.findall(".//*[@DeviceIndex='1']")) > 0
        
    xmlBindings = (tree.findall(".//Binding") + 
                   tree.findall(".//Primary") + 
                   tree.findall(".//Secondary"))
    
    for xmlBinding in xmlBindings:
        controlName = xmlBinding.getparent().tag

        hasHoldModifier = xmlBinding.find("Hold") is not None

        device = xmlBinding.get('Device')
        if not device or device == '{NoDevice}' or not xmlBinding.get('Key'):
            continue

        # Device rewrites for specific hardware configurations
        if device == 'T16000M' and hasT16000MThrottle:
            device = 'T16000MFCS'

        deviceIndex = xmlBinding.get('DeviceIndex', 0)

        # VPC MongoosT-50CM3 Throttle 32 button split mode rewrites
        device, deviceIndex = _rewriteVPCDevice(
            device, deviceIndex, vpcCM3Throttle32buttonmode
        )

        key = xmlBinding.get('Key')
        device = _gamepadDevice(device, deviceIndex, key)

        # Remove Neg_ and Pos_ prefixes for digital buttons on analogue devices
        if key is not None:
            if key.startswith('Neg_'):
                key = key.replace('Neg_', '', 1)
            if key.startswith('Pos_'):
                key = key.replace('Pos_', '', 1)

        def modifierSortKey(modifierInfo):
            modifierDevice = _gamepadDevice(modifierInfo.get('Device'),
                                            modifierInfo.get('DeviceIndex', 0),
                                            modifierInfo.get('Key'))
            if modifierDevice == 'T16000M' and hasT16000MThrottle:
                modifierDevice = 'T16000MFCS'
            return '%s::%s::%s' % (
                modifierDevice, 
                modifierInfo.get('DeviceIndex', 0), 
                modifierInfo.get('Key')
            )

        # Use a fake modifier for hold button actions
        if hasHoldModifier:
            xmlBinding.append(etree.Element(
                'Modifier',
                Device=str(device), DeviceIndex=str(deviceIndex), Key='HOLD'
            ))
            
        modifiersInfo = sorted(xmlBinding.findall('Modifier'), key=modifierSortKey)
        modifiersKey = 'Unmodified'

        if modifiersInfo:
            modifiersKey = '/'.join(modifierSortKey(m) for m in modifiersInfo)
            
            # See if we already have the modifier
            keyModifiers = modifiers.setdefault(modifiersKey, [])
            foundKeyModifier = any(
                km.get('ModifierKey') == modifiersKey for km in keyModifiers
            )
            
            if not foundKeyModifier:
                # Create individual modifiers
                for modifierInfo in modifiersInfo:
                    modifier = {'ModifierKey': modifiersKey}
                    modifierDevice = _gamepadDevice(modifierInfo.get('Device'),
                                                    modifierInfo.get('DeviceIndex', 0),
                                                    modifierInfo.get('Key'))
                    
                    if modifierDevice == 'T16000M' and hasT16000MThrottle:
                        modifierDevice = 'T16000MFCS'
                    
                    modifier['Number'] = (keyboardModifierNum 
                                          if modifierDevice == 'Keyboard' 
                                          else hotasModifierNum)
                    modifier['Device'] = modifierDevice
                    modifier['DeviceIndex'] = modifierInfo.get('DeviceIndex', 0)
                    modifier['Key'] = modifierInfo.get('Key')
                    
                    modifierKey = '%s::%s::%s' % (
                        modifierDevice, 
                        modifierInfo.get('DeviceIndex', 0), 
                        modifierInfo.get('Key')
                    )
                    modifiers.setdefault(modifierKey, []).append(modifier)
                
                # Add composite modifier if multiple modifiers
                if '/' in modifiersKey:
                    modifier = {
                        'ModifierKey': modifiersKey,
                        'Number': (keyboardModifierNum 
                                   if modifierInfo.get('Device') == 'Keyboard' 
                                   else hotasModifierNum)
                    }
                    keyModifiers.append(modifier)
                
                # Increment modifier numbers
                if modifierInfo.get('Device') == 'Keyboard':
                    keyboardModifierNum += 1
                else:
                    hotasModifierNum += 1
        
        # Get control info
        control = controls.get(controlName)
        if control is None:
            logError('%s: No control for %s\n' % (runId, controlName))
            control = {
                'Group': 'General',
                'Name': controlName,
                'Order': 999,
                'HideIfSameAs': [],
                'Type': 'Digital'
            }
        
        if control['Group'] not in displayGroups:
            continue

        itemKey = '%s::%s::%s' % (device, deviceIndex, key)
        deviceKey = '%s::%s' % (device, deviceIndex)
        
        # Find the supported device
        thisDevice = None
        for supportedDevice in supportedDevices.values():
            if deviceKey in supportedDevice['HandledDevices']:
                thisDevice = supportedDevice
                break
            if device in supportedDevice['HandledDevices']:
                thisDevice = supportedDevice
                break
        
        devices[deviceKey] = thisDevice
        
        # Create or update physical key entry
        physicalKey = physicalKeys.get(itemKey)
        if physicalKey is None:
            physicalKey = {
                'Device': device,
                'DeviceIndex': deviceIndex,
                'BaseKey': xmlBinding.get('Key'),
                'Key': key,
                'Binds': {}
            }
            physicalKeys[itemKey] = physicalKey
        
        # Create or update bind entry
        bind = physicalKey['Binds'].setdefault(modifiersKey, {'Controls': OrderedDict()})
        # Legacy cards aggregate half-axis actions. Retain each action's original
        # input so data-driven rows can distinguish opposite directions.
        bind['Controls'][controlName] = {**control, 'InputKey': xmlBinding.get('Key')}

    errors.deviceWarnings = mapping_software_warning(devices)
    return (physicalKeys, modifiers, devices)


def _gamepadDevice(device, deviceIndex, key):
    """Draw an unknown pad in Xbox mode on the generic gamepad card.

    Elite writes XInput pads as GamePad_* keys under the pad's own hardware ID
    (8BitDo, GameSir, newer Microsoft pads...). The layout is the Xbox one
    whatever the ID, so a device no template handles is renamed 'GamePad'.
    Pads that have their own card (Xbox Elite, Steam...) keep it.
    """
    bare = key or ''
    for prefix in ('Neg_', 'Pos_'):
        if bare.startswith(prefix):
            bare = bare[len(prefix):]
    if not bare.startswith('GamePad_') or device == 'GamePad':
        return device
    deviceKey = '%s::%s' % (device, deviceIndex)
    for supportedDevice in supportedDevices.values():
        handled = supportedDevice['HandledDevices']
        if device in handled or deviceKey in handled:
            return device
    return 'GamePad'


def _rewriteVPCDevice(device, deviceIndex, vpcCM3Throttle32buttonmode):
    """Rewrite VPC MongoosT-50CM3 device IDs based on configuration.
    
    Args:
        device: Original device ID
        deviceIndex: Original device index
        vpcCM3Throttle32buttonmode: Whether 32-button mode is detected
    
    Returns:
        Tuple of (device, deviceIndex) with any rewrites applied
    """
    if device == "33448197" and vpcCM3Throttle32buttonmode:
        if deviceIndex == "0":
            device = "VPC-MongoosT-50CM3-Throttle-32B0"
        elif deviceIndex == "1":
            device = "VPC-MongoosT-50CM3-Throttle-32B1"
            deviceIndex = "0"
        elif deviceIndex == "2":
            device = "VPC-MongoosT-50CM3-Throttle-32B2"
            deviceIndex = "0"

    if device == "33448198":
        if deviceIndex == "0":
            device = "VPC-MongoosT-50CM3-Throttle-32B-NS0"
        elif deviceIndex == "1":
            device = "VPC-MongoosT-50CM3-Throttle-32B-NS1"
            deviceIndex = "0"

    if device == "33440197" and vpcCM3Throttle32buttonmode:
        if deviceIndex == "0":
            device = "VPC-MongoosT-50CM3-Throttle-32B1"
        elif deviceIndex == "1":
            device = "VPC-MongoosT-50CM3-Throttle-32B0"
            deviceIndex = "0"
        elif deviceIndex == "2":
            device = "VPC-MongoosT-50CM3-Throttle-32B2"
            deviceIndex = "0"

    return device, deviceIndex


def isRedundantSpecialisation(control, bind):
    """Check if a binding is a redundant specialisation.
    
    Some controls are more specific versions of others (e.g., 
    'GalMap Pitch Up' vs 'Pitch Up'). If both are bound to the 
    same key, we can hide the more specific one.
    
    Args:
        control: Control dictionary with 'HideIfSameAs' list
        bind: Bind dictionary with 'Controls' ordered dict
    
    Returns:
        True if this is a redundant specialisation, False otherwise
    """
    moreGeneralControls = control.get('HideIfSameAs', [])
    if len(moreGeneralControls) == 0:
        return False
    
    for moreGeneralMatch in bind.get('Controls').keys():
        if moreGeneralMatch in moreGeneralControls:
            return True
    
    return False
