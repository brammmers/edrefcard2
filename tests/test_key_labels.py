"""Key labels on the text keyboard card must be drawable by the card font."""
import unittest

from scripts import utils


class KeyLabelTests(unittest.TestCase):
    def test_every_label_is_plain_text(self):
        # The card font (Exo 2) has no arrow or keycap symbols: a label such
        # as '⇧' was drawn as an empty key on every card.
        for key, label in utils.keymap.items():
            with self.subTest(key=key):
                self.assertTrue(label.isascii() and label.isprintable(), repr(label))

    def test_modifiers_keep_their_side(self):
        self.assertEqual(utils.transKey('Key_LeftShift'), 'Left Shift')
        self.assertEqual(utils.transKey('Key_RightAlt'), 'Right Alt')
        self.assertEqual(utils.transKey('Key_RightControl'), 'Right Ctrl')

    def test_unknown_keys_fall_back_to_their_name(self):
        self.assertEqual(utils.transKey('Key_F13'), 'F13')
        self.assertIsNone(utils.transKey(None))


if __name__ == '__main__':
    unittest.main()
