#!/usr/bin/env python3
"""
EDRefCard Flask Application

This module provides the Flask web application for generating Elite: Dangerous
reference cards from controller bindings files.
"""

import os
import sys
from pathlib import Path

from flask import Flask, render_template, request

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
from commands import clean_cache_command, find_unsupported_command, import_defaults_command, rebuild_db_command  # noqa: E402
from flask_limiter.errors import RateLimitExceeded  # noqa: E402


app = Flask(__name__, 
            static_folder=str(WWW_DIR), 
            static_url_path='',
            template_folder=str(WWW_DIR / 'templates'))

# Configure the application
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload
app.config['CONFIGS_FOLDER'] = WWW_DIR / 'configs'
app.config['WWW_DIR'] = WWW_DIR
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure the bindings Config class for Flask
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
# Store DB# Initialize database
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


# Register CLI commands
app.cli.add_command(clean_cache_command)
app.cli.add_command(find_unsupported_command)
app.cli.add_command(import_defaults_command)
app.cli.add_command(rebuild_db_command)


# =============================================================================
# Backup Scheduler (Production Only)
# =============================================================================
# The scheduler runs automatic nightly backups ONLY when:
# 1. APP_ENV=production
# 2. auto_backup_enabled=True in backup settings (Admin UI)

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
    except (IOError, OSError):
        print("Backup scheduler DISABLED on this worker (already running in another worker)")
        return
    
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from admin.backup import get_backup_settings, run_scheduled_backup
        
        settings = get_backup_settings()
        
        if not settings.get('auto_backup_enabled'):
            print("Backup scheduler will NOT run (auto_backup_enabled=False in settings)")
            return
        
        scheduler = BackgroundScheduler()
        hour = settings.get('backup_schedule_hour', 4)
        
        scheduler.add_job(
            run_scheduled_backup,
            CronTrigger(hour=hour, minute=0),
            id='nightly_backup',
            replace_existing=True,
            misfire_grace_time=3600  # Allow 1 hour grace for missed jobs
        )
        
        scheduler.start()
        print(f"Backup scheduler ENABLED - nightly at {hour:02d}:00 UTC")
        
    except Exception as e:
        print(f"Warning: Could not initialize backup scheduler: {e}")


# Initialize scheduler (only in production with settings enabled)
init_backup_scheduler()






@app.errorhandler(RateLimitExceeded)
def handle_ratelimit_error(e):
    """Handle rate limit exceeded."""
    return render_template('error.html', 
                           error_message=f'<h1>Rate Limit Exceeded</h1><p>{e.description}</p>'), 429

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle uncaught exceptions and log them."""
    import traceback
    tb = traceback.format_exc()
    
    # Log to our memory buffer
    try:
        from scripts import logError
        logError(f"UNCAUGHT 500: {str(e)}\n{tb}")
    except Exception as e:
        print(f"Failed to log to memory buffer: {e}")
        
    # Re-raise key system exceptions
    if isinstance(e,  KeyboardInterrupt | SystemExit):
        raise e
        
    # Prepare error message for user
    return render_template('error.html', 
                           error_message=f'<h1>Internal Server Error</h1><p>An unexpected error occurred.</p><!-- {str(e)} -->'), 500


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

