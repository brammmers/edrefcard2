#!/usr/bin/env python3
"""
EDRefCard Admin Authentication

HTTP Basic Authentication for the admin panel.
Credentials are read from environment variables.
"""

import os
import hmac
import hashlib
import logging
from functools import wraps
from flask import request, Response, session, redirect, url_for
from scripts.models import Config


# Default credentials (override with environment variables)
ADMIN_USERNAME = os.environ.get('EDREFCARD_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('EDREFCARD_ADMIN_PASS', 'changeme')

# Configure admin access logging (use persistent configs directory)
log_dir = Config.configsPath()
# Note: mkdir should be handled by app startup, but safe to allow existing
try:
    log_dir.mkdir(parents=True, exist_ok=True)
except Exception:
    pass # Assume exists or permission issue will be caught later

log_file = log_dir / 'admin_access.log'

admin_logger = logging.getLogger('admin_access')
admin_logger.setLevel(logging.INFO)

try:
    # Try to log to file
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
except PermissionError:
    # Fallback to stderr if file is not writable
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '[ADMIN-AUTH] %(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    print(f"Warning: Could not write to {log_file}. Logging to stderr instead.")
except Exception as e:
    # Fallback for other errors
    handler = logging.StreamHandler()
    print(f"Warning: Failed to setup admin log file: {e}. Logging to stderr instead.")

admin_logger.addHandler(handler)


def _sanitize_log(value, max_len=200):
    """Strip CR/LF and control chars from a value before logging (anti log-injection)."""
    text = str(value or '')
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = ''.join(ch for ch in text if ch >= ' ')
    return text[:max_len]


def _same(a, b):
    """Constant-time string comparison (bytes: compare_digest rejects
    non-ASCII str, which turned an accented username into a 500)."""
    return hmac.compare_digest(str(a or '').encode('utf-8'), str(b or '').encode('utf-8'))


def _credential_stamp(secret):
    """Short fingerprint of a credential, stored in the session so that a
    password change (or reset) invalidates the sessions opened before it."""
    return hashlib.sha256(str(secret or '').encode('utf-8')).hexdigest()[:16]


def check_auth(username, password):
    """Check if username/password combination is valid.

    Args:
        username: Provided username
        password: Provided password

    Returns:
        True if valid, False otherwise
    """
    # Constant-time comparison to avoid leaking credential length/prefix via timing.
    # Compute both halves before AND-ing so the check doesn't short-circuit.
    user_ok = _same(username, ADMIN_USERNAME)
    pass_ok = _same(password, ADMIN_PASSWORD)
    is_valid = user_ok and pass_ok

    # Log authentication attempts (values sanitized: IP/UA/username are attacker-controlled)
    ip_address = _sanitize_log(request.remote_addr)
    user_agent = _sanitize_log(request.headers.get('User-Agent', 'Unknown'))
    username = _sanitize_log(username)

    if is_valid:
        admin_logger.info(
            f"SUCCESS - User: {username} | IP: {ip_address} | UA: {user_agent}"
        )
    else:
        admin_logger.warning(
            f"FAILED - User: {username} | IP: {ip_address} | UA: {user_agent}"
        )
    
    return is_valid


def authenticate():
    """Send a 401 response that enables basic auth."""
    return Response(
        'Authentication required.\n'
        'Please provide valid admin credentials.',
        401,
        {'WWW-Authenticate': 'Basic realm="EDRefCard Admin"'}
    )


def _session_user():
    """Return the session-auth user dict ({'name', 'role'}) or None.

    The session is a signed cookie the server cannot revoke, so it is
    re-checked against the source of truth on every request: a deleted user,
    a changed role or a changed password takes effect immediately instead of
    when the cookie expires.
    """
    u = session.get('edrc_user')
    if not (isinstance(u, dict) and u.get('name') and u.get('role') in ('admin', 'mapper')):
        return None
    stamp = str(u.get('stamp') or '')
    if u.get('src') == 'env':
        if _same(u['name'], ADMIN_USERNAME) and _same(stamp, _credential_stamp(ADMIN_PASSWORD)):
            return {'name': ADMIN_USERNAME, 'role': 'admin'}
    elif u.get('src') == 'db':
        try:
            from scripts import database
            row = database.get_user_by_username(u['name'])
        except Exception:
            row = None
        if (row and row['role'] in ('admin', 'mapper')
                and _same(stamp, _credential_stamp(row['password_hash']))):
            return {'name': row['username'], 'role': row['role']}
    # Unknown, revoked or pre-upgrade session: drop it, the user logs in again
    session.pop('edrc_user', None)
    return None


def login_session_user(username, password):
    """DB-backed (or env-admin) login. On success stores the user in the
    session and returns its dict; on failure returns None. Attempts logged."""
    from werkzeug.security import check_password_hash
    from scripts import database

    ip_address = _sanitize_log(request.remote_addr)
    safe_name = _sanitize_log(username)

    user = None
    # Env-configured admin can also use the login form (no DB row needed)
    user_ok = _same(username, ADMIN_USERNAME)
    pass_ok = _same(password, ADMIN_PASSWORD)
    if user_ok and pass_ok:
        user = {'name': ADMIN_USERNAME, 'role': 'admin', 'src': 'env',
                'stamp': _credential_stamp(ADMIN_PASSWORD)}
    else:
        try:
            row = database.get_user_by_username(username or '')
        except Exception:
            row = None
        if row and check_password_hash(row['password_hash'], password or ''):
            user = {'name': row['username'], 'role': row['role'], 'src': 'db',
                    'stamp': _credential_stamp(row['password_hash'])}
            try:
                database.touch_user_login(row['id'])
            except Exception:
                pass

    if user:
        session['edrc_user'] = user
        session.permanent = True
        admin_logger.info(f"SESSION LOGIN - User: {safe_name} ({user['role']}) | IP: {ip_address}")
    else:
        admin_logger.warning(f"SESSION LOGIN FAILED - User: {safe_name} | IP: {ip_address}")
    return user


def logout_session_user():
    session.pop('edrc_user', None)


def own_account_can_change_password():
    """True for a named account signed in with the form; False for the env
    admin and HTTP Basic, whose password lives in the environment."""
    u = session.get('edrc_user')
    return bool(_session_user() and isinstance(u, dict) and u.get('src') == 'db')


def change_own_password(current_password, new_password, confirmation):
    """Change the signed-in named account's password. Returns an error message,
    or None on success. The session gets the new stamp, so this browser stays
    signed in while the sessions opened elsewhere with the old password end."""
    from werkzeug.security import check_password_hash, generate_password_hash
    from scripts import database

    if not own_account_can_change_password():
        return 'This account is configured on the server; its password cannot be changed here.'
    row = database.get_user_by_username(session['edrc_user']['name'])
    if not row or not check_password_hash(row['password_hash'], current_password or ''):
        admin_logger.warning(f"PASSWORD CHANGE FAILED - User: {_sanitize_log(session['edrc_user']['name'])}"
                             f" | IP: {_sanitize_log(request.remote_addr)}")
        return 'Your current password is incorrect.'
    if len(new_password or '') < 8:
        return 'The new password must be at least 8 characters long.'
    if len(new_password) > 256:
        return 'The new password must be at most 256 characters long.'
    if new_password != confirmation:
        return 'The two new passwords do not match.'
    if new_password == current_password:
        return 'The new password is the same as the current one.'
    password_hash = generate_password_hash(new_password)
    database.update_user_password(row['id'], password_hash)
    session['edrc_user'] = {**session['edrc_user'], 'stamp': _credential_stamp(password_hash)}
    admin_logger.info(f"PASSWORD CHANGED - User: {_sanitize_log(row['username'])}"
                      f" | IP: {_sanitize_log(request.remote_addr)}")
    return None


def current_user():
    """Resolve the request's (name, role): session first, then HTTP Basic
    against the env admin credentials. (None, None) when unauthenticated."""
    su = _session_user()
    if su:
        return su['name'], su['role']
    auth = request.authorization
    if auth and check_auth(auth.username, auth.password):
        return auth.username, 'admin'
    return None, None


def _require(roles):
    """Decorator factory: allow the request only for the given roles."""
    def deco(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            name, role = current_user()
            if role in roles:
                return f(*args, **kwargs)
            if name:
                return Response('Forbidden: your role does not allow this page.', 403)
            # Unauthenticated: browsers go to the login form; API/tools that
            # sent (bad) Basic credentials keep getting the Basic challenge.
            if request.authorization:
                return authenticate()
            return redirect(url_for('admin.login', next=request.full_path.rstrip('?')))
        return decorated
    return deco


def require_admin(f):
    """Full admin panel access (role 'admin' via session, or env HTTP Basic)."""
    return _require(('admin',))(f)


def require_mapper(f):
    """Controller-mapping access: role 'mapper' or 'admin'."""
    return _require(('admin', 'mapper'))(f)
