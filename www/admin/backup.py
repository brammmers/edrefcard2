#!/usr/bin/env python3
"""
EDRefCard Backup Module

Provides backup/restore functionality with SFTP support, Discord notifications,
and maintenance mode integration.
"""

import os
import json
import shutil
import tarfile
import tempfile
import datetime
import logging
import signal
from pathlib import Path

import paramiko
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from scripts.models import Config

logger = logging.getLogger(__name__)


# ============== Encryption Utilities ==============

def _get_fernet_key() -> bytes:
    """Derive a Fernet key from FLASK_SECRET_KEY."""
    secret = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key').encode()
    # Use PBKDF2 to derive a proper 32-byte key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'edrefcard_backup_salt',  # Static salt is OK since key is already secret
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret))
    return key


def encrypt_password(password: str) -> str:
    """Encrypt a password using Fernet."""
    if not password:
        return ''
    f = Fernet(_get_fernet_key())
    return f.encrypt(password.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    """Decrypt a password using Fernet."""
    if not encrypted:
        return ''
    try:
        f = Fernet(_get_fernet_key())
        return f.decrypt(encrypted.encode()).decode()
    except Exception as e:
        logger.error(f"Failed to decrypt password: {e}")
        return ''


# ============== Database Functions for Backup Settings ==============

def init_backup_tables(conn):
    """Initialize backup-related tables. Called from database.init_db()."""
    conn.executescript("""
        -- Backup settings (singleton table)
        CREATE TABLE IF NOT EXISTS backup_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            sftp_enabled INTEGER DEFAULT 0,
            sftp_host TEXT,
            sftp_port INTEGER DEFAULT 22,
            sftp_user TEXT,
            sftp_password_encrypted TEXT,
            sftp_remote_dir TEXT DEFAULT '/backups/edrefcard',
            auto_backup_enabled INTEGER DEFAULT 0,
            backup_schedule_hour INTEGER DEFAULT 4,
            discord_webhook_url TEXT,
            last_backup_at TEXT,
            last_backup_status TEXT,
            updated_at TEXT
        );
        
        -- Backup history log
        CREATE TABLE IF NOT EXISTS backup_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_type TEXT NOT NULL,
            filename TEXT NOT NULL,
            size_bytes INTEGER,
            includes_db INTEGER DEFAULT 1,
            includes_binds INTEGER DEFAULT 1,
            uploaded_to_sftp INTEGER DEFAULT 0,
            status TEXT NOT NULL,
            error_message TEXT,
            created_at TEXT NOT NULL
        );
        
        -- Application state
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        );
    """)


def get_backup_settings() -> dict:
    """Get backup settings from database."""
    from scripts import database
    with database.get_db() as conn:
        row = conn.execute("SELECT * FROM backup_settings WHERE id = 1").fetchone()
        if row:
            settings = dict(row)
            # Decrypt password when reading
            if settings.get('sftp_password_encrypted'):
                settings['sftp_password'] = decrypt_password(settings['sftp_password_encrypted'])
            else:
                settings['sftp_password'] = ''
            return settings
        return {
            'sftp_enabled': False,
            'sftp_host': '',
            'sftp_port': 22,
            'sftp_user': '',
            'sftp_password': '',
            'sftp_remote_dir': '/backups/edrefcard',
            'auto_backup_enabled': False,
            'backup_schedule_hour': 4,
            'discord_webhook_url': '',
        }


def save_backup_settings(settings: dict) -> None:
    """Save backup settings to database."""
    from scripts import database
    now = datetime.datetime.now(datetime.UTC).isoformat()
    
    # Encrypt password before saving
    encrypted_password = ''
    if settings.get('sftp_password'):
        encrypted_password = encrypt_password(settings['sftp_password'])
    
    with database.get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO backup_settings 
            (id, sftp_enabled, sftp_host, sftp_port, sftp_user, sftp_password_encrypted,
             sftp_remote_dir, auto_backup_enabled, backup_schedule_hour, discord_webhook_url,
             updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1 if settings.get('sftp_enabled') else 0,
            settings.get('sftp_host', ''),
            settings.get('sftp_port', 22),
            settings.get('sftp_user', ''),
            encrypted_password,
            settings.get('sftp_remote_dir', '/backups/edrefcard'),
            1 if settings.get('auto_backup_enabled') else 0,
            settings.get('backup_schedule_hour', 4),
            settings.get('discord_webhook_url', ''),
            now
        ))


def log_backup_history(backup_type: str, filename: str, size_bytes: int,
                       includes_db: bool, includes_binds: bool,
                       uploaded_to_sftp: bool, status: str, 
                       error_message: str = '') -> None:
    """Log a backup operation to history."""
    from scripts import database
    now = datetime.datetime.now(datetime.UTC).isoformat()
    
    with database.get_db() as conn:
        conn.execute("""
            INSERT INTO backup_history 
            (backup_type, filename, size_bytes, includes_db, includes_binds,
             uploaded_to_sftp, status, error_message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (backup_type, filename, size_bytes, 
              1 if includes_db else 0, 1 if includes_binds else 0,
              1 if uploaded_to_sftp else 0, status, error_message, now))


def get_backup_history(limit: int = 20) -> list:
    """Get recent backup history."""
    from scripts import database
    with database.get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM backup_history
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]


# ============== App State (Maintenance Mode) ==============

def get_app_state(key: str, default: str = '') -> str:
    """Get an app state value."""
    from scripts import database
    with database.get_db() as conn:
        row = conn.execute(
            "SELECT value FROM app_state WHERE key = ?", (key,)
        ).fetchone()
        return row['value'] if row else default


def set_app_state(key: str, value: str) -> None:
    """Set an app state value."""
    from scripts import database
    now = datetime.datetime.now(datetime.UTC).isoformat()
    with database.get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO app_state (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, now))


def is_maintenance_mode() -> bool:
    """Check if maintenance mode is active."""
    return get_app_state('maintenance_mode', '0') == '1'


def set_maintenance_mode(enabled: bool, message: str = '') -> None:
    """Enable or disable maintenance mode."""
    set_app_state('maintenance_mode', '1' if enabled else '0')
    if message:
        set_app_state('maintenance_message', message)


def get_maintenance_message() -> str:
    """Get the maintenance mode message."""
    return get_app_state('maintenance_message', 'System is under maintenance. Please try again later.')


# ============== Backup Manager ==============

class BackupManager:
    """Handles creating and managing backups."""
    
    def __init__(self):
        self.configs_path = Config.configsPath()
        self.data_path = Path(__file__).parent.parent / 'data'
        self.backup_dir = self.data_path / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Debug logging
        print(f"[BackupManager] configs_path: {self.configs_path}")
        print(f"[BackupManager] data_path: {self.data_path}")
        print(f"[BackupManager] backup_dir: {self.backup_dir}")
    
    def create_backup(self, include_db: bool = True, include_binds: bool = True,
                      backup_type: str = 'manual') -> Path:
        """Create a backup archive.
        
        Args:
            include_db: Include SQLite database
            include_binds: Include .binds files
            backup_type: Type of backup ('manual', 'scheduled', 'pre_restore')
            
        Returns:
            Path to created backup archive
        """
        timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')
        filename = f"backup_{timestamp}.tar.gz"
        final_backup_path = self.backup_dir / filename
        
        # Use a temporary file to avoid concurrent write corruption
        temp_fd, temp_path_str = tempfile.mkstemp(suffix='.tar.gz', dir=str(self.backup_dir))
        temp_path = Path(temp_path_str)
        os.close(temp_fd)  # Close the fd since tarfile will open it
        
        # Create metadata
        metadata = {
            'version': '1.0',
            'created_at': datetime.datetime.now(datetime.UTC).isoformat(),
            'backup_type': backup_type,
            'includes_db': include_db,
            'includes_binds': include_binds,
        }
        
        try:
            with tarfile.open(temp_path, 'w:gz') as tar:
                # Add metadata
                metadata_json = json.dumps(metadata, indent=2)
                metadata_bytes = metadata_json.encode('utf-8')
                
                # Create a tarinfo for metadata
                import io
                metadata_io = io.BytesIO(metadata_bytes)
                tarinfo = tarfile.TarInfo(name='metadata.json')
                tarinfo.size = len(metadata_bytes)
                tarinfo.mtime = datetime.datetime.now().timestamp()
                tar.addfile(tarinfo, metadata_io)
                
                # Add database - check configs_path first, then data_path
                if include_db:
                    db_path = self.configs_path / 'edrefcard.db'
                    if not db_path.exists():
                        db_path = self.data_path / 'edrefcard.db'
                    if db_path.exists():
                        tar.add(db_path, arcname='database/edrefcard.db')
                        logger.info(f"Added database from {db_path}")
                
                # Add binds files only (no images/PDFs)
                if include_binds:
                    for binds_file in self.configs_path.rglob('*.binds'):
                        rel_path = binds_file.relative_to(self.configs_path)
                        tar.add(binds_file, arcname=f'binds/{rel_path}')
            
            # Atomically rename temp file to final location
            import shutil
            shutil.move(str(temp_path), str(final_backup_path))
            backup_path = final_backup_path
            
            # Get file size
            size_bytes = backup_path.stat().st_size
            
            # Log to history
            log_backup_history(
                backup_type=backup_type,
                filename=filename,
                size_bytes=size_bytes,
                includes_db=include_db,
                includes_binds=include_binds,
                uploaded_to_sftp=False,
                status='success'
            )
            
            # Update last backup time
            from scripts import database
            with database.get_db() as conn:
                now = datetime.datetime.now(datetime.UTC).isoformat()
                conn.execute(
                    "UPDATE backup_settings SET last_backup_at = ?, last_backup_status = ? WHERE id = 1",
                    (now, 'success')
                )
            
            logger.info(f"Backup created: {filename} ({size_bytes} bytes)")
            return backup_path
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass
            log_backup_history(
                backup_type=backup_type,
                filename=filename,
                size_bytes=0,
                includes_db=include_db,
                includes_binds=include_binds,
                uploaded_to_sftp=False,
                status='failed',
                error_message=str(e)
            )
            raise
    
    def list_local_backups(self) -> list:
        """List local backup files."""
        backups = []
        for f in self.backup_dir.glob('backup_*.tar.gz'):
            try:
                stat = f.stat()
                backups.append({
                    'filename': f.name,
                    'path': str(f),
                    'size_bytes': stat.st_size,
                    'created_at': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except Exception as e:
                logger.warning(f"Could not stat backup file {f}: {e}")
        
        # Sort by created_at descending
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 1) -> int:
        """Remove old local backups, keeping only the most recent ones.
        
        Args:
            keep_count: Number of backups to keep
            
        Returns:
            Number of backups deleted
        """
        backups = self.list_local_backups()
        deleted = 0
        
        for backup in backups[keep_count:]:
            try:
                Path(backup['path']).unlink()
                deleted += 1
                logger.info(f"Deleted old backup: {backup['filename']}")
            except Exception as e:
                logger.warning(f"Could not delete backup {backup['filename']}: {e}")
        
        return deleted
    
    def get_backup_path(self, filename: str) -> Path | None:
        """Get full path to a backup file."""
        path = self.backup_dir / filename
        if path.exists() and path.is_file():
            return path
        return None


# ============== SFTP Manager ==============

class SFTPManager:
    """Handles SFTP operations for remote backups."""
    
    def __init__(self, host: str, port: int, user: str, password: str, remote_dir: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.remote_dir = remote_dir
    
    @classmethod
    def from_settings(cls) -> 'SFTPManager':
        """Create an SFTPManager from saved settings."""
        settings = get_backup_settings()
        return cls(
            host=settings.get('sftp_host', ''),
            port=settings.get('sftp_port', 22),
            user=settings.get('sftp_user', ''),
            password=settings.get('sftp_password', ''),
            remote_dir=settings.get('sftp_remote_dir', '/backups/edrefcard')
        )
    
    def _connect(self) -> paramiko.SFTPClient:
        """Establish SFTP connection."""
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.user, password=self.password)
        return paramiko.SFTPClient.from_transport(transport)
    
    def test_connection(self) -> tuple[bool, str]:
        """Test SFTP connection.
        
        Returns:
            Tuple of (success, message)
        """
        if not self.host:
            return False, "SFTP host not configured"
        
        try:
            sftp = self._connect()
            
            # Try to list the remote directory
            try:
                sftp.listdir(self.remote_dir)
            except OSError:
                # Directory doesn't exist, try to create it
                try:
                    sftp.mkdir(self.remote_dir)
                except OSError:
                    pass  # Parent dirs might not exist
            
            sftp.close()
            return True, f"Successfully connected to {self.host}"
            
        except paramiko.AuthenticationException:
            return False, "Authentication failed - check username/password"
        except paramiko.SSHException as e:
            return False, f"SSH error: {e}"
        except TimeoutError:
            return False, f"Connection timeout to {self.host}:{self.port}"
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    def upload_backup(self, backup_path: Path) -> bool:
        """Upload a backup to remote SFTP server.
        
        Args:
            backup_path: Local path to backup file
            
        Returns:
            True if upload successful
        """
        try:
            sftp = self._connect()
            
            # Ensure remote directory exists
            try:
                sftp.stat(self.remote_dir)
            except OSError:
                # Create directory path recursively
                parts = self.remote_dir.strip('/').split('/')
                current = ''
                for part in parts:
                    current += '/' + part
                    try:
                        sftp.stat(current)
                    except OSError:
                        sftp.mkdir(current)
            
            remote_path = f"{self.remote_dir}/{backup_path.name}"
            sftp.put(str(backup_path), remote_path)
            sftp.close()
            
            logger.info(f"Uploaded backup to {remote_path}")
            return True
            
        except Exception as e:
            logger.error(f"SFTP upload failed: {e}")
            raise
    
    def list_remote_backups(self) -> list:
        """List backups on remote SFTP server."""
        backups = []
        
        try:
            sftp = self._connect()
            
            try:
                files = sftp.listdir_attr(self.remote_dir)
                for f in files:
                    if f.filename.startswith('backup_') and f.filename.endswith('.tar.gz'):
                        backups.append({
                            'filename': f.filename,
                            'size_bytes': f.st_size,
                            'created_at': datetime.datetime.fromtimestamp(f.st_mtime).isoformat() if f.st_mtime else '',
                        })
            except OSError:
                pass  # Directory doesn't exist yet
            
            sftp.close()
            
        except Exception as e:
            logger.error(f"Failed to list remote backups: {e}")
            raise
        
        # Sort by filename (which contains timestamp) descending
        backups.sort(key=lambda x: x['filename'], reverse=True)
        return backups
    
    def download_backup(self, remote_filename: str) -> Path:
        """Download a backup from remote SFTP server.
        
        Args:
            remote_filename: Name of the backup file on remote
            
        Returns:
            Path to downloaded file (in temp directory)
        """
        try:
            sftp = self._connect()
            
            remote_path = f"{self.remote_dir}/{remote_filename}"
            local_path = Path(tempfile.gettempdir()) / remote_filename
            
            sftp.get(remote_path, str(local_path))
            sftp.close()
            
            logger.info(f"Downloaded backup from {remote_path}")
            return local_path
            
        except Exception as e:
            logger.error(f"SFTP download failed: {e}")
            raise
    
    def cleanup_remote(self, retention_days: int = 7) -> int:
        """Remove old backups from remote server.
        
        Args:
            retention_days: Keep backups newer than this many days
            
        Returns:
            Number of backups deleted
        """
        deleted = 0
        # Use naive datetime for comparison with SFTP timestamps (which are naive)
        cutoff = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        
        try:
            sftp = self._connect()
            
            try:
                files = sftp.listdir_attr(self.remote_dir)
                for f in files:
                    if f.filename.startswith('backup_') and f.filename.endswith('.tar.gz'):
                        if f.st_mtime and datetime.datetime.fromtimestamp(f.st_mtime) < cutoff:
                            remote_path = f"{self.remote_dir}/{f.filename}"
                            sftp.remove(remote_path)
                            deleted += 1
                            logger.info(f"Deleted old remote backup: {f.filename}")
            except OSError:
                pass
            
            sftp.close()
            
        except Exception as e:
            logger.error(f"Failed to cleanup remote backups: {e}")
        
        return deleted


# ============== Restore Manager ==============

class RestoreManager:
    """Handles restoring from backups."""
    
    def __init__(self):
        self.configs_path = Config.configsPath()
        self.data_path = Path(__file__).parent.parent / 'data'
        self.backup_manager = BackupManager()
    
    def restore_from_archive(self, archive_path: Path, 
                             restore_db: bool = True,
                             restore_binds: bool = True,
                             create_safety_backup: bool = True) -> dict:
        """Restore from a backup archive.
        
        Args:
            archive_path: Path to backup archive
            restore_db: Restore the database
            restore_binds: Restore binds files
            create_safety_backup: Create a backup before restore
            
        Returns:
            Dictionary with restore results
        """
        results = {
            'success': False,
            'safety_backup': None,
            'db_restored': False,
            'binds_restored': 0,
            'errors': []
        }
        
        # Enable maintenance mode during restore
        set_maintenance_mode(True, 'System restore in progress...')
        
        try:
            # Create safety backup first
            if create_safety_backup:
                try:
                    safety_path = self.backup_manager.create_backup(
                        include_db=restore_db,
                        include_binds=restore_binds,
                        backup_type='pre_restore'
                    )
                    results['safety_backup'] = str(safety_path)
                except Exception as e:
                    results['errors'].append(f"Safety backup failed: {e}")
            
            # Extract and restore
            with tarfile.open(archive_path, 'r:gz') as tar:
                # Read metadata
                try:
                    metadata_file = tar.extractfile('metadata.json')
                    if metadata_file:
                        metadata = json.loads(metadata_file.read().decode('utf-8'))
                        logger.info(f"Restoring backup from {metadata.get('created_at', 'unknown')}")
                except Exception as e:
                    logger.warning(f"Could not read backup metadata: {e}")
                
                # Restore database
                if restore_db:
                    try:
                        db_member = tar.getmember('database/edrefcard.db')
                        print(f"[RESTORE] Found database in backup: {db_member.name}")
                        
                        with tempfile.TemporaryDirectory() as tmpdir:
                            tar.extract(db_member, path=tmpdir)
                            extracted_db = Path(tmpdir) / 'database' / 'edrefcard.db'
                            
                            # ALWAYS restore to configs_path - that's where the app reads from
                            # (as configured by EDREFCARD_CONFIGS_DIR)
                            target_db = self.configs_path / 'edrefcard.db'
                            target_db.parent.mkdir(parents=True, exist_ok=True)
                            
                            print(f"[RESTORE] Extracted DB size: {extracted_db.stat().st_size} bytes")
                            print(f"[RESTORE] Target path: {target_db}")
                            
                            # Check current DB state before overwrite
                            if target_db.exists():
                                print(f"[RESTORE] Existing DB size: {target_db.stat().st_size} bytes")
                            else:
                                print("[RESTORE] No existing DB at target path")
                            
                            # Copy the restored database
                            shutil.copy2(extracted_db, target_db)
                            
                            print(f"[RESTORE] After copy, DB size: {target_db.stat().st_size} bytes")
                            
                            results['db_restored'] = True
                            results['db_path'] = str(target_db)
                            logger.info(f"Database restored to {target_db}")
                            print(f"[RESTORE] Database restored successfully to {target_db}")
                            
                    except KeyError:
                        print("[RESTORE] ERROR: Database not found in backup archive")
                        results['errors'].append("Database not found in backup")
                    except Exception as e:
                        print(f"[RESTORE] ERROR: Database restore failed: {e}")
                        results['errors'].append(f"Database restore failed: {e}")
                
                # Restore binds files
                if restore_binds:
                    binds_count = 0
                    for member in tar.getmembers():
                        if member.name.startswith('binds/') and member.name.endswith('.binds'):
                            try:
                                # Extract relative path
                                rel_path = member.name[6:]  # Remove 'binds/' prefix
                                target_path = self.configs_path / rel_path
                                
                                # Create parent directory
                                target_path.parent.mkdir(parents=True, exist_ok=True)
                                
                                # Extract file
                                with tempfile.TemporaryDirectory() as tmpdir:
                                    tar.extract(member, path=tmpdir)
                                    extracted_file = Path(tmpdir) / member.name
                                    shutil.copy2(extracted_file, target_path)
                                    binds_count += 1
                            except Exception as e:
                                results['errors'].append(f"Failed to restore {member.name}: {e}")
                    
                    results['binds_restored'] = binds_count
                    logger.info(f"Restored {binds_count} binds files")
            
            results['success'] = len(results['errors']) == 0
            
            # CRITICAL: Reinitialize database connection after restore
            # SQLite keeps the old file handle, so we must reconnect
            if restore_db and results['db_restored']:
                try:
                    from scripts import database
                    # Use the path where we actually restored the DB
                    db_path = results.get('db_path')
                    if db_path:
                        database.init_db(db_path)
                        logger.info(f"Database reconnected: {db_path}")
                        print(f"[RESTORE] Database reconnected: {db_path}")
                except Exception as e:
                    results['errors'].append(f"Database reconnection failed: {e}")
                    logger.error(f"Database reconnection failed: {e}")
            
            # Signal Gunicorn to reload all workers (multi-worker fix)
            if results['success'] and restore_db and results['db_restored']:
                try:
                    reloaded = self.reload_gunicorn()
                    if reloaded:
                        results['gunicorn_reloaded'] = True
                        print("[RESTORE] Gunicorn HUP signal sent - workers will reload")
                except Exception as e:
                    # Don't fail the restore if reload fails
                    print(f"[RESTORE] Warning: Gunicorn reload failed: {e}")
            
        except Exception as e:
            results['errors'].append(f"Restore failed: {e}")
            logger.error(f"Restore failed: {e}")
        
        finally:
            # Disable maintenance mode
            set_maintenance_mode(False)
        
        return results
    
    def reload_gunicorn(self) -> bool:
        """Send HUP signal to Gunicorn master process for graceful reload.
        
        Returns:
            True if signal sent successfully
        """
        try:
            # In a Gunicorn environment, the master PID is in a file or we can use os.getppid()
            # For most setups, sending HUP to the parent process triggers reload
            parent_pid = os.getppid()
            os.kill(parent_pid, signal.SIGHUP)
            logger.info(f"Sent HUP signal to Gunicorn master (PID {parent_pid})")
            return True
        except Exception as e:
            logger.error(f"Failed to reload Gunicorn: {e}")
            return False


# ============== Discord Notifier ==============

class DiscordNotifier:
    """Sends notifications to Discord webhook."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    @classmethod
    def from_settings(cls) -> 'DiscordNotifier':
        """Create a DiscordNotifier from saved settings."""
        settings = get_backup_settings()
        return cls(webhook_url=settings.get('discord_webhook_url', ''))
    
    def send_notification(self, title: str, message: str, 
                          success: bool = True, fields: list = None) -> bool:
        """Send a notification to Discord.
        
        Args:
            title: Embed title
            message: Embed description
            success: True for green color, False for red
            fields: Optional list of {'name': ..., 'value': ...} dicts
            
        Returns:
            True if notification sent successfully
        """
        if not self.webhook_url:
            return False
        
        embed = {
            'title': title,
            'description': message,
            'color': 0x28a745 if success else 0xdc3545,  # Green or red
            'timestamp': datetime.datetime.now(datetime.UTC).isoformat(),
            'footer': {'text': 'EDRefCard Backup System'}
        }
        
        if fields:
            embed['fields'] = fields
        
        payload = {'embeds': [embed]}
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Discord notification failed: {e}")
            return False
    
    def test_webhook(self) -> tuple[bool, str]:
        """Test the Discord webhook.
        
        Returns:
            Tuple of (success, message)
        """
        if not self.webhook_url:
            return False, "Discord webhook URL not configured"
        
        success = self.send_notification(
            title="🔔 Test Notification",
            message="This is a test notification from EDRefCard backup system.",
            success=True
        )
        
        if success:
            return True, "Test notification sent successfully"
        else:
            return False, "Failed to send test notification"


# ============== Scheduled Backup Job ==============

def run_scheduled_backup():
    """Run the scheduled nightly backup job."""
    
    # Verify settings at runtime (in case it was disabled in UI without restarting workers)
    settings = get_backup_settings()
    if not settings.get('auto_backup_enabled'):
        logger.info("Scheduled backup skipped (disabled in settings)")
        return
        
    logger.info("Running scheduled backup...")
    
    try:
        # Create backup
        backup_manager = BackupManager()
        backup_path = backup_manager.create_backup(backup_type='scheduled')
        
        # Upload to SFTP if enabled
        settings = get_backup_settings()
        uploaded = False
        
        if settings.get('sftp_enabled') and settings.get('sftp_host'):
            try:
                sftp_manager = SFTPManager.from_settings()
                sftp_manager.upload_backup(backup_path)
                
                # Update history to mark as uploaded
                from scripts import database
                with database.get_db() as conn:
                    conn.execute("""
                        UPDATE backup_history 
                        SET uploaded_to_sftp = 1 
                        WHERE filename = ?
                    """, (backup_path.name,))
                
                # Cleanup old remote backups
                sftp_manager.cleanup_remote(retention_days=7)
                uploaded = True
                
            except Exception as e:
                logger.error(f"SFTP upload failed during scheduled backup: {e}")
        
        # Cleanup old local backups (keep only 1)
        backup_manager.cleanup_old_backups(keep_count=1)
        
        # Send Discord notification
        notifier = DiscordNotifier.from_settings()
        if notifier.webhook_url:
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            notifier.send_notification(
                title="✅ Scheduled Backup Complete",
                message="Nightly backup completed successfully.",
                success=True,
                fields=[
                    {'name': 'Filename', 'value': backup_path.name, 'inline': True},
                    {'name': 'Size', 'value': f"{size_mb:.2f} MB", 'inline': True},
                    {'name': 'Uploaded to SFTP', 'value': 'Yes' if uploaded else 'No', 'inline': True},
                ]
            )
        
        logger.info(f"Scheduled backup completed: {backup_path.name}")
        
    except Exception as e:
        logger.error(f"Scheduled backup failed: {e}")
        
        # Send failure notification
        notifier = DiscordNotifier.from_settings()
        if notifier.webhook_url:
            notifier.send_notification(
                title="❌ Scheduled Backup Failed",
                message=f"The nightly backup encountered an error:\n```{e}```",
                success=False
            )
