"""Admin dashboard chart: cards created per day."""
import datetime
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    'activity_chart', Path(__file__).resolve().parents[1] / 'www' / 'admin' / 'activity_chart.py')
chart_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chart_module)
build_chart, nice_max = chart_module.build_chart, chart_module._nice_max


def series(counts, end=datetime.date(2026, 11, 17)):
    start = end - datetime.timedelta(days=len(counts) - 1)
    return [(start + datetime.timedelta(days=i), c) for i, c in enumerate(counts)]


class ActivityChartTests(unittest.TestCase):
    def test_axis_top_is_a_round_value_just_above_the_peak(self):
        for peak, top in ((0, 4), (3, 4), (45, 60), (90, 100), (101, 120), (2000, 2000)):
            self.assertEqual(nice_max(peak), top, peak)

    def test_one_bar_per_day_and_empty_days_draw_nothing(self):
        chart = build_chart(series([5, 0, 10, 2]))
        self.assertEqual(len(chart['bars']), 4)
        self.assertEqual(chart['bars'][1]['path'], '')
        self.assertTrue(all(b['path'] for i, b in enumerate(chart['bars']) if i != 1))

    def test_today_is_marked_partial_and_left_out_of_the_mean(self):
        chart = build_chart(series([40, 50, 3]))
        self.assertEqual([b['partial'] for b in chart['bars']], [False, False, True])
        self.assertIn('today, so far', chart['bars'][-1]['title'])
        self.assertEqual(chart['mean'], 45)
        self.assertEqual(chart['today'], 3)
        self.assertEqual(chart['total'], 93)
        self.assertEqual(chart['best'][1], 50)

    def test_average_line_stops_before_today(self):
        chart = build_chart(series([10] * 30))
        self.assertEqual(chart['line'].count('L') + 1, 29)

    def test_tallest_bar_reaches_the_top_grid_line(self):
        chart = build_chart(series([10, 100, 20, 1]))
        top_grid = chart['grid'][-1]
        self.assertEqual(top_grid['label'], '100')
        # "M<x> <baseline>v<-(h - r)>q0 -r ..." with r = 4
        start, rest = chart['bars'][1]['path'][1:].split('v', 1)
        baseline = float(start.split()[1])
        rise = float(rest.split('q')[0])
        self.assertEqual(baseline, chart['baseline'])
        self.assertAlmostEqual(baseline + rise - 4, top_grid['y'], places=0)

    def test_month_ticks_on_long_ranges_week_ticks_on_short_ones(self):
        long_chart = build_chart(series([1] * 365))
        self.assertEqual(len(long_chart['ticks']), 12)
        short_chart = build_chart(series([1] * 30))
        self.assertTrue(4 <= len(short_chart['ticks']) <= 5)

    def test_wide_bars_are_rounded_narrow_ones_are_not(self):
        self.assertIn('q', build_chart(series([5] * 30))['bars'][0]['path'])
        self.assertNotIn('q', build_chart(series([5] * 365))['bars'][0]['path'])


if __name__ == '__main__':
    unittest.main()
