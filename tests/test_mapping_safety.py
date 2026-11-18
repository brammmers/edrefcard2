"""Run without web dependencies: python -m unittest discover -s tests -v."""

import copy
import importlib.util
import json
import sqlite3
import sys
import tempfile
import threading
import types
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


db = load_module('mapping_test_database', 'www/scripts/database.py')
validation = load_module('mapping_test_validation', 'www/scripts/mapping_validation.py')


def document(image='original', ids=None):
    return {'title': 'Test controller', 'image': image, 'width': 4400, 'height': 2560,
            'device_ids': ids or ['TEST0001', 'TEST0002'],
            'boxes': [{'label': 'Hat', 'box_xy': [70, 200], 'box_wh': [1000, 400],
                       'button_xy': [2000, 600], 'rows': [{'joy': 'Joy_1', 'number': '1'}]}]}


class MappingSafetyTests(unittest.TestCase):
    def test_imported_artwork_can_keep_its_title_and_move_generated_url(self):
        mapping = document()
        mapping.update(show_title=False, url_xy=[40, 2500])
        validation.validate_mapping(mapping)

    def test_leader_detour_must_stay_inside_the_image(self):
        mapping = document()
        mapping['boxes'][0]['leader_via_y'] = 80
        validation.validate_mapping(mapping)
        for value in (-1, mapping['height'], float('inf'), '80'):
            mapping['boxes'][0]['leader_via_y'] = value
            with self.assertRaises(ValueError):
                validation.validate_mapping(mapping)

    def test_imported_header_geometry_rejects_invalid_metadata(self):
        for value in ([40, 2560], [-1, 100], [40, float('nan')], '40,100'):
            mapping = document()
            mapping['url_xy'] = value
            with self.assertRaises(ValueError):
                validation.validate_mapping(mapping)
        mapping = document()
        mapping['show_title'] = 'false'
        with self.assertRaises(ValueError):
            validation.validate_mapping(mapping)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='edrefcard-mapping-tests-')
        db.DB_PATH = Path(self.temp.name) / 'test.db'
        # Pre-migration schema, with no imports or writes to app config folders.
        with db.get_db() as conn:
            conn.executescript('''
                CREATE TABLE controller_mappings (
                    id INTEGER PRIMARY KEY, device_id TEXT UNIQUE, device_name TEXT,
                    template_name TEXT, image_filename TEXT, image_width INTEGER,
                    image_height INTEGER, mapping_json TEXT, created_at TEXT,
                    updated_at TEXT, status TEXT DEFAULT 'published', updated_by TEXT);
                CREATE TABLE controller_mapping_versions (
                    id INTEGER PRIMARY KEY, mapping_id INTEGER, device_name TEXT,
                    mapping_json TEXT, saved_by TEXT, saved_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE legacy_device_aliases (
                    device_id TEXT PRIMARY KEY, legacy_key TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP, created_by TEXT);
            ''')
            conn.execute('INSERT INTO controller_mappings VALUES '
                         "(1, 'TEST0001', 'Original', 'original', 'original.jpg', 4400, 2560, ?, "
                         "'old', 'old', 'published', 'mapper')", (json.dumps(document()),))
            db.migrate_controller_publications(conn)

    def tearDown(self):
        self.temp.cleanup()

    def test_legacy_alias_is_persistent_and_not_silently_reassigned(self):
        db.attach_legacy_device_alias('07382221', 'SaitekX56', 'mapper')
        self.assertEqual(db.list_legacy_device_aliases()[0]['legacy_key'], 'SaitekX56')
        with self.assertRaises(ValueError):
            db.attach_legacy_device_alias('07382221', 'SaitekX52', 'mapper')

    def test_pdf_requires_owner_verification_before_publication(self):
        mapping = document()
        mapping['input_verification_required'] = True
        entry = mapping['boxes'][0]['rows'][0]
        entry['verification'] = 'unverified'
        self.save(mapping)
        revision = db.get_all_controller_mappings()[0]['updated_at']
        with self.assertRaises(db.MappingConflict):
            db.set_controller_publication(1, 'published', revision, 'admin')
        entry['verification'] = 'verified'
        self.save(mapping, revision)
        revision = db.get_all_controller_mappings()[0]['updated_at']
        db.set_controller_publication(1, 'published', revision, 'admin')

    def save(self, mapping=None, base='old'):
        return db.save_controller_draft('TEST0001', 'Edited', mapping or document('new-image'),
                                        'mapper', base, 1)

    def test_migration_preserves_live_and_is_repeatable(self):
        before = db.get_published_controller_mappings()[0]
        self.save()
        with db.get_db() as conn:
            db.migrate_controller_publications(conn)
        live = db.get_published_controller_mappings()[0]
        self.assertEqual(before['mapping_json'], live['mapping_json'])
        self.assertEqual(live['device_name'], 'Original')

    def test_draft_save_keeps_published_document_and_image(self):
        draft = self.save()
        live = db.get_published_controller_mappings()[0]
        self.assertEqual(draft['status'], 'published')
        self.assertTrue(draft['has_draft'])
        self.assertEqual(live['image_filename'], 'original.jpg')
        self.assertEqual(json.loads(live['mapping_json'])['image'], 'original')
        self.assertEqual(json.loads(draft['mapping_json'])['image'], 'new-image')

    def test_aliases_survive_old_single_id_client(self):
        draft = self.save(document(ids=['TEST0001']))
        self.assertEqual(json.loads(draft['mapping_json'])['device_ids'], ['TEST0001', 'TEST0002'])

    def test_publish_only_the_reviewed_revision(self):
        draft = self.save()
        with self.assertRaises(db.MappingConflict):
            db.set_controller_publication(1, 'published', 'old', 'admin')
        db.set_controller_publication(1, 'published', draft['updated_at'], 'admin')
        self.assertEqual(db.get_published_controller_mappings()[0]['device_name'], 'Edited')
        self.assertFalse(db.get_controller_mapping(1)['has_draft'])

    def test_new_admin_draft_is_not_public(self):
        row = db.save_controller_draft('NEW1', 'New', document(ids=['NEW1']), 'admin')
        self.assertEqual(row['status'], 'draft')
        self.assertIsNone(row['published_snapshot'])
        self.assertEqual(len(db.get_published_controller_mappings()), 1)

    def test_two_concurrent_saves_only_one_wins(self):
        gate = threading.Barrier(2)

        def attempt():
            gate.wait()
            try:
                self.save()
                return 'saved'
            except db.MappingConflict:
                return 'conflict'
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: attempt(), range(2)))
        self.assertCountEqual(results, ['saved', 'conflict'])
        self.assertEqual(len(db.list_mapping_versions(1)), 2)

    def test_history_failure_rolls_back_draft(self):
        with patch.object(db, '_record_mapping_version', side_effect=sqlite3.OperationalError('full')):
            with self.assertRaises(sqlite3.OperationalError):
                self.save()
        self.assertEqual(db.get_controller_mapping(1)['updated_at'], 'old')
        self.assertEqual(db.get_controller_mapping(1)['device_name'], 'Original')

    def test_existing_alias_cannot_be_claimed_by_new_mapping(self):
        with self.assertRaises(db.MappingConflict):
            db.save_controller_draft('TEST0002', 'Duplicate', document(ids=['TEST0002']), 'mapper')
        self.assertEqual(len(db.get_all_controller_mappings()), 1)

    def test_deleted_mapping_is_not_recreated_by_stale_editor(self):
        db.delete_controller_mapping(1)
        with self.assertRaises(db.MappingConflict):
            self.save()

    def test_unpublish_is_explicit(self):
        db.set_controller_publication(1, 'draft', 'old', 'admin')
        self.assertEqual(db.get_published_controller_mappings(), [])
        self.assertIsNotNone(db.get_controller_mapping(1)['published_snapshot'])

    def test_full_database_initialization_and_seed_publication(self):
        # The backup module imports the web app; stub only its unrelated table setup.
        backup = types.ModuleType('admin.backup')
        backup.init_backup_tables = lambda conn: None
        with patch.dict(sys.modules, {'admin.backup': backup}):
            db.init_db(Path(self.temp.name) / 'fresh.db')
            mid = db.create_controller_mapping('SEED1', 'Seed', 'original', 'original.jpg',
                                               4400, 2560, json.dumps(document(ids=['SEED1'])))
            before = db.get_controller_mapping(mid)['published_snapshot']
            db.init_db(db.DB_PATH)
        self.assertEqual(db.get_controller_mapping(mid)['published_snapshot'], before)
        self.assertEqual(db.get_published_controller_mappings()[0]['device_id'], 'SEED1')

    def test_history_pruning_never_removes_public_revision(self):
        base = 'old'
        for index in range(22):
            row = self.save(document(f'revision-{index}'), base)
            base = row['updated_at']
        self.assertEqual(len(db.list_mapping_versions(1)), 20)
        self.assertEqual(db.get_published_controller_mappings()[0]['image_filename'], 'original.jpg')

    def test_valid_document(self):
        validation.validate_mapping(document())

    def test_bad_shapes_and_nonfinite_coordinates_rejected(self):
        for field, value in [('width', 0), ('height', float('nan')), ('device_ids', 'TEST'),
                             ('boxes', {}), ('image', '../outside')]:
            data = document()
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validation.validate_mapping(data)
        data = copy.deepcopy(document())
        data['boxes'][0]['box_xy'] = [float('inf'), 0]
        with self.assertRaises(ValueError):
            validation.validate_mapping(data)


class TemplateSafetyTests(unittest.TestCase):
    def setUp(self):
        try:
            import jinja2
        except ImportError:
            self.skipTest('Jinja2 is not installed')
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(ROOT / 'www/admin/templates'),
                                     autoescape=True)
        self.env.globals.update(url_for=lambda endpoint, **kw: '/' + endpoint,
                                get_flashed_messages=lambda **kw: [],
                                request=types.SimpleNamespace(endpoint='admin.controllers'))

    def test_editor_bootstrap_escapes_script_terminator(self):
        row = {'mapping_json': json.dumps({'title': '</script><script>bad()</script>'})}
        rendered = self.env.get_template('admin/mapping_editor.html').render(
            existing_json=json.dumps(row), editor_user='mapper', draft_note='')
        self.assertNotIn('</script><script>bad()', rendered)
        self.assertIn('const EXISTING = JSON.parse(', rendered)
        self.assertIn('Save draft', rendered)

    def test_public_controller_with_pending_draft_has_explicit_publish(self):
        mapping = {'id': 1, 'device_id': 'TEST0001', 'device_ids': ['TEST0001', 'TEST0002'],
                   'device_name': 'Test', 'image': 'original', 'box_count': 1,
                   'status': 'published', 'has_draft': 1, 'updated_at': 'base-1'}
        rendered = self.env.get_template('admin/controllers.html').render(
            mappings=[mapping], unknown=[], legacy=[], audit=[], role='admin')
        self.assertIn('Publish draft', rendered)
        self.assertIn('unpublished changes', rendered)
        self.assertIn('name="base_updated_at" value="base-1"', rendered)

    def test_mapper_cannot_see_publish_action(self):
        rendered = self.env.get_template('admin/controllers.html').render(
            mappings=[{'id': 1, 'device_id': 'TEST', 'status': 'published', 'has_draft': 1}],
            unknown=[], legacy=[], audit=[], role='mapper')
        self.assertNotIn('>Publish draft<', rendered)

    def test_drafts_lead_and_unknown_matches_require_selection(self):
        rendered = self.env.get_template('admin/controllers.html').render(
            mappings=[{'id': 1, 'device_name': 'Published example', 'status': 'published'},
                      {'id': 2, 'device_name': 'Draft example', 'status': 'draft'}],
            unknown=[{'device_id': 'UNKNOWN'}], legacy=[], audit=[], role='mapper')
        self.assertLess(rendered.index('Draft example'), rendered.index('Published example'))
        self.assertLess(rendered.index('Controller mappings'), rendered.index('id="unknown-devices"'))
        self.assertIn('<details class="card" id="unknown-devices">', rendered)
        self.assertIn('<option value="" selected disabled>Choose a verified match...</option>', rendered)
        self.assertIn('name="mapping_id" required', rendered)


if __name__ == '__main__':
    unittest.main()
