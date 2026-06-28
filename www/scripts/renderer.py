#!/usr/bin/env python3
"""
EDRefCard Renderer Module

This module contains functions for generating reference card images
using the Wand/ImageMagick library.
"""

import math
import re
from collections import OrderedDict

try:
    from wand.drawing import Drawing
    from wand.image import Image
    from wand.font import Font
    from wand.color import Color
except ImportError as e:
    # Log the error but don't fail immediately to allow app to start
    print(f"Warning: Failed to import wand (ImageMagick): {e}")
    Drawing = None
    Image = None
    Font = None
    Color = None

from .models import Config
from .utils import getFontPath, transKey, logError

# Import data files
try:
    from .bindingsData import supportedDevices, hotasDetails
except ImportError:  # pragma: no cover
    from bindingsData import supportedDevices, hotasDetails

# Import styles (lazy to avoid circular imports)
_styles_initialized = False
groupStyles = None
categoryStyles = None
ModifierStyles = None


def _init_styles():
    """Lazily initialize styles to avoid circular imports."""
    global _styles_initialized, groupStyles, categoryStyles, ModifierStyles
    if not _styles_initialized:
        try:
            from .styles import groupStyles as gs, categoryStyles as cs, ModifierStyles as ms
        except ImportError:
            from styles import groupStyles as gs, categoryStyles as cs, ModifierStyles as ms
        groupStyles = gs
        categoryStyles = cs
        ModifierStyles = ms
        _styles_initialized = True


def writeUrlToDrawing(config, drawing, public):
    """Write the reference card URL to the image.
    
    Args:
        config: Config object
        drawing: Wand Drawing context
        public: Whether this is a public reference card
    """
    url = config.refcardURL() if public else Config.webRoot()
    drawing.push()
    drawing.font = getFontPath('SemiBold', 'Normal')
    drawing.font_size = 36
    drawing.text(x=23, y=252, body=url)
    drawing.pop()


def createKeyboardImage(physicalKeys, modifiers, source, imageDevices, 
                        biggestFontSize, displayGroups, runId, public):
    """Create a keyboard reference card image.
    
    Args:
        physicalKeys: Dictionary of physical key bindings
        modifiers: Dictionary of modifier key bindings
        source: Template image name
        imageDevices: List of device names to include
        biggestFontSize: Maximum font size to use
        displayGroups: List of control groups to display
        runId: Configuration run identifier
        public: Whether this is a public configuration
    
    Returns:
        True if image was created successfully
    """
    if Drawing is None:
        raise RuntimeError("Image generation library (ImageMagick/Wand) is not installed or failed to load.")
        
    _init_styles()
    config = Config(runId)
    filePath = config.pathWithNameAndSuffix(source, '.jpg')

    # Check if already exists
    if filePath.exists():
        return True
    
    with Image(filename='../res/' + source + '.jpg') as sourceImg:
        with Drawing() as context:
            # Font defaults
            context.font = getFontPath('Regular', 'Normal')
            context.text_antialias = True
            context.font_style = 'normal'
            context.stroke_width = 1
            context.fill_opacity = 1
            context.fill_color = Color('Black')

            # Add URL to title
            writeUrlToDrawing(config, context, public)

            # Organize outputs by group
            outputs = {group: {} for group in displayGroups}

            # Find bindings and order them
            for _physicalKeySpec, physicalKey in physicalKeys.items():
                itemDevice = physicalKey.get('Device')
                itemKey = physicalKey.get('Key')

                if itemDevice not in imageDevices:
                    continue

                for modifier, bind in physicalKey.get('Binds').items():
                    for _controlKey, control in bind.get('Controls').items():
                        bindInfo = {
                            'Control': control,
                            'Key': itemKey,
                            'Modifiers': []
                        }

                        if modifier != 'Unmodified':
                            for _modifierKey, modifierControls in modifiers.items():
                                for modifierControl in modifierControls:
                                    if (modifierControl.get('ModifierKey') == modifier 
                                            and modifierControl.get('Key') is not None):
                                        bindInfo['Modifiers'].append(modifierControl.get('Key'))

                        outputs[control['Group']][control['Name']] = bindInfo

            # Set up screen state for layout
            screenState = {
                'baseX': 60,
                'baseY': 320,
                'maxWidth': 0,
                'thisWidth': 0,
                'currentX': 60,
                'currentY': 320,
            }

            font = Font(getFontPath('Regular', 'Normal'), antialias=True, size=biggestFontSize)
            groupTitleFont = Font(getFontPath('Regular', 'Normal'), antialias=True, size=biggestFontSize * 2)
            context.stroke_width = 1
            context.stroke_color = Color('Black')
            context.fill_opacity = 0

            # Render each display group
            for displayGroup in displayGroups:
                if not outputs[displayGroup]:
                    continue

                writeText(context, sourceImg, displayGroup, screenState, groupTitleFont, False, True)

                orderedOutputs = OrderedDict(
                    sorted(outputs[displayGroup].items(), 
                           key=lambda x: x[1].get('Control').get('Order'))
                )
                for _bindKey, bind in orderedOutputs.items():
                    for modifier in bind.get('Modifiers', []):
                        writeText(context, sourceImg, transKey(modifier), screenState, font, True, False)
                    writeText(context, sourceImg, transKey(bind.get('Key')), screenState, font, True, False)
                    writeText(context, sourceImg, bind.get('Control').get('Name'), screenState, font, False, True)

            context.draw(sourceImg)
            sourceImg.save(filename=str(filePath))
    
    return True


def appendKeyboardImage(createdImages, physicalKeys, modifiers, displayGroups, runId, public):
    """Create and append a keyboard image to the list of created images.
    
    Args:
        createdImages: List to append created image name to
        physicalKeys: Dictionary of physical key bindings
        modifiers: Dictionary of modifier bindings
        displayGroups: List of control groups to display
        runId: Configuration run identifier
        public: Whether this is a public configuration
    """
    def countKeyboardItems(physicalKeys):
        keyboardItems = 0
        for physicalKey in physicalKeys.values():
            if physicalKey.get('Device') == 'Keyboard':
                for bind in physicalKey.get('Binds').values():
                    keyboardItems += len(bind.get('Controls'))
        return keyboardItems
    
    def fontSizeForKeyBoardItems(physicalKeys):
        keyboardItems = countKeyboardItems(physicalKeys)
        if keyboardItems > 48:
            fontSize = 40 - int(((keyboardItems - 48) / 20) * 4)
            if fontSize < 24:
                fontSize = 24
        else:
            fontSize = 40
        return fontSize
    
    fontSize = fontSizeForKeyBoardItems(physicalKeys)
    createKeyboardImage(physicalKeys, modifiers, 'keyboard', ['Keyboard'], 
                        fontSize, displayGroups, runId, public)
    createdImages.append('Keyboard')


# ---------------------------------------------------------------------------
# Keyboard layout image – ported from clockbrain/edrefcard2 PR #39
# ---------------------------------------------------------------------------

def _prepareCapList(physicalKeys, modifiers, styling, keyboardLayout):
    """Build a faceBandset mapping cap labels to their binding bands."""
    unmapped = []
    capReverseMap = {}
    for keyboardRow in keyboardLayout:
        for keyboardItem in keyboardRow:
            if isinstance(keyboardItem, dict):
                continue
            if isinstance(keyboardItem, list):
                lcaseKey = keyboardItem[1].casefold()
                capReverseMap[lcaseKey] = keyboardItem[0]
            else:
                lcaseKey = f'Key_{keyboardItem}'.casefold()
                capReverseMap[lcaseKey] = keyboardItem

    faceBandset = {}
    for _physicalKeySpec, physicalKey in physicalKeys.items():
        if physicalKey.get('Device') != 'Keyboard':
            continue
        itemKey = physicalKey.get('Key')
        if itemKey is None:
            continue
        cap = capReverseMap.get(itemKey.casefold())
        if cap is None and itemKey not in unmapped:
            unmapped.append(itemKey)
        binds = physicalKey.get('Binds', {}).items()
        if binds:
            faceBandset[cap] = {}
        for bindKey, controlList in binds:
            for controlTag, control in controlList.get('Controls', {}).items():
                entry = None
                if styling == 'Group':
                    entry = control.get('Group')
                elif styling == 'Category':
                    entry = control.get('Category')
                else:
                    # For 'None' and 'Modifier' modes, fall back to group colours
                    # so the visual keyboard always shows meaningful colours.
                    # Modifier strip colours still indicate which modifier is used.
                    entry = control.get('Group')
                bandIndex = f'{entry}::{controlTag}::{bindKey}'
                skip = False
                for sameAs in control.get('HideIfSameAs', []):
                    if f'{entry}::{sameAs}::{bindKey}' in faceBandset.get(cap, {}):
                        skip = True
                        break
                if not skip and bandIndex not in faceBandset.get(cap, {}):
                    color = 'White'
                    if styling == 'Category':
                        color = categoryStyles.get(entry, categoryStyles.get('General')).get('Color')
                    else:
                        # 'Group', 'Modifier', and 'None' all use group colours
                        color = groupStyles.get(entry, groupStyles.get('General')).get('Color')
                    stripColors = []
                    hold = False
                    if bindKey == 'Keyboard::0::HOLD':
                        hold = True
                    elif bindKey != 'Unmodified':
                        for modifier in modifiers.get(bindKey, []):
                            modColor = ModifierStyles.index(modifier.get('Number') - 101).get('Color')
                            stripColors.append(modColor)
                    faceBandset[cap][bandIndex] = {
                        'Label': control.get('Name', ''),
                        'Color': color,
                        'StripColors': stripColors,
                        'Hold': hold,
                    }

    for _modifierKey, modifierControls in modifiers.items():
        for modifier in modifierControls:
            if modifier.get('Device') != 'Keyboard':
                continue
            itemKey = modifier.get('Key')
            if itemKey is None:
                continue
            cap = capReverseMap.get(itemKey.casefold())
            if cap is None and itemKey != 'HOLD' and itemKey not in unmapped:
                unmapped.append(itemKey)
            if faceBandset.get(cap) is None:
                faceBandset[cap] = {}
            bandIndex = f"Modifier::{modifier.get('Number')}::Modifier"
            color = ModifierStyles.index(modifier.get('Number') - 101).get('Color')
            faceBandset[cap][bandIndex] = {
                'Label': f"Modifier-{str(modifier.get('Number') - 100)}",
                'Color': color, 'StripColors': [], 'Hold': False,
            }

    return faceBandset, unmapped


def _balance_wrap(text, num_lines):
    """Wrap text across num_lines with balanced line lengths."""
    from itertools import combinations as _comb
    words = text.split()
    if num_lines <= 1 or len(words) <= 1:
        return text
    word_lengths = [len(w) for w in words]
    total_chars = sum(word_lengths)
    ideal_length = total_chars / num_lines
    best_score = float('inf')
    best_breaks = None
    for breaks in _comb(range(1, len(words)), num_lines - 1):
        segments = []
        start = 0
        for b in breaks:
            segments.append(word_lengths[start:b])
            start = b
        segments.append(word_lengths[start:])
        line_lengths = [sum(seg) + len(seg) - 1 for seg in segments]
        score = max(abs(line_len - ideal_length) for line_len in line_lengths)
        if score < best_score:
            best_score = score
            best_breaks = breaks
    result = []
    start = 0
    for b in best_breaks:
        result.append(' '.join(words[start:b]))
        start = b
    result.append(' '.join(words[start:]))
    return '\n'.join(result)


def _contrastColor(bg_color):
    """Return black or white depending on background luminance (WCAG formula).

    Args:
        bg_color: A Wand Color object

    Returns:
        A Wand Color object ('Black' or 'White')
    """
    try:
        r = bg_color.red
        g = bg_color.green
        b = bg_color.blue
        # Relative luminance (linearised sRGB)
        def _lin(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        lum = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
        return Color('White') if lum < 0.35 else Color('Black')
    except Exception:
        return Color('Black')

def _writeCenteredWrapableText(context, sourceImg, x, y, w, h, text):
    """Draw text centered and word-wrapped within a rectangle."""
    def _writeCentered(ctx, img, x, y, w, h, t):
        m = ctx.get_font_metrics(img, t, multiline=True)
        x2 = int(round(x + (w - m.text_width) / 2))
        y2 = int(round(y + (h - stdH) / 2 + m.ascender))
        ctx.text(x=x2, y=y2, body=t)

    metrics = context.get_font_metrics(sourceImg, 'A', multiline=False)
    stdH = metrics.text_height
    maxLines = max(int(h / stdH), 1)
    spaces = text.count(' ')
    if spaces < maxLines:
        text = text.replace(' ', '\n', maxLines - 1)
    else:
        text = _balance_wrap(text, maxLines)
    lines = text.split('\n')
    y2 = y - stdH * (len(lines) - 1) / 2
    for line in lines:
        _writeCentered(context, sourceImg, x, y2, w, h, line)
        y2 += stdH


def _drawFaceBands(context, sourceImg, faceBands, faceX, faceWidth, faceTop, faceBottom):
    """Draw one horizontal colored band per binding on the key face."""
    bandTop = faceTop
    bandHeight = int((faceBottom - faceTop) / len(faceBands))
    bandWidth = 30
    for bandIndex, controlSet in faceBands.items():
        context.stroke_color = Color('DarkGrey')
        context.stroke_width = 1
        bandInset = 0
        bindKey = '::'.join(bandIndex.split('::')[2:])
        if bindKey == 'Keyboard::0::HOLD':
            context.stroke_color = Color('Black')
            context.stroke_width = 6
        elif bindKey not in ('Unmodified', 'Modifier'):
            for bandColor in controlSet['StripColors']:
                context.fill_color = bandColor
                context.rectangle(int(faceX + bandInset), top=bandTop,
                                  width=bandWidth, height=bandHeight - 2, radius=5)
                bandInset += bandWidth

        context.fill_color = controlSet['Color']
        context.rectangle(int(faceX + bandInset), top=bandTop,
                          width=faceWidth - bandInset, height=bandHeight - 2, radius=5)
        # Text should be drawn solid, without the border stroke from the rectangle
        context.stroke_color = Color('transparent')
        context.fill_color = _contrastColor(controlSet['Color'])
        _writeCenteredWrapableText(context, sourceImg, faceX, bandTop,
                                   faceWidth, bandHeight, controlSet['Label'])
        bandTop += bandHeight


def _drawKeyLabel(context, sourceImg, x, y, width, height, bottom, label):
    """Draw the physical key label (e.g. 'A', 'Tab') at the bottom of the key."""
    if label != '':
        context.push()
        context.stroke_color = Color('Black')
        context.stroke_width = 1
        context.fill_color = Color('Black')
        label = label.replace('\n', ' .. ')
        metrics = context.get_font_metrics(sourceImg, label, multiline=False)
        context.text(x=int(x + (width - metrics.text_width) / 2),
                     y=int(y + height - bottom) + 24, body=label)
        context.pop()


def _roundCorners(points, radius):
    """Round the corners of a 5-right-angle notched polygon (for ISO Enter)."""
    steps = 3
    step_rad = (math.pi / 2) / steps
    rounded = [points[0]]
    for i in range(1, 6):
        prev = points[i - 1]
        curr = points[i]
        if curr[0] > prev[0] and curr[1] == prev[1]:
            direction = math.pi / 2
            dx, dy = -1, 1
        elif curr[0] == prev[0] and curr[1] > prev[1]:
            direction = math.pi * 2
            dx, dy = -1, -1
        elif curr[0] < prev[0] and curr[1] == prev[1]:
            direction = math.pi * 1.5
            dx, dy = 1, -1
        else:
            direction = math.pi
            dx, dy = 1, 1
        cx = curr[0] + radius * dx
        cy = curr[1] + radius * dy
        for j in range(steps + 1):
            angle = direction - j * step_rad
            rounded.append((cx + radius * math.cos(angle),
                             cy - radius * math.sin(angle)))
    return rounded


def _drawKey(context, sourceImg, capConfig, capSpecial, cap, faceBands):
    """Draw a single keycap (rectangle or ISO polygon) with bands and label."""
    offsetX = int(capConfig['capWidth'] * capSpecial.get('x', 0))
    offsetY = int(capConfig['capHeight'] * capSpecial.get('y', 0))
    capConfig['x'] += offsetX
    capConfig['y'] += offsetY
    capWidth = int(capConfig['capWidth'] * capSpecial.get('w', 1))
    capHeight = int(capConfig['capHeight'] * capSpecial.get('h', 1))
    capRadius = capConfig['capRadius']
    capAdjustX = 0

    faceX = capConfig['x'] + capConfig['capSideInset']
    faceWidth = capWidth - (capConfig['capSideInset'] * 2)
    faceTop = int(capConfig['y'] + capConfig['capTopInset'])
    faceBottom = int(capConfig['y'] + capHeight - capConfig['capBottomInset'])

    context.stroke_color = Color('Black')
    context.stroke_width = 3
    context.fill_color = Color('Silver')
    context.fill_opacity = 1

    if any(k in capSpecial for k in ('x2', 'y2', 'w2', 'h2')):
        # ISO Enter — draw as a notched polygon
        ox2 = int(capConfig['capWidth'] * capSpecial.get('x2', 0))
        oy2 = int(capConfig['capHeight'] * capSpecial.get('y2', 0))
        cw2 = int(capConfig['capWidth'] * capSpecial.get('w2', 1))
        ch2 = int(capConfig['capHeight'] * capSpecial.get('h2', 1))
        points = []
        if capSpecial.get('y2', 0) == 0:
            if capSpecial.get('x2', 0) < 0:
                points = [
                    (capConfig['x'], capConfig['y'] + ch2),
                    (capConfig['x'] + ox2, capConfig['y'] + ch2),
                    (capConfig['x'] + ox2, capConfig['y']),
                    (capConfig['x'] + capWidth, capConfig['y']),
                    (capConfig['x'] + capWidth, capConfig['y'] + capHeight),
                    (capConfig['x'], capConfig['y'] + capHeight),
                ]
                capAdjustX = -int(capConfig['capWidth'] * capSpecial.get('x', 0))
            else:
                points = [
                    (capConfig['x'] + capWidth, capConfig['y'] + ch2),
                    (capConfig['x'] + capWidth, capConfig['y'] + capHeight),
                    (capConfig['x'], capConfig['y'] + capHeight),
                    (capConfig['x'], capConfig['y']),
                    (capConfig['x'] + cw2, capConfig['y']),
                    (capConfig['x'] + cw2, capConfig['y'] + ch2),
                ]
            capWidth = cw2
        elif capSpecial.get('y2', 0) > 0:
            if capSpecial.get('x2', 0) < 0:
                points = [
                    (capConfig['x'], capConfig['y'] + oy2),
                    (capConfig['x'], capConfig['y']),
                    (capConfig['x'] + capWidth, capConfig['y']),
                    (capConfig['x'] + capWidth, capConfig['y'] + capHeight),
                    (capConfig['x'] + ox2, capConfig['y'] + capHeight),
                    (capConfig['x'] + ox2, capConfig['y'] + oy2),
                ]
            else:
                points = [
                    (capConfig['x'] + capWidth, capConfig['y'] + oy2),
                    (capConfig['x'] + cw2, capConfig['y'] + oy2),
                    (capConfig['x'] + cw2, capConfig['y'] + capHeight),
                    (capConfig['x'], capConfig['y'] + capHeight),
                    (capConfig['x'], capConfig['y']),
                    (capConfig['x'] + capWidth, capConfig['y']),
                ]
        context.polygon(_roundCorners(points, capRadius))
    else:
        context.rectangle(capConfig['x'], top=capConfig['y'],
                          width=capWidth, height=capHeight, radius=capRadius)

    label = cap.split('__')[0]
    context.font_size = capConfig['capFontSize']
    _drawKeyLabel(context, sourceImg, faceX, capConfig['y'],
                  width=faceWidth, height=capHeight,
                  bottom=capConfig['capBottomInset'], label=label)

    context.stroke_color = Color('Silver')
    context.stroke_width = 1
    context.fill_color = Color('White')
    if faceBands is None:
        context.rectangle(faceX, top=faceTop, width=faceWidth,
                          height=capHeight - (capConfig['capTopInset'] + capConfig['capBottomInset']),
                          radius=5)
    else:
        _drawFaceBands(context, sourceImg, faceBands, faceX, faceWidth, faceTop, faceBottom)

    capConfig['x'] += capAdjustX + capWidth


def _drawLegendEntry(context, sourceImg, label, color, strip_colors, hold, capConfig):
    """Draw a single legend entry using a fake face band."""
    bindKey = 'Keyboard::0::HOLD' if hold else ('Modified' if strip_colors else 'Unmodified')
    fakeBands = {
        f'Legend::Legend::{bindKey}': {
            'Label': label, 'Color': color,
            'StripColors': strip_colors, 'Hold': hold,
        }
    }
    _drawKey(context, sourceImg, capConfig, {}, '', fakeBands)


def _writeKeyboardLayout(context, sourceImg, physicalKeys, modifiers, styling, layout):
    """Iterate through the keyboard layout rows and draw each key."""
    try:
        from .keyboardLayouts import keyboardLayouts
    except ImportError:
        from keyboardLayouts import keyboardLayouts

    keyboardLayout = keyboardLayouts.get(layout)

    faceBandset, unmapped = _prepareCapList(physicalKeys, modifiers, styling, keyboardLayout)

    stdcapWidth = 165
    stdcapHeight = 220
    capConfig = {
        'x': 0, 'y': 0,
        'capWidth': stdcapWidth, 'capHeight': stdcapHeight,
        'capTopInset': 10, 'capBottomInset': 35,
        'capSideInset': 15, 'capRadius': 25,
        'capFontSize': 18,
    }
    keyboardX = 60
    keyboardY = 320

    context.font = getFontPath('Regular', 'Normal')
    context.text_antialias = True
    context.stroke_color = Color('Black')
    context.fill_color = Color('Black')
    context.fill_opacity = 1

    # Legend
    legendX = 60
    legendXStep = stdcapWidth * 1.5
    legendY = 1850
    legendYStep = 150
    context.font_size = 32
    context.text(x=legendX, y=legendY + 60, body='Legend')
    legendX += legendXStep

    capConfig['capFontSize'] = 24
    if styling == 'Category':
        legendEntries = categoryStyles.items()
    else:
        # 'Group', 'Modifier', 'None' all use group colours in the visual keyboard
        legendEntries = groupStyles.items()

    capConfig['x'] = legendX
    capConfig['y'] = legendY
    capConfig['capWidth'] = int(stdcapWidth * 1.2)
    capConfig['capHeight'] = stdcapHeight // 2
    for label, style in legendEntries:
        _drawLegendEntry(context, sourceImg, label, style['Color'], [], False, capConfig)
        if (capConfig['x'] + capConfig['capWidth']) > 3800:
            capConfig['x'] = 60 + legendXStep
            capConfig['y'] += legendYStep

    modColor = ModifierStyles.index(0).get('Color')
    _drawLegendEntry(context, sourceImg, 'Modified', 'White', [f'{modColor}'], False, capConfig)
    if (capConfig['x'] + capConfig['capWidth']) > 3800:
        capConfig['x'] = 60 + legendXStep
        capConfig['y'] += legendYStep
    _drawLegendEntry(context, sourceImg, 'Hold', 'White', [], True, capConfig)

    # Draw keyboard rows
    capConfig['capWidth'] = stdcapWidth
    capConfig['capHeight'] = stdcapHeight
    capConfig['y'] = keyboardY
    capConfig['capFontSize'] = 18

    for keyboardRow in keyboardLayout:
        capConfig['x'] = keyboardX
        capSpecial = {}
        for keyboardItem in keyboardRow:
            if isinstance(keyboardItem, dict):
                capSpecial = keyboardItem
                continue
            cap = keyboardItem[0] if isinstance(keyboardItem, list) else keyboardItem
            faceBands = faceBandset.get(cap)
            _drawKey(context, sourceImg, capConfig, capSpecial, cap, faceBands)
            capSpecial = {}
        capConfig['y'] += stdcapHeight

    if unmapped:
        context.stroke_color = Color('Black')
        context.fill_color = Color('Black')
        context.font_size = 24
        context.text(x=50, y=2050, body='No keycaps for: ' + str(unmapped).replace('Key_', '')[1:-1])


def createKeyboardLayoutImage(physicalKeys, modifiers, layout, config, styling):
    """Create a visual keyboard layout image by drawing ANSI/ISO keys as keycaps.

    Ported from clockbrain/edrefcard2 PR #39.  Draws each key as a silver
    rounded rectangle with a coloured inset band for each binding.
    A legend is drawn at the bottom of the image.

    Args:
        physicalKeys: dict of physical key bindings from parseBindings
        modifiers: dict of modifier bindings from parseBindings
        layout: 'ANSI 104', 'ISO 105', or 'ЙЦУКЕН'
        config: Config object (for output path and URL)
        styling: 'None', 'Group', 'Category', or 'Modifier'

    Returns:
        True on success, None if layout not supported
    """
    if Drawing is None:
        raise RuntimeError("Image generation library (ImageMagick/Wand) is not installed.")

    try:
        from .keyboardLayouts import keyboardLayouts
    except ImportError:
        from keyboardLayouts import keyboardLayouts

    if layout not in keyboardLayouts:
        return None

    _init_styles()

    filePath = config.pathWithNameAndSuffix('keyboard-layout', '.jpg')
    if filePath.exists():
        return True

    # Find the template image (white background with title)
    from pathlib import Path as _Path
    for candidate in [
        _Path('../res/keyboard-layout.jpg'),
        _Path('res/keyboard-layout.jpg'),
        _Path('static/images/keyboard-layout.jpg'),
        _Path('/app/www/res/keyboard-layout.jpg'),
        _Path('/app/www/static/images/keyboard-layout.jpg'),
    ]:
        if candidate.exists():
            sourceImagePath = candidate
            break
    else:
        return None  # No template found

    with Image(filename=str(sourceImagePath)) as sourceImg:
        with Drawing() as context:
            context.font = getFontPath('Regular', 'Normal')
            context.text_antialias = True
            context.font_style = 'normal'
            context.stroke_width = 1
            context.fill_opacity = 1
            context.fill_color = Color('Black')

            # Write URL at top
            context.font_size = 36
            context.text(x=60, y=280, body=config.refcardURL())

            _writeKeyboardLayout(context, sourceImg, physicalKeys, modifiers, styling, layout)

            context.draw(sourceImg)
            sourceImg.save(filename=str(filePath))

    return True


def writeText(context, img, text, screenState, font, surround, newLine):
    """Write text to an image with wrapping support.
    
    Args:
        context: Wand Drawing context
        img: Wand Image
        text: Text to write
        screenState: Dictionary tracking current position
        font: Font to use
        surround: Whether to draw a box around the text
        newLine: Whether to move to next line after writing
    """
    border = 4

    context.font = font.path
    context.font_style = 'normal'
    context.font_size = font.size
    
    context.push()
    
    context.stroke_width = 0
    context.fill_opacity = 1 
    context.fill_color = Color('Black')

    if text is None or text == '':
        context.fill_color = Color('Red')
        text = 'invalid'

    metrics = context.get_font_metrics(img, text, multiline=False)
    
    # Check if we need to wrap to next column
    if screenState['currentY'] + int(metrics.text_height + 32) > 2160:
        screenState['currentY'] = screenState['baseY']
        screenState['baseX'] = screenState['baseX'] + screenState['maxWidth'] + 49
        screenState['currentX'] = screenState['baseX']
        screenState['maxWidth'] = 0
        screenState['thisWidth'] = 0
    
    x = screenState['currentX']
    y = screenState['currentY'] + int(metrics.ascender)
    context.text(x=x, y=y, body=text)
    context.pop()

    if surround:
        y = screenState['currentY'] - border
        context.rectangle(
            left=x - (border * 4), 
            top=y - (border * 2), 
            width=int(metrics.text_width) + (border * 8), 
            height=int(metrics.text_height) + (border * 4), 
            radius=30
        )
        width = int(metrics.text_width + 48)
    else:
        width = int((metrics.text_width + 72) / 48) * 48
    
    screenState['thisWidth'] += width

    if newLine:
        if screenState['thisWidth'] > screenState['maxWidth']:
            screenState['maxWidth'] = screenState['thisWidth']
        screenState['currentY'] += int(metrics.text_height + 32)
        screenState['currentX'] = screenState['baseX']
        screenState['thisWidth'] = 0
    else:
        screenState['currentX'] += width


def createBlockImage(supportedDeviceKey, strokeColor='Red', fillColor='LightGreen', dryRun=False):
    """Create a block diagram image showing all controls on a device.
    
    Args:
        supportedDeviceKey: Name of the supported device
        strokeColor: Color for control box borders
        fillColor: Color for control box fills
        dryRun: If True, don't actually save the image
    
    Raises:
        KeyError: If device is not supported
    """
    if Drawing is None and not dryRun:
        raise RuntimeError("Image generation library (ImageMagick/Wand) is not installed or failed to load.")
        
    _init_styles()
    supportedDevice = supportedDevices[supportedDeviceKey]
    templateName = supportedDevice['Template']
    config = Config(templateName)
    config.makeDir()
    filePath = config.pathWithSuffix('.jpg')
    
    with Image(filename='../res/' + supportedDevice['Template'] + '.jpg') as sourceImg:
        with Drawing() as context:
            if not dryRun:        
                context.font = getFontPath('Regular', 'Normal')
                context.text_antialias = True
                context.font_style = 'normal'
            maxFontSize = 40

            for keyDevice in supportedDevice.get('KeyDevices', supportedDevice.get('HandledDevices')):
                for (keycode, box) in hotasDetails[keyDevice].items():
                    if keycode == 'displayName':
                        continue
                    if not dryRun:        
                        context.stroke_width = 1
                        context.stroke_color = Color(strokeColor)
                        context.fill_color = Color(fillColor)
                        context.rectangle(
                            top=box['y'], 
                            left=box['x'], 
                            width=box['width'], 
                            height=box.get('height', 54)
                        )
                        context.stroke_width = 0
                        context.fill_color = Color('Black')
                        sourceTexts = [{
                            'Text': keycode, 
                            'Group': 'General', 
                            'Style': groupStyles['General']
                        }]
                        texts = layoutText(sourceImg, context, sourceTexts, box, maxFontSize)
                        for text in texts:
                            context.font_size = text['Size']
                            context.font = text['Style']['Font']
                            context.text(x=text['X'], y=text['Y'], body=text['Text'])
            
            if not dryRun:        
                context.draw(sourceImg)
                sourceImg.save(filename=str(filePath))


def isRedundantSpecialisation(control, bind):
    """Check if a binding is a redundant specialisation.
    
    Args:
        control: Control dictionary with 'HideIfSameAs' list
        bind: Bind dictionary with 'Controls' ordered dict
    
    Returns:
        True if this is a redundant specialisation
    """
    moreGeneralControls = control.get('HideIfSameAs', [])
    if len(moreGeneralControls) == 0:
        return False
    
    for moreGeneralMatch in bind.get('Controls').keys():
        if moreGeneralMatch in moreGeneralControls:
            return True
    
    return False


def createHOTASImage(physicalKeys, modifiers, source, imageDevices, biggestFontSize, 
                     config, public, styling, deviceIndex, misconfigurationWarnings):
    """Create a HOTAS reference card image.
    
    Args:
        physicalKeys: Dictionary of physical key bindings
        modifiers: Dictionary of modifier bindings
        source: Template image name
        imageDevices: List of device names to include
        biggestFontSize: Maximum font size
        config: Config object
        public: Whether this is public
        styling: Styling mode ('None', 'Group', 'Category', 'Modifier')
        deviceIndex: Device index (0 or 1)
```
        misconfigurationWarnings: Current misconfiguration warnings string
    
    Returns:
        True if image was created successfully
    """
    if Drawing is None:
        raise RuntimeError("Image generation library (ImageMagick/Wand) is not installed or failed to load.")

    _init_styles()

    runId = config.name
    
    if deviceIndex == 0:
        name = source
    else:
        name = '%s-%s' % (source, deviceIndex)
    filePath = config.pathWithNameAndSuffix(name, '.jpg')
    
    # Check if already exists
    if filePath.exists():
        return True
    
    # Ensure template exists
    from pathlib import Path
    template_path = Path('../res') / (source + '.jpg')
    if not template_path.exists():
        raise FileNotFoundError(f"Template image '../res/{source}.jpg' not found")

    with Image(filename=str(template_path)) as sourceImg:

        with Drawing() as context:
            # Font defaults
            context.font = getFontPath('Regular', 'Normal')
            context.text_antialias = True
            context.font_style = 'normal'
            context.stroke_width = 0
            context.fill_color = Color('Black')
            context.fill_opacity = 1

            # Add URL to title
            writeUrlToDrawing(config, context, public)

            for physicalKeySpec, physicalKey in physicalKeys.items():
                itemDevice = physicalKey.get('Device')
                itemDeviceIndex = int(physicalKey.get('DeviceIndex'))
                itemDeviceKey = f'{itemDevice}::{itemDeviceIndex}'
                itemKey = physicalKey.get('Key')

                # Only show for appropriate device
                if itemDevice not in imageDevices and itemDeviceKey not in imageDevices:
                    continue

                # Only show for appropriate index
                if itemDeviceIndex != deviceIndex: 
                    continue

                # Find control details
                texts = []
                hotasDetail = None
                try:
                    if itemDeviceKey in hotasDetails:
                        hotasDetail = hotasDetails.get(itemDeviceKey).get(itemKey)
                    else:
                        hotasDetail = hotasDetails.get(itemDevice).get(itemKey)
                except AttributeError:
                    hotasDetail = None
                
                if hotasDetail is None:
                    logError('%s: No drawing box found for %s\n' % (runId, physicalKeySpec))
                    continue

                # Get modifiers
                for keyModifier in modifiers.get(physicalKeySpec, []):
                    if styling == 'Modifier':
                        style = ModifierStyles.index(keyModifier.get('Number'))
                    else:
                        style = groupStyles.get('Modifier')
                    texts.append({
                        'Text': 'Modifier %s' % keyModifier.get('Number'), 
                        'Group': 'Modifier', 
                        'Style': style
                    })
                
                # Handle positive/negative modifiers for joystick axes
                if '::Joy' in physicalKeySpec:
                    for variant in ['::Pos_Joy', '::Neg_Joy']:
                        for keyModifier in modifiers.get(physicalKeySpec.replace('::Joy', variant), []):
                            if styling == 'Modifier':
                                style = ModifierStyles.index(keyModifier.get('Number'))
                            else:
                                style = groupStyles.get('Modifier')
                            texts.append({
                                'Text': 'Modifier %s' % keyModifier.get('Number'), 
                                'Group': 'Modifier', 
                                'Style': style
                            })

                # Get unmodified bindings
                for modifier, bind in physicalKey.get('Binds').items():
                    if modifier == 'Unmodified':
                        for _controlKey, control in bind.get('Controls').items():
                            if isRedundantSpecialisation(control, bind):
                                continue
                            
                            # Check for misconfigured analogue controls
                            if (control.get('Type') == 'Digital' 
                                    and control.get('HasAnalogue') is True 
                                    and hotasDetail.get('Type') == 'Analogue'):
                                if misconfigurationWarnings == '':
                                    misconfigurationWarnings = (
                                        '<h1>Misconfiguration detected</h1>'
                                        'You have one or more analogue controls configured incorrectly. '
                                        'Please see <a href="https://forums.frontier.co.uk/threads/627609/">'
                                        'this thread</a> for details of the problem and how to correct it.<br/> '
                                        '<b>Your misconfigured controls:</b> <b>%s</b> ' % control['Name']
                                    )
                                else:
                                    misconfigurationWarnings = '%s, <b>%s</b>' % (
                                        misconfigurationWarnings, control['Name']
                                    )

                            # Determine style
                            if styling == 'Modifier':
                                style = ModifierStyles.index(0)
                            elif styling == 'Category':
                                style = categoryStyles.get(control.get('Category', 'General'))
                            else:
                                style = groupStyles.get(control.get('Group'))
                            
                            texts.append({
                                'Text': control.get('Name'),
                                'Group': control.get('Group'),
                                'Style': style
                            })

                # Get modified bindings
                for curModifierNum in range(1, 200):
                    for modifier, bind in physicalKey.get('Binds').items():
                        if modifier != 'Unmodified':
                            keyModifiers = modifiers.get(modifier)
                            modifierNum = 0
                            for keyModifier in keyModifiers:
                                if keyModifier['ModifierKey'] == modifier:
                                    modifierNum = keyModifier['Number']
                                    break
                            
                            if modifierNum != curModifierNum:
                                continue
                            
                            for _controlKey, control in bind.get('Controls').items():
                                if isRedundantSpecialisation(control, bind):
                                    continue
                                
                                if styling == 'Modifier':
                                    style = ModifierStyles.index(curModifierNum)
                                    texts.append({
                                        'Text': control.get('Name'),
                                        'Group': 'Modifier',
                                        'Style': style
                                    })
                                elif styling == 'Category':
                                    style = categoryStyles.get(control.get('Category', 'General'))
                                    texts.append({
                                        'Text': '%s[%s]' % (control.get('Name'), curModifierNum),
                                        'Group': control.get('Group'),
                                        'Style': style
                                    })
                                else:
                                    style = groupStyles.get(control.get('Group'))
                                    texts.append({
                                        'Text': '%s[%s]' % (control.get('Name'), curModifierNum),
                                        'Group': control.get('Group'),
                                        'Style': style
                                    })

                # Layout and render texts
                texts = layoutText(sourceImg, context, texts, hotasDetail, biggestFontSize)
                for text in texts:
                    context.font_size = text['Size']
                    context.font = text['Style']['Font']
                    if styling != 'None':
                        context.fill_color = text['Style']['Color']
                    context.text(x=text['X'], y=text['Y'], body=text['Text'])

            # Add standalone modifiers
            for modifierSpec, keyModifiers in modifiers.items():
                modifierTexts = []
                for keyModifier in keyModifiers:
                    if keyModifier.get('Device') not in imageDevices:
                        continue
                    if int(keyModifier.get('DeviceIndex')) != deviceIndex:
                        continue
                    if '/' in modifierSpec:
                        continue
                    
                    # Check if already handled
                    variants = [modifierSpec]
                    if '::Joy' in modifierSpec:
                        variants.extend([
                            modifierSpec.replace('::Pos_Joy', '::Joy'),
                            modifierSpec.replace('::Neg_Joy', '::Joy')
                        ])
                    if any(physicalKeys.get(v) is not None for v in variants):
                        continue

                    modifierKey = keyModifier.get('Key')
                    hotasDetail = hotasDetails.get(keyModifier.get('Device')).get(modifierKey)
                    if hotasDetail is None:
                        logError('%s: No location for %s\n' % (runId, modifierSpec))
                        continue

                    if styling == 'Modifier':
                        style = ModifierStyles.index(keyModifier.get('Number'))
                    else:
                        style = groupStyles.get('Modifier')
                    modifierTexts.append({
                        'Text': 'Modifier %s' % keyModifier.get('Number'),
                        'Group': 'Modifier',
                        'Style': style
                    })

                if modifierTexts:
                    modifierTexts = layoutText(sourceImg, context, modifierTexts, hotasDetail, biggestFontSize)
                    for text in modifierTexts:
                        context.font_size = text['Size']
                        context.font = text['Style']['Font']
                        if styling != 'None':
                            context.fill_color = text['Style']['Color']
                        context.text(x=text['X'], y=text['Y'], body=text['Text'])

            context.draw(sourceImg)
            sourceImg.save(filename=str(filePath))
    
    return True


def layoutText(img, context, texts, hotasDetail, biggestFontSize):
    """Calculate text layout within a bounding box.
    
    Args:
        img: Wand Image for font metrics
        context: Drawing context
        texts: List of text dictionaries
        hotasDetail: Bounding box info (x, y, width, height)
        biggestFontSize: Maximum font size
    
    Returns:
        List of texts with X, Y, Size added
    """
    width = hotasDetail.get('width')
    height = hotasDetail.get('height', 54)

    # Calculate best fit font size
    fontSize = calculateBestFitFontSize(context, width, height, texts, biggestFontSize)

    # Calculate positions
    currentX = hotasDetail.get('x')
    currentY = hotasDetail.get('y')
    maxX = hotasDetail.get('x') + hotasDetail.get('width')

    for text in texts:
        text['Size'] = fontSize
        context.font = text['Style']['Font']
        context.font_size = fontSize
        metrics = context.get_font_metrics(img, text['Text'], multiline=False)
        
        if currentX + int(metrics.text_width) > maxX:
            currentX = hotasDetail.get('x')
            currentY = currentY + fontSize
        
        text['X'] = currentX
        text['Y'] = currentY + int(metrics.ascender)
        currentX = currentX + int(metrics.text_width + metrics.character_width)

    # Center texts vertically
    textHeight = currentY + fontSize - hotasDetail.get('y')
    yOffset = int((height - textHeight) / 2) - int(fontSize / 6)
    for text in texts:
        text['Y'] = text['Y'] + yOffset

    return texts


def calculateBestFitFontSize(context, width, height, texts, biggestFontSize):
    """Calculate the best font size to fit texts in a box.
    
    Args:
        context: Drawing context
        width: Box width
        height: Box height
        texts: List of text dictionaries
        biggestFontSize: Starting font size
    
    Returns:
        Best fit font size
    """
    fontSize = biggestFontSize
    context.push()
    
    with Image(width=width, height=height) as img:
        fits = False
        while not fits:
            currentX = 0
            currentY = 0
            tooLong = False
            
            for text in texts:
                context.font = text['Style']['Font']
                context.font_size = fontSize
                metrics = context.get_font_metrics(img, text['Text'], multiline=False)
                
                if currentX + int(metrics.text_width) > width:
                    if currentX == 0:
                        tooLong = True
                        break
                    else:
                        currentX = 0
                        currentY = currentY + fontSize
                
                text['X'] = currentX
                text['Y'] = currentY + int(metrics.ascender)
                currentX = currentX + int(metrics.text_width + metrics.character_width)
            
            if not tooLong and currentY + metrics.text_height < height:
                fits = True
            else:
                fontSize = fontSize - 1
    
    context.pop()
    return fontSize


def calculateBestFontSize(context, text, hotasDetail, biggestFontSize):
    """Calculate the best font size for a single text in a box.
    
    Args:
        context: Drawing context
        text: Text string
        hotasDetail: Bounding box info
        biggestFontSize: Starting font size
    
    Returns:
        Tuple of (formatted_text, font_size, metrics)
    """
    width = hotasDetail.get('width')
    height = hotasDetail.get('height', 54)
    
    with Image(width=width, height=height) as img:
        fontSize = biggestFontSize
        fits = False
        
        while not fits:
            fitText = text
            context.font_size = fontSize
            metrics = context.get_font_metrics(img, fitText, multiline=False)
            
            if metrics.text_width <= hotasDetail.get('width'):
                fits = True
            else:
                lines = max(int(height / metrics.text_height), 1)
                if lines == 1:
                    fontSize = fontSize - 1
                else:
                    fitText = ''
                    minLineLength = int(len(text) / lines)
                    regex = r'.{%s}[^,]*, |.+' % minLineLength
                    matches = re.findall(regex, text)
                    for match in matches:
                        if fitText == '':
                            fitText = match
                        else:
                            fitText = '%s\n%s' % (fitText, match)

                    metrics = context.get_font_metrics(img, fitText, multiline=True)
                    if metrics.text_width <= hotasDetail.get('width'):
                        fits = True
                    else:
                        fontSize = fontSize - 1

    return (fitText, fontSize, metrics)
