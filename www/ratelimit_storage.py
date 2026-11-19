"""Rate-limit counters shared by every gunicorn worker, in a small SQLite file.

Flask-Limiter's default ``memory://`` storage lives inside each worker process,
so with 4 workers a limit of "60 per minute" really allowed about 240 requests
a minute from one address: enough for a scraper to keep every worker busy
drawing cards. This storage keeps the fixed-window counters in one SQLite file
that all the workers of the container open, so a limit means what it says.

Enabled by ``RATELIMIT_STORAGE_URI=sqlite:////tmp/edrefcard-ratelimit.db`` (set
in the Dockerfile). The file holds only counters that expire within the hour,
so a path outside the data volume is fine: it is not backed up and starts empty
with each container. Without the variable (local development, tests) the
limiter keeps ``memory://``.

Only the fixed-window strategy used by the app is implemented.
"""
from __future__ import annotations

import os
import random
import sqlite3
import threading
import time

from limits.storage import Storage

DEFAULT_URI = 'memory://'


def storage_uri() -> str:
    return os.environ.get('RATELIMIT_STORAGE_URI', '').strip() or DEFAULT_URI


class SQLiteStorage(Storage):
    """Fixed-window counters in a SQLite file, safe across processes."""

    STORAGE_SCHEME = ['sqlite']

    def __init__(self, uri: str | None = None, wrap_exceptions: bool = False, **options):
        uri = uri or 'sqlite:///:memory:'
        if not uri.startswith('sqlite:///'):
            raise ValueError(f'Expected sqlite:///<path>, got {uri!r}')
        # sqlite:////tmp/x.db -> /tmp/x.db ; sqlite:///x.db -> x.db (relative)
        self.path = uri[len('sqlite:///'):]
        self._local = threading.local()
        # The file is opened on the first counted request, not here: a `flask`
        # command run as root with docker exec must not create it as root,
        # or the workers (appuser) could no longer write to it.
        super().__init__(uri, wrap_exceptions=wrap_exceptions, **options)

    @property
    def base_exceptions(self) -> type[Exception] | tuple[type[Exception], ...]:
        return sqlite3.Error

    def _connect(self) -> sqlite3.Connection:
        # One connection per thread and per process: a connection opened before
        # gunicorn forks is not reused by the children (pid check).
        conn = getattr(self._local, 'conn', None)
        if conn is not None and getattr(self._local, 'pid', None) == os.getpid():
            return conn
        conn = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=OFF')
        conn.execute(
            'CREATE TABLE IF NOT EXISTS counters ('
            ' key TEXT PRIMARY KEY, value INTEGER NOT NULL, expiry REAL NOT NULL)')
        self._local.conn = conn
        self._local.pid = os.getpid()
        return conn

    def incr(self, key: str, expiry: float, amount: int = 1) -> int:
        conn = self._connect()
        now = time.time()
        conn.execute('BEGIN IMMEDIATE')
        try:
            conn.execute('DELETE FROM counters WHERE key = ? AND expiry <= ?', (key, now))
            conn.execute(
                'INSERT INTO counters (key, value, expiry) VALUES (?, ?, ?) '
                'ON CONFLICT(key) DO UPDATE SET value = value + excluded.value',
                (key, amount, now + expiry))
            value = conn.execute('SELECT value FROM counters WHERE key = ?', (key,)).fetchone()[0]
            if random.random() < 0.01:
                conn.execute('DELETE FROM counters WHERE expiry <= ?', (now,))
            conn.execute('COMMIT')
        except BaseException:
            conn.execute('ROLLBACK')
            raise
        return int(value)

    def get(self, key: str) -> int:
        row = self._connect().execute(
            'SELECT value FROM counters WHERE key = ? AND expiry > ?', (key, time.time())).fetchone()
        return int(row[0]) if row else 0

    def get_expiry(self, key: str) -> float:
        row = self._connect().execute(
            'SELECT expiry FROM counters WHERE key = ? AND expiry > ?', (key, time.time())).fetchone()
        return float(row[0]) if row else time.time()

    def check(self) -> bool:
        try:
            self._connect().execute('SELECT 1')
            return True
        except sqlite3.Error:
            return False

    def reset(self) -> int | None:
        return self._connect().execute('DELETE FROM counters').rowcount

    def clear(self, key: str) -> None:
        self._connect().execute('DELETE FROM counters WHERE key = ?', (key,))
