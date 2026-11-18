#!/usr/bin/env python3
"""
EDRefCard Database Module

SQLite database for storing configurations and device information.
"""

import sqlite3
import datetime
import json
import re
from pathlib import Path
from contextlib import contextmanager

# Database file location
DB_PATH = None  # Set by init_db()


def init_db(db_path):
    """Initialize the database connection and create tables if needed.
    
    Args:
        db_path: Path to the SQLite database file
    """
    global DB_PATH
    DB_PATH = Path(db_path)
    
    # Create parent directory if needed
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Create tables
    with get_db() as conn:
        conn.executescript("""
            -- Configurations (reference cards)
            CREATE TABLE IF NOT EXISTS configurations (
                id TEXT PRIMARY KEY,
                description TEXT DEFAULT '',
                styling TEXT DEFAULT 'None',
                keyboard_display TEXT DEFAULT 'text',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_public INTEGER DEFAULT 1,
                is_featured INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                unhandled_devices_warnings TEXT DEFAULT '',
                device_warnings TEXT DEFAULT '',
                misconfiguration_warnings TEXT DEFAULT ''
            );
            
            -- Devices associated with a configuration
            CREATE TABLE IF NOT EXISTS config_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_id TEXT NOT NULL,
                device_key TEXT NOT NULL,
                device_display_name TEXT,
                FOREIGN KEY (config_id) REFERENCES configurations(id) ON DELETE CASCADE,
                UNIQUE(config_id, device_key)
            );
            
            -- Display groups selected for a configuration
            CREATE TABLE IF NOT EXISTS config_display_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_id TEXT NOT NULL,
                group_name TEXT NOT NULL,
                FOREIGN KEY (config_id) REFERENCES configurations(id) ON DELETE CASCADE,
                UNIQUE(config_id, group_name)
            );
            
            -- Controller template mappings (for admin mapping tool)
            CREATE TABLE IF NOT EXISTS controller_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL UNIQUE,
                device_name TEXT NOT NULL,
                template_name TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                image_width INTEGER NOT NULL,
                image_height INTEGER NOT NULL,
                mapping_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Named admin-panel users (role 'admin' = full panel,
            -- 'mapper' = controllers + mapping editor only)
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'mapper',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );

            -- Audit trail of controller-mapping actions (who did what when)
            CREATE TABLE IF NOT EXISTS mapping_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mapping_id INTEGER,
                device_id TEXT,
                action TEXT NOT NULL,
                actor TEXT,
                detail TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Saved revisions of controller mappings (rollback safety net for
            -- autonomous mapper work; pruned to the most recent per mapping)
            CREATE TABLE IF NOT EXISTS controller_mapping_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mapping_id INTEGER NOT NULL,
                device_name TEXT,
                mapping_json TEXT NOT NULL,
                saved_by TEXT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Unknown controllers seen at generation time (admin triage queue)
            CREATE TABLE IF NOT EXISTS unknown_device_sightings (
                device_id TEXT PRIMARY KEY,
                sighting_count INTEGER NOT NULL DEFAULT 1,
                last_run_id TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Runtime aliases for legacy templates, reviewed by a mapper.
            -- This keeps hardware-ID additions out of the source file while
            -- allowing a confirmed variant to use an existing legacy card.
            CREATE TABLE IF NOT EXISTS legacy_device_aliases (
                device_id TEXT PRIMARY KEY,
                legacy_key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT
            );

            -- Create indexes
            CREATE INDEX IF NOT EXISTS idx_config_created ON configurations(created_at);
            CREATE INDEX IF NOT EXISTS idx_config_public ON configurations(is_public);
            CREATE INDEX IF NOT EXISTS idx_config_devices_config ON config_devices(config_id);
            CREATE INDEX IF NOT EXISTS idx_controller_mappings_device ON controller_mappings(device_id);
            CREATE INDEX IF NOT EXISTS idx_mapping_versions_mapping ON controller_mapping_versions(mapping_id);
        """)
        
        # Initialize backup-related tables
        from admin.backup import init_backup_tables
        init_backup_tables(conn)

        # Add keyboard_display column if it doesn't exist (migration for existing DBs)
        try:
            conn.execute("ALTER TABLE configurations ADD COLUMN keyboard_display TEXT DEFAULT 'text'")
        except Exception:
            pass  # Column already exists

        # Draft/review workflow for controller mappings (mapper saves are
        # drafts, hidden from public rendering until an admin publishes).
        # Pre-existing mappings default to published.
        for ddl in ("ALTER TABLE controller_mappings ADD COLUMN status TEXT NOT NULL DEFAULT 'published'",
                    "ALTER TABLE controller_mappings ADD COLUMN updated_by TEXT"):
            try:
                conn.execute(ddl)
            except Exception:
                pass  # Column already exists

        migrate_controller_publications(conn)


def migrate_controller_publications(conn):
    """Preserve the currently published document before introducing draft edits.

    Additive and repeatable: never replace an existing publication snapshot.
    """
    columns = {r[1] for r in conn.execute('PRAGMA table_info(controller_mappings)')}
    for name, definition in (('published_snapshot', 'TEXT'),
                             ('has_draft', 'INTEGER NOT NULL DEFAULT 0')):
        if name not in columns:
            try:
                conn.execute(f'ALTER TABLE controller_mappings ADD COLUMN {name} {definition}')
            except sqlite3.OperationalError as exc:
                if 'duplicate column name' not in str(exc):
                    raise
    for row in conn.execute("SELECT * FROM controller_mappings WHERE status = 'published' "
                            "AND published_snapshot IS NULL").fetchall():
        conn.execute('UPDATE controller_mappings SET published_snapshot = ? WHERE id = ?',
                     (json.dumps(_publication_document(dict(row))), row['id']))


def _publication_document(row):
    return {key: row[key] for key in ('device_name', 'template_name', 'image_filename',
                                     'image_width', 'image_height', 'mapping_json')}


@contextmanager
def get_db():
    """Get a database connection context manager."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ============== Configuration CRUD ==============

def create_configuration(config_id, description='', styling='None', display_groups=None,
                         devices=None, keyboard_display='text', unhandled_warnings='',
                         device_warnings='', misc_warnings='', created_at=None,
                         is_public=True):
    """Create a new configuration in the database.
    
    Args:
        config_id: Unique 6-character identifier
        description: User description
        styling: Styling mode ('None', 'Group', 'Category', 'Modifier')
        display_groups: List of group names
        devices: Dictionary of device_key -> device_info
        unhandled_warnings: Warning about unsupported devices
        device_warnings: Device-specific warnings
        misc_warnings: Misconfiguration warnings
        created_at: Timestamp (defaults to now)
    """
    if created_at is None:
        created_at = datetime.datetime.now(datetime.UTC)
    
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO configurations
            (id, description, styling, keyboard_display, created_at,
             unhandled_devices_warnings, device_warnings, misconfiguration_warnings,
             is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (config_id, description, styling, keyboard_display, created_at,
              unhandled_warnings, device_warnings, misc_warnings,
              1 if is_public else 0))
        
        # Insert display groups
        if display_groups:
            conn.executemany("""
                INSERT OR IGNORE INTO config_display_groups (config_id, group_name)
                VALUES (?, ?)
            """, [(config_id, group) for group in display_groups])
        
        # Insert devices
        if devices:
            for device_key, device_info in devices.items():
                display_name = None
                if device_info and isinstance(device_info, dict):
                    display_name = device_info.get('Template', device_key)
                conn.execute("""
                    INSERT OR REPLACE INTO config_devices 
                    (config_id, device_key, device_display_name)
                    VALUES (?, ?, ?)
                """, (config_id, device_key, display_name))


def get_configuration(config_id):
    """Get a configuration by ID.
    
    Returns:
        Dictionary with config data or None
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM configurations WHERE id = ?", (config_id,)
        ).fetchone()
        
        if row is None:
            return None
        
        config = dict(row)
        
        # Get display groups
        groups = conn.execute(
            "SELECT group_name FROM config_display_groups WHERE config_id = ?",
            (config_id,)
        ).fetchall()
        config['display_groups'] = [g['group_name'] for g in groups]
        
        # Get devices
        devices = conn.execute(
            "SELECT device_key, device_display_name FROM config_devices WHERE config_id = ?",
            (config_id,)
        ).fetchall()
        config['devices'] = {d['device_key']: d['device_display_name'] for d in devices}
        
        return config


def list_configurations(page=1, per_page=50, public_only=True, search=None, device_filter=None, **kwargs):
    """List configurations with pagination.
    
    Args:
        page: Page number (1-indexed)
        per_page: Items per page
        public_only: Only show public configurations
        search: Search term for description
        device_filter: Filter by device name (LIKE)
        **kwargs: Additional filters like device_filters (list of names for IN)
    
    Returns:
        Tuple of (list of configs, total count)
    """
    offset = (page - 1) * per_page
    params = []
    where_clauses = []
    
    if public_only:
        where_clauses.append("c.is_public = 1")
    
    if search:
        # Search in description OR in device names (both display_name and device_key)
        # Using parameterized queries to prevent SQL injection
        where_clauses.append("""(
            c.description LIKE ? 
            OR c.id IN (
                SELECT config_id FROM config_devices 
                WHERE device_display_name LIKE ? OR device_key LIKE ?
            )
        )""")
        search_pattern = f"%{search}%"
        params.extend([search_pattern, search_pattern, search_pattern])
    
    if device_filter:
        where_clauses.append("""
            c.id IN (SELECT config_id FROM config_devices WHERE device_display_name LIKE ?)
        """)
        params.append(f"%{device_filter}%")

    device_filters = kwargs.get('device_filters')
    if device_filters:
        placeholders = ', '.join(['?'] * len(device_filters))
        where_clauses.append(f"c.id IN (SELECT config_id FROM config_devices WHERE device_display_name IN ({placeholders}))")
        params.extend(device_filters)
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    with get_db() as conn:
        # Get total count
        count = conn.execute(
            f"SELECT COUNT(*) FROM configurations c WHERE {where_sql}",
            params
        ).fetchone()[0]
        
        # Get page of results
        rows = conn.execute(f"""
            SELECT c.*, GROUP_CONCAT(DISTINCT cd.device_display_name) as device_names
            FROM configurations c
            LEFT JOIN config_devices cd ON c.id = cd.config_id
            WHERE {where_sql}
            GROUP BY c.id
            ORDER BY c.created_at DESC
            LIMIT ? OFFSET ?
        """, params + [per_page, offset]).fetchall()
        
        configs = [dict(row) for row in rows]
        
    return configs, count


def update_configuration(config_id, **kwargs):
    """Update a configuration.
    
    Args:
        config_id: Configuration ID
        **kwargs: Fields to update (description, is_public, is_featured)
    """
    allowed_fields = {'description', 'is_public', 'is_featured', 'styling'}
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return
    
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [config_id]
    
    with get_db() as conn:
        conn.execute(
            f"UPDATE configurations SET {set_clause} WHERE id = ?",
            values
        )


def replace_configuration(config_id, **kwargs):
    """Recreate a configuration with new metadata, keeping its counters.

    Used when an original replaces a degraded earlier import of the same
    card: display groups and devices are rebuilt from scratch, view_count
    and is_featured survive.
    """
    with get_db() as conn:
        old = conn.execute(
            "SELECT view_count, is_featured FROM configurations WHERE id = ?",
            (config_id,)).fetchone()
        conn.execute("DELETE FROM config_display_groups WHERE config_id = ?", (config_id,))
        conn.execute("DELETE FROM config_devices WHERE config_id = ?", (config_id,))
        conn.execute("DELETE FROM configurations WHERE id = ?", (config_id,))
    create_configuration(config_id, **kwargs)
    if old is not None:
        with get_db() as conn:
            conn.execute(
                "UPDATE configurations SET view_count = ?, is_featured = ? WHERE id = ?",
                (old['view_count'], old['is_featured'], config_id))


def delete_configuration(config_id):
    """Delete a configuration and its associated files.
    
    Args:
        config_id: Configuration ID
    """
    with get_db() as conn:
        conn.execute("DELETE FROM configurations WHERE id = ?", (config_id,))


def get_configuration_stats():
    """Get statistics about configurations.
    
    Returns:
        Dictionary with stats
    """
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM configurations").fetchone()[0]
        public = conn.execute(
            "SELECT COUNT(*) FROM configurations WHERE is_public = 1"
        ).fetchone()[0]
        
        # Configs per day (last 30 days)
        daily = conn.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM configurations
            WHERE created_at >= DATE('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """).fetchall()
        
        # Most popular devices
        popular_devices = conn.execute("""
            SELECT device_display_name, COUNT(*) as count
            FROM config_devices
            WHERE device_display_name IS NOT NULL
            GROUP BY device_display_name
            ORDER BY count DESC
            LIMIT 10
        """).fetchall()
        
        device_types = conn.execute("""
            SELECT COUNT(DISTINCT device_display_name) FROM config_devices
            WHERE device_display_name IS NOT NULL AND device_display_name != 'keyboard'
        """).fetchone()[0]
        last_30_days = conn.execute(
            "SELECT COUNT(*) FROM configurations WHERE DATE(created_at) > DATE('now', '-30 days')"
        ).fetchone()[0]

        return {
            'total_configurations': total,
            'public_configurations': public,
            'device_types': device_types,
            'last_30_days': last_30_days,
            'daily_stats': [dict(d) for d in daily],
            'popular_devices': [dict(d) for d in popular_devices]
        }

def get_daily_creations(days, today=None):
    """Cards created per UTC day over the last `days` days, today included.

    Returns [(date, count)] oldest first, with a 0 for each day without a card.
    """
    import datetime
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    start = today - datetime.timedelta(days=days - 1)
    with get_db() as conn:
        rows = conn.execute("""
            SELECT DATE(created_at) AS day, COUNT(*) AS count
            FROM configurations
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY DATE(created_at)
        """, (start.isoformat(), today.isoformat())).fetchall()
    counts = {row['day']: row['count'] for row in rows}
    return [(day, counts.get(day.isoformat(), 0))
            for day in (start + datetime.timedelta(days=i) for i in range(days))]


def get_monthly_creations(since='2024-01', today=None):
    """Cards created per UTC month from `since` (YYYY-MM) to the current month.

    Returns [('YYYY-MM', count)] oldest first, with a 0 for each empty month.
    """
    import datetime
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    with get_db() as conn:
        rows = conn.execute("""
            SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS count
            FROM configurations
            WHERE substr(created_at, 1, 7) BETWEEN ? AND ?
            GROUP BY month
        """, (since, today.strftime('%Y-%m'))).fetchall()
    counts = {row['month']: row['count'] for row in rows}
    year, month = map(int, since.split('-'))
    months = []
    while (year, month) <= (today.year, today.month):
        key = '%04d-%02d' % (year, month)
        months.append((key, counts.get(key, 0)))
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return months


def get_controller_cards(days, today=None):
    """Which controllers the cards of the last `days` days were made for.

    Returns (cards in the period, distinct [(template name, config id)]),
    keyboards and unrecognised devices left out.
    """
    import datetime
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    period = ((today - datetime.timedelta(days=days - 1)).isoformat(), today.isoformat())
    with get_db() as conn:
        total = conn.execute("""SELECT COUNT(*) FROM configurations
            WHERE DATE(created_at) BETWEEN ? AND ?""", period).fetchone()[0]
        pairs = conn.execute("""
            SELECT DISTINCT d.device_display_name, d.config_id
            FROM config_devices d JOIN configurations c ON c.id = d.config_id
            WHERE DATE(c.created_at) BETWEEN ? AND ?
              AND d.device_display_name IS NOT NULL AND d.device_display_name != 'keyboard'
        """, period).fetchall()
    return total, [(row[0], row[1]) for row in pairs]


def get_device_counts(public_only=False):
    """Get count of configurations for each device type.
    
    Args:
        public_only: If True, only count public configurations with descriptions.
        
    Returns:
        Dictionary mapping device_display_name to count
    """
    where_clause = ""
    if public_only:
        where_clause = "WHERE c.is_public = 1 AND c.description != ''"
        
    with get_db() as conn:
        rows = conn.execute(f"""
            SELECT cd.device_display_name, COUNT(DISTINCT cd.config_id) as count
            FROM config_devices cd
            JOIN configurations c ON cd.config_id = c.id
            {where_clause}
            GROUP BY cd.device_display_name
        """).fetchall()
        return {r['device_display_name']: r['count'] for r in rows}


def get_all_device_names():
    """Get all unique device names from configurations.
    
    Returns:
        List of device names
    """
    with get_db() as conn:
        rows = conn.execute("""
            SELECT DISTINCT device_display_name 
            FROM config_devices 
            WHERE device_display_name IS NOT NULL
            ORDER BY device_display_name
        """).fetchall()
        
    return [r['device_display_name'] for r in rows] # type: ignore


def get_all_config_ids():
    """Get all configuration IDs from the database.
    
    Returns:
        Set of configuration IDs
    """
    with get_db() as conn:
        rows = conn.execute("SELECT id FROM configurations").fetchall()
        return {r['id'] for r in rows}


# ============== Controller Mapping CRUD ==============

def create_controller_mapping(device_id, device_name, template_name, image_filename,
                               image_width, image_height, mapping_json,
                               status='published', updated_by=None):
    """Create a new controller mapping.
    
    Args:
        device_id: Device ID (e.g., '231D0300')
        device_name: Display name (e.g., 'VKB Gladiator Ultra 2026')
        template_name: Template filename without extension
        image_filename: Filename of the controller image
        image_width: Image width in pixels
        image_height: Image height in pixels
        mapping_json: JSON string with button mappings
        
    Returns:
        ID of created mapping
    """
    import datetime
    now = datetime.datetime.now(datetime.UTC)
    
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO controller_mappings
            (device_id, device_name, template_name, image_filename,
             image_width, image_height, mapping_json, created_at, updated_at,
             status, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (device_id, device_name, template_name, image_filename,
              image_width, image_height, mapping_json, now, now,
              status, updated_by))
        if status == 'published':
            row = conn.execute('SELECT * FROM controller_mappings WHERE id = ?',
                               (cursor.lastrowid,)).fetchone()
            conn.execute('UPDATE controller_mappings SET published_snapshot = ? WHERE id = ?',
                         (json.dumps(_publication_document(dict(row))), cursor.lastrowid))
        return cursor.lastrowid


def get_controller_mapping(mapping_id):
    """Get a controller mapping by ID.
    
    Args:
        mapping_id: Mapping ID
        
    Returns:
        Dictionary with mapping data or None
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM controller_mappings WHERE id = ?", (mapping_id,)
        ).fetchone()
        
        return dict(row) if row else None


def get_controller_mapping_by_device_id(device_id):
    """Get a controller mapping by device ID.

    Case-insensitive: Elite .binds emit device IDs in uppercase hex, but a
    mapper may type them in any case in the editor. Matching on UPPER() keeps
    a lowercase-entered mapping working (and out of the unknown-device queue).

    Args:
        device_id: Device ID (e.g., '231D0300')

    Returns:
        Dictionary with mapping data or None
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM controller_mappings WHERE UPPER(device_id) = UPPER(?)",
            (device_id,)
        ).fetchone()

        return dict(row) if row else None


def list_controller_mappings():
    """List all controller mappings.
    
    Returns:
        List of mapping dictionaries
    """
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, device_id, device_name, template_name, created_at, updated_at
            FROM controller_mappings
            ORDER BY created_at DESC
        """).fetchall()
        
        return [dict(row) for row in rows]


def update_controller_mapping(mapping_id, **kwargs):
    """Update a controller mapping.
    
    Args:
        mapping_id: Mapping ID
        **kwargs: Fields to update
    """
    import datetime
    
    allowed_fields = {'device_name', 'template_name', 'image_filename',
                      'image_width', 'image_height', 'mapping_json',
                      'status', 'updated_by'}
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return
    
    updates['updated_at'] = datetime.datetime.now(datetime.UTC)
    
    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [mapping_id]
    
    with get_db() as conn:
        conn.execute(
            f"UPDATE controller_mappings SET {set_clause} WHERE id = ?",
            values
        )


def delete_controller_mapping(mapping_id):
    """Delete a controller mapping.
    
    Args:
        mapping_id: Mapping ID
    """
    with get_db() as conn:
        conn.execute("DELETE FROM controller_mappings WHERE id = ?", (mapping_id,))


def save_mapping_version(mapping_id, device_name, mapping_json, saved_by=None,
                         keep=20):
    """Record a mapping revision (called on every editor save/rollback),
    pruning history beyond the `keep` most recent entries."""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO controller_mapping_versions
            (mapping_id, device_name, mapping_json, saved_by)
            VALUES (?, ?, ?, ?)
        """, (mapping_id, device_name, mapping_json, saved_by))
        conn.execute("""
            DELETE FROM controller_mapping_versions
            WHERE mapping_id = ? AND id NOT IN (
                SELECT id FROM controller_mapping_versions
                WHERE mapping_id = ? ORDER BY id DESC LIMIT ?
            )
        """, (mapping_id, mapping_id, keep))


def list_mapping_versions(mapping_id):
    """Version history of one mapping, newest first (no mapping_json payload)."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, mapping_id, device_name, saved_by, saved_at,
                   length(mapping_json) AS json_size
            FROM controller_mapping_versions
            WHERE mapping_id = ? ORDER BY id DESC
        """, (mapping_id,)).fetchall()
        return [dict(r) for r in rows]


def get_mapping_version(version_id):
    """One full version row (with mapping_json) or None."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM controller_mapping_versions WHERE id = ?",
            (version_id,)).fetchone()
        return dict(row) if row else None


def get_all_controller_mappings():
    """Return all controller mappings as full dicts (including mapping_json).

    Used at generation time to build a device-id -> mapping index for the
    data-driven render path.
    """
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM controller_mappings").fetchall()
        return [dict(r) for r in rows]


class MappingConflict(ValueError):
    """The submitted base is stale or the requested identity already exists."""


def _record_mapping_version(conn, row, actor):
    conn.execute('INSERT INTO controller_mapping_versions '
                 '(mapping_id, device_name, mapping_json, saved_by) VALUES (?, ?, ?, ?)',
                 (row['id'], row['device_name'], row['mapping_json'], actor))
    conn.execute('DELETE FROM controller_mapping_versions WHERE mapping_id = ? AND id NOT IN '
                 '(SELECT id FROM controller_mapping_versions WHERE mapping_id = ? '
                 'ORDER BY id DESC LIMIT 20)', (row['id'], row['id']))


def save_controller_draft(device_id, device_name, mapping, actor, base_updated_at=None,
                          mapping_id=None):
    """Save a draft and its history in one serialized transaction, never publish.

    Existing aliases are preserved even for older clients sending only one ID.
    BEGIN IMMEDIATE makes checking the base and updating it one atomic operation.
    """
    import copy
    document = copy.deepcopy(mapping)
    device_id = str(device_id).strip().upper()
    with get_db() as conn:
        conn.execute('BEGIN IMMEDIATE')
        if mapping_id is not None:
            row = conn.execute('SELECT * FROM controller_mappings WHERE id = ?',
                               (mapping_id,)).fetchone()
            if row is None or row['device_id'].upper() != device_id:
                raise MappingConflict('This mapping was removed or its identity changed. Reload before saving.')
        else:
            row = conn.execute('SELECT * FROM controller_mappings WHERE UPPER(device_id) = ?',
                               (device_id,)).fetchone()
        previous = dict(row) if row else None
        if previous and str(previous['updated_at'] or '') != str(base_updated_at or ''):
            raise MappingConflict('A newer revision exists. Download your JSON, then reload and compare before saving.')
        if not previous and base_updated_at:
            raise MappingConflict('The original mapping no longer exists. Download your JSON before reloading.')
        old_ids = json.loads(previous['mapping_json']).get('device_ids', []) if previous else []
        document['device_ids'] = list(dict.fromkeys(
            str(value).strip().upper() for value in
            [device_id, *old_ids, *(document.get('device_ids') or [])] if str(value).strip()))
        # A new draft must not silently steal an ID from another controller.
        wanted = set(document['device_ids'])
        for other in conn.execute('SELECT * FROM controller_mappings').fetchall():
            if previous and other['id'] == previous['id']:
                continue
            ids = set(str(v).upper() for v in json.loads(other['mapping_json']).get('device_ids', []))
            ids.add(other['device_id'].upper())
            if other['published_snapshot']:
                live = json.loads(other['published_snapshot'])
                ids.update(str(v).upper() for v in json.loads(live['mapping_json']).get('device_ids', []))
            if wanted & ids:
                raise MappingConflict('One of these hardware IDs already belongs to another controller.')
        now = datetime.datetime.now(datetime.UTC).isoformat()
        payload = json.dumps(document)
        if previous:
            if not conn.execute('SELECT 1 FROM controller_mapping_versions WHERE mapping_id = ?',
                                (previous['id'],)).fetchone():
                _record_mapping_version(conn, previous, previous.get('updated_by'))
            mid = previous['id']
            conn.execute('UPDATE controller_mappings SET device_name = ?, template_name = ?, '
                         'image_filename = ?, image_width = ?, image_height = ?, mapping_json = ?, '
                         'updated_at = ?, updated_by = ?, has_draft = 1 WHERE id = ?',
                         (device_name, document['image'], document['image'] + '.jpg',
                          document['width'], document['height'], payload, now, actor, mid))
        else:
            mid = conn.execute('INSERT INTO controller_mappings '
                               '(device_id, device_name, template_name, image_filename, image_width, '
                               'image_height, mapping_json, updated_at, updated_by, status, has_draft) '
                               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', 1)",
                               (device_id, device_name, document['image'], document['image'] + '.jpg',
                                document['width'], document['height'], payload, now, actor)).lastrowid
        fresh = dict(conn.execute('SELECT * FROM controller_mappings WHERE id = ?', (mid,)).fetchone())
        _record_mapping_version(conn, fresh, actor)
        return fresh


def set_controller_publication(mapping_id, state, base_updated_at, actor):
    """Publish exactly the reviewed revision, or explicitly take it offline."""
    if state not in ('published', 'draft'):
        raise ValueError('Invalid publication state.')
    with get_db() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row = conn.execute('SELECT * FROM controller_mappings WHERE id = ?', (mapping_id,)).fetchone()
        if not row or str(row['updated_at']) != str(base_updated_at):
            raise MappingConflict('This mapping changed since you opened the page. Review the latest revision first.')
        now = datetime.datetime.now(datetime.UTC).isoformat()
        if state == 'published':
            mapping = json.loads(row['mapping_json'])
            pending = []
            for box in mapping.get('boxes', []):
                for entry in box.get('rows', []):
                    if mapping.get('input_verification_required') or 'verification' in entry:
                        valid = re.fullmatch(r'Joy_(?:[1-9][0-9]*|(?:X|Y|Z|RX|RY|RZ|U|V)Axis|POV[1-9][0-9]*(?:Up|Right|Down|Left))', entry.get('joy') or '')
                        if entry.get('verification') != 'verified' or not valid:
                            pending.append(box.get('label', 'Unnamed input'))
            if pending:
                raise MappingConflict(f'Publication blocked: {len(pending)} input(s) still need a valid game code and owner verification.')
            conn.execute('UPDATE controller_mappings SET published_snapshot = ?, status = ?, '
                         'has_draft = 0, updated_at = ?, updated_by = ? WHERE id = ?',
                         (json.dumps(_publication_document(dict(row))), state, now, actor, mapping_id))
        else:
            conn.execute('UPDATE controller_mappings SET status = ?, updated_at = ?, updated_by = ? '
                         'WHERE id = ?', (state, now, actor, mapping_id))


def get_published_controller_mappings():
    """Public consumers must never read editable draft documents."""
    result = []
    for row in get_all_controller_mappings():
        if row.get('status') != 'published' or not row.get('published_snapshot'):
            continue
        result.append({**row, **json.loads(row['published_snapshot'])})
    return result


def get_render_dependencies():
    """Compact description of everything shared that a rendered card depends on:
    the published controller mappings and the legacy hardware aliases.

    Part of the render-cache signature: publishing, unpublishing or editing a
    mapping, or attaching an alias, changes this value and so invalidates
    every cached card on its next view.
    """
    with get_db() as conn:
        mappings = conn.execute(
            "SELECT id, updated_at FROM controller_mappings "
            "WHERE status = 'published' ORDER BY id").fetchall()
        aliases = conn.execute(
            "SELECT device_id, legacy_key FROM legacy_device_aliases "
            "ORDER BY device_id").fetchall()
    return [[row['id'], str(row['updated_at'])] for row in mappings], \
           [[row['device_id'], row['legacy_key']] for row in aliases]


def record_unknown_device(device_id, run_id):
    """Upsert a sighting of an unmapped controller (admin triage queue).

    Returns True when this is the FIRST sighting of the device (callers can
    notify on new hardware without spamming on every upload)."""
    with get_db() as conn:
        known = conn.execute(
            "SELECT 1 FROM unknown_device_sightings WHERE device_id = ?",
            (device_id,)).fetchone()
        conn.execute("""
            INSERT INTO unknown_device_sightings (device_id, last_run_id)
            VALUES (?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                sighting_count = sighting_count + 1,
                last_run_id = excluded.last_run_id,
                last_seen = CURRENT_TIMESTAMP
        """, (device_id, run_id))
        return known is None


def list_unknown_devices():
    """Return unknown-device sightings, most requested first."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM unknown_device_sightings
            ORDER BY sighting_count DESC, last_seen DESC
        """).fetchall()
        return [dict(r) for r in rows]


def dismiss_unknown_device(device_id):
    """Remove a device from the unknown-sightings queue."""
    with get_db() as conn:
        conn.execute("DELETE FROM unknown_device_sightings WHERE device_id = ?",
                     (device_id,))


def list_legacy_device_aliases():
    """Return reviewed aliases from hardware IDs to legacy controller keys."""
    with get_db() as conn:
        rows = conn.execute(
            'SELECT device_id, legacy_key, created_at, created_by '
            'FROM legacy_device_aliases ORDER BY legacy_key, device_id').fetchall()
        return [dict(row) for row in rows]


def get_legacy_device_alias(device_id):
    with get_db() as conn:
        row = conn.execute(
            'SELECT * FROM legacy_device_aliases WHERE device_id = ?',
            (device_id,)).fetchone()
        return dict(row) if row else None


def attach_legacy_device_alias(device_id, legacy_key, actor):
    """Persist a mapper-reviewed alias. Existing aliases are never replaced silently."""
    with get_db() as conn:
        existing = conn.execute(
            'SELECT * FROM legacy_device_aliases WHERE device_id = ?',
            (device_id,)).fetchone()
        if existing and existing['legacy_key'] != legacy_key:
            raise ValueError(f'{device_id} is already attached to {existing["legacy_key"]}.')
        conn.execute(
            'INSERT OR IGNORE INTO legacy_device_aliases (device_id, legacy_key, created_by) '
            'VALUES (?, ?, ?)', (device_id, legacy_key, actor))


def count_configs_for_device_ids(device_ids):
    """Count distinct configurations using any of these hardware IDs.

    config_devices.device_key is '<ID>::<index>'; data-driven devices have no
    display name there, so counting by key prefix is the reliable route.
    """
    if not device_ids:
        return 0
    with get_db() as conn:
        clauses = " OR ".join("device_key LIKE ?" for _ in device_ids)
        row = conn.execute(
            f"SELECT COUNT(DISTINCT config_id) AS n FROM config_devices WHERE {clauses}",
            [f"{did}::%" for did in device_ids]).fetchone()
        return row['n'] if row else 0


def list_recent_configs_for_device_ids(device_ids, limit=15):
    """Most recent configurations binding any of these hardware IDs.

    Feeds the mapping editor's preview picker: a mapper reviews a draft
    against real uploads instead of typing a card reference by hand.
    """
    device_ids = [str(did).strip() for did in device_ids or [] if str(did).strip()]
    if not device_ids:
        return []
    with get_db() as conn:
        clauses = " OR ".join("UPPER(cd.device_key) LIKE ?" for _ in device_ids)
        rows = conn.execute(f"""
            SELECT c.id, c.description, c.created_at
            FROM configurations c
            WHERE c.id IN (SELECT cd.config_id FROM config_devices cd WHERE {clauses})
            ORDER BY c.created_at DESC
            LIMIT ?
        """, [f"{did.upper()}::%" for did in device_ids] + [limit]).fetchall()
        return [dict(row) for row in rows]


# ---- controller-mapping audit trail ----

def log_mapping_action(action, actor, mapping_id=None, device_id=None, detail=None):
    """Append an entry to the mapping audit trail. Never raises."""
    try:
        with get_db() as conn:
            conn.execute("""
                INSERT INTO mapping_audit_log (mapping_id, device_id, action, actor, detail)
                VALUES (?, ?, ?, ?, ?)
            """, (mapping_id, device_id, action, actor, detail))
    except Exception:
        pass


def list_mapping_audit(limit=30):
    """Return the most recent mapping audit entries."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM mapping_audit_log ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]


# ---- admin-panel users (session auth) ----

def create_user(username, password_hash, role='mapper'):
    """Create a named admin-panel user. Returns the new user id."""
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role))
        return cur.lastrowid


def get_user_by_username(username):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?",
                           (username,)).fetchone()
        return dict(row) if row else None


def list_users():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, username, role, created_at, last_login FROM users "
            "ORDER BY username").fetchall()
        return [dict(r) for r in rows]


def delete_user(user_id):
    with get_db() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


def update_user_password(user_id, password_hash):
    with get_db() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                     (password_hash, user_id))


def touch_user_login(user_id):
    with get_db() as conn:
        conn.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                     (user_id,))
