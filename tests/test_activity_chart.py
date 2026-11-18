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
build_monthly, build_top = chart_module.build_monthly, chart_module.build_top


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
        self.assertEqual(chart['bars'][1]['height'], 0)
        self.assertTrue(all(b['height'] for i, b in enumerate(chart['bars']) if i != 1))

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
        self.assertEqual(chart['grid'][-1], {'pct': 100, 'label': '100'})
        self.assertEqual(chart['bars'][1]['height'], 100)
        self.assertEqual(chart['bars'][0]['height'], 10)

    def test_month_ticks_on_long_ranges_week_ticks_on_short_ones(self):
        long_chart = build_chart(series([1] * 365))
        self.assertEqual(len(long_chart['ticks']), 12)
        short_chart = build_chart(series([1] * 30))
        self.assertTrue(4 <= len(short_chart['ticks']) <= 5)
        self.assertTrue(all(0 < t['pct'] < 100 for t in long_chart['ticks']))

    def test_bars_touch_only_on_the_yearly_view(self):
        self.assertFalse(build_chart(series([5] * 90))['dense'])
        self.assertTrue(build_chart(series([5] * 365))['dense'])


    def test_monthly_bars_mark_the_current_month_and_label_years(self):
        months = [('2025-11', 10), ('2025-12', 0), ('2026-01', 40), ('2026-02', 5)]
        chart = build_monthly(months)
        self.assertEqual([b['height'] for b in chart['bars']], [25, 0, 100, 12.5])
        self.assertEqual([b['partial'] for b in chart['bars']], [False, False, False, True])
        self.assertIn('(so far)', chart['bars'][-1]['title'])
        self.assertEqual([t['label'] for t in chart['ticks']], ['2026'])
        self.assertEqual(chart['since'], 'November 2025')
        self.assertEqual(chart['total'], 55)

    def test_top_counts_each_card_once_per_product(self):
        pairs = [('vkb-gladiator-nxt-premium-right', 1), ('vkb-gladiator-nxt-premium-left', 1),
                 ('vkb-gladiator-nxt-premium-left-ota', 2), ('xbox', 3), ('xboxelite', 4),
                 ('xbox-elite-b00', 3), ('x56', 5), ('winwing-ursa-minor-fighter-right', 6)]
        top = build_top(10, pairs)
        self.assertEqual([(r['name'], r['count']) for r in top[:2]],
                         [('VKB Gladiator NXT', 2), ('Xbox controller', 2)])
        self.assertEqual(top[0]['share'], 20)
        self.assertEqual(top[0]['width'], 100)
        self.assertEqual(top[2]['width'], 50)
        self.assertIn('Winwing Ursa Minor Fighter', [r['name'] for r in top])

    def test_unknown_families_get_a_readable_name_and_the_list_is_capped(self):
        pairs = [('family-%d' % i, i) for i in range(8)] + [('vpc-mongoost-50cm2-throttle', 99)]
        top = build_top(20, pairs)
        self.assertEqual(len(top), 5)
        self.assertEqual(top[0]['name'], 'Family 0')
        self.assertEqual(build_top(0, []), [])


if __name__ == '__main__':
    unittest.main()
