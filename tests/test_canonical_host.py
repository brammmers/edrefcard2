"""Redirects from the site's former names: inactive by default, path kept."""
import os
import unittest
from unittest.mock import patch

from flask import Flask

import canonical_host

ACTIVE = {
    'CANONICAL_URL': 'https://edrefcard.info/',
    'REDIRECT_HOSTS': 'beta.edrefcard.info, WWW.edrefcard.info,edrefcard2.l0l.fr',
}


def make_app():
    app = Flask(__name__)
    canonical_host.register(app)

    @app.route('/binds/<run_id>')
    def binds(run_id):
        return f'binds {run_id}'

    return app


class CanonicalHostTests(unittest.TestCase):
    def test_inactive_without_settings(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('CANONICAL_URL', None)
            os.environ.pop('REDIRECT_HOSTS', None)
            client = make_app().test_client()
            response = client.get('/binds/abcdef', base_url='https://beta.edrefcard.info')
            self.assertEqual(response.status_code, 200)

    def test_former_hosts_redirect_with_path_and_query(self):
        with patch.dict(os.environ, ACTIVE):
            client = make_app().test_client()
            for host in ('beta.edrefcard.info', 'www.edrefcard.info', 'edrefcard2.l0l.fr'):
                response = client.get('/binds/abcdef?x=1', base_url=f'https://{host}')
                self.assertEqual(response.status_code, 301, host)
                self.assertEqual(response.headers['Location'],
                                 'https://edrefcard.info/binds/abcdef?x=1')
            response = client.get('/binds/abcdef', base_url='http://beta.edrefcard.info:8000')
            self.assertEqual(response.headers['Location'], 'https://edrefcard.info/binds/abcdef')

    def test_canonical_and_internal_hosts_are_served(self):
        with patch.dict(os.environ, ACTIVE):
            client = make_app().test_client()
            for base in ('https://edrefcard.info', 'http://127.0.0.1:8000', 'http://localhost'):
                response = client.get('/binds/abcdef', base_url=base)
                self.assertEqual(response.status_code, 200, base)


if __name__ == '__main__':
    unittest.main()
