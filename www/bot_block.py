"""Refuse crawlers that ignore robots.txt, by User-Agent.

On the original server, CorsairBot (anonymous, run from rented Google Cloud
machines, no contact address) made 26% of all requests in two weekly passes,
never read robots.txt and fetched thousands of card pages and raw .binds
files. Here every card opened for the first time is drawn, so such a crawler
costs real work.

BLOCKED_USER_AGENTS is a comma-separated list of case-insensitive substrings
of the User-Agent header; matching requests get a plain 403. Default:
"CorsairBot". Set it to an empty value to block nothing.
"""
import os

from flask import Flask, Response, request

DEFAULT_BLOCKED = 'CorsairBot'


def _patterns() -> tuple[str, ...]:
    raw = os.environ.get('BLOCKED_USER_AGENTS', DEFAULT_BLOCKED)
    return tuple(p.strip().lower() for p in raw.split(',') if p.strip())


def register(app: Flask) -> None:
    patterns = _patterns()
    if not patterns:
        return

    @app.before_request
    def _refuse_blocked_crawlers():
        agent = (request.headers.get('User-Agent') or '').lower()
        if agent and any(p in agent for p in patterns):
            return Response('Forbidden\n', status=403, mimetype='text/plain')
        return None
