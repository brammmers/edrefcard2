"""Regressions found by the 2026-11 code review.

1. Deleting one config removed the whole two-character prefix directory.
2. Error pages reflected the URL as raw HTML (XSS).
3. Behind the reverse proxy every visitor shared one rate-limit bucket and
   request.is_secure was False (no HSTS, http:// links).
4. Hand-written display-group lists drifted from the parser's names.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

from scripts.models import Config

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / 'www'


class OwnedFilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='edrefcard-owned-')
        self.saved = Config._configs_path
        Config.setConfigsPath(self.temp.name)
        self.folder = Path(self.temp.name).resolve() / 'cu'
        self.folder.mkdir()
        for name in ('custom-4-2.binds', 'custom-4-2-t16000m.jpg', 'custom-4-2-A4.pdf',
                     'custom-4-2-abc.binds', 'custom-4-2-abc-t16000m.jpg', 'custom-4-2-abc-A4.pdf',
                     'cuxx.binds', 'cuxx-keyboard.jpg'):
            (self.folder / name).write_text('x')

    def tearDown(self):
        Config._configs_path = self.saved
        self.temp.cleanup()

    def names(self, config_id, other_ids=()):
        return sorted(p.name for p in Config(config_id).ownedFiles(other_ids))

    def test_owner_gets_its_files_and_not_those_of_a_longer_sibling_id(self):
        self.assertEqual(self.names('custom-4-2'),
                         ['custom-4-2-A4.pdf', 'custom-4-2-t16000m.jpg', 'custom-4-2.binds'])

    def test_suffixed_sibling_only_gets_its_own_files(self):
        self.assertEqual(self.names('custom-4-2-abc'),
                         ['custom-4-2-abc-A4.pdf', 'custom-4-2-abc-t16000m.jpg', 'custom-4-2-abc.binds'])

    def test_database_ids_protect_siblings_whose_source_is_missing(self):
        (self.folder / 'custom-4-2-abc.binds').unlink()
        self.assertNotIn('custom-4-2-abc-t16000m.jpg', self.names('custom-4-2', {'custom-4-2-abc'}))

    def test_unknown_config_owns_nothing(self):
        self.assertEqual(self.names('zz-missing'), [])

    def test_only_generated_ids_are_valid_names(self):
        for name in ('custom-4-2-abc', 'abcdef', 'My_Config1'):
            self.assertTrue(Config.isValidName(name), name)
        for name in ('', '..', '../x', 'a/b', 'a*', '<img src=x onerror=alert(1)>', 'a b', None):
            self.assertFalse(Config.isValidName(name), name)


class DisplayGroupTests(unittest.TestCase):
    def test_every_control_group_can_be_displayed(self):
        from scripts.controlsData import controls
        from scripts.parser import ALL_DISPLAY_GROUPS
        used = {control['Group'] for control in controls.values()}
        self.assertEqual(used - set(ALL_DISPLAY_GROUPS), set())

    def test_no_hand_written_group_list_outside_the_parser(self):
        for name in ('api.py', 'admin/__init__.py'):
            source = (WWW / name).read_text(encoding='utf-8')
            self.assertIn('ALL_DISPLAY_GROUPS', source, name)
            self.assertNotIn("'On Foot'", source, name)


# The Flask app is imported in a child process: importing it initializes a
# database and rewires Config for the whole interpreter.
APP_PROBE = textwrap.dedent('''
    import base64, json, os, sys, types
    try:
        import wand.image  # noqa: F401
    except ImportError:
        # ImageMagick absent (developer machine): these checks never render.
        for name in ('wand', 'wand.image', 'wand.drawing', 'wand.color', 'wand.font'):
            module = types.ModuleType(name)
            sys.modules[name] = module
            for attr in ('Image', 'Drawing', 'Color', 'Font'):
                setattr(module, attr, type(attr, (), {'__init__': lambda self, *a, **k: None}))
    www = sys.argv[1]
    sys.path.insert(0, www)
    os.chdir(www)
    import app as appmod
    from scripts import database
    from scripts.models import Config
    from flask import request, url_for
    from flask_limiter.util import get_remote_address

    @appmod.app.route('/__probe')  # routes must exist before the first request
    def probe():
        return json.dumps([get_remote_address(), request.is_secure,
                           url_for('web.show_binds', run_id='x', _external=True)])

    client = appmod.app.test_client()
    out = {}

    payload = '<img src=x onerror=alert(1)>'
    for key, url in (('binds', '/binds/%3Cimg%20src=x%20onerror=alert(1)%3E'),
                     ('device', '/device/%3Cimg%20src=x%20onerror=alert(1)%3E'),
                     ('pdf', '/download/%3Cimg%20src=x%20onerror=alert(1)%3E/pdf'),
                     ('glob', '/download/cu*/pdf'),
                     ('unknown', '/binds/does-not-exist')):
        response = client.get(url)
        out[key] = [response.status_code, payload in response.get_data(as_text=True)]

    for name in ('custom-aaa', 'custom-bbb', 'cuxx'):
        config = Config(name)
        config.makeDir()
        config.pathWithSuffix('.binds').write_text('<Root/>')
        config.pathWithNameAndSuffix('card', '.jpg').write_text('x')
        database.create_configuration(config_id=name, description=name)
    headers = {'Authorization': 'Basic ' + base64.b64encode(b'admin:probe-password').decode(),
               'Origin': 'http://localhost'}
    out['delete_status'] = client.post('/admin/configs/custom-aaa/delete', headers=headers).status_code
    out['remaining_files'] = sorted(p.name for p in Config('cuxx').path().parent.iterdir())
    out['remaining_rows'] = sorted(database.get_all_config_ids())
    out['traversal_status'] = client.post('/admin/configs/../delete', headers=headers).status_code
    out['configs_dir_alive'] = Config.configsPath().is_dir()

    response = client.get('/__probe', environ_base={'REMOTE_ADDR': '172.18.0.5'},
                          headers={'X-Forwarded-For': '203.0.113.9',
                                   'X-Forwarded-Proto': 'https', 'Host': 'cards.example'})
    out['proxy'] = json.loads(response.get_data(as_text=True))
    out['hsts'] = 'Strict-Transport-Security' in response.headers

    # --- unique ids: same filename uploaded again and again
    first = Config.claimUnique('custom-4-2')
    claimed = [Config.claimUnique('custom-4-2').name for _ in range(40)]
    out['unique'] = [first.name, len(set(claimed + [first.name])),
                     all(Config.isValidName(name) for name in claimed),
                     Config.claimUnique('reserved', is_taken=lambda name: name == 'reserved').name != 'reserved']

    # --- a PDF only holds the pages of its own config
    try:
        import fitz
        from PIL import Image
        for name in ('pdfcard', 'pdfcard-abc'):
            config = Config(name)
            config.makeDir()
            config.pathWithSuffix('.binds').write_text('<Root/>')
            Image.new('RGB', (600, 400), 'red').save(config.pathWithNameAndSuffix('device', '.jpg'))
        response = client.get('/download/pdfcard/pdf')
        with fitz.open(stream=response.get_data(), filetype='pdf') as pdf:
            out['pdf_pages'] = len(pdf)
        response.close()
    except ImportError:
        out['pdf_pages'] = None

    # --- sessions follow the user table
    from werkzeug.security import generate_password_hash
    origin = {'Origin': 'http://localhost'}
    user_id = database.create_user('mapper1', generate_password_hash('first-password'), 'mapper')
    mapper = appmod.app.test_client()
    steps = [mapper.post('/admin/login', headers=origin,
                         data={'username': 'mapper1', 'password': 'first-password'}).status_code,
             mapper.get('/admin/controllers').status_code]
    database.update_user_password(user_id, generate_password_hash('second-password'))
    steps.append(mapper.get('/admin/controllers').status_code)
    mapper.post('/admin/login', headers=origin, data={'username': 'mapper1', 'password': 'second-password'})
    steps.append(mapper.get('/admin/controllers').status_code)
    database.delete_user(user_id)
    steps.append(mapper.get('/admin/controllers').status_code)
    out['session'] = steps
    out['login_redirect'] = client.post(
        '/admin/login?next=/%5Cevil.example', headers=origin,
        data={'username': 'admin', 'password': 'probe-password'}).headers.get('Location')

    # --- backups: rotation only touches scheduled backups, settings keep their status
    import time
    from admin import backup as bk
    settings = {'sftp_enabled': False, 'sftp_host': 'sftp.example', 'sftp_port': 22}
    bk.save_backup_settings(settings)
    manager = bk.BackupManager()
    made = {}
    for index, kind in enumerate(('manual', 'pre_restore', 'scheduled', 'scheduled')):
        path = manager.create_backup(backup_type=kind)
        stamp = time.time() - 1000 + index * 100
        os.utime(path, (stamp, stamp))
        made.setdefault(kind, []).append(path)
    deleted = manager.cleanup_old_backups(keep_count=1)
    out['retention'] = [deleted, made['manual'][0].exists(), made['pre_restore'][0].exists(),
                        made['scheduled'][0].exists(), made['scheduled'][1].exists()]
    bk.save_backup_settings(settings)
    out['last_backup_kept'] = bool(bk.get_backup_settings().get('last_backup_at'))

    # --- SFTP: host key pinned on first use, filenames validated before any connection
    def refused(call):
        try:
            call()
        except ValueError:
            return True
        return False
    pinned = bk.SFTPManager('sftp.example', 22, 'u', 'p', '/d', pin_host_key=True)
    pinned._verify_host_key('SHA256:first')
    adhoc = bk.SFTPManager('other.example', 22, 'u', 'p', '/d')
    adhoc._verify_host_key('SHA256:whatever')
    out['sftp'] = [bk.get_pinned_sftp_host_key('SFTP.example', 22),
                   refused(lambda: pinned._verify_host_key('SHA256:second')),
                   refused(lambda: pinned._verify_host_key('SHA256:first')),
                   bk.get_pinned_sftp_host_key('other.example', 22),
                   refused(lambda: pinned.download_backup('../backup_x.tar.gz')),
                   refused(lambda: pinned.download_backup('notes.txt'))]
    bk.forget_sftp_host_key('sftp.example', 22)
    out['sftp'].append(bk.get_pinned_sftp_host_key('sftp.example', 22))

    # --- mapping editor: checks endpoint, preview picker, publication gate
    def gate_mapping(code):
        return {'title': 'Gate', 'image': 'gate', 'width': 2200, 'height': 1280, 'device_ids': ['GATE0001'],
                'boxes': [{'label': 'A', 'box_xy': [100, 100], 'box_wh': [600, 190],
                           'button_xy': [900, 400], 'rows': [{'joy': code}]}]}
    issues = client.post('/admin/mapping-editor/lint', headers=headers,
                         json={'mapping': gate_mapping('joy_1')}).get_json()['issues']
    out['lint'] = [[issue['level'], issue['box']] for issue in issues]
    for name, with_source in (('gatecard-one', True), ('gatecard-two', False)):
        if with_source:
            config = Config(name)
            config.makeDir()
            config.pathWithSuffix('.binds').write_text('<Root/>')
        database.create_configuration(config_id=name, description=name, devices={'GATE0001::0': None})
    out['references'] = [reference['id'] for reference in client.get(
        '/admin/mapping-editor/references?devices=gate0001', headers=headers).get_json()['references']]

    def publish(row):
        client.post('/admin/controllers/publish', headers=headers, data={
            'mapping_id': row['id'], 'state': 'published', 'base_updated_at': row['updated_at']})
        return database.get_controller_mapping(row['id'])['status']
    draft = database.save_controller_draft('GATE0001', 'Gate', gate_mapping('joy_1'), 'probe')
    out['gate'] = [publish(draft)]
    fixed = database.save_controller_draft('GATE0001', 'Gate', gate_mapping('Joy_1'), 'probe',
                                           draft['updated_at'], draft['id'])
    out['gate'].append(publish(fixed))

    # --- review page: nothing to compare before a first publication, then the draft's changes
    compare_url = '/admin/controllers/compare/%d' % draft['id']
    live = database.get_controller_mapping(draft['id'])
    moved = gate_mapping('Joy_1')
    moved['boxes'][0]['box_xy'] = [300, 500]
    moved['boxes'].append({'label': 'B', 'box_xy': [100, 800], 'box_wh': [600, 190],
                           'button_xy': [900, 900], 'rows': [{'joy': 'Joy_2'}]})
    database.save_controller_draft('GATE0001', 'Gate', moved, 'probe', live['updated_at'], live['id'])
    page = client.get(compare_url, headers=headers)
    text = page.get_data(as_text=True)
    out['compare'] = [client.get('/admin/controllers/compare/999999', headers=headers).status_code,
                      page.status_code, 'Box &#34;A&#34;: moved' in text, 'Box added: &#34;B&#34;' in text]

    # --- render cache: a card is drawn once, then again only when a dependency changes
    import web
    from scripts import supportedDevices
    legacy_key = next(key for key in supportedDevices if key != 'Keyboard')
    draws = []

    def fake_legacy(physical_keys, modifiers, devices, config, public, styling, warnings,
                    skip_device_keys=()):
        image = config.pathWithNameAndSuffix('fake', '.jpg')
        draws.append(image.exists())  # an old image left on disk would be kept
        image.write_text('x')
        return [legacy_key + '::0'], []
    web.generate_legacy_images = fake_legacy
    web.render_data_driven = lambda *args, **kwargs: ([], set())
    card = Config('cachecard')
    card.makeDir()
    binds = ('<Root PresetName="Custom"><PrimaryFire><Primary Device="CACHE001" Key="Joy_1"/>'
             '</PrimaryFire>%s</Root>')
    card.pathWithSuffix('.binds').write_text(binds % '', encoding='utf-8')
    database.create_configuration(config_id='cachecard', description='cache', display_groups=['Ship'])

    def view():
        response = client.get('/binds/cachecard')
        return [response.status_code, len(draws), 'cachecard-' in response.get_data(as_text=True)]
    cache_steps = [view(), view()]
    database.attach_legacy_device_alias('CACHE999', legacy_key, 'probe')
    cache_steps.append(view())                       # shared dependency changed
    cache_steps.append(view())
    card.pathWithNameAndSuffix('fake', '.jpg').unlink()
    cache_steps.append(view())                       # an image was cleaned up
    card.pathWithSuffix('.binds').write_text(binds % '<!-- edited -->', encoding='utf-8')
    cache_steps.append(view())                       # the source changed
    out['cache'] = cache_steps
    out['stale_images_left'] = draws

    # --- scheduler tick follows the settings without a restart
    import datetime as dt
    ticks = []
    bk.run_scheduled_backup = lambda: ticks.append('run')
    base = {'sftp_enabled': False, 'sftp_host': '', 'auto_backup_enabled': True, 'backup_schedule_hour': 4}

    def at(hour):
        return dt.datetime(2030, 1, 1, hour, 0, tzinfo=dt.UTC)
    bk.save_backup_settings(base)
    tick = [bk.run_scheduled_backup_tick(at(3)), bk.run_scheduled_backup_tick(at(4))]
    bk.save_backup_settings({**base, 'backup_schedule_hour': 9})
    tick += [bk.run_scheduled_backup_tick(at(4)), bk.run_scheduled_backup_tick(at(9))]
    bk.save_backup_settings({**base, 'auto_backup_enabled': False, 'backup_schedule_hour': 9})
    tick.append(bk.run_scheduled_backup_tick(at(9)))
    # a scheduled backup was recorded moments ago (retention check above): not twice in the hour
    bk.save_backup_settings({**base, 'backup_schedule_hour': dt.datetime.now(dt.UTC).hour})
    tick.append(bk.run_scheduled_backup_tick())
    out['tick'] = tick + [len(ticks)]

    # --- editor previews are temporary
    from admin import _purge_old_previews
    preview_folder = Config('ddpreview-x').path().parent
    preview_folder.mkdir(parents=True, exist_ok=True)
    for name, age in (('ddpreview-old-card.jpg', 7200), ('ddpreview-new-card.jpg', 60), ('ddkeep.jpg', 7200)):
        (preview_folder / name).write_text('x')
        os.utime(preview_folder / name, (time.time() - age,) * 2)
    _purge_old_previews(preview_folder)
    out['previews'] = sorted(p.name for p in preview_folder.iterdir())

    # --- error.log is rotated instead of growing forever
    from scripts import utils
    log_path = Config.configsPath() / 'error.log'
    log_path.write_text('x' * (utils.ERROR_LOG_MAX_BYTES + 1))
    utils.logError('after rotation')
    out['log'] = [log_path.with_name('error.log.1').exists(), log_path.stat().st_size < 1000]

    # --- the original site's form action still works, other .py files stay hidden
    legacy_post = client.post('/scripts/bindings.py', data={'description': 'x'})
    legacy_get = client.get('/scripts/bindings.py')
    out['legacy_form'] = [legacy_post.status_code, legacy_post.headers.get('Location'),
                          legacy_get.status_code, legacy_get.headers.get('Location'),
                          client.get('/scripts/parser.py').status_code]

    # --- admin dashboard: cards per day chart, period picked from an allow-list
    pages = [client.get('/admin/?days=%s' % d, headers=headers) for d in ('30', '365', 'abc')]
    daily_part = lambda html: html.split('Cards created per month')[0]
    out['dashboard'] = [[p.status_code, daily_part(p.get_data(as_text=True)).count('class="day'),
                         'aria-current="page">%s days' % d in p.get_data(as_text=True)]
                        for p, d in zip(pages, ('30', '365', '90'))]

    print('PROBE=' + json.dumps(out))
''')

STARTUP_PROBE = textwrap.dedent('''
    import os, sys, types
    try:
        import wand.image  # noqa: F401
    except ImportError:
        for name in ('wand', 'wand.image', 'wand.drawing', 'wand.color', 'wand.font'):
            module = types.ModuleType(name)
            sys.modules[name] = module
            for attr in ('Image', 'Drawing', 'Color', 'Font'):
                setattr(module, attr, type(attr, (), {'__init__': lambda self, *a, **k: None}))
    sys.path.insert(0, sys.argv[1])
    os.chdir(sys.argv[1])
    import app  # noqa: F401
    print('STARTED')
''')

APP_DEPENDENCIES = ('flask', 'flask_limiter', 'lxml', 'paramiko', 'requests', 'cryptography')


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in APP_DEPENDENCIES),
                     'application dependencies required')
class AppRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='edrefcard-app-probe-')
        env = {**os.environ, 'EDREFCARD_CONFIGS_DIR': cls.temp.name,
               'EDREFCARD_ADMIN_USER': 'admin', 'EDREFCARD_ADMIN_PASS': 'probe-password',
               'APP_ENV': 'development', 'APP_URL': ''}
        for name in ('ACCESS_TOKEN', 'TRUSTED_PROXY_HOPS'):
            env.pop(name, None)
        completed = subprocess.run([sys.executable, '-c', APP_PROBE, str(WWW)],
                                   capture_output=True, text=True, env=env, timeout=120)
        lines = [line for line in completed.stdout.splitlines() if line.startswith('PROBE=')]
        if not lines:
            raise AssertionError(f'probe failed:\n{completed.stdout}\n{completed.stderr}')
        cls.out = json.loads(lines[-1][len('PROBE='):])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_error_pages_never_reflect_markup_and_answer_404(self):
        for key in ('binds', 'device', 'pdf', 'glob', 'unknown'):
            status, reflected = self.out[key]
            self.assertEqual(status, 404, key)
            self.assertFalse(reflected, key)

    def test_deleting_one_config_keeps_its_directory_siblings(self):
        self.assertEqual(self.out['delete_status'], 302)
        self.assertEqual(self.out['remaining_files'],
                         ['custom-bbb-card.jpg', 'custom-bbb.binds', 'cuxx-card.jpg', 'cuxx.binds'])
        self.assertEqual(self.out['remaining_rows'], ['custom-bbb', 'cuxx'])

    def test_delete_rejects_ids_that_are_not_generated_ids(self):
        self.assertIn(self.out['traversal_status'], (302, 404))
        self.assertTrue(self.out['configs_dir_alive'])

    def test_forwarded_headers_of_the_reverse_proxy_are_honoured(self):
        address, secure, url = self.out['proxy']
        self.assertEqual(address, '203.0.113.9')
        self.assertTrue(secure)
        self.assertEqual(url, 'https://cards.example/binds/x')
        self.assertTrue(self.out['hsts'])

    def test_same_filename_never_reuses_an_id(self):
        first, distinct, valid, avoided_reserved = self.out['unique']
        self.assertEqual(first, 'custom-4-2')
        self.assertEqual(distinct, 41)
        self.assertTrue(valid)
        self.assertTrue(avoided_reserved)

    def test_pdf_excludes_the_cards_of_a_longer_sibling_id(self):
        if self.out['pdf_pages'] is None:
            self.skipTest('PyMuPDF and Pillow required')
        self.assertEqual(self.out['pdf_pages'], 1)

    def test_session_ends_when_password_changes_or_user_is_deleted(self):
        # login, page, page after reset, page after new login, page after delete
        self.assertEqual(self.out['session'], [302, 200, 302, 200, 302])

    def test_login_redirect_stays_on_the_site(self):
        self.assertNotIn('evil.example', self.out['login_redirect'])

    def test_rotation_keeps_manual_and_safety_backups(self):
        self.assertEqual(self.out['retention'], [1, True, True, False, True])
        self.assertTrue(self.out['last_backup_kept'])

    def test_sftp_host_key_is_pinned_and_filenames_are_validated(self):
        pinned, changed_refused, same_refused, adhoc_pin, traversal, not_backup, forgotten = self.out['sftp']
        self.assertEqual(pinned, 'SHA256:first')
        self.assertTrue(changed_refused)
        self.assertFalse(same_refused)
        self.assertEqual(adhoc_pin, '')
        self.assertTrue(traversal)
        self.assertTrue(not_backup)
        self.assertEqual(forgotten, '')

    def test_editor_checks_endpoint_reports_blocking_errors(self):
        # the mistyped code in box 0, then "no usable input code" for the mapping
        self.assertEqual(self.out['lint'], [['error', 0], ['error', None]])

    def test_preview_picker_lists_only_cards_with_a_source_file(self):
        self.assertEqual(self.out['references'], ['gatecard-one'])

    def test_publication_is_blocked_until_errors_are_fixed(self):
        self.assertEqual(self.out['gate'], ['draft', 'published'])

    def test_review_page_lists_what_the_draft_changes(self):
        self.assertEqual(self.out['compare'], [404, 200, True, True])

    def test_card_is_drawn_once_until_a_dependency_changes(self):
        # [status, number of draws so far, page shows the card image]
        self.assertEqual(self.out['cache'], [
            [200, 1, True],   # first view draws
            [200, 1, True],   # second view is served from the cache
            [200, 2, True],   # a controller alias changed
            [200, 2, True],
            [200, 3, True],   # an image was removed from disk
            [200, 4, True],   # the .binds source changed
        ])

    def test_a_stale_render_drops_its_old_images_first(self):
        # The drawing functions keep any image already on disk: without the
        # cleanup, a new release never reached cards drawn by the previous one.
        self.assertEqual(self.out['stale_images_left'], [False, False, False, False])

    def test_scheduler_tick_follows_the_settings(self):
        # wrong hour, due, hour changed (old hour), new hour, disabled, already ran this hour
        self.assertEqual(self.out['tick'], [False, True, False, True, False, False, 2])

    def test_old_editor_previews_are_purged(self):
        self.assertEqual(self.out['previews'], ['ddkeep.jpg', 'ddpreview-new-card.jpg'])

    def test_error_log_is_rotated(self):
        self.assertEqual(self.out['log'], [True, True])

    def test_original_form_action_reposts_to_generate(self):
        post_status, post_to, get_status, get_to, python_source = self.out['legacy_form']
        self.assertEqual(post_status, 307)
        self.assertTrue(post_to.endswith('/generate'), post_to)
        self.assertEqual(get_status, 301)
        self.assertTrue(get_to.endswith('/'), get_to)
        self.assertEqual(python_source, 404)

    def test_dashboard_draws_one_bar_slot_per_day(self):
        self.assertEqual(self.out['dashboard'], [[200, 30, True], [200, 365, True], [200, 90, True]])


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in APP_DEPENDENCIES),
                     'application dependencies required')
class ProductionStartupTests(unittest.TestCase):
    def start(self, **overrides):
        with tempfile.TemporaryDirectory(prefix='edrefcard-startup-') as folder:
            env = {**os.environ, 'EDREFCARD_CONFIGS_DIR': folder, 'APP_ENV': 'production', 'APP_URL': ''}
            for name in ('ACCESS_TOKEN', 'FLASK_SECRET_KEY', 'EDREFCARD_ADMIN_PASS'):
                env.pop(name, None)
            env.update(overrides)
            return subprocess.run([sys.executable, '-c', STARTUP_PROBE, str(WWW)],
                                  capture_output=True, text=True, env=env, timeout=120)

    def test_production_refuses_placeholder_credentials(self):
        for overrides in ({},
                          {'FLASK_SECRET_KEY': 'change-this-in-production', 'EDREFCARD_ADMIN_PASS': 'a-real-password'},
                          {'FLASK_SECRET_KEY': 'a-long-private-random-key', 'EDREFCARD_ADMIN_PASS': 'changeme'}):
            completed = self.start(**overrides)
            self.assertNotEqual(completed.returncode, 0, overrides)
            self.assertIn('placeholder credentials', completed.stderr)
            self.assertNotIn('STARTED', completed.stdout)

    def test_production_starts_with_private_credentials(self):
        completed = self.start(FLASK_SECRET_KEY='a-long-private-random-key',
                               EDREFCARD_ADMIN_PASS='a-real-password')
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('STARTED', completed.stdout)


if __name__ == '__main__':
    unittest.main()
