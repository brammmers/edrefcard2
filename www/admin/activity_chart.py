"""Geometry of the admin "cards created per day" chart (inline SVG, no JS).

Pure functions: the template only draws what build_chart returns.
"""
import math

WIDTH, HEIGHT = 1000, 280
LEFT, RIGHT, TOP, BOTTOM = 48, 12, 14, 30
RANGES = (30, 90, 365)
AVERAGE_DAYS = 7


def _nice_max(value):
    """Top of the y axis: 4 x a round integer step, just above value."""
    step = max(value / 4, 1)
    power = 10 ** math.floor(math.log10(step))
    for factor in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        candidate = factor * power
        if candidate >= step and candidate == int(candidate):
            return int(4 * candidate)
    return int(40 * power)


def _bar_path(x, y, w, h):
    """Bar anchored to the baseline, top corners rounded when wide enough."""
    r = min(4, w / 2, h) if w >= 6 else 0
    if r <= 0:
        return 'M%.1f %.1fh%.1fv%.1fh%.1fz' % (x, y + h, w, -h, -w)
    return ('M%.1f %.1fv%.1fq0 %.1f %.1f %.1fh%.1fq%.1f 0 %.1f %.1fv%.1fz'
            % (x, y + h, -(h - r), -r, r, -r, w - 2 * r, r, r, r, h - r))


def build_chart(series):
    """series: [(date, count)] oldest first, last item = today (partial)."""
    n = len(series)
    plot_w, plot_h = WIDTH - LEFT - RIGHT, HEIGHT - TOP - BOTTOM
    counts = [count for _, count in series]
    averages = []
    for i in range(n):
        window = counts[max(0, i - AVERAGE_DAYS + 1):i + 1]
        averages.append(sum(window) / len(window))
    top = _nice_max(max(counts + [0]))
    slot = plot_w / n if n else plot_w
    gap = 2 if slot >= 6 else (0.5 if slot >= 2 else 0)
    baseline = TOP + plot_h

    def y_of(value):
        return baseline - plot_h * value / top

    bars = []
    for i, (day, count) in enumerate(series):
        x = LEFT + i * slot
        h = plot_h * count / top
        partial = i == n - 1
        bars.append({
            'path': _bar_path(x + gap / 2, baseline - h, max(slot - gap, 0.6), h) if count else '',
            'hit_x': round(x, 1), 'hit_w': round(slot, 1),
            'title': '%s: %d card%s%s, 7-day average %.1f' % (
                day.strftime('%a %d %b %Y'), count, '' if count == 1 else 's',
                ' (today, so far)' if partial else '', averages[i]),
            'partial': partial,
        })
    # The trailing average stops before today: a partial day would drag it down.
    points = [(LEFT + (i + 0.5) * slot, y_of(a)) for i, a in enumerate(averages[:-1])]
    line = 'M' + ' L'.join('%.1f %.1f' % p for p in points) if len(points) > 1 else ''
    grid = [{'y': round(y_of(top * k / 4), 1), 'label': str(int(top * k / 4))} for k in range(5)]
    ticks = []
    for i, (day, _) in enumerate(series):
        if (n <= 31 and day.weekday() == 0) or (n > 31 and day.day == 1):
            label = day.strftime('%d %b') if n <= 31 else (
                day.strftime('%b %Y') if day.month == 1 or not ticks else day.strftime('%b'))
            ticks.append({'x': round(LEFT + (i + 0.5) * slot, 1), 'label': label})
    complete = counts[:-1] or counts
    return {
        'width': WIDTH, 'height': HEIGHT, 'left': LEFT, 'right': WIDTH - RIGHT,
        'baseline': baseline, 'bars': bars, 'line': line, 'grid': grid, 'ticks': ticks,
        'total': sum(counts), 'today': counts[-1] if counts else 0,
        'mean': sum(complete) / len(complete) if complete else 0,
        'best': max(series[:-1] or series, key=lambda item: item[1]) if series else None,
    }
