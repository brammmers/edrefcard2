import os
import tempfile
from pathlib import Path
from flask import Blueprint, render_template, request, url_for, send_from_directory, current_app, abort
from markupsafe import escape
from extensions import limiter
from scripts import (
    Config,
    Errors,
    supportedDevices,
    parseBindings,
    parseFormData,
    createHOTASImage,
    appendKeyboardImage,
    createKeyboardLayoutImage,
    createBlockImage,
    createDataDrivenImage,
    logError,
    slugify
)
from scripts import database



web_bp = Blueprint('web', __name__)

# Extensions servable as static front-end assets (never source code or data files).
_STATIC_ASSET_EXTS = frozenset({'.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.svg', '.woff', '.woff2', '.txt', '.map'})
# Extensions servable from the configs directory (generated artifacts only, never the DB/logs).
_CONFIG_SERVABLE_EXTS = frozenset({'.jpg', '.jpeg', '.binds'})

# keyboard_display form value -> visual layout name in keyboardLayouts
_VISUAL_KEYBOARD_LAYOUTS = {
    'visual-ansi': 'ANSI 104',
    'visual-iso-azerty': 'ISO 105 AZERTY',
}

# Route handlers


def render_data_driven(physical_keys, modifiers, devices, config, public, styling, errors=None):
    """Render data-driven cards for any device matching a controller_mappings entry.

    Returns (image_base_names, handled_device_keys). The clean image + box layout
    come from controller_mappings; the binding text comes from the uploaded config.
    """
    import json
    created, handled = [], set()
    try:
        rows = database.get_published_controller_mappings()
    except Exception as e:
        logError(f"data-driven: cannot load mappings: {e}\n")
        return created, handled
    index = {}
    for row in rows:
        # Draft mappings (mapper work awaiting admin review) are not rendered
        if row.get('status', 'published') != 'published':
            continue
        try:
            m = json.loads(row['mapping_json'])
        except Exception:
            continue
        for did in (m.get('device_ids') or [row.get('device_id')]):
            if did:
                # Case-insensitive: .binds device IDs are uppercase, mappers
                # may store them in any case (see get_controller_mapping_by_device_id)
                index[str(did).upper()] = m
    if not index:
        return created, handled
    for device_key in list(devices.keys()):
        parts = device_key.split('::')
        if len(parts) != 2:
            continue
        dev_id, idx = parts[0], parts[1]
        try:
            idx = int(idx)
        except ValueError:
            continue
        m = index.get(dev_id.upper())
        if not m:
            continue
        try:
            createDataDrivenImage(m, config, public, physicalKeys=physical_keys,
                                  modifiers=modifiers, styling=styling,
                                  imageDevices=[dev_id], deviceIndex=idx)
            created.append(m['image'] if idx == 0 else f"{m['image']}-{idx}")
            handled.add(device_key)
        except Exception as e:
            logError(f"data-driven render failed for {device_key}: {e}\n")
            continue
        # Continuous enrichment: surface inputs this user actually bound that the
        # mapping doesn't cover yet (VIRPIL configs vary per user), with a
        # ready-to-open editor URL that merges them as an UNASSIGNED box.
        try:
            from scripts.mapping_runtime import missing_inputs, used_inputs
            used = used_inputs(physical_keys, modifiers, [dev_id], idx)
            miss = missing_inputs(m, used)
            if miss:
                logError(f"data-driven: {dev_id} inputs not in mapping: {', '.join(miss)} "
                         f"-> /admin/mapping-editor?device={dev_id}&from={config.name}\n")
                if errors is not None:
                    import html
                    warning = (
                        f'<p data-controller-coverage="{html.escape(dev_id, quote=True)}">'
                        '<strong>Incomplete controller card:</strong> '
                        f'{html.escape(dev_id)} has bound inputs not covered by its template: '
                        f'{html.escape(", ".join(miss))}. '
                        'These commands are missing from the card. '
                        'Please report this configuration reference.</p>')
                    if warning not in errors.misconfigurationWarnings:
                        errors.misconfigurationWarnings += warning
        except Exception as e:
            logError(f"data-driven enrichment check failed for {device_key}: {e}\n")
    return created, handled


# ---- render cache ------------------------------------------------------------
# A card page used to redraw every image with ImageMagick on each view, which
# is slow and is what made a worker grow to 1.4 GB. The result of a render is
# now remembered next to the images ('<id>-render.json') together with a
# signature of everything it depends on. A view with an unchanged signature
# and all its images still on disk serves the stored result without drawing.
_RENDER_CACHE_VERSION = 1
_render_build_stamp = None


def _render_build():
    """Identifies the rendering code and artwork of this deployment, so a
    new release never serves cards drawn by the previous one."""
    global _render_build_stamp
    if _render_build_stamp is None:
        from scripts import __version__
        www = Path(__file__).resolve().parent
        newest = 0
        for pattern in ('web.py', 'scripts/*.py', 'res/*.jpg'):
            for path in www.glob(pattern):
                try:
                    newest = max(newest, path.stat().st_mtime_ns)
                except OSError:
                    pass
        _render_build_stamp = f'{__version__}:{newest}'
    return _render_build_stamp


def _render_signature(xml, display_groups, styling, keyboard_display):
    import hashlib
    import json
    mappings, aliases = database.get_render_dependencies()
    payload = json.dumps({
        'cache': _RENDER_CACHE_VERSION,
        'build': _render_build(),
        'source': hashlib.sha256(xml.encode('utf-8')).hexdigest(),
        'groups': sorted(display_groups),
        'styling': styling,
        'keyboard': keyboard_display,
        'web_root': Config.webRoot(),  # printed on every card
        'mappings': mappings,
        'aliases': aliases,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def _load_render_cache(config, signature):
    """Stored render result for this signature, or None. Never raises."""
    import json
    try:
        path = config.pathWithNameAndSuffix('render', '.json')
        with open(path, encoding='utf-8') as handle:
            data = json.load(handle)
        if data.get('signature') != signature:
            return None
        files = data['files']
        if not all(isinstance(name, str) and Path(name).name == name
                   and (path.parent / name).is_file() for name in files):
            return None  # an image was cleaned up: draw again
        if not (isinstance(data['created_images'], list) and isinstance(data['data_driven_images'], list)
                and isinstance(data['unsupported_devices'], list) and isinstance(data['errors'], dict)):
            return None
        return data
    except Exception:
        return None


def _drop_rendered_images(config):
    """Delete this card's generated images and PDFs before drawing it again.
    Never raises: a file that cannot be removed is only logged."""
    for path in config.ownedFiles():
        if path.suffix.lower() in ('.jpg', '.pdf'):
            try:
                path.unlink(missing_ok=True)
            except OSError as e:
                logError(f'stale image not removed for {config.name}: {e}\n')


def _store_render_cache(config, signature, result):
    """Remember a successful render. Never raises."""
    import json
    temp_name = None
    try:
        path = config.pathWithNameAndSuffix('render', '.json')
        files = sorted(p.name for p in config.ownedFiles() if p.suffix.lower() == '.jpg')
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent,
                                         suffix='.tmp', delete=False) as handle:
            temp_name = handle.name
            json.dump({'signature': signature, 'files': files, **result}, handle)
        os.replace(temp_name, path)
        temp_name = None
    except Exception as e:
        logError(f'render cache not stored for {config.name}: {e}\n')
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def generate_legacy_images(physical_keys, modifiers, devices, config, public,
                           styling, misconfiguration_warnings):
    """Render the legacy template-based cards for every supported device
    present in the parsed bindings.

    Shared by web.generate, web.show_binds and the API (was duplicated 3x).
    Returns (created_images, unsupported_devices): created_images entries are
    '<DeviceKey>::<index>', unsupported_devices lists devices whose template
    image is missing on disk.
    """
    created_images = []
    unsupported_devices = []
    already_handled_devices = []

    for supported_device_key, supported_device in supportedDevices.items():
        if supported_device_key == 'Keyboard':
            continue
        for device_index in range(4):
            handled = False
            device_key = None
            for handled_device in supported_device.get('KeyDevices', supported_device.get('HandledDevices')):
                if handled_device.find('::') > -1:
                    if device_index == int(handled_device.split('::')[1]) and devices.get(handled_device) is not None:
                        handled = True
                        device_key = handled_device
                        break
                else:
                    if devices.get(f'{handled_device}::{device_index}') is not None:
                        handled = True
                        device_key = f'{handled_device}::{device_index}'
                        break

            if not handled or device_key in already_handled_devices:
                continue

            try:
                createHOTASImage(
                    physical_keys, modifiers,
                    supported_device['Template'],
                    supported_device['HandledDevices'],
                    40, config, public, styling, device_index,
                    misconfiguration_warnings
                )
                created_images.append(f'{supported_device_key}::{device_index}')
                for handled_device in supported_device['HandledDevices']:
                    already_handled_devices.append(f'{handled_device}::{device_index}')
            except FileNotFoundError as e:
                logError(f"Template missing: {e}\n")
                unsupported_devices.append(supported_device_key)

    return created_images, unsupported_devices


def _config_not_found(run_id=None):
    """404 page for an unknown or malformed config id (id escaped: the error
    template renders its message as HTML)."""
    if run_id is None:
        message = '<h1>Configuration not found</h1>'
    else:
        message = f'<h1>Configuration "{escape(run_id)}" not found</h1>'
    return render_template('error.html', error_message=message), 404


@web_bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@web_bp.route('/privacy')
def privacy():
    """Render the Privacy Policy and Legal Notice page."""
    return render_template('privacy.html')

@web_bp.route('/generate', methods=['POST'])
@limiter.limit("10 per hour")
def generate():
    """Process uploaded bindings file and generate reference cards."""
    errors = Errors()
    
    # Check description validity
    description = request.form.get('description', '')
    if len(description) > 0 and not description[0].isalnum():
        return render_template('error.html', 
                               error_message='That is not a valid description. Leading punctuation is not allowed.')
    
    # Check for uploaded file
    if 'bindings' not in request.files:
        return render_template('error.html',
                               error_message='<h1>No bindings file supplied; please go back and select your binds file as per the instructions.</h1>')
    
    file = request.files['bindings']
    if not file or not file.filename:
        return render_template('error.html',
                               error_message='<h1>No bindings file supplied; please go back and select your binds file as per the instructions.</h1>')
    
    # Enhanced file validation
    if not file.filename.endswith('.binds'):
        return render_template('error.html',
                               error_message='<h1>Only .binds files are allowed</h1>')
    
    try:
        # Read one byte past the limit at most: the global MAX_CONTENT_LENGTH
        # (sized for admin backup uploads) must not let a public upload
        # load 100 MB in memory before being rejected.
        xml_bytes = file.read(512001)
        if len(xml_bytes) > 512000:
            return render_template('error.html',
                                   error_message='<h1>File too large. Maximum size is 500KB</h1>')
        
        xml = xml_bytes.decode('utf-8')
        if xml.count('<!ENTITY') > 10:
            return render_template('error.html',
                                   error_message='<h1>Invalid XML structure detected</h1>')
        
    except UnicodeDecodeError:
        return render_template('error.html',
                               error_message='<h1>Invalid file encoding. UTF-8 required</h1>')
    except Exception as e:
        logError(f"File validation error: {e}\n")
        return render_template('error.html',
                               error_message='<h1>File validation failed</h1>')
    
    # Parse form options
    display_groups = parseFormData(request.form)
    keyboard_display = request.form.get('keyboard_display', 'text')
    styling = 'None'
    if request.form.get('styling') == 'group':
        styling = 'Group'
    elif request.form.get('styling') == 'category':
        styling = 'Category'
    elif request.form.get('styling') == 'modifier':
        styling = 'Modifier'
    
    # Reserve a unique config ID derived from the filename (never reuses or
    # overwrites an existing card, see Config.claimUnique)
    base_id = slugify(file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename)
    config = Config.claimUnique(
        base_id, is_taken=lambda name: database.get_configuration(name) is not None)
    run_id = config.name
    
    binds_path = config.pathWithSuffix('.binds')
    with open(str(binds_path), 'w', encoding='utf-8') as f:
        f.write(xml)
    
    # If no description provided, try to extract PresetName from XML
    if not description or len(description.strip()) == 0:
        import re
        preset_match = re.search(r'PresetName="([^"]+)"', xml)
        if preset_match:
            preset_name = preset_match.group(1)
            # Use preset name if meaningful (not generic like 'Custom' or 'Empty')
            if preset_name and preset_name not in ('Custom', 'Empty', ''):
                description = preset_name
            else:
                description = f"Configuration {run_id}"
        else:
            description = f"Configuration {run_id}"


    
    public = True
    # Public-catalogue opt-out: the card stays reachable by its link, it just
    # never appears in /list (second report of the misleading old "Publish"
    # label, after Brammmers: BiscuitMx, forum post 10852xxx)
    list_publicly = request.form.get('public') == 'on'
    data_driven_images = []
    handled_dd = set()
    created_images = []
    unsupported_devices = []
    keyboard_layout_image = False
    devices = {}

    try:
        (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)

        created_images, unsupported_devices = generate_legacy_images(
            physical_keys, modifiers, devices, config, public, styling,
            errors.misconfigurationWarnings)

        if devices.get('Keyboard::0') is not None:
            layout = _VISUAL_KEYBOARD_LAYOUTS.get(keyboard_display)
            if layout:
                result = createKeyboardLayoutImage(
                    physical_keys, modifiers, layout, config, styling
                )
                if result is True:
                    keyboard_layout_image = True
                else:
                    # Fallback to text list if visual not available
                    appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, public)
            else:
                appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, public)

        # Data-driven controllers (from controller_mappings) - rendered from the
        # clean image + box layout, filled with this config's real bindings.
        dd_created, handled_dd = render_data_driven(physical_keys, modifiers, devices,
                                                    config, public, styling, errors)
        data_driven_images.extend(dd_created)

    except RuntimeError as e:
        logError(f'Runtime error in generation for {run_id}: {e}\n')
        errors.errors = f'<h1>System Error</h1><p>{escape(str(e))}</p>'
    except Exception as e:
        logError(f'Unexpected error in generation for {run_id}: {e}\n')
        import traceback
        traceback.print_exc()
        errors.errors = '<h1>Unexpected System Error</h1><p>An unexpected error occurred while processing your request. Please try again later.</p>'
    
    for device_key, device in devices.items():
        ignored_devices = ['Mouse::0', 'ArduinoLeonardo::0', 'vJoy::0', 'vJoy::1', '16D00AEA::0']
        if device is None and device_key not in ignored_devices and device_key not in handled_dd:
            logError(f'{run_id}: found unsupported device {device_key} '
                     f'-> scaffold: /admin/mapping-editor?device={device_key.split("::")[0]}&from={run_id}\n')
            # Feed the admin triage queue (/admin/controllers); ping Discord
            # only on the FIRST sighting of a device.
            try:
                if database.record_unknown_device(device_key.split('::')[0], run_id):
                    try:
                        from admin.backup import DiscordNotifier
                        DiscordNotifier.from_settings().send_notification(
                            'New unknown controller',
                            f'Device {device_key.split("::")[0]} seen for the first time '
                            f'(config "{run_id}"). Triage it on /admin/controllers.')
                    except Exception:
                        pass
            except Exception as e:
                logError(f'{run_id}: cannot record unknown device sighting: {e}\n')
            if errors.unhandledDevicesWarnings == '':
                errors.unhandledDevicesWarnings = f'<h1>Unknown controller detected</h1>You have a device that is not supported at this time. Please report details of your device by following the link at the bottom of this page supplying the reference "{run_id}" and we will attempt to add support for it.'
    
    if len(created_images) == 0 and len(data_driven_images) == 0 and not errors.misconfigurationWarnings and not errors.unhandledDevicesWarnings and not errors.errors:
        errors.errors = '<h1>The file supplied does not have any bindings for a supported controller or keyboard.</h1>'
    
    # Store configuration in SQLite database (no longer using .replay pickle files)
    try:

        database.create_configuration(
            config_id=run_id,
            description=description,
            styling=styling,
            display_groups=display_groups,
            devices=devices,
            keyboard_display=keyboard_display,
            unhandled_warnings=errors.unhandledDevicesWarnings,
            device_warnings=errors.deviceWarnings,
            misc_warnings=errors.misconfigurationWarnings,
            is_public=list_publicly
        )
    except Exception as e:
        logError(f"Database insertion error for {run_id}: {e}")
    
    refcard_url_dynamic = url_for('web.show_binds', run_id=run_id, _external=True)
    binds_url_dynamic = url_for('web.serve_config', path=f"{run_id[:2]}/{run_id}.binds", _external=True)

    return render_template('refcard.html',
                           run_id=run_id,
                           errors={
                               'unhandled_devices_warnings': errors.unhandledDevicesWarnings,
                               'misconfiguration_warnings': errors.misconfigurationWarnings,
                               'device_warnings': errors.deviceWarnings,
                               'errors': errors.errors,
                           },
                           created_images=created_images,
                           data_driven_images=data_driven_images,
                           keyboard_layout_image=keyboard_layout_image,
                           device_for_block_image=None,
                           public=public,
                           unlisted=not list_publicly,
                           refcard_url=refcard_url_dynamic,
                           binds_url=binds_url_dynamic,
                           unsupported_devices=unsupported_devices,
                           supported_devices=supportedDevices)

@web_bp.route('/stats')
def stats():
    """Show global statistics."""
    from scripts.database import get_configuration_stats
    
    try:
        stats_data = get_configuration_stats()
        
        daily_labels = [row['date'] for row in stats_data['daily_stats']]
        daily_values = [row['count'] for row in stats_data['daily_stats']]
        daily_labels.reverse()
        daily_values.reverse()
        
        device_labels = [row['device_display_name'] for row in stats_data['popular_devices']]
        device_values = [row['count'] for row in stats_data['popular_devices']]
        
        chart_data = {
            'daily': {'labels': daily_labels, 'values': daily_values},
            'devices': {'labels': device_labels, 'values': device_values}
        }
        
    except Exception as e:
        logError(f"Error fetching stats: {e}")
        stats_data = {}
        chart_data = {'daily': {'labels': [], 'values': []}, 'devices': {'labels': [], 'values': []}}

    return render_template('stats.html', stats=stats_data, chart_data=chart_data)

@web_bp.route('/list')
def list_configs():
    """List all public configurations."""
    import re
    
    # Get device filters from query params
    device_filters = request.args.getlist('deviceFilter')
    search_query = request.args.get('search', '').strip()
    
    # Sanitize search query: limit length and remove potentially dangerous characters
    if search_query:
        search_query = search_query[:100]  # Max 100 characters
        # Allow only alphanumeric, spaces, hyphens, underscores, and common punctuation
        search_query = re.sub(r'[^\w\s\-_.\'"]', '', search_query)
        if not search_query:  # If nothing left after sanitization
            search_query = None
    else:
        search_query = None
    
    # Sanitize page number
    try:
        page = max(1, int(request.args.get('page', 1)))
    except (ValueError, TypeError):
        page = 1
    
    per_page = 20  # Number of items per page

    # Resolve names to templates for database filtering
    selected_templates = []
    if device_filters:
        for controller in device_filters:
            device_info = supportedDevices.get(controller, {})
            selected_templates.append(device_info.get('Template', controller))

    # Retrieve configurations from database
    db_configs, total_configs = database.list_configurations(
        page=page, 
        per_page=per_page, 
        public_only=True,
        search=search_query if search_query else None,
        device_filters=selected_templates if selected_templates else None
    )
    
    configs = []
    for db_config in db_configs:
        config = dict(db_config)
        
        # Parse device names for display
        device_names = config.get('device_names', '') or ''
        controllers_list = [d.strip() for d in device_names.split(',') if d.strip()]
        
        # Format timestamp (US date format, no time)
        created_at = config.get('created_at', '')
        if hasattr(created_at, 'strftime'):
            date_str = created_at.strftime('%Y-%m-%d')
        elif isinstance(created_at, str):
            date_str = created_at[:10]
        else:
            date_str = ''

        configs.append({
            'url': url_for('web.show_binds', run_id=config['id'], _external=True),
            'description': config.get('description', 'Untitled'),
            'controllers': ', '.join(sorted(controllers_list)) if controllers_list else 'Unknown',
            'date': date_str,
        })
    
    controllers = sorted(supportedDevices.keys())
    selected_controllers = set(device_filters)
    
    return render_template('list.html',
                           controllers=controllers,
                           selected_controllers=selected_controllers,
                           items=configs,
                           total=total_configs,
                           page=page,
                           per_page=per_page)


@web_bp.route('/binds/<run_id>')
@limiter.limit("60 per minute")
def show_binds(run_id):
    """Show a saved configuration."""
    import codecs

    # run_id comes straight from the URL: reject anything that is not a
    # generated id before it reaches the filesystem or the error page.
    if not Config.isValidName(run_id):
        return _config_not_found()

    errors = Errors()
    unsupported_devices = []
    
    try:

        config = Config(run_id)
        binds_path = config.pathWithSuffix('.binds')
        
        # Get configuration from SQLite database (instead of .replay pickle files)
        db_config = database.get_configuration(run_id)
        
        if not binds_path.exists():
            if db_config is None:
                return _config_not_found(run_id)
            
            source_missing = True
            xml = None
        else:
            source_missing = False
            with codecs.open(str(binds_path), 'r', 'utf-8') as f:
                xml = f.read()
        
        # Get display options from database, with sensible defaults for legacy configs
        if db_config:
            display_groups = db_config.get('display_groups', ['Galaxy map', 'General', 'Head look', 'SRV', 'Ship', 'UI'])
            styling = db_config.get('styling', 'None')
            db_config.get('description', '')
            if not source_missing:
                import re
                # Keep unrelated stored notices, but recompute coverage and
                # software detection from the current source and public mapping.
                errors.misconfigurationWarnings = re.sub(
                    r'<p data-controller-coverage="[^"]*">.*?</p>', '',
                    db_config.get('misconfiguration_warnings', ''), flags=re.DOTALL)

        else:
            # Fallback defaults for configs not in database (very old legacy)
            display_groups = ['Galaxy map', 'General', 'Head look', 'SRV', 'Ship', 'UI']
            styling = 'None'


    except (ValueError):
        return render_template('error.html',
                               error_message=f'<h1>Configuration "{escape(run_id)}" invalid</h1>'), 404
    
    created_images = []
    keyboard_layout_image = False
    data_driven_images = []
    handled_dd = set()

    # Serve the previous render when nothing it depends on has changed
    signature = cached = None
    rendered = False
    if not source_missing:
        try:
            signature = _render_signature(
                xml, display_groups, styling,
                db_config.get('keyboard_display', 'text') if db_config else 'text')
            cached = _load_render_cache(config, signature)
        except Exception as e:
            logError(f'render cache unavailable for {run_id}: {e}\n')

    try:
        if cached is not None:
            created_images = cached['created_images']
            data_driven_images = cached['data_driven_images']
            unsupported_devices = cached['unsupported_devices']
            keyboard_layout_image = bool(cached.get('keyboard_layout_image'))
            errors.unhandledDevicesWarnings = cached['errors'].get('unhandled_devices_warnings', '')
            errors.misconfigurationWarnings = cached['errors'].get('misconfiguration_warnings', '')
            errors.deviceWarnings = cached['errors'].get('device_warnings', '')
            errors.errors = cached['errors'].get('errors', '')
        elif not source_missing:
            # Ensure directory exists for image regeneration
            config.makeDir()
            # The drawing functions keep any image already on disk, so the
            # images of a stale render (new release, settings or controller
            # mappings changed) must go first, or they would be served again.
            _drop_rendered_images(config)
            (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)

            created_images, unsupported_devices = generate_legacy_images(
                physical_keys, modifiers, devices, config, True, styling,
                errors.misconfigurationWarnings)

            if devices.get('Keyboard::0') is not None:
                keyboard_display = db_config.get('keyboard_display', 'text') if db_config else 'text'
                layout = _VISUAL_KEYBOARD_LAYOUTS.get(keyboard_display)
                if layout:
                    result = createKeyboardLayoutImage(
                        physical_keys, modifiers, layout, config, styling
                    )
                    if result is True:
                        keyboard_layout_image = True
                    else:
                        appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)
                else:
                    appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)

            # Data-driven controllers (from controller_mappings), same path as generate()
            dd_created, handled_dd = render_data_driven(physical_keys, modifiers, devices,
                                                        config, True, styling, errors)
            data_driven_images.extend(dd_created)
            rendered = True

        else:
            logError(f"Source missing for {run_id}, checking existing images...")
            errors.errors = "<strong>Source file missing.</strong><br>The `.binds` file for this configuration is missing from the server. Showing archived images if available."
            
            for supported_device_key, supported_device in supportedDevices.items():
                template = supported_device['Template']
                img_path_0 = config.pathWithNameAndSuffix(template, '.jpg')
                if img_path_0.exists():
                     created_images.append(f'{supported_device_key}::0')
                img_path_1 = config.pathWithNameAndSuffix(f'{template}-1', '.jpg')
                if img_path_1.exists():
                     created_images.append(f'{supported_device_key}::1')

            # Archived data-driven images (controller_mappings)
            try:
                import json as _json
                for _row in database.get_published_controller_mappings():
                    try:
                        _img = _json.loads(_row['mapping_json']).get('image')
                    except Exception:
                        _img = None
                    if _img and config.pathWithNameAndSuffix(_img, '.jpg').exists():
                        data_driven_images.append(_img)
            except Exception:
                pass

    except RuntimeError as e:
        logError(f'Runtime error in generation for {run_id}: {e}\n')
        errors.errors = f'<h1>System Error</h1><p>{escape(str(e))}</p>'
    except Exception as e:
        logError(f'Unexpected error in generation for {run_id}: {e}\n')
        # import traceback
        # traceback.print_exc()
        errors.errors = '<h1>Unexpected System Error</h1><p>An unexpected error occurred while processing your request. Please try again later.</p>'

    # Only a complete, error-free render is worth remembering
    if rendered and signature and not errors.errors:
        _store_render_cache(config, signature, {
            'created_images': created_images,
            'data_driven_images': data_driven_images,
            'unsupported_devices': unsupported_devices,
            'keyboard_layout_image': keyboard_layout_image,
            'errors': {
                'unhandled_devices_warnings': errors.unhandledDevicesWarnings,
                'misconfiguration_warnings': errors.misconfigurationWarnings,
                'device_warnings': errors.deviceWarnings,
                'errors': errors.errors,
            },
        })

    refcard_url_dynamic = url_for('web.show_binds', run_id=run_id, _external=True)
    binds_url_dynamic = url_for('web.serve_config', path=f"{run_id[:2]}/{run_id}.binds", _external=True)

    return render_template('refcard.html',
                           run_id=run_id,
                           errors={
                               'unhandled_devices_warnings': errors.unhandledDevicesWarnings,
                               'misconfiguration_warnings': errors.misconfigurationWarnings,
                               'device_warnings': errors.deviceWarnings,
                               'errors': errors.errors,
                           },
                           created_images=created_images,
                           data_driven_images=data_driven_images,
                           keyboard_layout_image=keyboard_layout_image,
                           device_for_block_image=None,
                           public=True,
                           refcard_url=refcard_url_dynamic,
                           binds_url=binds_url_dynamic,
                           unsupported_devices=unsupported_devices,
                           supported_devices=supportedDevices)


@web_bp.route('/devices')
def list_devices():
    """List all supported devices."""
    from scripts.database import get_device_counts
    try:
        from scripts.bindingsData import apply_legacy_device_aliases
        apply_legacy_device_aliases(database.list_legacy_device_aliases())
    except Exception:
        pass
    try:
        counts = get_device_counts(public_only=True)
    except Exception:
        counts = {}


    devices = []
    for name in sorted(supportedDevices.keys()):
        template = supportedDevices[name].get('Template', name)
        count = counts.get(template, counts.get(name, 0))
        
        devices.append({
            'name': name,
            'count': count,
            'handled_devices': supportedDevices[name]['HandledDevices'],
        })

    # Community-mapped controllers (published data-driven mappings)
    import json as _json
    dd_devices = []
    try:
        for row in database.get_published_controller_mappings():
            if row.get('status', 'published') != 'published':
                continue
            try:
                ids = _json.loads(row['mapping_json']).get('device_ids') or [row['device_id']]
            except Exception:
                ids = [row['device_id']]
            dd_devices.append({
                'name': row['device_name'],
                'handled_devices': ids,
                'count': database.count_configs_for_device_ids(ids),
            })
        dd_devices.sort(key=lambda d: d['name'].lower())
    except Exception as e:
        logError(f'devices page: cannot load data-driven mappings: {e}\n')

    return render_template('devices.html', devices=devices, dd_devices=dd_devices)

@web_bp.route('/device/<device_name>')
def show_device(device_name):
    """Show a device's button layout."""
    try:
        createBlockImage(device_name)
    except KeyError:
        return render_template('error.html',
                               error_message=f'<h1>{escape(device_name)} is not a supported controller.</h1>'), 404
    except Exception as e:
        # e.g. missing/corrupt template image: 500s leaked here before
        logError(f'show_device {device_name}: {e}\n')
        return render_template('error.html',
                               error_message=f'<h1>{escape(device_name)} does not have a visual layout yet.</h1>'), 404
    
    return render_template('refcard.html',
                           run_id='',
                           errors={
                               'unhandled_devices_warnings': '',
                               'misconfiguration_warnings': '',
                               'device_warnings': '',
                               'errors': '',
                           },
                           created_images=[],
                           device_for_block_image=device_name,
                           public=False,
                           refcard_url='',
                           binds_url='',
                           supported_devices=supportedDevices)

# PDF Generation Helper
def generate_pdf(run_id, page_format='A4'):
    from fpdf import FPDF
    from PIL import Image
    import hashlib
    import io
    import fitz
    
    # Use Flask's CONFIGS_FOLDER directly for consistency with serve_config
    configs_folder = Path(current_app.config['CONFIGS_FOLDER'])
    config_dir = configs_folder / run_id[:2]
    
    pdf_filename = f"{run_id}-{page_format}.pdf"
    pdf_path = config_dir / pdf_filename
    
    # Search for images. The directory is shared with other configs and ids
    # can be prefixes of one another ('custom-4-2' vs 'custom-4-2-abc'), so
    # drop the images that belong to a longer sibling id.
    search_pattern = f"{run_id}-*.jpg"
    siblings = [p.stem + '-' for p in config_dir.glob(f"{run_id}-*.binds")]
    all_files = [p for p in config_dir.glob(search_pattern)
                 if not any(p.name.startswith(sibling) for sibling in siblings)]

    keyboard_img = None
    device_images = []
    
    for p in all_files:
        if p.name.endswith('keyboard.jpg'):
            keyboard_img = p
        else:
            device_images.append(p)
            
    device_images.sort()
    
    ordered_images = device_images
    if keyboard_img:
        ordered_images.append(keyboard_img)
    
    if not ordered_images:
        logError(f"PDF Gen: No images found for {run_id} in {config_dir}. Search pattern: {search_pattern}")
        return None

    # Embed the source signature in the PDF itself, so concurrent workers can
    # atomically replace one complete cache file, not a PDF/sidecar pair.
    try:
        sources = [(p.name, p.read_bytes()) for p in ordered_images]
        signature = hashlib.sha256(b'edrefcard-pdf-v2\0' + page_format.encode())
        for name, content in sources:
            signature.update(name.encode('utf-8') + b'\0' + hashlib.sha256(content).digest())
        cache_key = 'edrefcard-source-sha256=' + signature.hexdigest()
        if pdf_path.exists():
            try:
                with fitz.open(pdf_path) as cached:
                    if cached.metadata.get('keywords') == cache_key and len(cached) == len(sources):
                        return str(pdf_path)
            except Exception:
                pass  # A legacy or damaged cache can be safely regenerated.
    except Exception as e:
        logError(f"Error reading PDF source images for {run_id}: {e}")
        return None
        
    pdf = FPDF(orientation='P', unit='mm', format=page_format)
    pdf.set_auto_page_break(False)
    pdf.set_keywords(cache_key)
    
    for image_name, image_bytes in sources:
        try:
            with Image.open(io.BytesIO(image_bytes)) as im:
                if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                    bg = Image.new('RGB', im.size, (255, 255, 255))
                    if im.mode != 'RGBA':
                        im = im.convert('RGBA')
                    bg.paste(im, mask=im.split()[3])
                    im = bg
                elif im.mode != 'RGB':
                    im = im.convert('RGB')
                
                width, height = im.size
                ratio = width / height
                orientation = 'L' if ratio >= 1.2 else 'P'
                pdf.add_page(orientation=orientation)
                
                if orientation == 'L':
                    pw = 297 if page_format == 'A4' else 279 
                    ph = 210 if page_format == 'A4' else 216 
                else:
                    pw = 210 if page_format == 'A4' else 216 
                    ph = 297 if page_format == 'A4' else 279
                
                target_w = pw
                target_h = ph
                page_ratio = pw / ph
                
                if ratio > page_ratio:
                    w = target_w
                    h = target_w / ratio
                else:
                    h = target_h
                    w = target_h * ratio
                
                x = (pw - w) / 2
                y = (ph - h) / 2
                
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
                    im.save(tmp_img, 'JPEG', quality=95)
                    tmp_name = tmp_img.name
                
                try:
                    pdf.image(tmp_name, x=x, y=y, w=w, h=h)
                finally:
                    if os.path.exists(tmp_name):
                        os.unlink(tmp_name)
        except Exception as e:
            logError(f"Error adding image {image_name} to PDF: {e}")
            return None  # Never cache a partial export or overwrite the last good PDF.

    temp_pdf = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', dir=config_dir, delete=False) as output:
            temp_pdf = output.name
        pdf.output(temp_pdf)
        try:
            os.replace(temp_pdf, pdf_path)
        except OSError:
            # Another worker published the same export first (Windows refuses
            # to replace a file that is being read): its file is ours if it
            # carries the same source signature.
            with fitz.open(pdf_path) as cached:
                if cached.metadata.get('keywords') != cache_key:
                    raise
    except Exception as e:
         logError(f"Error saving PDF {pdf_path}: {e}")
         return None
    finally:
        if temp_pdf and os.path.exists(temp_pdf):
            os.unlink(temp_pdf)
         
    return str(pdf_path)

@web_bp.route('/download/<run_id>/pdf')
@limiter.limit("30 per minute")
def download_pdf(run_id):
    """Download existing or generate new PDF."""
    if not Config.isValidName(run_id):
        return _config_not_found()

    format_type = request.args.get('format', 'A4')
    if format_type not in ['A4', 'Letter']:
        format_type = 'A4'
        
    try:
        pdf_path = generate_pdf(run_id, format_type)
        if pdf_path and os.path.exists(pdf_path):
             return send_from_directory(
                os.path.dirname(pdf_path),
                os.path.basename(pdf_path),
                as_attachment=True,
                download_name=f"EDRefCard-{run_id}-{format_type}.pdf"
            )
        else:
             return render_template('error.html',
                                    error_message='<h1>No images found to generate PDF</h1>'
                                                  '<p>Open the reference card page first, then retry.</p>'), 404
    except Exception as e:
        logError(f"PDF Gen Error: {e}")
        return render_template('error.html', error_message='<h1>Error generating PDF</h1>'), 500

@web_bp.route('/configs/<path:path>')
def serve_config(path):
    """Serve generated configuration artifacts (images and .binds files only).

    The configs directory also holds the SQLite DB and logs, so access is
    restricted to an explicit allow-list of generated-artifact extensions.
    """
    if Path(path).suffix.lower() not in _CONFIG_SERVABLE_EXTS:
        abort(404)
    configs_folder = current_app.config['CONFIGS_FOLDER']
    return send_from_directory(configs_folder, path)

@web_bp.route('/scripts/<path:filename>')
def serve_scripts(filename):
    """Serve front-end script files only (never Python source)."""
    if Path(filename).suffix.lower() != '.js':
        abort(404)
    scripts_path = current_app.config['WWW_DIR'] / 'scripts'
    return send_from_directory(scripts_path, filename)

@web_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static front-end assets (allow-listed extensions only).

    WWW_DIR contains source code and the configs/ data dir, so this route is
    limited to genuine asset file types to avoid exposing .py/.db/.log files.
    """
    if Path(filename).suffix.lower() not in _STATIC_ASSET_EXTS:
        abort(404)
    return send_from_directory(current_app.config['WWW_DIR'], filename)

@web_bp.route('/ed.css')
def serve_css():
    """Serve the main CSS file."""
    return send_from_directory(current_app.config['WWW_DIR'], 'ed.css')

@web_bp.route('/robots.txt')
def serve_robots():
    """Serve robots.txt (previously served by the now-disabled built-in static)."""
    return send_from_directory(current_app.config['WWW_DIR'], 'robots.txt')

@web_bp.route('/favicon.ico')
def serve_favicon():
    """Serve the favicon."""
    return send_from_directory(current_app.config['WWW_DIR'], 'favicon.ico')

@web_bp.route('/fonts/<path:filename>')
def serve_fonts(filename):
    """Serve font files."""
    return send_from_directory(current_app.config['WWW_DIR'] / 'fonts', filename)

@web_bp.route('/res/<path:filename>')
def serve_res(filename):
    """Serve resource files."""
    return send_from_directory(current_app.config['WWW_DIR'] / 'res', filename)
