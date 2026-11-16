"""The text keyboard card shrinks its font until every column fits (issue #42)."""
import unittest
from types import SimpleNamespace
from unittest import mock

from scripts import renderer


class FakeContext:
    """Measures text as 0.6 x font size per character, like a real font roughly."""

    def __init__(self):
        self.drawn = []

    def push(self):
        pass

    def pop(self):
        pass

    def text(self, x, y, body):
        self.drawn.append(body)

    def rectangle(self, **kwargs):
        self.drawn.append('box')

    def get_font_metrics(self, img, text, multiline=False):
        size = self.font_size
        return SimpleNamespace(text_width=len(text) * size * 0.6,
                               text_height=size * 1.2, ascender=size)


def fake_font(path, antialias=True, size=0):
    return SimpleNamespace(path=path, size=size)


def entries(count):
    result = [('Ship', True, False, True)]
    for i in range(count):
        result.append(('Left Ctrl', False, True, False))
        result.append((f'K{i}', False, True, False))
        result.append((f'Some control name {i}', False, False, True))
    return result


@mock.patch.object(renderer, 'Font', fake_font)
@mock.patch.object(renderer, 'Color', lambda name: name)
class KeyboardFitTests(unittest.TestCase):
    def measure(self, items, size):
        state = renderer._keyboardScreenState()
        (font, title) = renderer._keyboardFonts(size)
        context = FakeContext()
        for text, is_title, surround, new_line in items:
            renderer.writeText(context, None, text, state, title if is_title else font,
                               surround, new_line, draw=False)
        return state['rightEdge'], context.drawn

    def test_few_keys_keep_the_requested_size(self):
        self.assertEqual(renderer._fitKeyboardFontSize(FakeContext(), None, entries(20), 40), 40)

    def test_many_keys_shrink_until_the_columns_fit(self):
        items = entries(200)
        self.assertGreater(self.measure(items, 24)[0], renderer.CARD_WIDTH)
        size = renderer._fitKeyboardFontSize(FakeContext(), None, items, 24)
        self.assertLess(size, 24)
        self.assertGreaterEqual(size, renderer.KEYBOARD_MIN_FONT_SIZE)
        edge = self.measure(items, size)[0]
        self.assertLessEqual(edge, renderer.CARD_WIDTH - renderer.KEYBOARD_RIGHT_MARGIN)

    def test_never_below_the_minimum_size(self):
        size = renderer._fitKeyboardFontSize(FakeContext(), None, entries(5000), 24)
        self.assertEqual(size, renderer.KEYBOARD_MIN_FONT_SIZE)

    def test_measuring_draws_nothing(self):
        self.assertEqual(self.measure(entries(10), 24)[1], [])


if __name__ == '__main__':
    unittest.main()
