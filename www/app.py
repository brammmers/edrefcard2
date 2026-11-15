#!/usr/bin/env python3
"""
EDRefCard Flask Application

This module provides the Flask web application for generating Elite: Dangerous
reference cards from controller bindings files.
"""

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from markupsafe import escape
from werkzeug.middleware.proxy_fix import ProxyFix

# Get the www directory path
WWW_DIR = Path(__file__).parent.resolve()

# Add scripts directory to path for imports
scripts_path = WWW_DIR / 'scripts'
sys.path.insert(0, str(scripts_path))

from scripts import (  # noqa: E402
    __version__,
    Config,
)
from scripts import database  # noqa: E402


from extensions import limiter  # noqa: E402
from commands import clean_cache_command, find_unsupported_command, import_defaults_command, import_live_command, rebuild_db_command, seed_aeromax_command  # noqa: E402
from flask_limiter.errors import RateLimitExceeded  # noqa: E402


# Built-in static serving is DISABLED on purpose: WWW_DIR contains the application
# source code AND the configs/ data directory (including the SQLite DB and logs).
# Serving it at the web root (static_url_path='') exposed /web.py, /configs/edrefcard.db,
# etc. Assets are served via explicit, extension-allow-listed routes in web.py.
app = Flask(__name__,
            static_folder=None,
            template_folder=str(WWW_DIR / 'templates'))

# Configure the application
# The app runs behind a reverse proxy (Traefik on Dokploy). Without this,
# request.remote_addr is the proxy, so every visitor shares ONE rate-limit
# bucket, and request.is_secure is False, so no HSTS header is sent and
# external URLs are generated as http://. TRUSTED_PROXY_HOPS = number of
# proxies in front of the app whose X-Forwarded-* headers are trusted
# (default 1; set 0 when the container is exposed directly, otherwise a
# client could spoof its address).
_proxy_hops = int(os.environ.get('TRUSTED_PROXY_HOPS', '1') or 0)
if _proxy_hops > 0:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=_proxy_hops, x_proto=_proxy_hops)  # type: ignore[method-assign]

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload
app.config['CONFIGS_FOLDER'] = WWW_DIR / 'configs'
app.config['WWW_DIR'] = WWW_DIR
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Fail closed: the image and the code ship placeholder credentials so the app
# starts out of the box in development. In production they would sign the
# session cookies, derive the SFTP password encryption key and open the admin
# panel to anyone who read the repository.
_PLACEHOLDER_SECRETS = frozenset({
    '', 'dev-secret-key-change-in-production', 'dev-secret-key', 'change-this-in-production'})
_PLACEHOLDER_ADMIN_PASSWORDS = frozenset({'', 'changeme'})
if os.environ.get('APP_ENV', 'development').lower() == 'production':
    _unsafe = [name for name, value, placeholders in (
        ('FLASK_SECRET_KEY', app.secret_key, _PLACEHOLDER_SECRETS),
        ('EDREFCARD_ADMIN_PASS', os.environ.get('EDREFCARD_ADMIN_PASS', 'changeme'),
         _PLACEHOLDER_ADMIN_PASSWORDS),
    ) if value in placeholders]
    if _unsafe:
        raise RuntimeError(
            'Refusing to start with APP_ENV=production and placeholder credentials: set '
            + ' and '.join(_unsafe) + ' to strong private values.')
# Session cookie hardening (session auth for admin/mapper accounts)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('APP_URL', '').startswith('https')

# Configure the bindings Config class for Flask
Config.setDirRoot(WWW_DIR)
# Prioritize APP_URL, then SCRIPT_URI, then default
web_root = os.environ.get('APP_URL') or os.environ.get('SCRIPT_URI', 'http://localhost:8080/')
if not web_root.endswith('/'):
    web_root += '/'
Config.setWebRoot(web_root)

# Configure usage of external configs directory (for persistence in containers)
configs_dir_env = os.environ.get('EDREFCARD_CONFIGS_DIR')
if configs_dir_env:
    configs_dir = Path(configs_dir_env).resolve()
    # Ensure it exists
    configs_dir.mkdir(parents=True, exist_ok=True)
    # Tell Config class to use it
    Config.setConfigsPath(configs_dir)
    # Update Flask config
    app.config['CONFIGS_FOLDER'] = configs_dir
    print(f"Using persistent configs directory: {configs_dir}")
else:
    # Default behavior
    app.config['CONFIGS_FOLDER'] = WWW_DIR / 'configs'
print(f"Application configured with Web Root: {web_root}")

# Initialize SQLite database
with app.app_context():
    db_path = app.config['CONFIGS_FOLDER'] / 'edrefcard.db'
    database.init_db(str(db_path))


# Register admin blueprint
from admin import admin_bp  # noqa: E402
app.register_blueprint(admin_bp)


# Register API blueprint
from api import api_bp  # noqa: E402
app.register_blueprint(api_bp)


# Register Web blueprint
from web import web_bp  # noqa: E402
app.register_blueprint(web_bp)


# Initialize Limiter
# (Limiter is defined in extensions.py which web.py uses)
limiter.init_app(app)

# Staging access gate (ACCESS_TOKEN): registered before every other
# before_request hook so nothing renders for an unauthenticated visitor.
import staging_gate  # noqa: E402
import canonical_host  # noqa: E402

# Former names (beta, www, edrefcard2.l0l.fr) redirect first, inactive until
# CANONICAL_URL and REDIRECT_HOSTS are set.
canonical_host.register(app)
staging_gate.register(app)


# Register CLI commands
app.cli.add_command(clean_cache_command)
app.cli.add_command(find_unsupported_command)
app.cli.add_command(import_defaults_command)
app.cli.add_command(rebuild_db_command)
app.cli.add_command(import_live_command)
app.cli.add_command(seed_aeromax_command)


# =============================================================================
# Backup Scheduler (Production Only)
# =============================================================================
# The scheduler runs automatic nightly backups ONLY when:
# 1. APP_ENV=production
# 2. auto_backup_enabled=True in backup settings (Admin UI), read every hour

def init_backup_scheduler():
    """Initialize the backup scheduler for automatic nightly backups."""
    app_env = os.environ.get('APP_ENV', 'development').lower()
    
    if app_env != 'production':
        print(f"Backup scheduler DISABLED (APP_ENV={app_env}, requires 'production')")
        return
        
    # Prevent multiple workers from initializing the scheduler
    # using an exclusive file lock (fcntl)
    lock_file = app.config['CONFIGS_FOLDER'] / 'scheduler.lock'
    try:
        import fcntl
        f = open(lock_file, 'w')
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Keep the file open to hold the lock for the life of this worker process
        app.backup_scheduler_lock = f
    except ImportError:
        # Fallback for local Windows development where fcntl is not available
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 47200))
            app.backup_scheduler_lock = sock 
        except OSError:
            print("Backup scheduler DISABLED on this worker (already running in another worker)")
            return
    except OSError:
        print("Backup scheduler DISABLED on this worker (already running in another worker)")
        return
    
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from admin.backup import run_scheduled_backup_tick

        # Hourly tick: the job itself reads the settings, so enabling the
        # nightly backup or changing its hour in the admin panel takes effect
        # at the next hour instead of at the next container restart.
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            run_scheduled_backup_tick,
            CronTrigger(minute=0),
            id='nightly_backup',
            replace_existing=True,
            misfire_grace_time=1800,
            coalesce=True
        )
        scheduler.start()
        print("Backup scheduler ENABLED - hourly check of the backup settings (UTC)")

    except Exception as e:
        print(f"Warning: Could not initialize backup scheduler: {e}")


# Initialize scheduler (only in production with settings enabled)
init_backup_scheduler()






@app.errorhandler(RateLimitExceeded)
def handle_ratelimit_error(e):
    """Handle rate limit exceeded."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Rate limit exceeded', 'detail': str(e.description)}), 429
    return render_template('error.html', 
                           error_message=f'<h1>Rate Limit Exceeded</h1><p>{escape(str(e.description))}</p>'), 429

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle uncaught exceptions and log them."""
    from werkzeug.exceptions import HTTPException

    # Let Flask render real HTTP errors (404, 405, 413, ...) with their own
    # status code instead of masking every one of them as a 500.
    if isinstance(e, HTTPException):
        return e

    # Re-raise key system exceptions
    if isinstance(e, KeyboardInterrupt | SystemExit):
        raise e

    import traceback
    tb = traceback.format_exc()

    # Log to our memory buffer
    try:
        from scripts import logError
        logError(f"UNCAUGHT 500: {str(e)}\n{tb}")
    except Exception as log_err:
        print(f"Failed to log to memory buffer: {log_err}")

    # Prepare error message for user (no exception details leaked to the client)
    return render_template('error.html',
                           error_message='<h1>Internal Server Error</h1><p>An unexpected error occurred.</p>'), 500


def get_configs_path():
    """Get the path to the configs directory."""
    return app.config['CONFIGS_FOLDER']


@app.before_request
def check_maintenance_mode():
    """Check if maintenance mode is active and show maintenance page."""
    # Skip for admin routes (so admin can toggle it off)
    if request.path.startswith('/admin'):
        return None
    # Skip for static files
    if request.path.startswith('/static') or request.path.endswith(('.css', '.js', '.png', '.jpg', '.ico', '.woff', '.woff2')):
        return None
    
    try:
        from admin.backup import is_maintenance_mode, get_maintenance_message
        if is_maintenance_mode():
            return render_template('maintenance.html', message=get_maintenance_message()), 503
    except Exception:
        pass  # If backup module fails, don't block the app
    
    return None


@app.before_request
def set_working_directory():
    """Set working directory for image generation paths."""
    os.chdir(app.config['WWW_DIR'] / 'scripts')


@app.context_processor
def inject_version():
    """Inject version into all templates."""
    return {'version': __version__}


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # XSS Protection (legacy browsers)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "frame-ancestors 'self'"
    )
    
    # HSTS (only in production with HTTPS)
    if not app.debug and request.is_secure:
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains; preload'
        )
    
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions policy
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=()'
    )
    
    return response


if __name__ == '__main__':
    # Ensure configs directory exists
    configs_path = get_configs_path()
    configs_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting EDRefCard v{__version__}")
    print(f"WWW directory: {WWW_DIR}")
    print(f"Configs directory: {configs_path}")
    
    app.run(debug=True, host='0.0.0.0', port=8080)

