import click
import time
import re
from flask.cli import with_appcontext

@click.command('clean-cache')
@click.option('--days', default=1, help='Delete files older than X days')
@with_appcontext
def clean_cache_command(days):
    """Delete generated images older than the specified number of days."""
    from flask import current_app
    
    configs_dir = current_app.config['CONFIGS_FOLDER']
    if not configs_dir.exists():
        click.echo(f"Configs directory not found: {configs_dir}")
        return

    now = time.time()
    cutoff = now - (days * 86400)
    count = 0
    
    click.echo(f"Cleaning files older than {days} days in {configs_dir}...")
    
    # Generated cards live in the two-character prefix folders
    # (configs/<id[:2]>/<id>-<template>.jpg). The previous top-level glob
    # never matched anything. Cards are regenerated on their next view;
    # .binds sources, controller photos and backups are never touched.
    for folder in configs_dir.iterdir():
        if not folder.is_dir() or len(folder.name) > 2:
            continue
        for ext in ('*.jpg', '*.pdf', '*-render.json'):
            for file_path in folder.glob(ext):
                try:
                    if file_path.stat().st_mtime < cutoff:
                        file_path.unlink()
                        count += 1
                except OSError as e:
                    click.echo(f"Error deleting {file_path}: {e}")

    click.echo(f"Deleted {count} files.")


@click.command('find-unsupported')
@click.argument('logfile', type=click.Path(exists=True), required=False)
@with_appcontext
def find_unsupported_command(logfile):
    """Extract unsupported controls from logs.
    
    If no logfile is provided, it will check the standard error log location 
    if configured, or warn the user.
    """
    if not logfile:
        click.echo("Please provide a log file to analyze.")
        # In a real deployed env, we might default to /var/log/edrefcard.err
        return

    pattern = re.compile(r'.*No control for (.+)')
    unsupported = set()
    
    try:
        with open(logfile, encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    unsupported.add(match.group(1))
        
        if unsupported:
            click.echo(f"Found {len(unsupported)} unsupported controls:")
            for control in sorted(unsupported):
                click.echo(control)
        else:
            click.echo("No unsupported controls found in the log.")
            
    except Exception as e:
        click.echo(f"Error reading log file: {e}")



@click.command('import-defaults')
@click.option('--limit', default=None, type=int, help='Limit number of files to import')
@with_appcontext
def import_defaults_command(limit):
    """Import default bindings from bindings/Defaults 3.3."""
    from flask import current_app
    from scripts import database, parser
    from scripts.models import Config, Errors
    
    # Path to Defaults 3.3 relative to www root (parent of www is project root)
    # www/../bindings/Defaults 3.3
    defaults_dir = current_app.config['WWW_DIR'].parent / 'bindings' / 'Defaults 3.3'
    
    if not defaults_dir.exists():
        click.echo(f"Defaults directory not found: {defaults_dir}")
        return

    click.echo(f"Importing defaults from {defaults_dir}...")
    
    count = 0
    errors_count = 0
    
    # Standard display groups for defaults
    display_groups = ['Ship', 'SRV', 'OnFoot', 'UI', 'Galaxy map', 'Head look', 'Scanners', 'Fighter', 'Multicrew', 'Camera', 'Holo-Me', 'Misc']
    
    bind_files = list(defaults_dir.glob('*.binds'))
    if limit:
        bind_files = bind_files[:limit]
        
    for bind_file in bind_files:
        try:
            # Create a new config with random ID
            config = Config.newRandom()
            config.makeDir()
            
            # Read and parse
            with bind_file.open('r', encoding='utf-8') as f:
                xml = f.read()
            
            # Save the .binds file (required for display)
            binds_path = config.pathWithSuffix('.binds')
            with open(str(binds_path), 'w', encoding='utf-8') as f:
                f.write(xml)
                
            parse_errors = Errors()
            (physicalKeys, modifiers, devices) = parser.parseBindings(
                config.name, xml, display_groups, parse_errors
            )
            
            if parse_errors.hasErrors():
                click.echo(f"Skipping {bind_file.name}: Parsing error")
                errors_count += 1
                continue
                
            # Create description from filename
            description = f"Default: {bind_file.stem}"
            
            # Save to database (no longer using .replay pickle files)
            database.create_configuration(

                config_id=config.name,
                description=description,
                styling='None',
                display_groups=display_groups,
                devices=devices,
                unhandled_warnings=parse_errors.unhandledDevicesWarnings,
                device_warnings=parse_errors.deviceWarnings,
                misc_warnings=parse_errors.misconfigurationWarnings
            )
            
            count += 1
            if count % 10 == 0:
                click.echo(f"Imported {count} configurations...")
                
        except Exception as e:
            click.echo(f"Error importing {bind_file.name}: {e}")
            errors_count += 1

    click.echo(f"Import complete: {count} imported, {errors_count} errors.")


@click.command('rebuild-db')
@with_appcontext
def rebuild_db_command():
    """Rebuild database from existing .binds files in configs directory."""
    from flask import current_app
    from scripts import database, parser, utils
    from scripts.models import Errors
    
    configs_dir = current_app.config['CONFIGS_FOLDER']
    click.echo(f"Scanning {configs_dir} for .binds files...")
    
    # Standard display groups
    display_groups = ['Ship', 'SRV', 'OnFoot', 'UI', 'Galaxy map', 'Head look', 'Scanners', 'Fighter', 'Multicrew', 'Camera', 'Holo-Me', 'Misc']
    
    bind_files = list(configs_dir.rglob('*.binds'))
    total_files = len(bind_files)
    
    bind_files = list(configs_dir.rglob('*.binds'))
    total_files = len(bind_files)
    
    click.echo(f"Found {total_files} .binds files. Starting rebuild (silencing warnings)...")
    
    count = 0
    errors_count = 0
    
    # Silence logError to prevent console spam
    original_log_error = utils.logError
    utils.logError = lambda msg: None
    
    try:
        for bind_file in bind_files:
            try:
                # Extract config_id from path
                # Structure is usually configs/xx/config_id.binds
                config_id = bind_file.stem
                
                # Read file
                try:
                    with bind_file.open('r', encoding='utf-8') as f:
                        xml = f.read()
                except Exception as e:
                    click.echo(f"Error reading {bind_file}: {e}")
                    errors_count += 1
                    continue
                
                # Parse bindings
                parse_errors = Errors()
                (physicalKeys, modifiers, devices) = parser.parseBindings(
                    config_id, xml, display_groups, parse_errors
                )
                
                if parse_errors.hasErrors():
                    errors_count += 1
                    continue
                
                # Create description
                # Try to get PresetName from XML, fallback to filename
                description = config_id
                try:
                    # Simple regex to avoid full XML parsing overhead just for one attribute
                    # <Root PresetName="Keyboard" ...>
                    import re
                    match = re.search(r'PresetName="([^"]+)"', xml)
                    if match:
                        preset_name = match.group(1)
                        if preset_name and preset_name != "Custom":
                            description = preset_name
                except Exception:
                    pass  # Fallback to filename on any error
                
                # Save to database
                # Note: We can't easily restore the original creation time without modifying the DB schema
                # or SQL directly, so new entries will have current timestamp.
                
                database.create_configuration(
                    config_id=config_id,
                    description=description,
                    styling='None',
                    display_groups=display_groups,
                    devices=devices,
                    unhandled_warnings=parse_errors.unhandledDevicesWarnings,
                    device_warnings=parse_errors.deviceWarnings,
                    misc_warnings=parse_errors.misconfigurationWarnings
                )
                
                count += 1
                if count % 100 == 0:
                    click.echo(f"Processed {count}/{total_files}...")
                    
            except Exception as e:
                click.echo(f"Error processing {bind_file.name}: {e}")
                errors_count += 1
                
    finally:
        # Restore original logError
        utils.logError = original_log_error
            
    click.echo(f"Rebuild complete: {count} recovered, {errors_count} errors.")


@click.command('import-live')
@click.argument('source_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--dry-run', is_flag=True, help='Check everything, write nothing.')
@click.option('--limit', type=int, default=None, help='Stop after N cards.')
@click.option('--report', 'report_path', type=click.Path(dir_okay=False), default=None,
              help='Write the full per-id report as JSON.')
@with_appcontext
def import_live_command(source_dir, dry_run, limit, report_path):
    """Import the cards of the old live site from an extracted tarball.

    SOURCE_DIR holds the live configs folder (<id>.binds + <id>.replay pairs,
    any layout). Ids, titles, styling, display groups and dates are kept;
    existing ids are never overwritten.
    """
    import json

    from scripts import utils
    from scripts.live_import import import_live_configs

    original_log_error = utils.logError
    utils.logError = lambda msg: None  # the parser is chatty on old files
    try:
        report = import_live_configs(source_dir, dry_run=dry_run, limit=limit,
                                     log=click.echo)
    finally:
        utils.logError = original_log_error

    click.echo('DRY RUN, nothing written.' if dry_run else 'Import done.')
    for name, value in report.counts().items():
        click.echo(f'  {name}: {value}')
    for name in ('clashes', 'bad_replays', 'parse_errors', 'invalid_ids'):
        items = getattr(report, name)
        if items:
            click.echo(f'{name} (first 20): {items[:20]}')
    if report_path:
        with open(report_path, 'w', encoding='utf-8') as handle:
            json.dump(report.as_dict(), handle, indent=2, ensure_ascii=False)
        click.echo(f'Report written to {report_path}')


@click.command('seed-aeromax')
@with_appcontext
def seed_aeromax_command():
    """Seed a controller_mapping for the VIRPIL CDT-AEROMAX R (334444B0). Test scaffolding."""
    import json
    from scripts import database

    def r(symbol, number, joy, typ='Digital'):
        return {'symbol': symbol, 'number': number, 'joy': joy, 'type': typ}

    # Labels/numbers come from the VIRPIL CDT-AEROMAX R callout sheet (number == Joy_N
    # in game). Positions are a provisional two-column layout with NO leader lines yet:
    # exact button anchoring is done later from the manual + the click-to-place editor.
    # The mini-thruster (U axis) is a floating box (no button_xy) because the module is
    # removable (left/right/both). Empty boxes/rows are hidden per user at render time.
    # Canvas: composed wide card 4400x2560 (stick centred ~1485-2915), so the two
    # columns sit in the left/right margins. '-card' suffix avoids the stale square
    # upscayl shadowing it from the controllers/ volume.
    mapping = {
        'title': 'VIRPIL CDT-AEROMAX R Flightstick',
        'image': 'vpc-aeromax-r-card',
        'device_ids': ['334444B0'],
        'styling': 'Group',
        'boxes': [
            # --- left column (margin 0..1485) ---
            {'label': 'FIRE', 'box_xy': [70, 200], 'box_wh': [1380, 184],
             'rows': [r('stage1', '1', 'Joy_1'), r('stage2', '2', 'Joy_2')]},
            {'label': 'CMS', 'box_xy': [70, 420], 'box_wh': [1380, 328],
             'rows': [r('up', '8', 'Joy_8'), r('left', '11', 'Joy_11'),
                      r('press', '7', 'Joy_7'), r('right', '9', 'Joy_9')]},
            {'label': 'AP', 'box_xy': [70, 790], 'box_wh': [1380, 184],
             'rows': [r('up', '3', 'Joy_3'), r('down', '4', 'Joy_4')]},
            {'label': 'NWS / MSLS', 'box_xy': [70, 1010], 'box_wh': [1380, 112],
             'rows': [r('press', '5', 'Joy_5')]},
            {'label': 'GEAR', 'box_xy': [70, 1160], 'box_wh': [1380, 112],
             'rows': [r('press', '25', 'Joy_25')]},
            {'label': 'UI / FSS', 'box_xy': [70, 1310], 'box_wh': [1380, 112],
             'rows': [r('press', '6', 'Joy_6')]},
            # floating: removable mini-thruster module (no physical anchor)
            {'label': 'MINI-THRUSTER', 'box_xy': [70, 1480], 'box_wh': [1000, 112],
             'rows': [r(None, 'U', 'Joy_UAxis', 'Analogue')]},
            # --- right column (margin 2915..4400) ---
            {'label': 'VIEW / TRIM', 'box_xy': [2950, 200], 'box_wh': [1380, 400],
             'rows': [r('up', '27', 'Joy_27'), r('right', '28', 'Joy_28'),
                      r('down', '29', 'Joy_29'), r('left', '30', 'Joy_30'),
                      r('right', '16', 'Joy_16')]},
            {'label': 'POV1', 'box_xy': [2950, 640], 'box_wh': [1380, 328],
             'rows': [r('up', None, 'Joy_POV1Up'), r('right', None, 'Joy_POV1Right'),
                      r('down', None, 'Joy_POV1Down'), r('left', None, 'Joy_POV1Left')]},
            {'label': 'STICK', 'box_xy': [2950, 1010], 'box_wh': [1380, 184],
             'rows': [r(None, 'X', 'Joy_XAxis', 'Analogue'), r(None, 'Y', 'Joy_YAxis', 'Analogue')]},
            {'label': 'RUDDER (twist)', 'box_xy': [2950, 1230], 'box_wh': [1380, 112],
             'rows': [r(None, 'Z', 'Joy_ZAxis', 'Analogue')]},
            {'label': 'WHEEL BRAKE', 'box_xy': [2950, 1380], 'box_wh': [1380, 112],
             'rows': [r(None, 'RZ', 'Joy_RZAxis', 'Analogue')]},
        ],
    }
    mj = json.dumps(mapping)
    existing = database.get_controller_mapping_by_device_id('334444B0')
    if existing:
        database.update_controller_mapping(existing['id'], device_name=mapping['title'],
                                           template_name=mapping['image'],
                                           image_filename=mapping['image'] + '.jpg', mapping_json=mj)
        click.echo(f"Updated AEROMAX mapping id {existing['id']}")
    else:
        mid = database.create_controller_mapping('334444B0', mapping['title'], mapping['image'],
                                                 mapping['image'] + '.jpg', 4400, 2560, mj)
        click.echo(f"Created AEROMAX mapping id {mid}")
