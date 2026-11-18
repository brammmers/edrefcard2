"""Data of the admin "cards created per day" chart (HTML bars, no JS).

Pure functions: the template only draws what build_chart returns. Positions are
percentages of the plot area, so labels keep their pixel size at any width.
"""
import datetime
import math
import re

RANGES = (30, 90, 365)
AVERAGE_DAYS = 7
DENSE_FROM = 91          # above this many days, bars touch (no gap)


def _nice_max(value):
    """Top of the y axis: 4 x a round integer step, just above value."""
    step = max(value / 4, 1)
    power = 10 ** math.floor(math.log10(step))
    for factor in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        candidate = factor * power
        if candidate >= step and candidate == int(candidate):
            return int(4 * candidate)
    return int(40 * power)


def build_chart(series):
    """series: [(date, count)] oldest first, last item = today (partial)."""
    n = len(series)
    counts = [count for _, count in series]
    averages = []
    for i in range(n):
        window = counts[max(0, i - AVERAGE_DAYS + 1):i + 1]
        averages.append(sum(window) / len(window))
    top = _nice_max(max(counts + [0]))

    bars = []
    for i, (day, count) in enumerate(series):
        partial = i == n - 1
        bars.append({
            'height': round(100 * count / top, 2),
            'title': '%s: %d card%s%s, 7-day average %.1f' % (
                day.strftime('%a %d %b %Y'), count, '' if count == 1 else 's',
                ' (today, so far)' if partial else '', averages[i]),
            'partial': partial,
        })
    # Average line in a "0 0 n 100" viewBox stretched over the plot; it stops
    # before today: a partial day would drag it down.
    points = [(i + 0.5, 100 - 100 * a / top) for i, a in enumerate(averages[:-1])]
    line = 'M' + ' L'.join('%.2f %.2f' % p for p in points) if len(points) > 1 else ''
    grid = [{'pct': 25 * k, 'label': str(int(top * k / 4))} for k in range(5)]
    ticks = []
    for i, (day, _) in enumerate(series):
        if (n <= 31 and day.weekday() == 0) or (n > 31 and day.day == 1):
            label = day.strftime('%d %b') if n <= 31 else (
                day.strftime('%b %Y') if day.month == 1 or not ticks else day.strftime('%b'))
            ticks.append({'pct': round(100 * (i + 0.5) / n, 2), 'label': label})
    complete = counts[:-1] or counts
    return {
        'days': n, 'dense': n >= DENSE_FROM, 'bars': bars, 'line': line, 'grid': grid, 'ticks': ticks,
        'total': sum(counts), 'today': counts[-1] if counts else 0,
        'mean': sum(complete) / len(complete) if complete else 0,
        'best': max(series[:-1] or series, key=lambda item: item[1]) if series else None,
    }


def build_monthly(series):
    """series: [('YYYY-MM', count)] oldest first, last item = current month (partial)."""
    n = len(series)
    counts = [count for _, count in series]
    top = _nice_max(max(counts + [0]))
    bars, ticks = [], []
    for i, (key, count) in enumerate(series):
        year, month = map(int, key.split('-'))
        name = datetime.date(year, month, 1).strftime('%b %Y')
        partial = i == n - 1
        bars.append({'height': round(100 * count / top, 2), 'partial': partial,
                     'title': '%s: %s cards%s' % (name, format(count, ','), ' (so far)' if partial else '')})
        if month in (1, 7):
            ticks.append({'pct': round(100 * (i + 0.5) / n, 2), 'label': str(year) if month == 1 else 'Jul'})
    return {
        'days': n, 'dense': False, 'bars': bars, 'line': '', 'ticks': ticks,
        'grid': [{'pct': 25 * k, 'label': format(int(top * k / 4), ',')} for k in range(5)],
        'total': sum(counts),
        'since': datetime.date(*map(int, series[0][0].split('-')), 1).strftime('%B %Y') if series else None,
    }


# Template names that are one product: left and right hand sticks, OTA firmware
# variants and the Xbox pads are counted once.
SIDE_SUFFIX = re.compile(r'-(left|right)(-ota)?$')
FAMILY_ALIASES = {'xboxelite': 'xbox', 'xbox-elite-b00': 'xbox'}
FAMILY_NAMES = {
    'vkb-gladiator-nxt-premium': 'VKB Gladiator NXT',
    'x56': 'Logitech X56',
    'xbox': 'Xbox controller',
    't16000mfcs': 'Thrustmaster T.16000M FCS',
    't16000m': 'Thrustmaster T.16000M',
    'hotasx': 'Thrustmaster T.Flight HOTAS X',
    'hotas4': 'Thrustmaster T.Flight HOTAS 4',
    'warthog': 'Thrustmaster Warthog',
    'tfrp': 'Thrustmaster TFRP pedals',
    'x52pro': 'Saitek X52 Pro',
    'x52': 'Saitek X52',
    'x55': 'Saitek X55',
    'proflightpedals': 'Saitek Pro Flight pedals',
    'extreme3dpro': 'Logitech Extreme 3D Pro',
    'winwing-ursa-minor-fighter': 'Winwing Ursa Minor Fighter',
    'vpc-alpha': 'Virpil VPC Alpha',
    'vpc-mongoost-50cm3-throttle': 'Virpil MongoosT-50CM3 throttle',
    'chfighter': 'CH Fighterstick',
}


def controller_family(template):
    family = SIDE_SUFFIX.sub('', template)
    return FAMILY_ALIASES.get(family, family)


def family_name(family):
    return FAMILY_NAMES.get(family) or ' '.join(
        word.upper() if len(word) <= 3 and any(c.isdigit() for c in word) else word.capitalize()
        for word in family.split('-'))


def build_top(total, pairs, limit=5):
    """total: cards in the period; pairs: [(template, config id)] without keyboards."""
    cards = {}
    for template, config_id in pairs:
        cards.setdefault(controller_family(template), set()).add(config_id)
    ranked = sorted(cards.items(), key=lambda item: (-len(item[1]), item[0]))[:limit]
    peak = len(ranked[0][1]) if ranked else 1
    return [{'rank': rank, 'name': family_name(family), 'count': len(ids),
             'width': round(100 * len(ids) / peak, 1),
             'share': round(100 * len(ids) / total) if total else 0}
            for rank, (family, ids) in enumerate(ranked, 1)]
