"""Permanent redirects from the site's former names to its canonical URL.

Active only when both variables are set (production after the move to
edrefcard.info):

    CANONICAL_URL=https://edrefcard.info
    REDIRECT_HOSTS=beta.edrefcard.info,www.edrefcard.info,edrefcard2.l0l.fr

A request whose Host is in REDIRECT_HOSTS gets a 301 to the same path and
query on CANONICAL_URL, so a /binds/<id> link printed on an old card or PDF
still leads to that card. Every other host (the canonical one, localhost
health checks, the container's own address) is served normally.
"""
import os

from flask import Flask, redirect, request


def _settings():
    target = os.environ.get('CANONICAL_URL', '').strip().rstrip('/')
    hosts = {h.strip().lower() for h in os.environ.get('REDIRECT_HOSTS', '').split(',')
             if h.strip()}
    if not target or not hosts:
        return None, set()
    return target, hosts


def register(app: Flask) -> None:
    target, hosts = _settings()
    if not target:
        return

    @app.before_request
    def _redirect_former_hosts():
        host = request.host.split(':', 1)[0].lower()
        if host not in hosts:
            return None
        location = target + request.full_path
        if not request.query_string:
            location = location.rstrip('?')
        return redirect(location, code=301)
