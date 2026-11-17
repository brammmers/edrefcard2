import re
from flask import Blueprint, request, jsonify, url_for
from scripts import (
    Config,
    Errors,
    parseBindings,
    appendKeyboardImage,
    logError,
    slugify
)
from scripts import database
from extensions import limiter
from scripts.parser import ALL_DISPLAY_GROUPS


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/generate', methods=['GET', 'POST'])
@limiter.limit("30 per hour", methods=['POST'])
def generate_api():
    """
    API Endpoint to generate reference card.
    Expects 'bindings' file in multipart/form-data.
    Optional fields: description, styling (modifier|group|category|none)
    """
    if request.method == 'GET':
        return jsonify({
            'message': 'This endpoint expects a POST request with a .binds file.',
            'usage': {
                'method': 'POST',
                'url': url_for('api.generate_api', _external=True),
                'body': 'multipart/form-data',
                'fields': {
                    'bindings': 'File (required)',
                    'description': 'String (optional)',
                    'styling': 'modifier|group|category|none (optional)'
                }
            }
        }), 405

    errors = Errors()
    
    # 1. Validation
    if 'bindings' not in request.files:
        return jsonify({'error': 'No bindings file provided'}), 400
        
    file = request.files['bindings']
    if not file or not file.filename:
        return jsonify({'error': 'Empty filename'}), 400
        
    if not file.filename.endswith('.binds'):
        return jsonify({'error': 'Invalid file extension. Must be .binds'}), 400

    try:
        xml_bytes = file.read(512001)
        if len(xml_bytes) > 512000:
            return jsonify({'error': 'File too large (max 500KB)'}), 413
            
        xml = xml_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return jsonify({'error': 'Invalid file encoding. UTF-8 required'}), 400
    except Exception as e:
        logError(f'API file read error: {e}')
        return jsonify({'error': 'File could not be read'}), 400

    # 2. Setup Config
    try:
        # Reserve a unique config ID derived from the filename
        base_id = slugify(file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename)
        config = Config.claimUnique(
            base_id, is_taken=lambda name: database.get_configuration(name) is not None)
        run_id = config.name
        
        binds_path = config.pathWithSuffix('.binds')
        with open(str(binds_path), 'w', encoding='utf-8') as f:
            f.write(xml)
        
        # Get description from request, or extract PresetName from XML
        description = request.form.get('description', '').strip()
        if not description:
            preset_match = re.search(r'PresetName="([^"]+)"', xml)

            if preset_match:
                preset_name = preset_match.group(1)
                if preset_name and preset_name not in ('Custom', 'Empty', ''):
                    description = preset_name
                else:
                    description = f"API Config {run_id}"
            else:
                description = f"API Config {run_id}"

        
        styling_mode = request.form.get('styling', 'modifier').lower()

        
        styling_map = {
            'modifier': 'Modifier',
            'group': 'Group', 
            'category': 'Category',
            'none': 'None'
        }
        styling = styling_map.get(styling_mode, 'Modifier')
        
        # Default display groups (all On) if not specified
        display_groups = list(ALL_DISPLAY_GROUPS)
        
        # 3. Generation Logic (shared with the web UI, see web.generate_legacy_images)
        (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)

        from web import generate_legacy_images, render_data_driven

        # Data-driven controllers (from controller_mappings), same path as the
        # web UI: first, so that a published mapping replaces a legacy template.
        dd_created, handled_dd = [], set()
        try:
            dd_created, handled_dd = render_data_driven(physical_keys, modifiers, devices,
                                                        config, True, styling, errors)
        except Exception as e:
            logError(f'API data-driven render failed for {run_id}: {e}')

        created_images, unsupported_devices = generate_legacy_images(
            physical_keys, modifiers, devices, config, True, styling,
            errors.misconfigurationWarnings, handled_dd)

        if devices.get('Keyboard::0') is not None:
            appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)

        created_images.extend(dd_created)

        # 4. Save Metadata to SQLite database (no longer using .replay pickle files)
        
        # Public-catalogue opt-out: pass public=false/0/off/no to keep the
        # card unlisted (reachable by link only). Defaults to listed.
        list_publicly = str(request.form.get('public', 'on')).strip().lower() \
            not in ('off', 'false', '0', 'no')

        database.create_configuration(
            config_id=run_id,
            description=description,
            styling=styling,
            display_groups=display_groups,
            devices=devices,
            unhandled_warnings=errors.unhandledDevicesWarnings,
            device_warnings=errors.deviceWarnings,
            misc_warnings=errors.misconfigurationWarnings,
            is_public=list_publicly
        )
        
        # 5. Response
        return jsonify({
            'status': 'success',
            'id': run_id,
            'url': url_for('web.show_binds', run_id=run_id, _external=True),
            'images_created': created_images,
            'unsupported_devices': unsupported_devices,
            'warnings': {
                'unhandled': errors.unhandledDevicesWarnings,
                'device': errors.deviceWarnings,
                'misc': errors.misconfigurationWarnings
            }
        })

    except Exception as e:
        # Details go to the server log only, never to the client
        logError(f'API Error {run_id if "run_id" in locals() else "unknown"}: {e}')
        return jsonify({'error': 'Internal error while generating the reference card'}), 500

@api_bp.route('/binds/<run_id>', methods=['GET'])
def get_bind_info(run_id):
    """Get metadata for a specific config."""
    config = database.get_configuration(run_id)
    if not config:
        return jsonify({'error': 'Not found'}), 404
        
    return jsonify(config)
