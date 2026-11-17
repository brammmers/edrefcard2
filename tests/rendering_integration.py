"""Optional real-Wand/Flask integration, isolated from the live application DB.

Run inside the staging runtime against a scratch copy of the edited files.
Only synthetic profiles and temporary preview images are created.
"""
import ast
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import types

from flask import Flask, request, url_for, current_app
from wand.image import Image
from wand.drawing import Drawing


def run(root, installed_www):
    root, installed_www = Path(root), Path(installed_www)
    pkg = types.ModuleType('scripts')
    pkg.__path__ = [str(root / 'www/scripts'), str(installed_www / 'scripts')]
    sys.modules['scripts'] = pkg
    models = importlib.import_module('scripts.models')
    parser = importlib.import_module('scripts.parser')
    renderer = importlib.import_module('scripts.renderer')
    pkg.Config, pkg.Errors = models.Config, models.Errors
    pkg.createDataDrivenImage = renderer.createDataDrivenImage
    # No app import and no DB initialization. Runtime aliases have an empty
    # in-memory source, not a connection to the application's SQLite file.
    database = importlib.import_module('scripts.database')
    database.list_legacy_device_aliases = lambda: []
    os.chdir(installed_www / 'scripts')
    sandbox = Path(tempfile.mkdtemp(prefix='edrefcard-render-review-'))
    models.Config.setDirRoot(installed_www)
    models.Config.setConfigsPath(sandbox)
    models.Config.setWebRoot('https://editor-test.invalid/')
    (sandbox / 'controllers').mkdir()
    with Image(width=1200, height=850, background='white') as image:
        image.save(filename=str(sandbox / 'controllers/probe.jpg'))
    xml = '''<Root><PrimaryFire><Primary Device="TEST" Key="Joy_1"/></PrimaryFire>
    <YawLeftButton><Primary Device="TEST" Key="Neg_Joy_RYAxis"/></YawLeftButton>
    <YawRightButton><Primary Device="TEST" Key="Pos_Joy_RYAxis"/></YawRightButton>
    <PitchUpButton><Primary Device="TEST" Key="Joy_2"/></PitchUpButton>
    <Empty><Primary/></Empty></Root>'''
    (sandbox / 'pr').mkdir()
    (sandbox / 'pr/profile.binds').write_text(xml)
    mapping = {'image':'probe','title':'Stabilization render checks',
               'width':1200,'height':850,'device_ids':['TEST'],'styling':'Group', 'boxes':[
        {'label':'Small 193 x 40','box_xy':[60,180],'box_wh':[193,40],
         'button_xy':[580,320],
         'rows':[{'joy':'Joy_1','symbol':'press','number':1}]},
        {'label':'Negative direction','box_xy':[60,260],'box_wh':[500,120],
         'button_xy':[580,460],
         'rows':[{'joy':'Neg_Joy_RYAxis'}]},
        {'label':'Positive direction','box_xy':[620,260],'box_wh':[500,120],
         'button_xy':[580,540],
         'rows':[{'joy':'Pos_Joy_RYAxis'}]},
        {'label':'Imported hat','box_xy':[60,440],'box_wh':[500,300], 'no_chrome':True,
         'button_xy':[580,650],
         'rows':[{'joy':f'Joy_{n}', 'field_rect':[0,(n-1)*.25,1,.20]}
                 for n in range(1,5)]},
    ]}
    tree = ast.parse((root / 'www/admin/__init__.py').read_text())
    # The route and the module-level helpers it calls
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in ('_purge_old_previews', 'mapping_editor_preview')]
    assert len(nodes) == 2, [n.name for n in nodes]
    for node in nodes:
        node.decorator_list = []
    logs = []
    env = {'request':request,'url_for':url_for,'Config':models.Config,'Errors':models.Errors,
           'parseBindings':parser.parseBindings,'logError':logs.append}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'preview-probe','exec'),env)
    app = Flask('preview-probe')
    app.add_url_rule('/admin/mapping-editor/preview', view_func=env['mapping_editor_preview'], methods=['POST'])
    app.add_url_rule('/configs/<path:path>',endpoint='web.serve_config',view_func=lambda path:'')
    client = app.test_client()
    before = json.dumps(mapping,sort_keys=True)
    result = client.post('/admin/mapping-editor/preview',json={'mapping':mapping,'reference':'profile'})
    assert result.status_code == 200, result.get_json()
    payload = result.get_json()
    assert payload['coverage']['missing_inputs'] == [], payload
    assert payload['coverage']['used_inputs'] == 4, payload
    other = client.post('/admin/mapping-editor/preview',json={'mapping':mapping,'reference':'profile'})
    assert other.get_json()['url'] != payload['url']
    assert json.dumps(mapping,sort_keys=True) == before
    assert client.post('/admin/mapping-editor/preview',json={'mapping':mapping,'reference':'../secret'}).status_code == 400
    assert client.post('/admin/mapping-editor/preview',json={'mapping':mapping,'reference':'missing'}).status_code == 404
    assert client.post('/admin/mapping-editor/preview',json={'mapping':mapping,'reference':'profile','device_index':99}).status_code == 400
    incomplete = json.loads(before)
    incomplete['boxes'] = incomplete['boxes'][:1]
    incomplete_result = client.post('/admin/mapping-editor/preview',json={'mapping':incomplete,'reference':'profile'})
    assert incomplete_result.status_code == 200, incomplete_result.get_json()
    assert len(incomplete_result.get_json()['coverage']['missing_inputs']) == 3
    errors = models.Errors()
    physical, modifiers, devices = parser.parseBindings('probe',xml,list(parser.DISPLAY_GROUP_FIELDS.values()),errors)
    for styling in ['None','Group','Category','Modifier']:
        config = models.Config('style-' + styling.lower())
        config.makeDir()
        assert renderer.createDataDrivenImage(mapping, config, False, physical, modifiers, styling)
        assert config.pathWithNameAndSuffix('probe','.jpg').stat().st_size > 1000
    # A later command must fit individually even when the first command is short.
    with Image(width=400, height=200, background='white') as image, Drawing() as drawing:
        drawing.font = renderer.getFontPath('Regular', 'Normal')
        texts = [{'Text':text, 'Style':{'Font':drawing.font}} for text in ['A', 'W'*30]]
        size = renderer.calculateBestFitFontSize(drawing,120,180,texts,40)
        assert 0 < size < 40
        drawing.font_size = size
        for text in texts:
            assert int(drawing.get_font_metrics(image,text['Text'],multiline=False).text_width) <= 120
    registry = importlib.import_module('scripts.bindingsData').supportedDevices
    for hardware in ['ThrustMasterWarthogJoystick','SaitekX56Joystick','044F0405']:
        legacy_xml = f'<Root><PrimaryFire><Primary Device="{hardware}" Key="Joy_1"/></PrimaryFire></Root>'
        legacy_errors = models.Errors()
        lp, lm, _ = parser.parseBindings('legacy-probe',legacy_xml,['Ship'],legacy_errors)
        entry = next(v for v in registry.values() if hardware in v['HandledDevices'])
        config = models.Config('legacy-' + hardware.lower()); config.makeDir()
        assert renderer.createHOTASImage(lp,lm,entry['Template'],entry['HandledDevices'],
                                        40,config,False,'Group',0,'')
        assert config.pathWithNameAndSuffix(entry['Template'],'.jpg').stat().st_size > 1000
        assert legacy_errors.deviceWarnings == ''
    # Photo-less flow mapping: blank canvas sized to the bound boxes only, no
    # clean image needed, unbound boxes dropped, new word glyphs drawn.
    flow = {'image':'flow-probe-missing','title':'Flow render check','layout':'flow',
            'width':1200,'height':900,'device_ids':['TEST'],'boxes':[
        {'label':'ENCODER','zone':'BASE','box_xy':[0,0],'box_wh':[500,202],
         'rows':[{'joy':'Joy_1','symbol':'ccw','number':'1'},
                 {'joy':'Joy_2','symbol':'cw','number':'2'},
                 {'joy':'Joy_9','symbol':'mid','number':'9'}]},
        {'label':'UNBOUND','zone':'GRIP','box_xy':[0,0],'box_wh':[500,94],
         'rows':[{'joy':'Joy_99','number':'99'}]},
        {'label':'MINI-STICK','zone':'BASE','box_xy':[0,0],'box_wh':[500,94],
         'rows':[{'joy':'Joy_RYAxis'}]}]}
    config = models.Config('flow-probe'); config.makeDir()
    assert renderer.createDataDrivenImage(flow, config, False, physical, modifiers, 'Group')
    flow_image = str(config.pathWithNameAndSuffix('flow-probe-missing','.jpg'))
    with Image(filename=flow_image) as drawn:
        assert drawn.width == 1200 and 300 < drawn.height < 600, (drawn.width, drawn.height)
    # Exercise the shared web/API generation helper and visible coverage notice.
    web_tree = ast.parse((root / 'www/web.py').read_text())
    helper = next(n for n in web_tree.body if isinstance(n,ast.FunctionDef) and n.name=='render_data_driven')
    published = [{'status':'published','device_id':'TEST','mapping_json':json.dumps(incomplete)}]
    helper_env = {'database':types.SimpleNamespace(get_published_controller_mappings=lambda:published),
                  'createDataDrivenImage':renderer.createDataDrivenImage,'logError':lambda *args:None}
    exec(compile(ast.Module(body=[helper],type_ignores=[]),'shared-generation-probe','exec'),helper_env)
    coverage_errors = models.Errors()
    helper_config = models.Config('coverage-probe'); helper_config.makeDir()
    created, handled = helper_env['render_data_driven'](
        physical,modifiers,devices,helper_config,False,'Group',coverage_errors)
    assert created == ['probe'] and handled == {'TEST::0'}
    assert 'Neg_Joy_RYAxis' in coverage_errors.misconfigurationWarnings
    assert 'Pos_Joy_RYAxis' in coverage_errors.misconfigurationWarnings
    # Dense commands and a modifier-only button must remain present in every style.
    dense = json.loads(before)
    dense['boxes'] = [
        {'label':'Dense game modes + modifier','box_xy':[60,180],'box_wh':[1080,480],
         'rows':[{'joy':'Joy_1'}]},
        {'label':'Modifier button','box_xy':[60,690],'box_wh':[500,100],
         'rows':[{'joy':'Joy_3'}]}]
    controls = importlib.import_module('scripts.controlsData').controls
    selected = {name:{**c,'InputKey':'Joy_1'} for name,c in list(controls.items())
                if c.get('Type')=='Digital' and c.get('Group') in parser.DISPLAY_GROUP_FIELDS.values()}
    selected = dict(list(selected.items())[:15])
    mod_spec = 'TEST::0::Joy_3'
    dense_physical = {'TEST::0::Joy_1':{'Device':'TEST','DeviceIndex':0,'Key':'Joy_1',
        'BaseKey':'Joy_1','Binds':{'Unmodified':{'Controls':selected}, mod_spec:{'Controls':selected}}}}
    dense_modifiers = {mod_spec:[{'Number':1,'Device':'TEST','DeviceIndex':0,
                                'Key':'Joy_3','ModifierKey':mod_spec}]}
    for styling in ['None','Group','Category','Modifier']:
        config = models.Config('dense-' + styling.lower()); config.makeDir()
        assert renderer.createDataDrivenImage(dense,config,False,dense_physical,dense_modifiers,styling)
    # Never write stored sample commands into a real player's card.
    sample = json.loads(before)
    sample['boxes'] = [{'box_xy':[60,180],'box_wh':[500,120],
                        'rows':[{'joy':'','binds':[{'name':'SAMPLE MUST NOT LEAK'}]}]}]
    drawn = []
    real_draw = renderer._drawDataDrivenBox
    renderer._drawDataDrivenBox = lambda context,image,box,**kw:drawn.append(box)
    try:
        config = models.Config('sample-probe'); config.makeDir()
        renderer.createDataDrivenImage(sample,config,False,physical,modifiers)
        assert drawn == []
    finally:
        renderer._drawDataDrivenBox = real_draw
    pdf_node = next(n for n in web_tree.body if isinstance(n,ast.FunctionDef) and n.name=='generate_pdf')
    pdf_env = {'Path':Path,'current_app':current_app,'tempfile':tempfile,'os':os,'logError':logs.append}
    exec(compile(ast.Module(body=[pdf_node],type_ignores=[]),'pdf-probe','exec'),pdf_env)
    app.config['CONFIGS_FOLDER'] = sandbox
    import fitz
    with app.app_context():
        for fmt in ['A4','Letter']:
            path = pdf_env['generate_pdf']('dense-group',fmt)
            assert path
            with fitz.open(path) as pdf:
                assert pdf.page_count == 1
                assert pdf[0].rect.width > pdf[0].rect.height
                assert pdf[0].get_images()
                pdf[0].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(sandbox / ('pdf-' + fmt + '.png')))
    assert 'None::0' not in devices
    assert logs == [], logs
    return {'checks':'real preview, coverage, directions, dense modifiers, long-command fitting, four styles, three legacy templates, A4/Letter PDF, concurrent outputs and input errors passed',
            'review_image':str(sandbox / 'st/style-group-probe.jpg'),
            'pdf_review_images':[str(sandbox / 'pdf-A4.png'),str(sandbox / 'pdf-Letter.png'),
                                 flow_image]}


if __name__ == '__main__':
    result = run(sys.argv[1],sys.argv[2])
    if len(sys.argv) > 3:
        artifacts = Path(sys.argv[3])
        artifacts.mkdir(parents=True, exist_ok=True)
        for source in [result['review_image'], *result['pdf_review_images']]:
            shutil.copy2(source, artifacts / Path(source).name)
        (artifacts / 'checks.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
