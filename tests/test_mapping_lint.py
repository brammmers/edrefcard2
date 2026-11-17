"""Quality checks shared by the editor's Checks panel and the publication gate."""
import unittest

from scripts.mapping_lint import lint_mapping, lint_summary
from scripts.mapping_validation import validate_mapping


def box(label='TRIGGER', xy=(100, 100), wh=(600, 190), anchor=(900, 400), rows=None, **extra):
    return {'label': label, 'box_xy': list(xy), 'box_wh': list(wh),
            'button_xy': list(anchor) if anchor else None,
            'rows': rows if rows is not None else [{'joy': 'Joy_1'}], **extra}


def mapping(*boxes, **extra):
    return {'image': 'card', 'width': 2200, 'height': 1280, 'boxes': list(boxes), **extra}


def messages(issues, level):
    return [issue['message'] for issue in issues if issue['level'] == level]


class LintTests(unittest.TestCase):
    def test_clean_mapping_has_no_issue(self):
        document = mapping(box(rows=[{'joy': 'Joy_1'}, {'joy': 'Joy_XAxis'}, {'joy': 'Joy_POV1Up'},
                                     {'joy': 'Neg_Joy_RYAxis'}, {'joy': 'Pos_Joy_RYAxis'}]))
        self.assertEqual(lint_mapping(document), [])

    def test_mistyped_codes_block_publication(self):
        for code in ('joy_2', 'Joy 2', 'JOY_2', ' Joy_2', 'Joy_', 'Joy_POV1', 'Joy_0', 'pos_Joy_XAxis'):
            issues = lint_mapping(mapping(box(rows=[{'joy': 'Joy_1'}, {'joy': code}])))
            errors = messages(issues, 'error')
            self.assertEqual(len(errors), 1, code)
            self.assertIn(code, errors[0])
            self.assertEqual(issues[0]['box'], 0)

    def test_other_code_families_only_warn(self):
        issues = lint_mapping(mapping(box(rows=[{'joy': 'Pad_A'}])))
        self.assertEqual(messages(issues, 'error'), [])
        self.assertIn('Pad_A', messages(issues, 'warning')[0])

    def test_box_outside_the_image_blocks_publication(self):
        for outside in (box(xy=(1800, 100)), box(xy=(100, 1200)), box(xy=(-5, 100))):
            errors = messages(lint_mapping(mapping(outside)), 'error')
            self.assertEqual(len(errors), 1)
            self.assertIn('outside the image', errors[0])

    def test_warnings_for_anchor_blank_rows_duplicates_and_empty_box(self):
        issues = lint_mapping(mapping(
            box('A', anchor=None, rows=[{'joy': 'Joy_1'}, {'joy': ''}, {'joy': None}]),
            box('B', xy=(100, 400), rows=[{'joy': 'Joy_1'}]),
            box('C', xy=(100, 700), rows=[])))
        self.assertEqual(messages(issues, 'error'), [])
        warnings = ' | '.join(messages(issues, 'warning'))
        self.assertIn('"A" has no anchor point', warnings)
        self.assertIn('"A" has 2 rows without an input code', warnings)
        self.assertIn('"Joy_1" is used in "A" and "B"', warnings)
        self.assertIn('"C" has no rows', warnings)
        self.assertEqual(lint_summary(issues), (0, 4))

    def test_imported_artwork_boxes_do_not_need_an_anchor(self):
        self.assertEqual(lint_mapping(mapping(box(anchor=None, no_chrome=True))), [])

    def test_photo_less_flow_boxes_do_not_need_an_anchor(self):
        flow = {**mapping(box(anchor=None)), 'layout': 'flow'}
        self.assertEqual(lint_mapping(flow), [])

    def test_mapping_without_any_usable_code_is_an_error(self):
        errors = messages(lint_mapping(mapping(box(rows=[{'joy': ''}]))), 'error')
        self.assertTrue(any('every card would be empty' in message for message in errors))

    def test_malformed_documents_never_raise(self):
        for document in (None, [], {}, {'boxes': 'x'}, mapping('not a box'),
                         mapping({'box_xy': 'x', 'rows': [{'joy': 5}, 'row']})):
            issues = lint_mapping(document)
            self.assertTrue(messages(issues, 'error'), document)

    def test_text_positions_outside_the_image_warn(self):
        issues = lint_mapping(mapping(box(), title_xy=[5000, 64], url_xy=[44, 118]))
        self.assertEqual(len(messages(issues, 'warning')), 1)
        self.assertIn('title', messages(issues, 'warning')[0])


class TitlePositionValidationTests(unittest.TestCase):
    def test_title_position_follows_the_url_position_rule(self):
        validate_mapping(mapping(box(), title_xy=[900, 80], url_xy=[900, 140], show_title=False))
        for bad in ([2200, 80], [-1, 80], [10], 'top', [10, float('nan')]):
            with self.assertRaises(ValueError):
                validate_mapping(mapping(box(), title_xy=bad))


if __name__ == '__main__':
    unittest.main()
