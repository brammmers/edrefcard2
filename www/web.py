import os
import random
import string
import tempfile
from pathlib import Path
from flask import Blueprint, render_template, request, url_for, send_from_directory, current_app
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
    logError,
    slugify
)
from scripts import database



web_bp = Blueprint('web', __name__)

# Route handlers

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
        xml_bytes = file.read()
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
    
    # Generate config ID from filename
    base_id = slugify(file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename)
    if not base_id:
        base_id = Config.randomName()

    
    run_id = base_id
    config = Config(run_id)
    
    # If ID already exists, append a short random suffix
    if config.exists():
        suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
        run_id = f"{base_id}-{suffix}"
        config = Config(run_id)

    
    config.makeDir()
    
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
    
    try:
        (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)
        
        already_handled_devices = []
        created_images = []
        keyboard_layout_image = False
        
        for supported_device_key, supported_device in supportedDevices.items():
            if supported_device_key == 'Keyboard':
                continue
            
            for device_index in [0, 1]:
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
                
                if handled:
                    has_new_bindings = False
                    for _ in supported_device.get('KeyDevices', supported_device.get('HandledDevices')):
                        if device_key not in already_handled_devices:
                            has_new_bindings = True
                            break
                    
                    if has_new_bindings:
                        createHOTASImage(
                            physical_keys, modifiers, 
                            supported_device['Template'], 
                            supported_device['HandledDevices'], 
                            40, config, public, styling, device_index, 
                            errors.misconfigurationWarnings
                        )
                        created_images.append(f'{supported_device_key}::{device_index}')
                        for handled_device in supported_device['HandledDevices']:
                            already_handled_devices.append(f'{handled_device}::{device_index}')
        
        if devices.get('Keyboard::0') is not None:
            if keyboard_display == 'visual-ansi':
                result = createKeyboardLayoutImage(
                    physical_keys, modifiers, 'ANSI 104', config, styling
                )
                if result is True:
                    keyboard_layout_image = True
                else:
                    # Fallback to text list if visual not available
                    appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, public)
            else:
                appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, public)
            
    except RuntimeError as e:
        logError(f'Runtime error in generation for {run_id}: {e}\n')
        errors.errors = f'<h1>System Error</h1><p>{str(e)}</p>'
    except Exception as e:
        logError(f'Unexpected error in generation for {run_id}: {e}\n')
        import traceback
        traceback.print_exc()
        errors.errors = '<h1>Unexpected System Error</h1><p>An unexpected error occurred while processing your request. Please try again later.</p>'
    
    for device_key, device in devices.items():
        ignored_devices = ['Mouse::0', 'ArduinoLeonardo::0', 'vJoy::0', 'vJoy::1', '16D00AEA::0']
        if device is None and device_key not in ignored_devices:
            logError(f'{run_id}: found unsupported device {device_key}\n')
            if errors.unhandledDevicesWarnings == '':
                errors.unhandledDevicesWarnings = f'<h1>Unknown controller detected</h1>You have a device that is not supported at this time. Please report details of your device by following the link at the bottom of this page supplying the reference "{run_id}" and we will attempt to add support for it.'
        if device is not None and 'ThrustMasterWarthogCombined' in device['HandledDevices'] and errors.deviceWarnings == '':
            errors.deviceWarnings = '<h2>Mapping Software Detected</h2>You are using the ThrustMaster TARGET software. As a result it is possible that not all of the controls will show up. If you have missing controls then you should remove the mapping from TARGET and map them using Elite\'s own configuration UI.'
    
    if len(created_images) == 0 and not errors.misconfigurationWarnings and not errors.unhandledDevicesWarnings and not errors.errors:
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
            misc_warnings=errors.misconfigurationWarnings
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
                           keyboard_layout_image=keyboard_layout_image,
                           device_for_block_image=None,
                           public=public,
                           refcard_url=refcard_url_dynamic,
                           binds_url=binds_url_dynamic,
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
def show_binds(run_id):
    """Show a saved configuration."""
    import codecs
    
    errors = Errors()
    unsupported_devices = []
    
    try:

        config = Config(run_id)
        binds_path = config.pathWithSuffix('.binds')
        
        # Get configuration from SQLite database (instead of .replay pickle files)
        db_config = database.get_configuration(run_id)
        
        if not binds_path.exists():
            if db_config is None:
                return render_template('error.html', error_message=f'<h1>Configuration "{run_id}" not found</h1>')
            
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
                errors.misconfigurationWarnings = db_config.get('misconfiguration_warnings', '')
                errors.deviceWarnings = db_config.get('device_warnings', '')

        else:
            # Fallback defaults for configs not in database (very old legacy)
            display_groups = ['Galaxy map', 'General', 'Head look', 'SRV', 'Ship', 'UI']
            styling = 'None'


    except (ValueError):
        return render_template('error.html',
                               error_message=f'<h1>Configuration "{run_id}" invalid</h1>')
    
    created_images = []
    keyboard_layout_image = False
    
    try:
        if not source_missing:
            # Ensure directory exists for image regeneration
            config.makeDir()
            (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)
            
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
                    
                    if handled:
                        has_new_bindings = False
                        for _device in supported_device.get('KeyDevices', supported_device.get('HandledDevices')):
                            if device_key not in already_handled_devices:
                                has_new_bindings = True
                                break
                        
                        if has_new_bindings:
                            try:
                                createHOTASImage(
                                    physical_keys, modifiers,
                                    supported_device['Template'],
                                    supported_device['HandledDevices'],
                                    40, config, True, styling, device_index,
                                    errors.misconfigurationWarnings
                                )
                                created_images.append(f'{supported_device_key}::{device_index}')
                                for handled_device in supported_device['HandledDevices']:
                                    already_handled_devices.append(f'{handled_device}::{device_index}')
                            except FileNotFoundError as e:
                                logError(f"Template missing: {e}\n")
                                unsupported_devices.append(supported_device_key)


            
            if devices.get('Keyboard::0') is not None:
                keyboard_display = db_config.get('keyboard_display', 'text') if db_config else 'text'
                if keyboard_display == 'visual-ansi':
                    result = createKeyboardLayoutImage(
                        physical_keys, modifiers, 'ANSI 104', config, styling
                    )
                    if result is True:
                        keyboard_layout_image = True
                    else:
                        appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)
                else:
                    appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)

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

    except RuntimeError as e:
        logError(f'Runtime error in generation for {run_id}: {e}\n')
        errors.errors = f'<h1>System Error</h1><p>{str(e)}</p>'
    except Exception as e:
        logError(f'Unexpected error in generation for {run_id}: {e}\n')
        # import traceback
        # traceback.print_exc()
        errors.errors = '<h1>Unexpected System Error</h1><p>An unexpected error occurred while processing your request. Please try again later.</p>'
    
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
    
    return render_template('devices.html', devices=devices)

@web_bp.route('/device/<device_name>')
def show_device(device_name):
    """Show a device's button layout."""
    try:
        createBlockImage(device_name)
    except KeyError:
        return render_template('error.html',
                               error_message=f'<h1>{device_name} is not a supported controller.</h1>')
    
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
    
    # Use Flask's CONFIGS_FOLDER directly for consistency with serve_config
    configs_folder = Path(current_app.config['CONFIGS_FOLDER'])
    config_dir = configs_folder / run_id[:2]
    
    pdf_filename = f"{run_id}-{page_format}.pdf"
    pdf_path = config_dir / pdf_filename
    
    if pdf_path.exists():
         return str(pdf_path)

    # Search for images
    search_pattern = f"{run_id}-*.jpg"
    all_files = list(config_dir.glob(search_pattern))
    
    # Debug: log what we're searching for
    logError(f"PDF Gen Debug: Looking in {config_dir} for {search_pattern}")
    logError(f"PDF Gen Debug: config_dir.exists()={config_dir.exists()}")
    if config_dir.exists():
        dir_contents = list(config_dir.iterdir())[:20]  # List first 20 files
        logError(f"PDF Gen Debug: Directory contains {len(list(config_dir.iterdir()))} items, first 20: {[f.name for f in dir_contents]}")
    logError(f"PDF Gen Debug: Found {len(all_files)} matching files: {[f.name for f in all_files]}")
    
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
        
    pdf = FPDF(orientation='P', unit='mm', format=page_format)
    pdf.set_auto_page_break(False)
    
    for img_path in ordered_images:
        try:
            with Image.open(str(img_path)) as im:
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
            logError(f"Error adding image {img_path} to PDF: {e}")
            continue

    try:
        pdf.output(str(pdf_path))
    except Exception as e:
         logError(f"Error saving PDF {pdf_path}: {e}")
         return None
         
    return str(pdf_path)

@web_bp.route('/download/<run_id>/pdf')
def download_pdf(run_id):
    """Download existing or generate new PDF."""
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
             from scripts.models import Config as ConfigModel
             cfg = ConfigModel(run_id)
             search_path = cfg.path().parent
             return render_template('error.html', error_message=f'<h1>No images found to generate PDF</h1><p>Debug: Searched in {search_path} for pattern {run_id}-*.jpg</p>')
    except Exception as e:
        logError(f"PDF Gen Error: {e}")
        return render_template('error.html', error_message=f'<h1>Error generating PDF</h1><p>{e}</p>')

@web_bp.route('/configs/<path:path>')
def serve_config(path):
    """Serve generated configuration images and files."""
    configs_folder = current_app.config['CONFIGS_FOLDER']
    return send_from_directory(configs_folder, path)

@web_bp.route('/scripts/<path:filename>')
def serve_scripts(filename):
    """Serve script files."""
    scripts_path = current_app.config['WWW_DIR'] / 'scripts'
    return send_from_directory(scripts_path, filename)

@web_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(current_app.config['WWW_DIR'], filename)

@web_bp.route('/ed.css')
def serve_css():
    """Serve the main CSS file."""
    return send_from_directory(current_app.config['WWW_DIR'], 'ed.css')

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
