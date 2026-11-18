#!/usr/bin/env python3
"""
EDRefCard Admin Blueprint

Flask Blueprint for administration functionality.
"""

import re
from pathlib import Path
from urllib.parse import urlparse
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from scripts import database, parseBindings, slugify, logError
from scripts.parser import ALL_DISPLAY_GROUPS

from scripts.models import Config, Errors
from extensions import limiter
from .auth import (require_admin, require_mapper, current_user,
                   login_session_user, logout_session_user)




# Create blueprint
admin_bp = Blueprint('admin', __name__,
                     url_prefix='/admin',
                     template_folder='templates')


_CSRF_SAFE_METHODS = frozenset({'GET', 'HEAD', 'OPTIONS'})


@admin_bp.before_request
def _csrf_protect_admin():
    """Same-origin CSRF guard for state-changing admin requests.

    The admin panel uses HTTP Basic auth, so a browser auto-sends credentials
    on cross-site requests. For any non-safe method we require the Origin (or
    Referer fallback) to match the current host, which blocks forged POSTs from
    a malicious page (delete config, restore, settings change, ...).
    """
    if request.method in _CSRF_SAFE_METHODS:
        return
    for header in ('Origin', 'Referer'):
        value = request.headers.get(header)
        if value:
            if urlparse(value).netloc != request.host:
                abort(403, description='Cross-origin request blocked (CSRF protection)')
            return
    # No Origin and no Referer on a state-changing request: reject.
    abort(403, description='Missing Origin/Referer on state-changing request')


@admin_bp.route('/')
@require_admin
def dashboard():
    """Admin dashboard with statistics."""
    from .activity_chart import RANGES, build_chart, build_monthly, build_top
    stats = database.get_configuration_stats()
    days = request.args.get('days', type=int)
    days = days if days in RANGES else 90
    chart = build_chart(database.get_daily_creations(days))
    monthly = build_monthly(database.get_monthly_creations())
    top_total, top_pairs = database.get_controller_cards(days)
    top = build_top(top_total, top_pairs)
    return render_template('admin/dashboard.html', stats=stats, chart=chart, days=days, ranges=RANGES,
                           monthly=monthly, top=top, top_total=top_total)



@admin_bp.route('/configs')
@require_admin
def list_configs():
    """List all configurations with pagination."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    device = request.args.get('device', '')
    public_only = request.args.get('public_only', '0') == '1'
    
    configs, total = database.list_configurations(
        page=page,
        per_page=50,
        public_only=public_only,
        search=search if search else None,
        device_filter=device if device else None
    )

    
    total_pages = (total + 49) // 50
    
    return render_template('admin/configs.html',
                           configs=configs,
                           page=page,
                           total_pages=total_pages,
                           total=total,
                           search=search,
                           device=device,
                           public_only=public_only)


@admin_bp.route('/configs/<config_id>/delete', methods=['POST'])
@require_admin
def delete_config(config_id):
    """Delete a configuration."""
    db = database

    if not Config.isValidName(config_id):
        flash('Invalid configuration id.', 'error')
        return redirect(url_for('admin.list_configs'))

    # Only this config's own files. Its directory is shared with every other
    # config starting with the same two characters, so it must never be
    # removed as a whole (that used to wipe all sibling configs).
    other_ids = db.get_all_config_ids() - {config_id}
    owned = Config(config_id).ownedFiles(other_ids)

    # Delete from database
    db.delete_configuration(config_id)

    failed = []
    for path in owned:
        try:
            path.unlink()
        except Exception as e:
            failed.append(f'{path.name}: {e}')
    if failed:
        flash(f'Warning: Could not delete files: {"; ".join(failed)}', 'warning')

    flash(f'Configuration {config_id} deleted.', 'success')
    return redirect(url_for('admin.list_configs'))


@admin_bp.route('/configs/<config_id>/purge-pdf', methods=['POST'])
@require_admin
def purge_pdf(config_id):
    """Purge generated PDF files for a configuration."""
    if not Config.isValidName(config_id):
        flash('Invalid configuration id.', 'error')
        return redirect(url_for('admin.list_configs'))

    purged_count = 0
    errors = []

    # Only this config's PDFs (its directory is shared with sibling configs)
    other_ids = database.get_all_config_ids() - {config_id}
    for pdf_file in Config(config_id).ownedFiles(other_ids):
        if pdf_file.suffix.lower() != '.pdf':
            continue
        try:
            pdf_file.unlink()
            purged_count += 1
        except Exception as e:
            errors.append(f"Could not delete {pdf_file.name}: {e}")
    
    if errors:
        flash(f'Purged {purged_count} PDFs, but encountered errors: {"; ".join(errors)}', 'warning')
    elif purged_count > 0:
        flash(f'Successfully purged {purged_count} PDF files for {config_id}.', 'success')
    else:
        flash(f'No PDF files found to purge for {config_id}.', 'info')
        
    return redirect(url_for('admin.list_configs'))


@admin_bp.route('/configs/<config_id>/edit', methods=['POST'])
@require_admin
def edit_config(config_id):
    """Edit a configuration's description or visibility."""
    db = database
    
    description = request.form.get('description', '')
    is_public = request.form.get('is_public') == 'on'
    is_featured = request.form.get('is_featured') == 'on'
    
    db.update_configuration(
        config_id,
        description=description,
        is_public=1 if is_public else 0,
        is_featured=1 if is_featured else 0
    )
    
    flash(f'Configuration {config_id} updated.', 'success')
    return redirect(url_for('admin.list_configs'))


@admin_bp.route('/configs/<config_id>/toggle-public', methods=['POST'])
@require_admin
def toggle_public(config_id):
    """Toggle a configuration's public status."""
    db = database
    
    config = db.get_configuration(config_id)
    if config:
        new_status = 0 if config['is_public'] else 1
        db.update_configuration(config_id, is_public=new_status)
        status = 'public' if new_status else 'private'
        flash(f'Configuration {config_id} is now {status}.', 'success')
    
    return redirect(url_for('admin.list_configs'))


@admin_bp.route('/stats')
@require_admin
def stats():
    """Detailed statistics page."""
    db = database
    stats = db.get_configuration_stats()
    device_names = db.get_all_device_names()
    
    return render_template('admin/stats.html', stats=stats, device_names=device_names)


@admin_bp.route('/debug')
@require_admin
def debug_info():
    """Debug information about the environment."""
    from scripts.utils import RECENT_ERRORS

    
    # Check Wand status
    wand_status = "Not Installed"
    wand_path = "Unknown"
    wand_error = None
    try:
        import wand
        from wand.version import VERSION
        wand_status = f"Installed (v{VERSION})"
        wand_path = wand.__file__
    except ImportError as e:
        wand_status = "Import Failed"
        wand_error = str(e)
    
    # Path info
    www_dir = Path(__file__).parent.parent
    configs_path = Config.configsPath()
    
    # Directory listing - subdir restricted to the 2-char run-id prefix
    # folders (rejects path traversal like ../../)
    config_files = []
    subdir = request.args.get('subdir')
    if subdir and not re.fullmatch(r'[A-Za-z0-9]{1,2}', subdir):
        config_files.append(f"Invalid subdir {subdir!r}: expected 1-2 alphanumeric characters")
        subdir = None

    list_path = configs_path
    if subdir:
        list_path = configs_path / subdir

    if list_path.exists():
        try:
            # List top level standard dirs or files
            for p in sorted(list_path.glob('*')):
                config_files.append(f"{p.name} ({'DIR' if p.is_dir() else 'FILE'})")
        except Exception as e:
            config_files.append(f"Error listing files: {e}")
    else:
        config_files.append(f"Directory {list_path} does not exist!")

    # Read persistent log file
    persistent_logs = []
    try:
        log_path = Config.configsPath() / 'error.log'
        if log_path.exists():
            with open(log_path, encoding='utf-8') as f:
                # Read last 50 lines
                lines = f.readlines()
                persistent_logs = lines[-50:]
                persistent_logs.reverse() # Show newest first
    except Exception as e:
        persistent_logs = [f"Error reading log file: {e}"]
        
    return render_template('admin/debug.html',
                           www_dir=www_dir,
                           configs_path=configs_path,
                           wand_status=wand_status,
                           wand_path=wand_path,
                           wand_error=wand_error,
                           config_files=config_files,
                           recent_errors=RECENT_ERRORS,
                           persistent_logs=persistent_logs,
                           subdir=subdir)

@admin_bp.route('/batch-import', methods=['GET', 'POST'])
@require_admin
def batch_import():
    """Batch import multiple .binds files."""
    if request.method == 'GET':
        return render_template('admin/batch_import.html')
    
    # POST: Process uploaded files


    
    files = request.files.getlist('binds_files')
    if not files:
        flash('No files selected.', 'error')
        return redirect(url_for('admin.batch_import'))
    
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    
    for file in files:
        if not file or not file.filename:
            continue
            
        if not file.filename.endswith('.binds'):
            results['failed'].append((file.filename, 'Not a .binds file'))
            continue
        
        try:
            # Read file
            xml = file.read().decode('utf-8')
            
            # Generate config ID from filename
            base_id = slugify(file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename)

            if not base_id:
                base_id = Config.randomName()
            
            run_id = base_id
            config = Config(run_id)
            
            # If ID already exists, skip it (as requested for batch import)
            if config.exists():
                results['skipped'].append((file.filename, run_id))
                continue
            
            config.makeDir()

            errors = Errors()
            
            # Default display groups for batch import (all groups)
            display_groups = list(ALL_DISPLAY_GROUPS)
            
            # Parse bindings
            (physicalKeys, modifiers, devices) = parseBindings(config.name, xml, display_groups, errors)
            
            # Save if parsing successful (physicalKeys is None if parsing failed)
            if physicalKeys is not None:
                # Extract PresetName from XML for description
                preset_match = re.search(r'PresetName="([^"]+)"', xml)

                if preset_match:
                    preset_name = preset_match.group(1)
                    # Skip generic preset names, use them only if meaningful
                    if preset_name and preset_name not in ('Custom', 'Empty', ''):
                        description = preset_name
                    else:
                        # Use filename without extension as fallback
                        description = file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename
                else:
                    description = file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename

                
                # Save to database
                database.create_configuration(

                    config_id=config.name,
                    description=description,
                    display_groups=display_groups,
                    devices=devices,
                    unhandled_warnings=errors.unhandledDevicesWarnings,
                    device_warnings=errors.deviceWarnings,
                    misc_warnings=errors.misconfigurationWarnings
                )


                
                # Save binds file
                binds_path = config.pathWithSuffix('.binds')
                with binds_path.open('w', encoding='utf-8') as f:
                    f.write(xml)
                
                results['success'].append((file.filename, config.name))
            else:
                results['failed'].append((file.filename, 'Parsing failed'))

                
        except Exception as e:
            results['failed'].append((file.filename, str(e)))
    
    # Show results
    flash(f"Imported {len(results['success'])} files successfully.", 'success')
    if results['failed']:
        flash(f"Failed to import {len(results['failed'])} files.", 'warning')
    
    return render_template('admin/batch_import_results.html', results=results)


# ============== Backup & Restore Routes ==============

@admin_bp.route('/backup')
@require_admin
def backup_dashboard():
    """Backup dashboard showing status and options."""
    from .backup import (
        BackupManager, get_backup_settings, get_backup_history,
        is_maintenance_mode
    )
    
    backup_manager = BackupManager()
    local_backups = backup_manager.list_local_backups()
    settings = get_backup_settings()
    history = get_backup_history(limit=10)
    
    return render_template('admin/backup.html',
                           local_backups=local_backups,
                           settings=settings,
                           history=history,
                           maintenance_mode=is_maintenance_mode())


@admin_bp.route('/backup/create', methods=['POST'])
@require_admin
def backup_create():
    """Create a manual backup (local or download)."""
    from flask import send_file
    from .backup import BackupManager, DiscordNotifier
    
    include_db = request.form.get('include_db', '1') == '1'
    include_binds = request.form.get('include_binds', '1') == '1'
    action = request.form.get('action', 'download')
    
    try:
        backup_manager = BackupManager()
        backup_path = backup_manager.create_backup(
            include_db=include_db,
            include_binds=include_binds,
            backup_type='manual'
        )
        
        # Send notification
        notifier = DiscordNotifier.from_settings()
        if notifier.webhook_url:
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            notifier.send_notification(
                title="📦 Manual Backup Created",
                message=f"A manual backup was created ({action}).",
                success=True,
                fields=[
                    {'name': 'Size', 'value': f"{size_mb:.2f} MB", 'inline': True},
                    {'name': 'Type', 'value': action.capitalize(), 'inline': True},
                ]
            )
        
        if action == 'download':
            return send_file(
                backup_path,
                as_attachment=True,
                download_name=backup_path.name
            )
        else:
            flash(f'Backup created successfully: {backup_path.name}', 'success')
            return redirect(url_for('admin.backup_dashboard'))
        
    except Exception as e:
        flash(f'Backup failed: {e}', 'danger')
        return redirect(url_for('admin.backup_dashboard'))


@admin_bp.route('/backup/upload-sftp', methods=['POST'])
@require_admin
def backup_upload_sftp():
    """Upload a backup to SFTP (latest or specific)."""
    from .backup import BackupManager, SFTPManager, get_backup_settings
    
    settings = get_backup_settings()
    if not settings.get('sftp_enabled') or not settings.get('sftp_host'):
        flash('SFTP is not configured.', 'warning')
        return redirect(url_for('admin.backup_dashboard'))
    
    filename = request.form.get('filename')
    
    try:
        backup_manager = BackupManager()
        
        target_path = None
        if filename:
            # Upload specific file
            target_path = backup_manager.get_backup_path(filename)
            if not target_path:
                flash(f'Backup file not found: {filename}', 'danger')
                return redirect(url_for('admin.backup_dashboard'))
        else:
            # Upload latest
            local_backups = backup_manager.list_local_backups()
            if not local_backups:
                flash('No local backups to upload.', 'warning')
                return redirect(url_for('admin.backup_dashboard'))
            target_path = Path(local_backups[0]['path'])
        
        sftp_manager = SFTPManager.from_settings()
        sftp_manager.upload_backup(target_path)
        
        # Cleanup old remote backups if needed (only on auto/sync all)
        # sftp_manager.cleanup_remote(retention_days=7) 
        
        flash(f'Backup {target_path.name} uploaded to SFTP.', 'success')
        
    except Exception as e:
        flash(f'SFTP upload failed: {e}', 'danger')
    
    return redirect(url_for('admin.backup_dashboard'))


@admin_bp.route('/backup/delete/<filename>', methods=['POST'])
@require_admin
def backup_delete(filename):
    """Delete a local backup file."""
    from .backup import BackupManager
    
    try:
        backup_manager = BackupManager()
        backup_path = backup_manager.get_backup_path(filename)
        
        if backup_path and backup_path.exists():
            backup_path.unlink()
            flash(f'Backup {filename} deleted.', 'success')
        else:
            flash(f'Backup {filename} not found.', 'warning')
            
    except Exception as e:
        flash(f'Failed to delete backup: {e}', 'danger')
        
    return redirect(url_for('admin.backup_dashboard'))


@admin_bp.route('/backup/download/<filename>')
@require_admin
def backup_download(filename):
    """Download a specific local backup file."""
    from flask import send_file
    from .backup import BackupManager
    
    try:
        backup_manager = BackupManager()
        backup_path = backup_manager.get_backup_path(filename)
        
        if backup_path and backup_path.exists():
            return send_file(
                backup_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            flash(f'Backup {filename} not found.', 'danger')
            return redirect(url_for('admin.backup_dashboard'))
            
    except Exception as e:
        flash(f'Download failed: {e}', 'danger')
        return redirect(url_for('admin.backup_dashboard'))


@admin_bp.route('/backup/settings', methods=['GET', 'POST'])
@require_admin
def backup_settings():
    """Backup settings page."""
    from .backup import get_backup_settings, save_backup_settings, get_pinned_sftp_host_key
    
    if request.method == 'POST':
        settings = {
            'sftp_enabled': request.form.get('sftp_enabled') == 'on',
            'sftp_host': request.form.get('sftp_host', ''),
            'sftp_port': int(request.form.get('sftp_port', 22)),
            'sftp_user': request.form.get('sftp_user', ''),
            'sftp_password': request.form.get('sftp_password', ''),
            'sftp_remote_dir': request.form.get('sftp_remote_dir', '/backups/edrefcard'),
            'auto_backup_enabled': request.form.get('auto_backup_enabled') == 'on',
            'backup_schedule_hour': int(request.form.get('backup_schedule_hour', 4)),
            'discord_webhook_url': request.form.get('discord_webhook_url', ''),
        }
        
        # Secrets (SFTP password, Discord webhook) are never echoed back to the
        # form, so a blank submission means "keep existing" rather than "clear".
        if not settings['sftp_password'] or not settings['discord_webhook_url']:
            existing = get_backup_settings()
            if not settings['sftp_password']:
                settings['sftp_password'] = existing.get('sftp_password', '')
            if not settings['discord_webhook_url']:
                settings['discord_webhook_url'] = existing.get('discord_webhook_url', '')

        save_backup_settings(settings)
        flash('Backup settings saved.', 'success')
        return redirect(url_for('admin.backup_settings'))
    
    settings = get_backup_settings()
    return render_template('admin/backup_settings.html', settings=settings,
                           sftp_host_key=get_pinned_sftp_host_key(
                               settings.get('sftp_host') or '', settings.get('sftp_port') or 22))


@admin_bp.route('/backup/sftp-forget-key', methods=['POST'])
@require_admin
def backup_sftp_forget_key():
    """Forget the pinned SFTP host key (server legitimately reinstalled).
    The next connection made from the saved settings pins the new key."""
    from .backup import get_backup_settings, forget_sftp_host_key
    settings = get_backup_settings()
    if settings.get('sftp_host'):
        forget_sftp_host_key(settings['sftp_host'], settings.get('sftp_port') or 22)
        flash('Pinned SFTP host key forgotten. The next connection will record the new one.', 'success')
    return redirect(url_for('admin.backup_settings'))


@admin_bp.route('/backup/sftp-test', methods=['POST'])
@require_admin
def backup_sftp_test():
    """Test SFTP connection."""
    from flask import jsonify
    from .backup import SFTPManager
    
    sftp_manager = SFTPManager(
        host=request.form.get('sftp_host', ''),
        port=int(request.form.get('sftp_port', 22)),
        user=request.form.get('sftp_user', ''),
        password=request.form.get('sftp_password', ''),
        remote_dir=request.form.get('sftp_remote_dir', '/backups/edrefcard')
    )
    
    success, message = sftp_manager.test_connection()
    return jsonify({'success': success, 'message': message})


@admin_bp.route('/backup/discord-test', methods=['POST'])
@require_admin
def backup_discord_test():
    """Test Discord webhook."""
    from flask import jsonify
    from .backup import DiscordNotifier
    
    webhook_url = request.form.get('discord_webhook_url', '')
    notifier = DiscordNotifier(webhook_url=webhook_url)
    
    success, message = notifier.test_webhook()
    return jsonify({'success': success, 'message': message})


@admin_bp.route('/restore')
@require_admin
def restore_dashboard():
    """Restore dashboard."""
    from .backup import get_backup_settings, SFTPManager, BackupManager, is_maintenance_mode
    
    settings = get_backup_settings()
    remote_backups = []
    sftp_error = None
    
    # Get local backups
    backup_manager = BackupManager()
    local_backups = backup_manager.list_local_backups()
    
    if settings.get('sftp_enabled') and settings.get('sftp_host'):
        try:
            sftp_manager = SFTPManager.from_settings()
            remote_backups = sftp_manager.list_remote_backups()
        except Exception as e:
            sftp_error = str(e)
    
    return render_template('admin/restore.html',
                           settings=settings,
                           local_backups=local_backups,
                           remote_backups=remote_backups,
                           sftp_error=sftp_error,
                           maintenance_mode=is_maintenance_mode())


@admin_bp.route('/restore/from-upload', methods=['POST'])
@require_admin
def restore_from_upload():
    """Restore from an uploaded backup file."""
    from .backup import RestoreManager, DiscordNotifier
    import tempfile
    
    if 'backup_file' not in request.files:
        flash('No backup file uploaded.', 'danger')
        return redirect(url_for('admin.restore_dashboard'))
    
    file = request.files['backup_file']
    if not file.filename or not file.filename.endswith('.tar.gz'):
        flash('Invalid backup file. Must be a .tar.gz file.', 'danger')
        return redirect(url_for('admin.restore_dashboard'))
    
    restore_db = request.form.get('restore_db') == 'on'
    restore_binds = request.form.get('restore_binds') == 'on'
    
    if not restore_db and not restore_binds:
        flash('Please select at least one component to restore.', 'warning')
        return redirect(url_for('admin.restore_dashboard'))
    
    tmp_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz') as tmp:
            tmp_path = Path(tmp.name)
            file.save(tmp)
        
        # Perform restore
        restore_manager = RestoreManager()
        results = restore_manager.restore_from_archive(
            tmp_path,
            restore_db=restore_db,
            restore_binds=restore_binds
        )
        
        if results['success']:
            flash(f'Restore completed. DB: {results["db_restored"]}, Binds: {results["binds_restored"]} files.', 'success')
            
            # Send notification
            notifier = DiscordNotifier.from_settings()
            if notifier.webhook_url:
                notifier.send_notification(
                    title="🔄 Restore Completed",
                    message="A restore operation completed successfully.",
                    success=True,
                    fields=[
                        {'name': 'Database', 'value': 'Yes' if results['db_restored'] else 'No', 'inline': True},
                        {'name': 'Binds Files', 'value': str(results['binds_restored']), 'inline': True},
                    ]
                )
        else:
            flash(f'Restore completed with errors: {", ".join(results["errors"])}', 'warning')
            
    except Exception as e:
        flash(f'Restore failed: {e}', 'danger')
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
    
    return redirect(url_for('admin.restore_dashboard'))


@admin_bp.route('/restore/from-local', methods=['POST'])
@require_admin
def restore_from_local():
    """Restore from a local backup file."""
    from .backup import RestoreManager, BackupManager, DiscordNotifier
    
    filename = request.form.get('filename')
    if not filename:
        flash('No backup file selected.', 'danger')
        return redirect(url_for('admin.restore_dashboard'))
    
    restore_db = request.form.get('restore_db') == 'on'
    restore_binds = request.form.get('restore_binds') == 'on'
    
    if not restore_db and not restore_binds:
        flash('Please select at least one component to restore.', 'warning')
        return redirect(url_for('admin.restore_dashboard'))
    
    try:
        # Get local backup path
        backup_manager = BackupManager()
        backup_path = backup_manager.get_backup_path(filename)
        
        if not backup_path:
            flash(f'Backup file not found: {filename}', 'danger')
            return redirect(url_for('admin.restore_dashboard'))
        
        # Perform restore
        restore_manager = RestoreManager()
        results = restore_manager.restore_from_archive(
            backup_path,
            restore_db=restore_db,
            restore_binds=restore_binds
        )
        
        if results['success']:
            flash(f'Restore completed. DB: {results["db_restored"]}, Binds: {results["binds_restored"]} files.', 'success')
            
            # Send notification
            notifier = DiscordNotifier.from_settings()
            if notifier.webhook_url:
                notifier.send_notification(
                    title="🔄 Restore Completed",
                    message=f"Restored from local backup: {filename}",
                    success=True
                )
        else:
            flash(f'Restore completed with errors: {", ".join(results["errors"])}', 'warning')
            
    except Exception as e:
        flash(f'Restore failed: {e}', 'danger')
    
    return redirect(url_for('admin.restore_dashboard'))


@admin_bp.route('/restore/from-sftp', methods=['POST'])
@require_admin
def restore_from_sftp():
    """Restore from a backup on SFTP server."""
    from .backup import RestoreManager, SFTPManager, DiscordNotifier
    
    filename = request.form.get('filename')
    
    if not filename:
        flash('No backup file selected.', 'danger')
        return redirect(url_for('admin.restore_dashboard'))
    
    restore_db = request.form.get('restore_db') == 'on'
    restore_binds = request.form.get('restore_binds') == 'on'
    
    if not restore_db and not restore_binds:
        flash('Please select at least one component to restore.', 'warning')
        return redirect(url_for('admin.restore_dashboard'))
    
    try:
        # Download from SFTP
        sftp_manager = SFTPManager.from_settings()
        local_path = sftp_manager.download_backup(filename)
        
        # Perform restore
        restore_manager = RestoreManager()
        results = restore_manager.restore_from_archive(
            local_path,
            restore_db=restore_db,
            restore_binds=restore_binds
        )
        
        # Cleanup downloaded file
        local_path.unlink(missing_ok=True)
        
        if results['success']:
            flash(f'Restore completed. DB: {results["db_restored"]}, Binds: {results["binds_restored"]} files.', 'success')
            
            # Send notification
            notifier = DiscordNotifier.from_settings()
            if notifier.webhook_url:
                notifier.send_notification(
                    title="🔄 Restore Completed",
                    message=f"Restored from SFTP backup: {filename}",
                    success=True
                )
        else:
            flash(f'Restore completed with errors: {", ".join(results["errors"])}', 'warning')
            
    except Exception as e:
        flash(f'Restore failed: {e}', 'danger')
    
    return redirect(url_for('admin.restore_dashboard'))


@admin_bp.route('/maintenance/toggle', methods=['POST'])
@require_admin
def maintenance_toggle():
    """Toggle maintenance mode."""
    from .backup import is_maintenance_mode, set_maintenance_mode
    
    current = is_maintenance_mode()
    message = request.form.get('message', 'System is under maintenance.')
    
    set_maintenance_mode(not current, message)
    
    status = 'enabled' if not current else 'disabled'
    flash(f'Maintenance mode {status}.', 'success')
    
    return redirect(request.referrer or url_for('admin.dashboard'))


# ============== Controller mapping editor (feature B1) ==============

# ============== Session auth (multi-user: admin + mappers) ==============

@admin_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20 per hour", methods=['POST'])
def login():
    """Session login form. Accepts DB users (admin/mapper roles) and the
    env-configured admin. HTTP Basic remains usable for scripts/tools."""
    error = None
    if request.method == 'POST':
        user = login_session_user(request.form.get('username', '').strip(),
                                  request.form.get('password', ''))
        if user:
            nxt = request.form.get('next') or request.args.get('next') or ''
            # Internal path only ("//x", a backslash and control chars leave the site)
            if (not nxt.startswith('/') or nxt.startswith('//') or '\\' in nxt
                    or any(c < ' ' for c in nxt)):
                nxt = ''
            if not nxt:
                nxt = url_for('admin.controllers') if user['role'] == 'mapper' \
                    else url_for('admin.dashboard')
            return redirect(nxt)
        error = 'Invalid username or password.'
    nxt = request.args.get('next', '')
    return render_template('admin/login.html', error=error, next=nxt)


@admin_bp.route('/logout', methods=['POST'])
def logout():
    logout_session_user()
    return redirect(url_for('admin.login'))


@admin_bp.route('/users')
@require_admin
def users():
    """Manage admin-panel users (mappers and additional admins)."""
    return render_template('admin/users.html', users=database.list_users())


@admin_bp.route('/users/create', methods=['POST'])
@require_admin
def users_create():
    from werkzeug.security import generate_password_hash
    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''
    role = request.form.get('role') or 'mapper'
    if role not in ('admin', 'mapper'):
        role = 'mapper'
    if not re.fullmatch(r'[A-Za-z0-9_.-]{3,32}', username) or len(password) < 8:
        flash('Username 3-32 chars [A-Za-z0-9_.-], password 8+ chars.', 'error')
        return redirect(url_for('admin.users'))
    if database.get_user_by_username(username):
        flash(f'User "{username}" already exists.', 'error')
        return redirect(url_for('admin.users'))
    database.create_user(username, generate_password_hash(password), role)
    flash(f'User "{username}" created ({role}).', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/delete', methods=['POST'])
@require_admin
def users_delete():
    user_id = request.form.get('user_id')
    if user_id:
        database.delete_user(user_id)
        flash('User deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/reset', methods=['POST'])
@require_admin
def users_reset():
    from werkzeug.security import generate_password_hash
    user_id = request.form.get('user_id')
    password = request.form.get('password') or ''
    if not user_id or len(password) < 8:
        flash('Password 8+ chars required.', 'error')
        return redirect(url_for('admin.users'))
    database.update_user_password(user_id, generate_password_hash(password))
    flash('Password updated.', 'success')
    return redirect(url_for('admin.users'))


def _find_mapping_for_device(device_id):
    """Find a controller mapping by primary device_id, falling back to the
    attached device_ids list inside mapping_json (same hardware, different
    hardware ID: country / colour / revision variants)."""
    import json
    row = database.get_controller_mapping_by_device_id(device_id)
    if row:
        return row
    did_u = (device_id or '').upper()
    for r in database.get_all_controller_mappings():
        try:
            ids = json.loads(r['mapping_json']).get('device_ids') or []
            if did_u in [str(x).upper() for x in ids]:
                return r
        except Exception:
            continue
    return None


@admin_bp.route('/controllers')
@require_mapper
def controllers():
    """Control tower: existing data-driven mappings + unknown-device queue."""
    import json
    from scripts.mapping_lint import lint_mapping, lint_summary
    mappings = []
    for r in database.get_all_controller_mappings():
        try:
            m = json.loads(r['mapping_json'])
        except Exception:
            m = {}
        mappings.append({
            'id': r['id'], 'device_id': r['device_id'],
            'device_name': r['device_name'],
            'device_ids': m.get('device_ids') or [r['device_id']],
            'image': m.get('image'), 'box_count': len(m.get('boxes') or []),
            'updated_at': r.get('updated_at'),
            'status': r.get('status', 'published'),
            'has_draft': r.get('has_draft', False),
            'updated_by': r.get('updated_by'),
            'lint': lint_summary(lint_mapping(m)),
        })
    _, role = current_user()
    unknown = [u for u in database.list_unknown_devices()
               if _find_mapping_for_device(u['device_id']) is None]
    # Legacy controllers: baked artwork + coords in bindingsData.py (read-only
    # here; migrating one to data-driven = create a mapping for its device IDs)
    from scripts.bindingsData import supportedDevices, apply_legacy_device_aliases
    aliases = database.list_legacy_device_aliases()
    apply_legacy_device_aliases(aliases)
    dd_ids = {did for m in mappings for did in m['device_ids']}
    alias_by_key = {}
    for alias in aliases:
        alias_by_key.setdefault(alias['legacy_key'], []).append(alias['device_id'])
    legacy = []
    for key, sd in sorted(supportedDevices.items()):
        if key == 'Keyboard':
            continue
        ids = [h.split('::')[0] for h in sd.get('HandledDevices', [])]
        legacy.append({
            'key': key, 'template': sd.get('Template'),
            'device_ids': sorted(set(ids)),
            'dd_overlap': any(i in dd_ids for i in ids),
            'alias_count': len(alias_by_key.get(key, [])),
        })
    legacy_targets = [dict(item) for item in legacy]

    def name_clue_score(run_id, target):
        import re
        haystack = re.sub(r'[^a-z0-9]+', '', (run_id or '').lower())
        if not haystack:
            return 0
        candidates = [target['key'], target['template']]
        score = 0
        for candidate in candidates:
            needle = re.sub(r'[^a-z0-9]+', '', str(candidate or '').lower())
            if len(needle) >= 3 and needle in haystack:
                score = max(score, 100 + len(needle))
            for token in re.findall(r'[a-z]+|[0-9]+', str(candidate or '').lower()):
                if len(token) >= 3 and token in haystack:
                    score = max(score, 20 + len(token))
        return score

    for unknown_item in unknown:
        ranked = [(name_clue_score(unknown_item.get('last_run_id'), target), target)
                  for target in legacy_targets]
        unknown_item['legacy_suggestions'] = [target for score, target in
                                              sorted(ranked, key=lambda item: (-item[0], item[1]['key']))
                                              if score > 0][:5]
    return render_template('admin/controllers.html', mappings=mappings,
                           unknown=unknown, mappings_legacy=legacy_targets,
                           legacy=legacy, role=role,
                           audit=database.list_mapping_audit(25))


@admin_bp.route('/controllers/publish', methods=['POST'])
@require_admin
def controllers_publish():
    """Publish or unpublish a mapping (draft = hidden from public rendering)."""
    mapping_id = request.form.get('mapping_id')
    state = request.form.get('state')
    row = database.get_controller_mapping(mapping_id) if mapping_id else None
    if not row or state not in ('published', 'draft'):
        flash('Mapping and target state required.', 'error')
        return redirect(url_for('admin.controllers'))
    user_name, _ = current_user()
    if state == 'published':
        # Same checks as the editor's "Checks" panel: errors would ship a
        # card that is wrong for every user, so they block publication.
        import json
        from scripts.mapping_lint import lint_mapping
        try:
            issues = lint_mapping(json.loads(row['mapping_json']))
        except ValueError:
            issues = [{'level': 'error', 'box': None, 'message': 'The mapping is not valid JSON.'}]
        blocking = [issue['message'] for issue in issues if issue['level'] == 'error']
        if blocking:
            shown = ' '.join(blocking[:3]) + (f' (+{len(blocking) - 3} more)' if len(blocking) > 3 else '')
            flash(f'Publication blocked for "{row["device_name"]}": {shown} '
                  'Open the editor: the Checks panel lists every issue.', 'error')
            return redirect(url_for('admin.controllers'))
    try:
        database.set_controller_publication(row['id'], state,
                                            request.form.get('base_updated_at'), user_name)
    except database.MappingConflict as exc:
        flash(str(exc), 'error')
        return redirect(url_for('admin.controllers'))
    database.log_mapping_action('publish' if state == 'published' else 'unpublish',
                                user_name, row['id'], row['device_id'])
    flash(f'"{row["device_name"]}" is now {state}.', 'success')
    return redirect(url_for('admin.controllers'))


@admin_bp.route('/controllers/attach', methods=['POST'])
@require_mapper
def controllers_attach():
    """Attach an unknown hardware ID to an existing mapping (variant IDs)."""
    import json
    device_id = (request.form.get('device_id') or '').strip().upper()
    mapping_id = request.form.get('mapping_id')
    user_name, _ = current_user()
    if mapping_id and str(mapping_id).startswith('mapping:'):
        mapping_id = str(mapping_id)[len('mapping:'):]
    if mapping_id and str(mapping_id).startswith('legacy:'):
        from scripts.bindingsData import supportedDevices, apply_legacy_device_aliases
        legacy_key = str(mapping_id)[len('legacy:'):]
        target = supportedDevices.get(legacy_key)
        if not device_id or target is None:
            flash('Device ID and a valid legacy controller are required.', 'error')
            return redirect(url_for('admin.controllers'))
        try:
            database.attach_legacy_device_alias(device_id, legacy_key, user_name)
        except ValueError as exc:
            flash(str(exc), 'error')
            return redirect(url_for('admin.controllers'))
        apply_legacy_device_aliases([{'device_id': device_id, 'legacy_key': legacy_key}])
        database.dismiss_unknown_device(device_id)
        database.log_mapping_action('attach-legacy', user_name, None, device_id,
                                    f'to legacy "{legacy_key}"')
        flash(f'{device_id} attached to legacy "{legacy_key}". Verify it with a new upload.', 'success')
        return redirect(url_for('admin.controllers'))
    row = database.get_controller_mapping(mapping_id) if mapping_id else None
    if not device_id or not row:
        flash('Device ID and mapping required.', 'error')
        return redirect(url_for('admin.controllers'))
    m = json.loads(row['mapping_json'])
    ids = m.get('device_ids') or [row['device_id']]
    if device_id not in [str(x).upper() for x in ids]:
        ids.append(device_id)
    m['device_ids'] = ids
    try:
        database.save_controller_draft(row['device_id'], row['device_name'], m, user_name,
                                       row['updated_at'], row['id'])
    except database.MappingConflict as exc:
        flash(str(exc), 'error')
        return redirect(url_for('admin.controllers'))
    database.dismiss_unknown_device(device_id)
    database.log_mapping_action('attach', user_name, row['id'], device_id,
                                f'to "{row["device_name"]}"')
    flash(f'{device_id} attached to the draft of "{row["device_name"]}". Publish after review.', 'success')
    return redirect(url_for('admin.controllers'))


@admin_bp.route('/controllers/dismiss', methods=['POST'])
@require_mapper
def controllers_dismiss():
    """Drop a device from the unknown queue (not a real controller, etc.)."""
    device_id = (request.form.get('device_id') or '').strip()
    if device_id:
        database.dismiss_unknown_device(device_id)
        user_name, _ = current_user()
        database.log_mapping_action('dismiss', user_name, None, device_id)
        flash(f'{device_id} dismissed.', 'success')
    return redirect(url_for('admin.controllers'))


@admin_bp.route('/controllers/duplicate', methods=['POST'])
@require_mapper
def controllers_duplicate():
    """Duplicate a mapping under a new device ID (L/R or extended variants)."""
    import json
    mapping_id = request.form.get('mapping_id')
    new_device_id = (request.form.get('new_device_id') or '').strip().upper()
    row = database.get_controller_mapping(mapping_id) if mapping_id else None
    if not row or not new_device_id:
        flash('Source mapping and new device ID required.', 'error')
        return redirect(url_for('admin.controllers'))
    if _find_mapping_for_device(new_device_id):
        flash(f'{new_device_id} is already covered by a mapping.', 'error')
        return redirect(url_for('admin.controllers'))
    m = json.loads(row['mapping_json'])
    m['device_ids'] = [new_device_id]
    template_name = row['template_name']
    suffix = '(copy)'
    if request.form.get('mirror'):
        # L/R variant: flip the clean photo and mirror every coordinate.
        # Chrome and text are drawn at runtime, so nothing ends up reversed
        # (unlike baked legacy artwork, cf. the TCA Sidestick Left saga).
        from PIL import Image as PILImage
        cdir = Config.configsPath() / 'controllers'
        res_dir = Path(__file__).parent.parent / 'res'
        src = next((p for p in (cdir / f'{template_name}.jpg',
                                res_dir / f'{template_name}.jpg') if p.exists()), None)
        if src is None:
            flash(f'Source image "{template_name}.jpg" not found, cannot mirror.', 'error')
            return redirect(url_for('admin.controllers'))
        from uuid import uuid4
        template_name = f'{template_name[:100]}-mirror-{uuid4().hex}'
        cdir.mkdir(parents=True, exist_ok=True)
        with PILImage.open(str(src)) as im:
            flipped = im.transpose(PILImage.FLIP_LEFT_RIGHT)
            flipped.save(str(cdir / f'{template_name}.jpg'), quality=92)
            width = m.get('width') or row['image_width'] or im.width
        for b in m.get('boxes', []):
            b['box_xy'][0] = width - b['box_xy'][0] - b['box_wh'][0]
            if b.get('button_xy'):
                b['button_xy'][0] = width - b['button_xy'][0]
        m['image'] = template_name
        suffix = '(mirror)'
    m['title'] = f"{m.get('title') or row['device_name']} {suffix}"
    user_name, _ = current_user()
    # Duplicates always need adjustment, so they start as drafts
    mid = database.create_controller_mapping(
        new_device_id, m['title'], template_name, f'{template_name}.jpg',
        row['image_width'], row['image_height'], json.dumps(m),
        status='draft', updated_by=user_name)
    database.log_mapping_action('duplicate', user_name, mid, new_device_id,
                                f'from "{row["device_name"]}"' + (' (mirror)' if suffix == '(mirror)' else ''))
    database.dismiss_unknown_device(new_device_id)
    flash(f'Mapping duplicated (id {mid}). Open it to adjust.', 'success')
    return redirect(url_for('admin.mapping_editor', device=new_device_id))


@admin_bp.route('/controllers/delete', methods=['POST'])
@require_admin
def controllers_delete():
    """Delete a mapping. Its version history is kept on purpose: with the
    audit log it makes an accidental delete recoverable (manual restore)."""
    mapping_id = request.form.get('mapping_id')
    row = database.get_controller_mapping(mapping_id) if mapping_id else None
    if not row:
        flash('Mapping not found.', 'error')
        return redirect(url_for('admin.controllers'))
    database.delete_controller_mapping(row['id'])
    user_name, _ = current_user()
    database.log_mapping_action('delete', user_name, row['id'], row['device_id'],
                                f'"{row["device_name"]}"')
    flash(f'Mapping "{row["device_name"]}" deleted (its version history is kept).', 'success')
    return redirect(url_for('admin.controllers'))


@admin_bp.route('/controllers/history/<int:mapping_id>')
@require_mapper
def controllers_history(mapping_id):
    """Version history of a mapping (rollback safety net)."""
    row = database.get_controller_mapping(mapping_id)
    if not row:
        abort(404)
    _, role = current_user()
    return render_template('admin/mapping_history.html', mapping=row,
                           versions=database.list_mapping_versions(mapping_id),
                           role=role)


@admin_bp.route('/controllers/history/<int:mapping_id>/version/<int:version_id>.json')
@require_mapper
def controllers_history_json(mapping_id, version_id):
    """Raw mapping_json of one version (inspection / manual merge)."""
    from flask import Response
    v = database.get_mapping_version(version_id)
    if not v or v['mapping_id'] != mapping_id:
        abort(404)
    return Response(v['mapping_json'], mimetype='application/json')


@admin_bp.route('/controllers/compare/<int:mapping_id>')
@require_mapper
def controllers_compare(mapping_id):
    """Review page: what the saved draft changes compared with the public
    revision, with both layouts side by side, before publishing."""
    import json
    from scripts.mapping_diff import diff_mappings
    from scripts.mapping_lint import lint_mapping
    row = database.get_controller_mapping(mapping_id)
    if not row:
        abort(404)
    try:
        draft = json.loads(row['mapping_json'])
    except ValueError:
        draft = {}
    public = {}
    if row.get('published_snapshot'):
        try:
            public = json.loads(json.loads(row['published_snapshot'])['mapping_json'])
        except (ValueError, KeyError, TypeError):
            public = {}
    if not public:
        flash(f'"{row["device_name"]}" has no public revision yet: there is nothing to compare with.', 'info')
        return redirect(url_for('admin.mapping_editor', device=row['device_id']))
    _, role = current_user()
    return render_template(
        'admin/mapping_compare.html', mapping=row, role=role,
        changes=diff_mappings(public, draft),
        blocking=[issue['message'] for issue in lint_mapping(draft) if issue['level'] == 'error'],
        revisions_json=json.dumps({'public': public, 'draft': draft}))


@admin_bp.route('/controllers/rollback', methods=['POST'])
@require_admin
def controllers_rollback():
    """Restore a mapping to a previous version (recorded as a new version)."""
    import json
    version_id = request.form.get('version_id')
    v = database.get_mapping_version(version_id) if version_id else None
    row = database.get_controller_mapping(v['mapping_id']) if v else None
    if not v or not row:
        flash('Version not found.', 'error')
        return redirect(url_for('admin.controllers'))
    try:
        m = json.loads(v['mapping_json'])
    except Exception:
        flash('This version holds invalid JSON, not restored.', 'error')
        return redirect(url_for('admin.controllers_history', mapping_id=row['id']))
    user_name, _ = current_user()
    device_name = v.get('device_name') or row['device_name']
    m.setdefault('image', row['template_name'])
    m.setdefault('width', row['image_width'])
    m.setdefault('height', row['image_height'])
    try:
        database.save_controller_draft(row['device_id'], device_name, m, user_name,
                                       request.form.get('base_updated_at'), row['id'])
    except database.MappingConflict as exc:
        flash(str(exc), 'error')
        return redirect(url_for('admin.controllers_history', mapping_id=row['id']))
    database.log_mapping_action('rollback', user_name, row['id'], row['device_id'],
                                f"to version {v['id']} of {v.get('saved_at')}")
    flash(f'"{device_name}" restored as a draft from version {v["id"]}. Publish after review.', 'success')
    return redirect(url_for('admin.controllers_history', mapping_id=row['id']))


def _read_binds_xml(run_id):
    """Return the raw .binds XML of an uploaded config, or None."""
    try:
        path = Config(run_id).pathWithSuffix('.binds')
        with open(str(path), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


@admin_bp.route('/help')
@require_mapper
def mapper_help():
    """Onboarding guide for mappers (workflow, stamps, rules)."""
    return render_template('admin/help.html')


@admin_bp.route('/mapping-editor')
@require_mapper
def mapping_editor():
    """Interactive click-to-place editor for data-driven controller mappings.

    ?device=<ID> loads the stored mapping for that device.
    ?device=<ID>&from=<run_id> semi-automates the work from a real .binds:
      - no stored mapping yet -> auto-scaffold a full draft (grouped boxes,
        provisional two-column layout) from every input used in that file;
      - stored mapping exists -> enrich it with the file's not-yet-covered
        inputs, appended as an UNASSIGNED box (VIRPIL config variance).
    """
    import json
    from scripts import scaffold
    device_id = request.args.get('device')
    from_id = request.args.get('from')
    existing = _find_mapping_for_device(device_id) if device_id else None
    draft_note = ''

    if device_id and from_id:
        xml = _read_binds_xml(from_id)
        if xml is None:
            draft_note = f'.binds file not found for "{from_id}"'
        elif existing is None:
            # Scaffold a brand-new draft mapping from the .binds
            try:
                draft = scaffold.scaffold_mapping_from_binds(xml, device_id)
                existing = {'device_id': device_id, 'device_name': '',
                            'mapping_json': json.dumps(draft),
                            'image_width': draft['width'], 'image_height': draft['height']}
                draft_note = (f'Draft scaffolded from "{from_id}": '
                              f'{len(draft["boxes"])} boxes (not saved yet)')
            except Exception as e:
                draft_note = f'Cannot scaffold: {e}'
        else:
            # Enrichment: surface inputs used in this .binds but absent from the mapping
            try:
                m = json.loads(existing['mapping_json'])
                keys = scaffold.extract_device_keys(xml, device_id)
                missing = scaffold.missing_keys(m, keys)
                if missing:
                    m['boxes'] = m['boxes'] + [
                        {'label': 'UNASSIGNED', 'box_xy': [70, 70],
                         'box_wh': [1380, 40 + 72 * len(missing)], 'button_xy': None,
                         'rows': [{'symbol': None, 'number': None, 'joy': k, 'type': 'Digital'}
                                  for k in missing]}]
                    existing = dict(existing)
                    existing['mapping_json'] = json.dumps(m)
                    draft_note = (f'{len(missing)} inputs from "{from_id}" missing from the mapping, '
                                  f'added as an UNASSIGNED box (not saved yet)')
                else:
                    draft_note = f'Nothing to enrich: "{from_id}" is already covered by the mapping'
            except Exception as e:
                draft_note = f'Cannot enrich: {e}'

    if existing and '(not saved yet)' in draft_note:
        existing = {**existing, '_unsaved_seed': True}
    existing_json = json.dumps(existing) if existing else 'null'
    editor_user, _ = current_user()
    return render_template('admin/mapping_editor.html', existing_json=existing_json,
                           draft_note=draft_note, editor_user=editor_user)


@admin_bp.route('/mapping-editor/upload', methods=['POST'])
@require_mapper
def mapping_editor_upload():
    """Save an uploaded clean controller image to the persistent controllers/ dir."""
    from flask import jsonify
    from PIL import Image as PILImage
    f = request.files.get('image')
    if not f or not f.filename:
        return jsonify({'error': 'No image provided'}), 400
    name = slugify(request.form.get('name') or f.filename.rsplit('.', 1)[0])
    if not name:
        return jsonify({'error': 'Invalid name'}), 400
    from uuid import uuid4
    name = f'{name[:100]}-{uuid4().hex}'
    cdir = Config.configsPath() / 'controllers'
    cdir.mkdir(parents=True, exist_ok=True)
    try:
        img = PILImage.open(f.stream).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Bad image: {e}'}), 400
    if request.form.get('pad'):
        # Card canvas helper: place the photo in the middle third of a wider
        # white canvas so boxes get side margins (what was hand-composed for
        # the AEROMAX card). Skip if the photo is already wide (ratio > 2).
        if img.width < img.height * 2:
            canvas = PILImage.new('RGB', (img.width * 3, img.height), 'white')
            canvas.paste(img, (img.width, 0))
            img = canvas
    img.save(str(cdir / f'{name}.jpg'), quality=92)
    user_name, _ = current_user()
    database.log_mapping_action('upload-image', user_name, None, None,
                                f'{name}.jpg ({img.width}x{img.height})')
    return jsonify({'name': name, 'width': img.width, 'height': img.height,
                    'url': url_for('web.serve_config', path=f'controllers/{name}.jpg')})


@admin_bp.route('/mapping-editor/import-pdf', methods=['POST'])
@require_mapper
def mapping_editor_import_pdf():
    """Import a manufacturer AcroForm reference sheet (VIRPIL-style):
    returns the rendered artwork image + every writing area as a
    pre-positioned no_chrome box with its Joy mapping."""
    from flask import jsonify
    from scripts.pdf_import import extract_mapping_from_pdf
    f = request.files.get('pdf')
    if not f or not f.filename:
        return jsonify({'error': 'No PDF provided'}), 400
    pdf_bytes = f.read()
    if len(pdf_bytes) > 20 * 1024 * 1024:
        return jsonify({'error': 'PDF too large (20MB max)'}), 400
    name = slugify(request.form.get('name') or f.filename.rsplit('.', 1)[0])
    if not name:
        return jsonify({'error': 'Invalid name'}), 400
    from uuid import uuid4
    name = f'{name[:100]}-{uuid4().hex}'
    try:
        mapping, jpg = extract_mapping_from_pdf(pdf_bytes)
    except Exception as e:
        return jsonify({'error': f'Cannot parse this PDF: {e}'}), 400
    cdir = Config.configsPath() / 'controllers'
    cdir.mkdir(parents=True, exist_ok=True)
    with open(str(cdir / f'{name}.jpg'), 'wb') as out:
        out.write(jpg)
    user_name, _ = current_user()
    database.log_mapping_action('import-pdf', user_name, None, None,
                                f'{f.filename} -> {name}.jpg, {len(mapping["boxes"])} boxes')
    return jsonify({**mapping, 'name': name, 'width': mapping['width'], 'height': mapping['height'],
                    'boxes': mapping['boxes'],
                    'title': mapping.get('title') or f.filename.rsplit('.', 1)[0],
                    'url': url_for('web.serve_config', path=f'controllers/{name}.jpg')})


def _purge_old_previews(folder, max_age_seconds=3600):
    """Editor previews are one-shot images: drop those older than an hour
    (nothing else ever removed them). Never raises."""
    import time
    cutoff = time.time() - max_age_seconds
    try:
        for path in folder.glob('ddpreview-*.jpg'):
            try:
                if path.stat().st_mtime < cutoff:
                    path.unlink()
            except OSError:
                pass
    except OSError:
        pass


@admin_bp.route('/mapping-editor/preview', methods=['POST'])
@require_mapper
def mapping_editor_preview():
    """Render a draft, optionally using a saved .binds, without saving a mapping."""
    import re
    import uuid
    from flask import jsonify
    from scripts import createDataDrivenImage
    from scripts.mapping_validation import validate_mapping
    from scripts.mapping_runtime import missing_inputs, used_inputs
    from scripts.parser import DISPLAY_GROUP_FIELDS
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Expected a JSON object.'}), 400
    mapping = data.get('mapping')
    physical_keys, modifiers, coverage = None, None, None
    device_ids = mapping.get('device_ids', []) if isinstance(mapping, dict) else []
    device_index = 0
    try:
        validate_mapping(mapping)
        reference = data.get('reference', '')
        if not isinstance(reference, str):
            raise ValueError('Enter a saved configuration reference, not a URL.')
        reference = reference.strip()
        if reference:
            if not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', reference):
                raise ValueError('Enter the reference after /binds/ in the card URL.')
            source = Config(reference).pathWithSuffix('.binds')
            if not source.is_file():
                return jsonify({'error': 'The .binds source for this reference is not available.'}), 404
            preview_errors = Errors()
            physical_keys, modifiers, devices = parseBindings(
                reference, source.read_text(encoding='utf-8-sig'),
                list(DISPLAY_GROUP_FIELDS.values()), preview_errors)
            if preview_errors.errors:
                raise ValueError('This reference does not contain a valid .binds XML file.')
            matched = [key for key in devices
                       if key.split('::')[0].upper() in {v.upper() for v in device_ids}]
            if not matched:
                raise ValueError('No bound inputs for this hardware ID were found in that reference.')
            # Default to the first matching instance. Explicit indices permit
            # profiles containing two identical controllers to be reviewed.
            selected_index = data.get('device_index')
            device_index = min(int(key.split('::')[1]) for key in matched)
            if selected_index is not None:
                if type(selected_index) is not int or selected_index < 0:
                    raise ValueError('Device index must be a non-negative integer.')
                device_index = selected_index
            selected_ids = [key.split('::')[0] for key in matched
                            if int(key.split('::')[1]) == device_index]
            if not selected_ids:
                raise ValueError('That device index has no bound inputs in this reference.')
            device_ids = selected_ids
            used = used_inputs(physical_keys, modifiers, device_ids, device_index)
            coverage = {'used_inputs': len(used), 'missing_inputs': missing_inputs(mapping, used),
                        'device_index': device_index, 'device_ids': device_ids}
    except (ValueError, UnicodeError) as exc:
        return jsonify({'error': str(exc)}), 400
    # Unique output prevents concurrent mapper previews overwriting one another.
    config = Config('ddpreview-' + uuid.uuid4().hex)
    config.makeDir()
    _purge_old_previews(config.path().parent)
    try:
        createDataDrivenImage(mapping, config, public=False, physicalKeys=physical_keys,
                              modifiers=modifiers, imageDevices=device_ids,
                              deviceIndex=device_index)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as e:
        logError(f'Mapping preview failed: {e}')
        return jsonify({'error': 'Preview failed. Check the image and box geometry, then retry.'}), 500
    image_name = mapping['image'] if device_index == 0 else f"{mapping['image']}-{device_index}"
    return jsonify({'url': url_for('web.serve_config',
                                  path=f'dd/{config.name}-{image_name}.jpg'),
                    'coverage': coverage})


@admin_bp.route('/mapping-editor/lint', methods=['POST'])
@require_mapper
def mapping_editor_lint():
    """Quality checks for the draft being edited (nothing is saved)."""
    from flask import jsonify
    from scripts.mapping_lint import lint_mapping
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Expected a JSON object.'}), 400
    return jsonify({'issues': lint_mapping(data.get('mapping'))})


@admin_bp.route('/mapping-editor/references')
@require_mapper
def mapping_editor_references():
    """Recent uploads that bind this controller, for the preview picker.
    Only cards whose .binds source is still on disk can be previewed."""
    from flask import jsonify
    ids = [part.strip() for part in (request.args.get('devices') or '').split(',')]
    ids = [part for part in ids if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', part)][:20]
    references = []
    for row in database.list_recent_configs_for_device_ids(ids, limit=40):
        if not Config.isValidName(row['id']) or not Config(row['id']).pathWithSuffix('.binds').is_file():
            continue
        references.append({'id': row['id'], 'description': row.get('description') or '',
                           'date': str(row.get('created_at') or '')[:10]})
        if len(references) >= 15:
            break
    return jsonify({'references': references})


def _notify_discord_mapping(title, message, fields=None):
    """Ping the (backup) Discord webhook about mapper activity. Never raises."""
    try:
        from .backup import DiscordNotifier
        DiscordNotifier.from_settings().send_notification(title, message, fields=fields)
    except Exception:
        pass


@admin_bp.route('/mapping-editor/save', methods=['POST'])
@require_mapper
def mapping_editor_save():
    """Save a draft, preserving the public revision and existing hardware IDs."""
    from flask import jsonify
    from scripts.mapping_validation import validate_mapping
    data = request.get_json(force=True) or {}
    if not isinstance(data, dict):
        return jsonify({'error': 'Expected a JSON object.'}), 400
    mapping = data.get('mapping') or {}
    try:
        validate_mapping(mapping)
        device_id = str(data.get('device_id') or '').strip().upper()
        if not device_id:
            raise ValueError('Enter a hardware ID before saving.')
        device_name = str(data.get('device_name') or mapping.get('title') or '').strip()
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    user_name, role = current_user()
    try:
        fresh = database.save_controller_draft(device_id, device_name, mapping, user_name,
                                               data.get('base_updated_at'), data.get('mapping_id'))
    except database.MappingConflict as exc:
        return jsonify({'error': str(exc)}), 409
    database.log_mapping_action('save-draft', user_name, fresh['id'], device_id,
                                f"{len(mapping['boxes'])} boxes; public revision unchanged")
    if role != 'admin':
        _notify_discord_mapping('Mapping draft saved',
                                f'{user_name} saved "{device_name}" ({device_id}). Awaiting review on /admin/controllers.')
    import json
    return jsonify({'ok': True, 'id': fresh['id'], 'status': 'draft',
                    'public_status': fresh['status'],
                    'device_ids': json.loads(fresh['mapping_json'])['device_ids'],
                    'updated_at': str(fresh['updated_at'])})
