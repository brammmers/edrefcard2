"""Validation shared by editor saves and imported mapping documents."""

import math
import re


def validate_mapping(mapping):
    """Validate structure without guessing hardware semantics or rearranging it."""
    if not isinstance(mapping, dict):
        raise ValueError('The mapping must be a JSON object.')
    image = mapping.get('image')
    if not isinstance(image, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,199}', image):
        raise ValueError('Upload an image before saving this draft.')
    for key in ('width', 'height'):
        value = mapping.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ValueError('Image width and height must be positive numbers.')
    if 'show_title' in mapping and type(mapping['show_title']) is not bool:
        raise ValueError('Title visibility must be true or false.')
    for key, label in (('url_xy', 'URL'), ('title_xy', 'Title')):
        if key not in mapping:
            continue
        position = mapping[key]
        if (not isinstance(position, list) or len(position) != 2 or
                any(type(v) not in (int, float) or not math.isfinite(v) or v < 0
                    for v in position) or position[0] >= mapping['width'] or
                position[1] >= mapping['height']):
            raise ValueError(f'{label} position must be inside the image.')
    ids = mapping.get('device_ids', [])
    if not isinstance(ids, list) or any(not isinstance(v, str) or not v.strip() for v in ids):
        raise ValueError('Hardware IDs must be a list of non-empty strings.')
    boxes = mapping.get('boxes')
    if not isinstance(boxes, list):
        raise ValueError('The mapping must contain a boxes list.')
    for index, box in enumerate(boxes, 1):
        if not isinstance(box, dict):
            raise ValueError(f'Group {index} is not an object.')
        for key in ('box_xy', 'box_wh', 'button_xy'):
            value = box.get(key)
            if key == 'button_xy' and value is None:
                continue
            if (not isinstance(value, list) or len(value) != 2 or
                    any(type(v) not in (int, float) or not math.isfinite(v) or
                        (v <= 0 if key == 'box_wh' else v < 0) for v in value)):
                raise ValueError(f'Group {index}: invalid {key}.')
        via = box.get('leader_via_y')
        if via is not None and (type(via) not in (int, float) or not math.isfinite(via) or
                                via < 0 or via >= mapping['height']):
            raise ValueError(f'Group {index}: the leader detour must stay inside the image.')
        rows = box.get('rows')
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError(f'Group {index}: rows must be a list of objects.')
        for row in rows:
            if not isinstance(row.get('joy', ''), str):
                raise ValueError(f'Group {index}: input codes must be text.')
            rect = row.get('field_rect')
            if rect is not None:
                if (not isinstance(rect, list) or len(rect) != 4 or
                        any(type(v) not in (int, float) or not math.isfinite(v) for v in rect) or
                        rect[0] < 0 or rect[1] < 0 or rect[2] <= 0 or rect[3] <= 0 or
                        rect[0] + rect[2] > 1.000001 or rect[1] + rect[3] > 1.000001):
                    raise ValueError(f'Group {index}: invalid imported field rectangle.')
