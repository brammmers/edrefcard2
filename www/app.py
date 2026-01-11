#!/usr/bin/env python3
"""
EDRefCard Flask Application

This module provides the Flask web application for generating Elite: Dangerous
reference cards from controller bindings files.
"""

import os
import sys
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Get the www directory path
WWW_DIR = Path(__file__).parent.resolve()

# Add scripts directory to path for imports
scripts_path = WWW_DIR / 'scripts'
sys.path.insert(0, str(scripts_path))

# Import from the modular package
from scripts import (
    __version__,
    Config,
    Mode,
    Errors,
    supportedDevices,
    groupStyles,
    parseBindings,
    parseFormData,
    createHOTASImage,
    appendKeyboardImage,
    createBlockImage,
    saveReplayInfo,
    controllerNames,
    logError,
)
from scripts import database

app = Flask(__name__, 
            static_folder=str(WWW_DIR), 
            static_url_path='',
            template_folder=str(WWW_DIR / 'templates'))

# Configure the application
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
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
# Initialize SQLite database
from scripts.database import init_db, get_configuration_stats, migrate_from_pickle
# Store DB# Initialize database
with app.app_context():
    db_path = app.config['CONFIGS_FOLDER'] / 'edrefcard.db'
    database.init_db(str(db_path))

# Auto-migrate legacy data if database is empty
try:
    stats = get_configuration_stats()
    if stats['total_configurations'] == 0:
        print("Database empty. Checking for legacy configurations to migrate...")
        configs_dir = WWW_DIR / 'configs'
        if configs_dir.exists():
            migrated, errors = migrate_from_pickle(configs_dir)
            if migrated > 0:
                print(f"Auto-migrated {migrated} legacy configurations ({errors} errors).")
            else:
                print("No legacy configurations found.")
except Exception as e:
    print(f"Warning: Auto-migration check failed: {e}")

# Register admin blueprint
from admin import admin_bp
app.register_blueprint(admin_bp)

# Register API blueprint
from api import api_bp
app.register_blueprint(api_bp)

# Register Web blueprint
from web import web_bp
app.register_blueprint(web_bp)

# Initialize Limiter
# (Limiter is defined in extensions.py which web.py uses)
from extensions import limiter
limiter.init_app(app)

# Register CLI commands
from commands import clean_cache_command, find_unsupported_command, migrate_legacy_command, import_defaults_command
app.cli.add_command(clean_cache_command)
app.cli.add_command(find_unsupported_command)
app.cli.add_command(migrate_legacy_command)
app.cli.add_command(import_defaults_command)


from flask_limiter.errors import RateLimitExceeded

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
    except:
        print(f"Failed to log to memory buffer: {e}")
        
    # Re-raise key system exceptions
    if isinstance(e,  (KeyboardInterrupt, SystemExit)):
        raise e
        
    # Prepare error message for user
    return render_template('error.html', 
                           error_message=f'<h1>Internal Server Error</h1><p>An unexpected error occurred.</p><!-- {str(e)} -->'), 500


def get_configs_path():
    """Get the path to the configs directory."""
    return app.config['CONFIGS_FOLDER']


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

