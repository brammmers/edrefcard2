"""Rendering regressions, including dependency-free geometry and input probes."""
import ast
import copy
import importlib.util
import math
from collections import OrderedDict
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('runtime_test', ROOT / 'www/scripts/mapping_runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def functions(path, names, namespace):
    """Execute the real function bodies, without app imports or live DB writes."""
    tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    for node in nodes:
        node.decorator_list = []
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace


class DrawingProbe:
    def __init__(self, impossible=False):
        self.font_size = 10
        self.balance = self.calls = 0
        self.impossible = impossible
        self.written = []
        self.lines = []
        self.circles = []

    def push(self):
        self.balance += 1

    def pop(self):
        self.balance -= 1

    def get_font_metrics(self, image, text, multiline=False):
        self.calls += 1
        return SimpleNamespace(text_width=100000 if self.impossible else len(text)*self.font_size/2,
                               text_height=self.font_size, ascender=self.font_size*.8,
                               character_width=self.font_size/2)

    def text(self, **kwargs):
        self.written.append(kwargs)

    def rectangle(self, **kwargs):
        pass

    def line(self, *args):
        self.lines.append((args, self.stroke_color, self.stroke_width))

    def circle(self, *args):
        self.circles.append((args, self.stroke_color, self.stroke_width, self.fill_color))


class ImageProbe:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise AssertionError('Invalid image extent')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class RenderingSafetyTests(unittest.TestCase):
    def setUp(self):
        self.rectangles = []
        def layout(image, context, texts, rect, font_size):
            self.assertGreater(rect['width'], 0)
            self.assertGreater(rect['height'], 0)
            self.rectangles.append(dict(rect))
            return []
        style = {'Font': 'test-font', 'Color': 'green'}
        self.env = functions('www/scripts/renderer.py',
                             ['_drawDataDrivenBox', '_drawControlSymbol', '_symbolColumnWidth', '_numberColumnWidth',
                              '_buildJoyTexts', '_dataDrivenRowHeights',
                              'calculateBestFitFontSize', 'calculateBestFontSize'], {
            'math': math, 'Image': ImageProbe, 'Color': lambda c: c,
            'getFontPath': lambda *args: 'test-font', 'layoutText': layout,
            '_LEADER_COLOR': '#962320', '_SYMBOL_GLYPHS': {'press':'0','up':'^','stage1':'stage 1'},
            'normalize_input': runtime.normalize_input, 'matches_input': runtime.matches_input,
            'groupStyles': {'Ship': style, 'Modifier': style, 'General': style},
            'categoryStyles': {'General': style},
            'ModifierStyles': SimpleNamespace(index=lambda n: style),
            'isRedundantSpecialisation': lambda control, bind: False,
        })

    def test_sol_small_box_has_positive_text_area(self):
        row = {'symbol':'press','number':'1','_texts':[{'Text':'Fire'}]}
        self.env['_drawDataDrivenBox'](DrawingProbe(), None, {
            'label':'BTN1','box_xy':[74,204],'box_wh':[193,40], 'rows':[row]})
        self.assertEqual(len(self.rectangles), 1)
        self.assertGreater(self.rectangles[0]['height'], 20)

    def test_leader_has_white_halo_red_stroke_and_marked_hardware_anchor(self):
        context = DrawingProbe()
        box = {'box_xy':[100,200], 'box_wh':[400,120], 'button_xy':[800,500],
               'rows':[{}]}
        before = copy.deepcopy(box)
        self.env['_drawDataDrivenBox'](context, None, box)
        route = [((500,260),(650,260)), ((650,260),(650,500)), ((650,500),(800,500))]
        self.assertEqual(context.lines, [(p,'white',13) for p in route] +
                         [(p,'#962320',7) for p in route])
        self.assertEqual(context.circles, [(((800,500),(815,500)), 'white',5,'#962320')])
        self.assertEqual(context.balance, 0)
        self.assertEqual(box, before)

    def test_leader_detour_drops_vertically_onto_a_boxed_in_control(self):
        context = DrawingProbe()
        self.env['_drawDataDrivenBox'](context, None, {
            'box_xy':[100,200], 'box_wh':[400,120], 'button_xy':[800,500],
            'leader_via_y':80, 'rows':[{}]})
        route = [((500,260),(650,260)), ((650,260),(650,80)), ((650,80),(800,80)),
                 ((800,80),(800,500))]
        self.assertEqual(context.lines, [(p,'white',13) for p in route] +
                         [(p,'#962320',7) for p in route])
        self.assertEqual(context.circles[0][0][0], (800,500))

    def test_long_number_label_widens_its_column_instead_of_touching_the_text(self):
        boxes = {}
        for number in ('27', 'M2 27'):
            self.rectangles.clear()
            row = {'symbol':'up','number':number,'_texts':[{'Text':'Thrust Up'}]}
            self.env['_drawDataDrivenBox'](DrawingProbe(), None, {
                'label':'Hat','box_xy':[0,0],'box_wh':[900,100],'rows':[row]})
            boxes[number] = self.rectangles[0]['x']
        self.assertEqual(boxes['M2 27'] - boxes['27'], 28)

    def test_compact_leader_starts_at_actual_frame_not_reserved_height(self):
        context = DrawingProbe()
        self.env['_drawDataDrivenBox'](context, None, {
            'label':'Compact', 'box_xy':[100,200], 'box_wh':[900,600],
            'button_xy':[50,500], 'rows':[{}]}, compact=True)
        self.assertEqual(context.lines[0][0][0], (100,247))
        self.assertEqual(context.circles[0][0][0], (50,500))

    def test_no_anchor_or_imported_pdf_has_no_new_leader_or_endpoint(self):
        for extra in [{}, {'button_xy':[800,500], 'no_chrome':True}]:
            context = DrawingProbe()
            self.env['_drawDataDrivenBox'](context, None, {
                'box_xy':[100,200], 'box_wh':[400,120], 'rows':[{}], **extra})
            self.assertEqual(context.lines, [])
            self.assertEqual(context.circles, [])
            self.assertEqual(context.balance, 0)

    def test_tiny_word_symbol_gutters_leave_room_for_text(self):
        self.env['_drawDataDrivenBox'](DrawingProbe(), None, {
            'label':'Trigger','box_xy':[0,0],'box_wh':[40,30],
            'rows':[{'symbol':'stage1','number':1,'_texts':[{'Text':'Fire'}]}]})
        self.assertEqual(len(self.rectangles), 1)

    def test_unused_pdf_rows_keep_original_slot(self):
        box = {'box_xy':[100,100],'box_wh':[400,400],'no_chrome':True,
               'rows':[{'_texts':[]} for _ in range(4)]}
        box['rows'][1]['_texts'] = [{'Text':'Only down is bound'}]
        self.env['_drawDataDrivenBox'](DrawingProbe(), None, box)
        self.assertEqual(self.rectangles[0]['y'], 206)
        self.assertEqual(self.rectangles[0]['height'], 88)

    def test_pdf_field_rect_preserves_gap_and_offset(self):
        self.env['_drawDataDrivenBox'](DrawingProbe(), None, {
            'box_xy':[100,100],'box_wh':[400,400],'no_chrome':True,
            'rows':[{'field_rect':[.25,.6,.5,.1], '_texts':[{'Text':'Brake'}]}]})
        self.assertAlmostEqual(self.rectangles[0]['x'], 208)
        self.assertAlmostEqual(self.rectangles[0]['y'], 344)
        self.assertAlmostEqual(self.rectangles[0]['height'], 32)

    def test_empty_font_fit_is_safe(self):
        self.assertEqual(self.env['calculateBestFitFontSize'](DrawingProbe(), 100, 20, [], 40), 40)

    def test_compact_sparse_rows_do_not_stretch_into_unused_space(self):
        rows=[{'symbol':'press','number':n,'_texts':[
            {'Text':'HUD Mode','Style':self.env['groupStyles']['Ship']}]} for n in [2,1]]
        before=copy.deepcopy(rows)
        context=DrawingProbe()
        heights,size=self.env['_dataDrivenRowHeights'](context,None,rows,900,570,40)
        self.assertEqual(heights,[54,54])
        self.assertEqual(size,40)
        self.assertEqual(context.balance,0)
        self.assertEqual(rows,before)

    def test_compact_dense_encoder_rows_get_more_space_than_push(self):
        style=self.env['groupStyles']['Ship']
        rows=[{'symbol':'press','number':11,'_texts':[{'Text':'100% Throttle','Style':style}]},
              *[{'symbol':'up','number':n,'_texts':[
                  {'Text':'Long command name','Style':style} for _ in range(8)]} for n in [12,13]]]
        heights,size=self.env['_dataDrivenRowHeights'](DrawingProbe(),None,rows,900,780,40)
        self.assertEqual(size,40)
        self.assertEqual(heights[0],54)
        self.assertGreater(heights[1],heights[0])
        self.assertEqual(heights[1],heights[2])
        self.assertLess(sum(heights),780)

    def test_compact_layout_respects_height_budget_with_shared_font(self):
        rows=[{'_texts':[{'Text':'Long command name','Style':self.env['groupStyles']['Ship']}
                         for _ in range(12)]} for _ in range(3)]
        heights,size=self.env['_dataDrivenRowHeights'](DrawingProbe(),None,rows,500,240,40)
        self.assertLess(size,40)
        self.assertLessEqual(sum(heights),240)
        self.assertTrue(all(h>=54 for h in heights))

    def test_compact_tiny_boxes_keep_existing_geometry(self):
        rows=[{'_texts':[{'Text':'Fire','Style':self.env['groupStyles']['Ship']}]}]
        heights,size=self.env['_dataDrivenRowHeights'](DrawingProbe(),None,rows,193,30,40)
        self.assertEqual(heights,[30])
        self.assertEqual(size,40)

    def test_compact_draw_uses_variable_text_rectangles(self):
        style=self.env['groupStyles']['Ship']
        rows=[{'_texts':[{'Text':'Fire','Style':style}]},
              {'_texts':[{'Text':'Long command name','Style':style} for _ in range(8)]}]
        self.env['_drawDataDrivenBox'](DrawingProbe(),None,{
            'label':'Mixed density','box_xy':[10,20],'box_wh':[900,610],'rows':rows},compact=True)
        self.assertEqual(self.rectangles[0]['height'],42)
        self.assertGreater(self.rectangles[1]['height'],self.rectangles[0]['height'])
        self.assertEqual(self.rectangles[1]['y'],self.rectangles[0]['y']+54)

    def test_compact_never_moves_imported_pdf_slots(self):
        box={'box_xy':[100,100],'box_wh':[400,400],'no_chrome':True,
             'rows':[{'_texts':[]} for _ in range(4)]}
        box['rows'][1]['_texts']=[{'Text':'Only down is bound'}]
        self.env['_drawDataDrivenBox'](DrawingProbe(),None,box,compact=True)
        self.assertEqual(self.rectangles[0]['y'],206)
        self.assertEqual(self.rectangles[0]['height'],88)

    def test_font_fit_stops_and_restores_context(self):
        context = DrawingProbe(impossible=True)
        with self.assertRaisesRegex(ValueError, 'minimum font size'):
            self.env['calculateBestFitFontSize'](context, 1, 1,
                [{'Text':'Very long', 'Style':{'Font':'test'}}], 40)
        self.assertEqual(context.calls, 40)
        self.assertEqual(context.balance, 0)

    def test_font_fit_accepts_exact_height(self):
        context = DrawingProbe()
        self.assertEqual(self.env['calculateBestFitFontSize'](context, 200, 20,
            [{'Text':'Test','Style':{'Font':'test'}}], 20), 20)

    def test_font_fit_checks_long_commands_after_a_short_command(self):
        texts = [{'Text':text, 'Style':{'Font':'test'}} for text in ['A', 'X'*30]]
        size = self.env['calculateBestFitFontSize'](DrawingProbe(), 100, 100, texts, 10)
        self.assertEqual(size, 6)
        self.assertTrue(all(len(t['Text'])*size/2 <= 100 for t in texts))

    def test_invalid_dimensions_fail_before_image_creation(self):
        for width, height in [(0,10),(10,-12)]:
            with self.assertRaises(ValueError):
                self.env['calculateBestFitFontSize'](DrawingProbe(), width, height, [], 40)

    def test_half_axes_do_not_duplicate_opposite_actions(self):
        pk = {'Device':'TEST','DeviceIndex':0,'Key':'Joy_RYAxis','BaseKey':'Neg_Joy_RYAxis',
              'Binds':{'Unmodified':{'Controls':{
                  'Left':{'Name':'Left thrust','Group':'Ship','InputKey':'Neg_Joy_RYAxis'},
                  'Right':{'Name':'Right thrust','Group':'Ship','InputKey':'Pos_Joy_RYAxis'},
                  'Axis':{'Name':'Analogue thrust','Group':'Ship','InputKey':'Joy_RYAxis'}}}}}
        physical = {'TEST::0::Joy_RYAxis':pk}
        before = copy.deepcopy(physical)
        build = self.env['_buildJoyTexts']
        self.assertEqual([t['Text'] for t in build(['TEST'],'Neg_Joy_RYAxis',0,physical,{},'Group')], ['Left thrust'])
        self.assertEqual([t['Text'] for t in build(['TEST'],'Pos_Joy_RYAxis',0,physical,{},'Group')], ['Right thrust'])
        self.assertEqual(len(build(['TEST'],'Joy_RYAxis',0,physical,{},'Group')),3)
        self.assertEqual(physical,before)

    def test_missing_inputs_distinguishes_full_and_half_axes(self):
        mapping = {'boxes':[{'rows':[{'joy':'Neg_Joy_RYAxis'}]}]}
        keys = ['Neg_Joy_RYAxis','Pos_Joy_RYAxis','Joy_RYAxis']
        self.assertEqual(runtime.missing_inputs(mapping,keys), ['Joy_RYAxis','Pos_Joy_RYAxis'])
        mapping['boxes'][0]['rows'][0]['joy'] = 'Joy_RYAxis'
        self.assertEqual(runtime.missing_inputs(mapping,keys),[])

    def test_unknown_or_empty_command_styles_use_general_fallback(self):
        for field, styling in [('Category','Category'),('Group','Group')]:
            for value in ['Unregistered command style', None, '']:
                with self.subTest(field=field, value=value):
                    control={'Name':'Example','Group':'Ship','Category':'General',
                             'InputKey':'Joy_1',field:value}
                    modifier='TEST::0::Joy_2'
                    physical={'TEST::0::Joy_1':{'Device':'TEST','DeviceIndex':0,
                        'Key':'Joy_1','BaseKey':'Joy_1','Binds':{
                            'Unmodified':{'Controls':{'Example':control}},
                            modifier:{'Controls':{'Example':control}}}}}
                    modifiers={modifier:[{'Number':1,'ModifierKey':modifier}]}
                    texts=self.env['_buildJoyTexts'](['TEST'],'Joy_1',0,physical,modifiers,styling)
                    self.assertEqual(len(texts),2)
                    expected=self.env['categoryStyles' if styling=='Category' else 'groupStyles']['General']
                    self.assertTrue(all(t['Style'] is expected for t in texts))

    def test_modifier_only_button_is_rendered_and_counted(self):
        modifiers = {'TEST::0::Joy_3':[{'Number':1,'Device':'TEST','DeviceIndex':0,
                                      'Key':'Joy_3','ModifierKey':'TEST::0::Joy_3'}]}
        texts = self.env['_buildJoyTexts'](['TEST'],'Joy_3',0,{},modifiers,'Group')
        self.assertEqual([t['Text'] for t in texts], ['Modifier 1'])
        self.assertEqual(runtime.used_inputs({},modifiers,['TEST'],0),{'Joy_3'})

    def test_directional_modifier_is_not_shown_on_opposite_half_axis(self):
        modifiers = {'TEST::0::Pos_Joy_RYAxis':[{'Number':1,'Device':'TEST',
                     'DeviceIndex':0,'Key':'Pos_Joy_RYAxis','ModifierKey':'TEST::0::Pos_Joy_RYAxis'}]}
        build = self.env['_buildJoyTexts']
        self.assertEqual(build(['TEST'],'Neg_Joy_RYAxis',0,{},modifiers,'Group'),[])
        self.assertEqual(len(build(['TEST'],'Joy_RYAxis',0,{},modifiers,'Group')),1)

    def test_physical_warthog_does_not_imply_target(self):
        self.assertEqual(runtime.mapping_software_warning({
            'ThrustMasterWarthogJoystick::0': {'HandledDevices':['ThrustMasterWarthogCombined']},
            'ThrustMasterWarthogThrottle::0':None}), '')
        self.assertIn('virtual', runtime.mapping_software_warning({'ThrustMasterWarthogCombined::0':None}))

    def test_parser_ignores_empty_nodes_and_preserves_each_direction(self):
        try:
            from lxml import etree
        except ImportError:
            self.skipTest('lxml required')
        controls = {name:{'Name':name,'Group':'Ship','Type':'Digital'}
                    for name in ['Left','Right','Empty','MissingKey']}
        parser = functions('www/scripts/parser.py',['parseBindings','_rewriteVPCDevice'], {
            '__name__':'standalone_probe', 'etree':etree, 'html':__import__('html'),
            'OrderedDict':OrderedDict, 'controls':controls, 'supportedDevices':{},
            'logError':lambda *args:None, 'mapping_software_warning':runtime.mapping_software_warning,
        })
        errors = SimpleNamespace(errors='',deviceWarnings='Old TARGET warning')
        xml = '<Root><Empty><Primary/><Secondary Device="{NoDevice}"/></Empty>' \
              '<MissingKey><Primary Device="TEST"/></MissingKey>' \
              '<Left><Primary Device="TEST" Key="Neg_Joy_RYAxis"/></Left>' \
              '<Right><Primary Device="TEST" Key="Pos_Joy_RYAxis"/></Right></Root>'
        physical, _, devices = parser['parseBindings']('test',xml,['Ship'],errors)
        self.assertEqual(set(devices),{'TEST::0'})
        actions = physical['TEST::0::Joy_RYAxis']['Binds']['Unmodified']['Controls']
        self.assertEqual(actions['Left']['InputKey'],'Neg_Joy_RYAxis')
        self.assertEqual(actions['Right']['InputKey'],'Pos_Joy_RYAxis')
        self.assertEqual(errors.deviceWarnings,'')
        self.assertNotIn('InputKey',controls['Left'])


class FlowLayoutAndPrecedenceTests(unittest.TestCase):
    """Photo-less mappings (S-TECS) and mappings replacing a legacy template."""

    def setUp(self):
        self.env = functions('www/scripts/renderer.py',
                             ['_flowColumnWidth', '_flowPositions', '_symbolColumnWidth'], {
            'math': math, '_FLOW_MARGIN': 40, '_FLOW_GAP': 24, '_FLOW_TOP': 160,
            '_FLOW_HEADING_H': 64, '_FLOW_ZONE_GAP': 40,
            '_SYMBOL_GLYPHS': {'press': '0', 'push': 'push', 'stage1': 'stage 1',
                               'ccw': 'ccw', 'cw': 'cw', 'mid': 'mid'},
        })

    def test_flow_packs_zones_in_columns_without_holes(self):
        boxes = [{'label': 'A', 'zone': 'BASE'}, {'label': 'B', 'zone': 'BASE'},
                 {'label': 'C', 'zone': 'GRIP'}, {'label': 'D', 'zone': 'BASE'}]
        before = copy.deepcopy(boxes)
        placed, headings, height = self.env['_flowPositions'](boxes, [100, 50, 80, 30], 1000, 2)
        self.assertEqual(boxes, before)
        # Zones keep their first-appearance order, D joins BASE under B (shortest column)
        self.assertEqual([b['label'] for b in placed], ['A', 'B', 'D', 'C'])
        self.assertEqual([h[0] for h in headings], ['BASE', 'GRIP'])
        a, b, d, c = (p['box_xy'] for p in placed)
        self.assertEqual(a, [40, 224])
        self.assertEqual(b, [512, 224])
        self.assertEqual(d, [512, 224 + 50 + 24])
        colw = self.env['_flowColumnWidth'](1000, 2)
        self.assertEqual(placed[0]['box_wh'], [math.floor(colw), 100])
        # Next zone starts below the tallest column of the previous one (B + D)
        tallest = 224 + 50 + 24 + 30
        self.assertEqual(headings[1][2], tallest + 40 + 44)
        self.assertEqual(c, [40, tallest + 40 + 64])
        self.assertEqual(height, c[1] + 80 + 40)
        for p in placed:
            self.assertLessEqual(p['box_xy'][0] + p['box_wh'][0], 1000 - 40)

    def test_flow_without_zones_and_empty_card(self):
        placed, headings, height = self.env['_flowPositions']([{'label': 'A'}], [94], 2400)
        self.assertEqual(headings, [])
        self.assertEqual(placed[0]['box_xy'], [40, 160])
        self.assertEqual(self.env['_flowPositions']([], [], 2400), ([], [], 160))

    def test_new_word_glyphs_keep_existing_gutters(self):
        width = self.env['_symbolColumnWidth']
        self.assertEqual([width('press'), width('push'), width('stage1')], [44, 150, 150])
        self.assertEqual([width('cw'), width('ccw'), width('mid'), width(None)], [44, 70, 70, 0])

    def test_published_mapping_replaces_legacy_template_except_virtual_controllers(self):
        drawn = []
        legacy = functions('www/web.py', ['generate_legacy_images'], {
            'supportedDevices': {'Keyboard': {}, 'VC1': {'Template': 'vc1', 'HandledDevices': ['STECS::0']},
                                 'VC2': {'Template': 'vc2', 'HandledDevices': ['STECS::1']}},
            'createHOTASImage': lambda *args: drawn.append(args[2]), 'logError': lambda *a: None})
        devices = {'STECS::0': {}, 'STECS::1': {}}
        created, _ = legacy['generate_legacy_images']({}, {}, devices, None, False, 'Group', '',
                                                     {'STECS::0'})
        self.assertEqual((created, drawn), (['VC2::1'], ['vc2']))

        mapping = {'image': 'stecs', 'device_ids': ['STECS'], 'boxes': [],
                   'legacy_when_index_present': [1]}
        rendered = []
        import json
        web = functions('www/web.py', ['render_data_driven'], {
            'database': SimpleNamespace(get_published_controller_mappings=lambda: [
                {'status': 'published', 'device_id': 'STECS', 'mapping_json': json.dumps(mapping)}]),
            'createDataDrivenImage': lambda m, *a, **kw: rendered.append(kw['deviceIndex']),
            'logError': lambda *a: None})
        self.assertEqual(web['render_data_driven']({}, {}, {'STECS::0': {}}, None, False, 'Group'),
                         (['stecs'], {'STECS::0'}))
        self.assertEqual(web['render_data_driven']({}, {}, devices, None, False, 'Group'),
                         ([], set()))
        self.assertEqual(rendered, [0])


if __name__ == '__main__':
    unittest.main()
