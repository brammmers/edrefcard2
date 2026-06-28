#!/usr/bin/env python3
"""
EDRefCard Database Module

SQLite database for storing configurations and device information.
"""

import sqlite3
import datetime
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
            
            -- Create indexes
            CREATE INDEX IF NOT EXISTS idx_config_created ON configurations(created_at);
            CREATE INDEX IF NOT EXISTS idx_config_public ON configurations(is_public);
            CREATE INDEX IF NOT EXISTS idx_config_devices_config ON config_devices(config_id);
            CREATE INDEX IF NOT EXISTS idx_controller_mappings_device ON controller_mappings(device_id);
        """)
        
        # Initialize backup-related tables
        from admin.backup import init_backup_tables
        init_backup_tables(conn)

        # Add keyboard_display column if it doesn't exist (migration for existing DBs)
        try:
            conn.execute("ALTER TABLE configurations ADD COLUMN keyboard_display TEXT DEFAULT 'text'")
        except Exception:
            pass  # Column already exists


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
                         device_warnings='', misc_warnings='', created_at=None):
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
             unhandled_devices_warnings, device_warnings, misconfiguration_warnings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (config_id, description, styling, keyboard_display, created_at, 
              unhandled_warnings, device_warnings, misc_warnings))
        
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

    if kwargs.get('device_filters'):
        device_filters = kwargs.get('device_filters')
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
        
        return {
            'total_configurations': total,
            'public_configurations': public,
            'daily_stats': [dict(d) for d in daily],
            'popular_devices': [dict(d) for d in popular_devices]
        }

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
#!/usr/bin/env python3
"""
Controller Mappings CRUD functions for database.py
Append these functions to www/scripts/database.py
"""

# ============== Controller Mapping CRUD ==============

def create_controller_mapping(device_id, device_name, template_name, image_filename,
                               image_width, image_height, mapping_json):
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
             image_width, image_height, mapping_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (device_id, device_name, template_name, image_filename,
              image_width, image_height, mapping_json, now, now))
        
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
    
    Args:
        device_id: Device ID (e.g., '231D0300')
        
    Returns:
        Dictionary with mapping data or None
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM controller_mappings WHERE device_id = ?", (device_id,)
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
                      'image_width', 'image_height', 'mapping_json'}
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
