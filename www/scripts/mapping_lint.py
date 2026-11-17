"""Quality checks for controller mappings.

validate_mapping() only guarantees a mapping is structurally safe to store and
render. These checks look for what makes a card wrong while still being valid:
a mistyped input code that never matches a binding, a box outside the image,
a box without a leader line. They are the single source of truth for the
editor's "Checks" panel, the review badge on /admin/controllers and the
publication gate (errors block publishing, warnings never do).
"""

import math
import re

# Codes Elite writes for joystick-class devices, optionally as a half axis.
_JOY_CODE = re.compile(
    r'(?:Neg_|Pos_)?Joy_(?:[1-9][0-9]*|(?:X|Y|Z|RX|RY|RZ|U|V)Axis'
    r'|POV[1-9][0-9]*(?:Up|Right|Down|Left))')
# Looks like a joystick code but is not one: wrong case, space, missing part.
_JOY_LOOKALIKE = re.compile(r'\s*(?:neg[_ ]|pos[_ ])?joy', re.IGNORECASE)

EXAMPLES = 'Joy_1, Joy_XAxis, Joy_POV1Up'


def _pair(value):
    return (isinstance(value, list) and len(value) == 2 and
            all(type(v) in (int, float) and math.isfinite(v) for v in value))


def lint_mapping(mapping):
    """Return a list of {'level': 'error'|'warning', 'box': index|None, 'message': str}.

    Never raises: a malformed document yields an error entry instead.
    """
    issues = []

    def add(level, message, box=None):
        issues.append({'level': level, 'box': box, 'message': message})

    if not isinstance(mapping, dict):
        add('error', 'The mapping is not a JSON object.')
        return issues
    width, height = mapping.get('width'), mapping.get('height')
    sized = all(type(v) in (int, float) and math.isfinite(v) and v > 0 for v in (width, height))
    boxes = mapping.get('boxes')
    if not isinstance(boxes, list) or not boxes:
        add('error', 'The mapping has no boxes.')
        return issues

    first_use = {}
    usable = 0
    for index, box in enumerate(boxes):
        if not isinstance(box, dict):
            add('error', f'Box {index + 1} is not an object.', index)
            continue
        name = str(box.get('label') or f'box {index + 1}')
        xy, wh = box.get('box_xy'), box.get('box_wh')
        if not _pair(xy) or not _pair(wh) or wh[0] <= 0 or wh[1] <= 0:
            add('error', f'"{name}" has an invalid position or size.', index)
        elif sized and (xy[0] < 0 or xy[1] < 0 or xy[0] + wh[0] > width + 0.5
                        or xy[1] + wh[1] > height + 0.5):
            add('error', f'"{name}" extends outside the image: its text would be cut off.', index)

        chrome = not box.get('no_chrome')
        anchor = box.get('button_xy')
        if anchor is None:
            # A photo-less "flow" card has no controller image to point at
            if chrome and mapping.get('layout') != 'flow':
                add('warning', f'"{name}" has no anchor point, so no leader line shows '
                               'which control it describes.', index)
        elif _pair(anchor) and sized and not (0 <= anchor[0] <= width and 0 <= anchor[1] <= height):
            add('warning', f'The anchor point of "{name}" is outside the image.', index)

        rows = box.get('rows')
        if not isinstance(rows, list) or not rows:
            add('warning', f'"{name}" has no rows: it never shows any command.', index)
            continue
        blank = 0
        for row in rows:
            joy = row.get('joy') if isinstance(row, dict) else None
            if joy is None or joy == '':
                blank += 1
                continue
            if not isinstance(joy, str):
                add('error', f'"{name}" has an input code that is not text.', index)
                continue
            if _JOY_CODE.fullmatch(joy):
                pass
            elif joy != joy.strip() or _JOY_LOOKALIKE.match(joy):
                add('error', f'"{name}": "{joy}" is not a valid input code, it will never match a '
                             f'binding (expected e.g. {EXAMPLES}).', index)
                continue
            else:
                add('warning', f'"{name}": "{joy}" is not a joystick input code. Keep it only if '
                               'this controller really reports it in .binds files.', index)
            usable += 1
            if joy in first_use and first_use[joy] != (index, name):
                other = first_use[joy][1]
                where = f'twice in "{name}"' if first_use[joy][0] == index else f'in "{other}" and "{name}"'
                add('warning', f'"{joy}" is used {where}: the same commands will be printed twice.', index)
            first_use.setdefault(joy, (index, name))
        if blank:
            add('warning', f'"{name}" has {blank} row{"s" if blank > 1 else ""} without an input '
                           'code: they stay empty on every card.', index)

    if usable == 0:
        add('error', 'No row has a usable input code: every card would be empty.')

    if sized:
        for key, label in (('title_xy', 'title'), ('url_xy', 'card URL')):
            position = mapping.get(key)
            if position is not None and (not _pair(position) or not (
                    0 <= position[0] < width and 0 <= position[1] < height)):
                add('warning', f'The {label} is positioned outside the image.')
    return issues


def lint_summary(issues):
    """(error_count, warning_count)"""
    errors = sum(1 for issue in issues if issue['level'] == 'error')
    return errors, len(issues) - errors
