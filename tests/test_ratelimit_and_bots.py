"""Rate-limit counters shared across processes, and the crawler block list."""
import multiprocessing
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import bot_block
from ratelimit_storage import SQLiteStorage, storage_uri


def _hit_many(uri, n, queue):
    storage = SQLiteStorage(uri)
    last = 0
    for _ in range(n):
        last = storage.incr('LIMITER/k', 60)
    queue.put(last)


class SQLiteStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)  # Windows keeps open SQLite files locked
        self.uri = 'sqlite:///' + str(Path(self.tmp.name) / 'rl.db').replace('\\', '/')

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_is_memory_without_variable(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('RATELIMIT_STORAGE_URI', None)
            self.assertEqual(storage_uri(), 'memory://')

    def test_counts_and_expires(self):
        storage = SQLiteStorage(self.uri)
        self.assertEqual(storage.incr('a', 60), 1)
        self.assertEqual(storage.incr('a', 60, amount=2), 3)
        self.assertEqual(storage.get('a'), 3)
        self.assertGreater(storage.get_expiry('a'), time.time())
        self.assertEqual(storage.incr('b', 0.2), 1)
        time.sleep(0.3)
        self.assertEqual(storage.get('b'), 0)
        self.assertEqual(storage.incr('b', 60), 1)  # a new window starts at 1
        storage.clear('a')
        self.assertEqual(storage.get('a'), 0)
        self.assertTrue(storage.check())
        storage.reset()
        self.assertEqual(storage.get('b'), 0)

    def test_counters_are_shared_between_processes(self):
        queue = multiprocessing.get_context('spawn').Queue()
        ctx = multiprocessing.get_context('spawn')
        procs = [ctx.Process(target=_hit_many, args=(self.uri, 25, queue)) for _ in range(4)]
        for p in procs:
            p.start()
        for p in procs:
            p.join(60)
        self.assertEqual(SQLiteStorage(self.uri).get('LIMITER/k'), 100)

    def test_flask_limiter_uses_it(self):
        app = Flask(__name__)
        limiter = Limiter(key_func=get_remote_address, storage_uri=self.uri,
                          strategy='fixed-window', app=app)

        @app.route('/x')
        @limiter.limit('3 per minute')
        def x():
            return 'ok'

        client = app.test_client()
        self.assertEqual([client.get('/x').status_code for _ in range(4)], [200, 200, 200, 429])
        # A second app on the same file (another worker) sees the same counter.
        app2 = Flask(__name__)
        limiter2 = Limiter(key_func=get_remote_address, storage_uri=self.uri,
                           strategy='fixed-window', app=app2)

        @app2.route('/x', endpoint='x')  # same endpoint, same key, as in another worker
        @limiter2.limit('3 per minute')
        def x2():
            return 'ok'

        self.assertEqual(app2.test_client().get('/x').status_code, 429)


def make_app():
    app = Flask(__name__)
    bot_block.register(app)

    @app.route('/binds/<run_id>')
    def binds(run_id):
        return run_id

    return app


class BotBlockTests(unittest.TestCase):
    CORSAIR = 'CorsairBot/1.0 (CorsairBot for web indexing)'
    BROWSER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/157.0 Safari/537.36'

    def test_default_blocks_corsairbot_only(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('BLOCKED_USER_AGENTS', None)
            client = make_app().test_client()
            self.assertEqual(client.get('/binds/abc', headers={'User-Agent': self.CORSAIR}).status_code, 403)
            self.assertEqual(client.get('/binds/abc', headers={'User-Agent': self.BROWSER}).status_code, 200)
            self.assertEqual(client.get('/binds/abc', headers={'User-Agent': ''}).status_code, 200)

    def test_list_is_configurable_and_can_be_emptied(self):
        with patch.dict(os.environ, {'BLOCKED_USER_AGENTS': 'badbot, Other'}):
            client = make_app().test_client()
            self.assertEqual(client.get('/binds/a', headers={'User-Agent': 'x BadBot/2'}).status_code, 403)
            self.assertEqual(client.get('/binds/a', headers={'User-Agent': self.CORSAIR}).status_code, 200)
        with patch.dict(os.environ, {'BLOCKED_USER_AGENTS': ''}):
            client = make_app().test_client()
            self.assertEqual(client.get('/binds/a', headers={'User-Agent': self.CORSAIR}).status_code, 200)


if __name__ == '__main__':
    unittest.main()
