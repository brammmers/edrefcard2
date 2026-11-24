"""A named account (mapper or admin) changes its own password at /admin/account/password."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

WWW = Path(__file__).resolve().parents[1] / 'www'
APP_DEPENDENCIES = ('flask', 'flask_limiter', 'werkzeug')

# The app is imported in a child process: importing it initializes a database
# and rewires Config for the whole interpreter.
PROBE = textwrap.dedent('''
    import json, os, sys, types
    try:
        import wand.image  # noqa: F401
    except ImportError:
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
    from werkzeug.security import check_password_hash, generate_password_hash

    origin = {'Origin': 'http://localhost'}
    database.create_user('mapper2', generate_password_hash('first-password'), 'mapper')
    def hash_ok(password):
        return check_password_hash(database.get_user_by_username('mapper2')['password_hash'], password)
    def login(client, password, name='mapper2'):
        return client.post('/admin/login', headers=origin,
                           data={'username': name, 'password': password}).status_code
    def change(client, current, new, confirm=None):
        r = client.post('/admin/account/password', headers=origin, data={
            'current_password': current, 'new_password': new,
            'confirm_password': new if confirm is None else confirm})
        return [r.status_code, r.get_data(as_text=True)]

    out = {}
    anonymous = appmod.app.test_client()
    out['anonymous'] = anonymous.get('/admin/account/password').status_code

    here, elsewhere = appmod.app.test_client(), appmod.app.test_client()
    login(here, 'first-password')
    login(elsewhere, 'first-password')
    page = here.get('/admin/account/password')
    out['page'] = [page.status_code, 'Change my password' in page.get_data(as_text=True)]

    status, body = change(here, 'wrong-password', 'second-password')
    out['wrong_current'] = [status, 'current password is incorrect' in body, hash_ok('first-password')]
    status, body = change(here, 'first-password', 'second-password', 'other-password')
    out['mismatch'] = [status, 'do not match' in body, hash_ok('first-password')]
    status, body = change(here, 'first-password', 'short')
    out['too_short'] = [status, 'at least 8' in body, hash_ok('first-password')]
    status, body = change(here, 'first-password', 'first-password')
    out['same'] = [status, 'same as the current' in body, hash_ok('first-password')]

    status, _ = change(here, 'first-password', 'second-password')
    out['changed'] = [status, hash_ok('second-password')]
    out['stays_signed_in'] = here.get('/admin/controllers').status_code
    out['other_session'] = elsewhere.get('/admin/controllers').status_code
    out['old_login'] = login(appmod.app.test_client(), 'first-password')
    fresh = appmod.app.test_client()
    login(fresh, 'second-password')
    out['new_login'] = fresh.get('/admin/controllers').status_code

    env_admin = appmod.app.test_client()
    login(env_admin, 'probe-password', name='admin')
    page = env_admin.get('/admin/account/password').get_data(as_text=True)
    status, body = change(env_admin, 'probe-password', 'another-password')
    out['env_admin'] = ['configured on the server' in page, 'Change my password' in page,
                        'configured on the server' in body]
    print('PROBE=' + json.dumps(out))
''')


@unittest.skipUnless(all(importlib.util.find_spec(name) for name in APP_DEPENDENCIES),
                     'application dependencies required')
class AccountPasswordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='edrefcard-password-', ignore_cleanup_errors=True)
        env = {**os.environ, 'EDREFCARD_CONFIGS_DIR': cls.temp.name,
               'EDREFCARD_ADMIN_USER': 'admin', 'EDREFCARD_ADMIN_PASS': 'probe-password',
               'APP_ENV': 'development', 'APP_URL': ''}
        for name in ('ACCESS_TOKEN', 'TRUSTED_PROXY_HOPS', 'RATELIMIT_STORAGE_URI'):
            env.pop(name, None)
        completed = subprocess.run([sys.executable, '-c', PROBE, str(WWW)],
                                   capture_output=True, text=True, env=env, timeout=120)
        lines = [line for line in completed.stdout.splitlines() if line.startswith('PROBE=')]
        if not lines:
            raise AssertionError(f'probe failed:\n{completed.stdout}\n{completed.stderr}')
        cls.out = json.loads(lines[-1][len('PROBE='):])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_page_needs_a_signed_in_account(self):
        self.assertEqual(self.out['anonymous'], 302)
        self.assertEqual(self.out['page'], [200, True])

    def test_bad_input_leaves_the_password_unchanged(self):
        for key in ('wrong_current', 'mismatch', 'too_short', 'same'):
            self.assertEqual(self.out[key], [200, True, True], key)

    def test_change_keeps_this_session_and_ends_the_others(self):
        self.assertEqual(self.out['changed'], [302, True])
        self.assertEqual(self.out['stays_signed_in'], 200)
        self.assertEqual(self.out['other_session'], 302)
        self.assertEqual(self.out['old_login'], 200)  # the form is shown again, no redirect
        self.assertEqual(self.out['new_login'], 200)

    def test_environment_admin_cannot_change_it_here(self):
        self.assertEqual(self.out['env_admin'], [True, False, True])


if __name__ == '__main__':
    unittest.main()
