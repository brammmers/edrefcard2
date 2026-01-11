from flask import Blueprint, request, jsonify, url_for, current_app
from scripts import (
    Config, 
    Errors, 
    supportedDevices, 
    parseBindings, 
    parseFormData,
    createHOTASImage,
    appendKeyboardImage,
    saveReplayInfo,
    logError
)
from scripts import database
import os

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/generate', methods=['GET', 'POST'])
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
        xml_bytes = file.read()
        if len(xml_bytes) > 512000:
            return jsonify({'error': 'File too large (max 500KB)'}), 413
            
        xml = xml_bytes.decode('utf-8')
    except Exception as e:
        return jsonify({'error': f'File parsing error: {str(e)}'}), 400

    # 2. Setup Config
    try:
        config = Config.newRandom()
        config.makeDir()
        run_id = config.name
        
        binds_path = config.pathWithSuffix('.binds')
        with open(str(binds_path), 'w', encoding='utf-8') as f:
            f.write(xml)
            
        description = request.form.get('description', f"API Config {run_id[:6]}")
        styling_mode = request.form.get('styling', 'modifier').lower()
        
        styling_map = {
            'modifier': 'Modifier',
            'group': 'Group', 
            'category': 'Category',
            'none': 'None'
        }
        styling = styling_map.get(styling_mode, 'Modifier')
        
        # Default display groups (all On) if not specified
        display_groups = ['Ship', 'SRV', 'Head look', 'UI', 'Galaxy map', 'Scanners', 'Fighter', 'On Foot', 'Multicrew', 'Camera', 'Holo-Me', 'Misc']
        
        # 3. Generation Logic (Simplified version of app.py)
        (physical_keys, modifiers, devices) = parseBindings(run_id, xml, display_groups, errors)
        
        created_images = []
        already_handled_devices = []
        
        # ... Reuse Generation Loop ...
        # Ideally this logic should be extracted to a shared function in scripts/generator.py
        # For now, replicating the core loop for the API to avoid major refactor risk in this step
        
        for supported_device_key, supported_device in supportedDevices.items():
            if supported_device_key == 'Keyboard': continue
            
            for device_index in [0, 1]:
                handled = False
                device_key = None
                for handled_device in supported_device.get('KeyDevices', supported_device.get('HandledDevices')):
                    if handled_device.find('::') > -1:
                        if device_index == int(handled_device.split('::')[1]) and devices.get(handled_device) is not None:
                            handled = True; device_key = handled_device; break
                    else:
                        if devices.get(f'{handled_device}::{device_index}') is not None:
                            handled = True; device_key = f'{handled_device}::{device_index}'; break
                
                if handled:
                    has_new_bindings = False
                    for device in supported_device.get('KeyDevices', supported_device.get('HandledDevices')):
                        if device_key not in already_handled_devices:
                            has_new_bindings = True; break
                            
                    if has_new_bindings:
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

        if devices.get('Keyboard::0') is not None:
            appendKeyboardImage(created_images, physical_keys, modifiers, display_groups, run_id, True)

        # 4. Save Metadata
        saveReplayInfo(config, description, styling, display_groups, devices, errors)
        
        database.create_configuration(
            config_id=run_id,
            description=description,
            styling=styling,
            display_groups=display_groups,
            devices=devices,
            unhandled_warnings=errors.unhandledDevicesWarnings,
            device_warnings=errors.deviceWarnings,
            misc_warnings=errors.misconfigurationWarnings
        )
        
        # 5. Response
        return jsonify({
            'status': 'success',
            'id': run_id,
            'url': url_for('web.show_binds', run_id=run_id, _external=True),
            'images_created': created_images,
            'warnings': {
                'unhandled': errors.unhandledDevicesWarnings,
                'device': errors.deviceWarnings,
                'misc': errors.misconfigurationWarnings
            }
        })

    except Exception as e:
        logError(f'API Error {run_id if "run_id" in locals() else "unknown"}: {e}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/binds/<run_id>', methods=['GET'])
def get_bind_info(run_id):
    """Get metadata for a specific config."""
    config = database.get_configuration(run_id)
    if not config:
        return jsonify({'error': 'Not found'}), 404
        
    return jsonify(config)
