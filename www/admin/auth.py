#!/usr/bin/env python3
"""
EDRefCard Admin Authentication

HTTP Basic Authentication for the admin panel.
Credentials are read from environment variables.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from functools import wraps
from flask import request, Response
from scripts.models import Config


# Default credentials (override with environment variables)
ADMIN_USERNAME = os.environ.get('EDREFCARD_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('EDREFCARD_ADMIN_PASS', 'changeme')

# Configure admin access logging
# Configure admin access logging
# Use persistent configs directory
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


def check_auth(username, password):
    """Check if username/password combination is valid.
    
    Args:
        username: Provided username
        password: Provided password
    
    Returns:
        True if valid, False otherwise
    """
    is_valid = username == ADMIN_USERNAME and password == ADMIN_PASSWORD
    
    # Log authentication attempts
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
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


def require_admin(f):
    """Decorator to require admin authentication for a route.
    
    Usage:
        @app.route('/admin/')
        @require_admin
        def admin_dashboard():
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
