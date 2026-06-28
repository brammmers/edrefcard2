#!/usr/bin/env python3
"""
EDRefCard Admin Blueprint

Flask Blueprint for administration functionality.
"""

import sys
import re
import shutil
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from scripts import database, parseBindings, slugify

from scripts.models import Config, Errors
from .auth import require_admin




# Create blueprint
admin_bp = Blueprint('admin', __name__, 
                     url_prefix='/admin',
                     template_folder='templates')




@admin_bp.route('/')
@require_admin
def dashboard():
    """Admin dashboard with statistics."""
    stats = database.get_configuration_stats()
    return render_template('admin/dashboard.html', stats=stats)



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
    
    # Get config path to delete files
    config = Config(config_id)
    config_path = config.path().parent
    
    # Delete from database
    db.delete_configuration(config_id)

    
    # Delete files on disk
    if config_path.exists():
        try:
            shutil.rmtree(config_path)
        except Exception as e:
            flash(f'Warning: Could not delete files: {e}', 'warning')
    
    flash(f'Configuration {config_id} deleted.', 'success')
    return redirect(url_for('admin.list_configs'))


@admin_bp.route('/configs/<config_id>/purge-pdf', methods=['POST'])
@require_admin
def purge_pdf(config_id):
    """Purge generated PDF files for a configuration."""
    config = Config(config_id)
    config_path = config.path().parent

    
    purged_count = 0
    errors = []
    
    # Look for PDF files in the config directory
    if config_path.exists():
        for pdf_file in config_path.glob('*.pdf'):
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


@admin_bp.route('/devices')
@require_admin
def list_devices():
    """List all supported devices."""
    from scripts.bindingsData import supportedDevices
    
    # Sort devices by name
    devices = sorted(supportedDevices.items(), key=lambda x: x[0])
    
    return render_template('admin/devices.html', devices=devices)



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
    
    # Directory listing
    config_files = []
    subdir = request.args.get('subdir')
    
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
                           sys_path=sys.path,
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
            display_groups = ['Ship', 'SRV', 'OnFoot', 'UI', 'Galaxy map', 'Head look', 
                              'Scanners', 'Fighter', 'Multicrew', 'Camera', 'Holo-Me', 'Misc']
            
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
    from .backup import get_backup_settings, save_backup_settings
    
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
        
        # Don't overwrite password if not provided (keep existing)
        if not settings['sftp_password']:
            existing = get_backup_settings()
            settings['sftp_password'] = existing.get('sftp_password', '')
        
        save_backup_settings(settings)
        flash('Backup settings saved.', 'success')
        return redirect(url_for('admin.backup_settings'))
    
    settings = get_backup_settings()
    return render_template('admin/backup_settings.html', settings=settings)


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
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz') as tmp:
            file.save(tmp.name)
            tmp_path = Path(tmp.name)
        
        # Perform restore
        restore_manager = RestoreManager()
        results = restore_manager.restore_from_archive(
            tmp_path,
            restore_db=restore_db,
            restore_binds=restore_binds
        )
        
        # Cleanup temp file
        tmp_path.unlink(missing_ok=True)
        
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
    print("[ROUTE] restore_from_sftp called")
    from .backup import RestoreManager, SFTPManager, DiscordNotifier
    
    filename = request.form.get('filename')
    print(f"[ROUTE] filename={filename}")
    
    if not filename:
        flash('No backup file selected.', 'danger')
        return redirect(url_for('admin.restore_dashboard'))
    
    restore_db = request.form.get('restore_db') == 'on'
    restore_binds = request.form.get('restore_binds') == 'on'
    print(f"[ROUTE] restore_db={restore_db}, restore_binds={restore_binds}")
    
    if not restore_db and not restore_binds:
        flash('Please select at least one component to restore.', 'warning')
        return redirect(url_for('admin.restore_dashboard'))
    
    try:
        print("[ROUTE] Connecting to SFTP...")
        # Download from SFTP
        sftp_manager = SFTPManager.from_settings()
        print(f"[ROUTE] SFTP host: {sftp_manager.host}")
        local_path = sftp_manager.download_backup(filename)
        print(f"[ROUTE] Downloaded to: {local_path}")
        
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
