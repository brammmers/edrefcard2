#!/usr/bin/env python3
"""
EDRefCard Renderer Module

This module contains functions for generating reference card images
using the Wand/ImageMagick library.
"""

import math
import re
import copy
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
from .mapping_runtime import matches_input, normalize_input

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


# Templates whose default top-left URL spot is occupied by artwork and need the URL
# elsewhere. The mirrored left-handed TCA sidestick has a wide central box that sits
# under the default position, so the URL goes to the clear bottom-left instead.
_URL_POSITION_OVERRIDES = {
    'tca-left': (30, 2110),
}


def writeUrlToDrawing(config, drawing, public, source=None):
    """Write the reference card URL to the image.

    Args:
        config: Config object
        drawing: Wand Drawing context
        public: Whether this is a public reference card
        source: Template name, used to look up a per-template URL position override
    """
    url = config.refcardURL() if public else Config.webRoot()
    x, y = _URL_POSITION_OVERRIDES.get(source, (23, 252))
    drawing.push()
    drawing.font = getFontPath('SemiBold', 'Normal')
    drawing.font_size = 36
    drawing.text(x=x, y=y, body=url)
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
            writeUrlToDrawing(config, context, public, source)

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

            # Everything to write, in order: (text, is_title, surround, newLine)
            entries = []
            for displayGroup in displayGroups:
                if not outputs[displayGroup]:
                    continue

                entries.append((displayGroup, True, False, True))

                orderedOutputs = OrderedDict(
                    sorted(outputs[displayGroup].items(),
                           key=lambda x: x[1].get('Control').get('Order'))
                )
                for _bindKey, bind in orderedOutputs.items():
                    for modifier in bind.get('Modifiers', []):
                        entries.append((transKey(modifier), False, True, False))
                    entries.append((transKey(bind.get('Key')), False, True, False))
                    entries.append((bind.get('Control').get('Name'), False, False, True))

            with Drawing() as measure:
                fontSize = _fitKeyboardFontSize(measure, sourceImg, entries, biggestFontSize)
            (font, groupTitleFont) = _keyboardFonts(fontSize)
            context.stroke_width = 1
            context.stroke_color = Color('Black')
            context.fill_opacity = 0

            screenState = _keyboardScreenState(fontSize / biggestFontSize)
            for text, isTitle, surround, newLine in entries:
                writeText(context, sourceImg, text, screenState,
                          groupTitleFont if isTitle else font, surround, newLine)

            context.draw(sourceImg)
            sourceImg.save(filename=str(filePath))
    
    return True


CARD_WIDTH = 3840
KEYBOARD_RIGHT_MARGIN = 40
KEYBOARD_MIN_FONT_SIZE = 16


def _keyboardScreenState(scale=1.0):
    return {
        'baseX': 60,
        'baseY': 320,
        'maxWidth': 0,
        'thisWidth': 0,
        'currentX': 60,
        'currentY': 320,
        'rightEdge': 0,
        'scale': scale,  # spacing between keys, lines and columns
    }


def _keyboardFonts(size):
    path = getFontPath('Regular', 'Normal')
    return (Font(path, antialias=True, size=size),
            Font(path, antialias=True, size=size * 2))


def _fitKeyboardFontSize(context, img, entries, biggestFontSize):
    """Largest font size, from biggestFontSize down, whose columns fit the card.

    The text keyboard card fills columns from left to right. With many keys
    bound (third-party tools bind almost every key) the last columns used to
    run past the right edge and were cut off (brammmers/edrefcard2#42), so
    the layout is measured first and shrinks until it fits. The spacing
    shrinks with the font (a uniform zoom out), otherwise the fixed gaps
    take most of the room at small sizes. A card that already fits is
    drawn exactly as before.
    """
    size = biggestFontSize
    while size > KEYBOARD_MIN_FONT_SIZE:
        (font, groupTitleFont) = _keyboardFonts(size)
        state = _keyboardScreenState(size / biggestFontSize)
        for text, isTitle, surround, newLine in entries:
            writeText(context, img, text, state, groupTitleFont if isTitle else font,
                      surround, newLine, draw=False)
        if state['rightEdge'] <= CARD_WIDTH - KEYBOARD_RIGHT_MARGIN:
            break
        size -= 1
    return size


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


def writeText(context, img, text, screenState, font, surround, newLine, draw=True):
    """Write text to an image with wrapping support.

    Args:
        context: Wand Drawing context
        img: Wand Image
        text: Text to write
        screenState: Dictionary tracking current position
        font: Font to use
        surround: Whether to draw a box around the text
        newLine: Whether to move to next line after writing
        draw: False only measures: the position advances and
            screenState['rightEdge'] records the right-most pixel used
    """
    # Spacing in pixels at scale 1, shrunk with the font by _fitKeyboardFontSize
    scale = screenState.get('scale', 1.0)
    border = max(1, round(4 * scale))
    lineGap = round(32 * scale)
    columnGap = round(49 * scale)
    keyGap = round(48 * scale)
    grid = 48 * scale

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
    if screenState['currentY'] + int(metrics.text_height + lineGap) > 2160:
        screenState['currentY'] = screenState['baseY']
        screenState['baseX'] = screenState['baseX'] + screenState['maxWidth'] + columnGap
        screenState['currentX'] = screenState['baseX']
        screenState['maxWidth'] = 0
        screenState['thisWidth'] = 0
    
    x = screenState['currentX']
    y = screenState['currentY'] + int(metrics.ascender)
    if draw:
        context.text(x=x, y=y, body=text)
    context.pop()

    right = x + int(metrics.text_width) + (border * 4 if surround else 0)
    screenState['rightEdge'] = max(screenState.get('rightEdge', 0), right)

    if surround:
        y = screenState['currentY'] - border
        if draw:
            context.rectangle(
                left=x - (border * 4),
                top=y - (border * 2),
                width=int(metrics.text_width) + (border * 8),
                height=int(metrics.text_height) + (border * 4),
                radius=round(30 * scale)
            )
        width = int(metrics.text_width + keyGap)
    else:
        width = int(int((metrics.text_width + 1.5 * grid) / grid) * grid)

    screenState['thisWidth'] += width

    if newLine:
        if screenState['thisWidth'] > screenState['maxWidth']:
            screenState['maxWidth'] = screenState['thisWidth']
        screenState['currentY'] += int(metrics.text_height + lineGap)
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
            writeUrlToDrawing(config, context, public, source)

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
    if width <= 0 or height <= 0:
        raise ValueError('Text area must have positive width and height.')
    if not texts:
        return []

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
    if width <= 0 or height <= 0:
        raise ValueError('Text area must have positive width and height.')
    maxFontSize = max(1, min(int(biggestFontSize), 256))
    if not texts:
        return maxFontSize
    context.push()
    try:
        with Image(width=max(1, math.ceil(width)), height=max(1, math.ceil(height))) as img:
            for fontSize in range(maxFontSize, 0, -1):
                currentX = 0
                currentY = 0
                tooLong = False
                for text in texts:
                    context.font = text['Style']['Font']
                    context.font_size = fontSize
                    metrics = context.get_font_metrics(img, text['Text'], multiline=False)
                    # Every command must fit on its own, including commands
                    # encountered after the first item on a line.
                    if int(metrics.text_width) > width:
                        tooLong = True
                        break
                    if currentX + int(metrics.text_width) > width:
                        currentX = 0
                        currentY += fontSize
                    text['X'] = currentX
                    text['Y'] = currentY + int(metrics.ascender)
                    currentX += int(metrics.text_width + metrics.character_width)
                if not tooLong and currentY + metrics.text_height <= height:
                    return fontSize
        raise ValueError('Text does not fit this box even at the minimum font size. Enlarge the box.')
    finally:
        context.pop()


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
    if width <= 0 or height <= 0:
        raise ValueError('Text area must have positive width and height.')
    
    with Image(width=width, height=height) as img:
        fontSize = biggestFontSize
        fits = False
        
        while not fits and fontSize >= 1:
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

    if not fits:
        raise ValueError('Text does not fit this box even at the minimum font size. Enlarge the box.')
    return (fitText, fontSize, metrics)


# ============== Data-driven controller rendering (feature B1) ==============
# Renders a card by DRAWING the chrome (box frame, leader line, group header,
# per-row symbol + number) from a mapping_json structure, on top of a CLEAN
# controller image - instead of relying on an artwork baked into the template.
# Legacy createHOTASImage is unchanged. Binding text rendering is reused from
# layoutText (added in a later step).

_LEADER_COLOR = '#962320'


# Legacy EdRefCard uses TEXT glyphs in the symbol column (matches the reference
# cards), not drawn shapes: ^ > v < 0 for hat up/right/down/left/press, and words
# for trigger stages / levers.
_SYMBOL_GLYPHS = {
    'press': '0', 'up': '^', 'right': '>', 'down': 'v', 'left': '<',
    'stage1': 'stage 1', 'stage2': 'stage 2', 'push': 'push', 'pull': 'pull',
}


def _symbolColumnWidth(symbol):
    """Width reserved for the symbol column (wider for word glyphs like 'stage 1')."""
    g = _SYMBOL_GLYPHS.get(symbol or '', '')
    if not g:
        return 0
    return 150 if len(g) > 2 else 44


def _drawControlSymbol(context, x, y_center, symbol, scale=1):
    """Render the legacy text glyph for a control, vertically centred on y_center."""
    g = _SYMBOL_GLYPHS.get(symbol or '')
    if not g:
        return
    context.push()
    context.stroke_color = Color('transparent')
    context.fill_color = Color('#333333')
    context.font = getFontPath('Bold', 'Normal')
    context.font_size = max(1, 28 * scale)
    context.text(x=int(x), y=int(y_center + 10 * scale), body=g)
    context.pop()


def _dataDrivenRowHeights(context, sourceImg, rows, width, available_height, biggestFontSize):
    """Measure content at one shared font size within the editor's height budget.

    Normal rows keep 6 px vertical padding and a 54 px minimum. This also
    keeps the symbol/number gutters identical to their drawing geometry.
    Tiny existing boxes retain the original fitting path instead of growing
    beyond their reserved space. The caller's rows and context are preserved.
    """
    count = max(len(rows), 1)
    font_size = max(1, min(int(biggestFontSize), 256))
    if not rows or available_height < 54 * count:
        return [available_height / count] * count, font_size
    context.push()
    try:
        for size in range(font_size, 0, -1):
            heights = []
            for row in rows:
                scale = min(1, width / 400)
                gutters = 16 + (_symbolColumnWidth(row.get('symbol')) if row.get('symbol') else 0)
                if row.get('number') is not None:
                    gutters += 56
                text_width = width - gutters * scale - 2 * min(10, width * 0.04)
                if text_width <= 0:
                    raise ValueError('Controller row must have a positive text width.')
                current_x = current_y = 0
                content_height = size
                for text in row.get('_texts') or []:
                    context.font = text['Style']['Font']
                    context.font_size = size
                    metrics = context.get_font_metrics(sourceImg, text['Text'], multiline=False)
                    if int(metrics.text_width) > text_width:
                        break
                    if current_x + int(metrics.text_width) > text_width:
                        current_x = 0
                        current_y += size
                    content_height = max(content_height, current_y + size,
                                         current_y + metrics.text_height)
                    current_x += int(metrics.text_width + metrics.character_width)
                else:
                    heights.append(max(54, math.ceil(content_height) + 12))
                    continue
                break  # An individual command needs a smaller font.
            else:
                if sum(heights) <= available_height:
                    return heights, size
        raise ValueError('Text does not fit this box even at the minimum font size. Enlarge the box.')
    finally:
        context.pop()


def _drawDataDrivenBox(context, sourceImg, box, biggestFontSize=40, styling='Group', compact=False):
    """Draw one box: leader line, header label, frame, per-row symbol + number + binding text.

    Boxes with no_chrome=True (imported from a manufacturer AcroForm sheet
    whose artwork already contains frames, badges and leader lines) only get
    their row content written, no chrome drawn on top."""
    x, y = box['box_xy']
    w, h = box['box_wh']
    if w <= 0 or h <= 0:
        raise ValueError('Controller box must have positive width and height.')
    rows = box.get('rows', [])
    chrome = not box.get('no_chrome')
    header_h = min(40, h / 4) if (box.get('label') and chrome) else 0
    row_heights = [(h - header_h) / max(len(rows), 1)] * max(len(rows), 1)
    if compact and chrome:
        row_heights, biggestFontSize = _dataDrivenRowHeights(
            context, sourceImg, rows, w, h - header_h, biggestFontSize)
        h = header_h + sum(row_heights)

    # Leader line (orthogonal elbow) from the box side facing the button to the button point
    btn = box.get('button_xy') if chrome else None
    if btn:
        bx, by = btn
        context.push()
        context.fill_color = Color('transparent')
        sx = x + w if bx >= x + w else x
        sy = y + h / 2
        midx = (sx + bx) / 2
        # Keep the stored layout and existing route. A white halo separates the
        # stronger red leader from dark hardware without changing its anchor.
        for color, width in [('white', 13), (_LEADER_COLOR, 7)]:
            context.stroke_color = Color(color)
            context.stroke_width = width
            context.line((sx, sy), (midx, sy))
            context.line((midx, sy), (midx, by))
            context.line((midx, by), (bx, by))
        context.pop()

    # Header bar + label
    if header_h:
        context.push()
        context.stroke_color = Color('transparent')
        context.fill_color = Color('#cfcfcf')
        context.rectangle(left=x, top=y, width=w, height=header_h)
        context.fill_color = Color('Black')
        context.font = getFontPath('Bold', 'Normal')
        context.font_size = max(1, min(26, header_h * 0.65))
        m = context.get_font_metrics(sourceImg, box['label'], multiline=False)
        if m.text_width > w - 4:
            context.font_size = max(1, context.font_size * max(1, w - 4) / m.text_width)
            m = context.get_font_metrics(sourceImg, box['label'], multiline=False)
        context.text(x=int(x + max(1, (w - m.text_width) / 2)),
                     y=int(y + header_h * 0.8), body=box['label'])
        context.pop()

    # Outer frame
    if chrome:
        context.push()
        context.stroke_color = Color('Black')
        context.stroke_width = 2
        context.fill_color = Color('transparent')
        context.rectangle(left=x, top=y, width=w, height=h)
        context.pop()

    # Per-row symbol + number gutters (+ light separators)
    rows_top = y + header_h
    row_y = rows_top
    for i, row in enumerate(rows):
        ry = row_y
        rx, rw, rh = x, w, row_heights[i]
        row_y += rh
        if not chrome and row.get('field_rect'):
            fx, fy, fw, fh = row['field_rect']
            rx, ry, rw, rh = x + fx * w, y + fy * h, fw * w, fh * h
        if not chrome and not row.get('_texts'):
            continue
        row_cy = ry + rh / 2
        if i > 0 and chrome:
            context.push()
            context.stroke_color = Color('#dddddd')
            context.stroke_width = 1
            context.line((x + 1, ry), (x + w - 1, ry))
            context.pop()
        # Column layout: [symbol glyph][number][binding text]
        gutter_scale = min(1, rw / 400, rh / 54)
        sym_w = _symbolColumnWidth(row.get('symbol')) * gutter_scale if chrome else 0
        if sym_w:
            _drawControlSymbol(context, rx + 16 * gutter_scale, row_cy, row['symbol'], gutter_scale)
        col_x = rx + (16 * gutter_scale if chrome else 0) + sym_w
        if row.get('number') is not None and chrome:
            context.push()
            context.stroke_color = Color('transparent')
            context.fill_color = Color('#555555')
            context.font = getFontPath('Bold', 'Normal')
            context.font_size = max(1, 24 * gutter_scale)
            context.text(x=int(col_x), y=int(row_cy + 8 * gutter_scale), body=str(row['number']))
            context.pop()
            col_x += 56 * gutter_scale
        # Binding text (pre-resolved by createDataDrivenImage), reusing layoutText fitting
        texts = row.get('_texts') or []
        if texts:
            pad_x = min(10, rw * 0.04)
            pad_y = 6 if compact and chrome and rh >= 54 else min(6, rh * 0.1)
            tx = col_x + pad_x
            rect = {'x': tx, 'y': ry + pad_y,
                    'width': rx + rw - tx - pad_x, 'height': rh - 2 * pad_y}
            laid = layoutText(sourceImg, context, texts, rect, biggestFontSize)
            for t in laid:
                context.push()
                context.stroke_color = Color('transparent')
                context.font_size = t['Size']
                context.font = t['Style']['Font']
                context.fill_color = Color('Black') if styling == 'None' else t['Style']['Color']
                context.text(x=int(t['X']), y=int(t['Y']), body=t['Text'])
                context.pop()

    if btn:
        # Draw last so the endpoint stays distinct from this box's chrome.
        context.push()
        context.stroke_color = Color('white')
        context.stroke_width = 5
        context.fill_color = Color(_LEADER_COLOR)
        context.circle((bx, by), (bx + 15, by))
        context.pop()


def _buildJoyTexts(deviceIds, joyKey, deviceIndex, physicalKeys, modifiers, styling):
    """Build the coloured texts list for one Joy_* key from the uploaded bindings.

    Mirrors createHOTASImage's per-key logic so a data-driven card shows the user's
    REAL bindings (not the mapping's sample binds). Returns [{Text, Group, Style}].
    """
    texts = []
    pk = None
    for k in physicalKeys.values():
        if (k.get('Key') == normalize_input(joyKey) and int(k.get('DeviceIndex', 0)) == deviceIndex
                and k.get('Device') in deviceIds):
            pk = k
            break
    if pk is None:
        pk = {'Key': normalize_input(joyKey), 'BaseKey': joyKey, 'Binds': {}}

    # Filter before specialization deduplication, without changing shared keys.
    pk = {**pk, 'Binds': {
        modifier: {**bind, 'Controls': {
            name: control for name, control in bind.get('Controls', {}).items()
            if matches_input(joyKey, control.get('InputKey', pk.get('BaseKey', pk['Key'])))
        }} for modifier, bind in pk.get('Binds', {}).items()
    }}

    seen_modifiers = set()
    for spec, entries in modifiers.items():
        parts = spec.split('::')
        if (len(parts) != 3 or parts[0] not in deviceIds or
                parts[1] != str(deviceIndex) or not matches_input(joyKey, parts[2])):
            continue
        for keyModifier in entries:
            number = keyModifier.get('Number')
            if number in seen_modifiers:
                continue
            seen_modifiers.add(number)
            style = ModifierStyles.index(number) if styling == 'Modifier' else groupStyles.get('Modifier')
            texts.append({'Text': 'Modifier %s' % number, 'Group': 'Modifier', 'Style': style})

    # Unmodified bindings
    for modifier, bind in pk.get('Binds', {}).items():
        if modifier != 'Unmodified':
            continue
        for _ck, control in bind.get('Controls', {}).items():
            if isRedundantSpecialisation(control, bind):
                continue
            if styling == 'Modifier':
                style = ModifierStyles.index(0)
            elif styling == 'Category':
                style = categoryStyles.get(control.get('Category')) or categoryStyles['General']
            else:
                style = groupStyles.get(control.get('Group')) or groupStyles['General']
            texts.append({'Text': control.get('Name'), 'Group': control.get('Group'), 'Style': style})

    # Modified bindings, in modifier-number order
    for curMod in range(1, 200):
        for modifier, bind in pk.get('Binds', {}).items():
            if modifier == 'Unmodified':
                continue
            mnum = 0
            for km in modifiers.get(modifier, []):
                if km['ModifierKey'] == modifier:
                    mnum = km['Number']
                    break
            if mnum != curMod:
                continue
            for _ck, control in bind.get('Controls', {}).items():
                if isRedundantSpecialisation(control, bind):
                    continue
                if styling == 'Modifier':
                    style = ModifierStyles.index(curMod)
                    txt = control.get('Name')
                elif styling == 'Category':
                    style = categoryStyles.get(control.get('Category')) or categoryStyles['General']
                    txt = '%s[%s]' % (control.get('Name'), curMod)
                else:
                    style = groupStyles.get(control.get('Group')) or groupStyles['General']
                    txt = '%s[%s]' % (control.get('Name'), curMod)
                texts.append({'Text': txt, 'Group': control.get('Group'), 'Style': style})
    return texts


def createDataDrivenImage(mapping, config, public, physicalKeys=None, modifiers=None,
                          styling=None, imageDevices=None, deviceIndex=0):
    """Render a data-driven controller card from a mapping_json structure.

    If physicalKeys/modifiers are given, each row's text comes from the user's real
    bindings (matched by row['joy']); otherwise the row's sample 'binds' are used
    (editor preview). mapping = {'title','image','device_ids':[...],'boxes':[...]}.
    """
    if Drawing is None:
        raise RuntimeError("Image generation library (ImageMagick/Wand) is not installed or failed to load.")
    _init_styles()

    source = mapping['image']
    name = source if deviceIndex == 0 else '%s-%s' % (source, deviceIndex)
    filePath = config.pathWithNameAndSuffix(name, '.jpg')

    from pathlib import Path
    # Data-driven clean images live in the persistent volume (added at runtime via
    # the mapping editor); fall back to baked res/ for bundled images.
    candidates = [
        config.configsPath() / 'controllers' / (source + '.jpg'),
        Path(__file__).resolve().parents[1] / 'res' / (source + '.jpg'),
    ]
    template_path = next((c for c in candidates if c.exists()), None)
    if template_path is None:
        raise FileNotFoundError(f"Clean image '{source}.jpg' not found in controllers/ or res/")

    with Image(filename=str(template_path)) as sourceImg:
        with Drawing() as context:
            context.font = getFontPath('Regular', 'Normal')
            context.text_antialias = True
            context.font_style = 'normal'
            context.stroke_width = 0
            context.fill_color = Color('Black')
            context.fill_opacity = 1

            if mapping.get('title') and mapping.get('show_title', True):
                context.push()
                context.font = getFontPath('Black', 'Normal')
                context.font_size = 52
                context.fill_color = Color('Black')
                title_x, title_y = mapping.get('title_xy', [40, 64])
                context.text(x=int(title_x), y=int(title_y), body=mapping['title'])
                context.pop()
            # URL under the title (legacy writeUrlToDrawing uses a fixed position
            # that collides with data-driven boxes).
            context.push()
            context.stroke_color = Color('transparent')
            context.font = getFontPath('Bold', 'Normal')
            context.font_size = 30
            context.fill_color = Color(_LEADER_COLOR)
            url_x, url_y = mapping.get('url_xy', [44, 118])
            context.text(x=int(url_x), y=int(url_y),
                         body=config.refcardURL() if public else Config.webRoot())
            context.pop()

            styling = styling or mapping.get('styling', 'Group')
            device_ids = imageDevices or mapping.get('device_ids') or []
            for original_box in mapping.get('boxes', []):
                box = copy.deepcopy(original_box)
                # Resolve each row's coloured texts: from the user's real bindings
                # (generation) or the row's sample binds (editor preview).
                for row in box.get('rows', []):
                    if physicalKeys is not None:
                        row['_texts'] = (_buildJoyTexts(device_ids, row['joy'], deviceIndex,
                                                       physicalKeys, modifiers or {}, styling)
                                         if row.get('joy') else [])
                    else:
                        row['_texts'] = [
                            {'Text': b.get('name', ''), 'Group': b.get('group', 'General'),
                             'Style': groupStyles.get(b.get('group', 'General'), groupStyles['General'])}
                            for b in (row.get('binds') or [])
                        ]
                # In generation mode, drop rows the user didn't bind and skip a box
                # entirely if none of its controls are used (each user binds a different
                # subset: VR/no-VR, multiple files, with/without pedals). Editor preview
                # (physicalKeys is None) keeps every box/row so the layout stays visible.
                if physicalKeys is not None:
                    kept = [r for r in box.get('rows', []) if r.get('_texts')]
                    if not kept:
                        continue
                    if not box.get('no_chrome'):
                        box = {**box, 'rows': kept}
                _drawDataDrivenBox(context, sourceImg, box, biggestFontSize=40, styling=styling,
                                   compact=physicalKeys is not None)

            context.draw(sourceImg)
            sourceImg.save(filename=str(filePath))
    return True
