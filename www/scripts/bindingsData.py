#!/usr/bin/env python3

__version__ = '1.3'

from collections import OrderedDict


supportedDevices = OrderedDict([
    ('HotasCougar',{'Template': 'hotascougar', 'HandledDevices': ['044F0400']}),
    ('LogitechExtreme3DPro', {'Template': 'extreme3dpro', 'HandledDevices': ['LogitechExtreme3DPro']}),
    ('Logitech710WirelessGamepad', {'Template': 'f710', 'HandledDevices': ['Logitech710WirelessGamepad']}),
    ('LogitechGTWheel', {'Template': 'gtwheel', 'HandledDevices': ['046DC29A']}),
    ('LogitechG940', {'Template': 'g940', 'HandledDevices': ['LogitechG940Joystick', 'LogitechG940Throttle']}),
    ('T16000M', {'Template': 't16000m', 'HandledDevices': ['T16000M']}),
    ('T16000MFCS', {'Template': 't16000mfcs', 'HandledDevices': ['T16000MFCS', 'T16000MTHROTTLE']}),
    ('TCASidestickLeft', {'Template': 'tca-left', 'HandledDevices': ['044F0405']}),
    ('TCASidestickRight', {'Template': 'tca-right', 'HandledDevices': ['044F0406']}),
    ('TFlightHOTASX', {'Template': 'hotasx', 'HandledDevices': ['ThrustMasterTFlightHOTASX']}),
    ('ThrustMasterHOTAS4', {'Template': 'hotas4', 'HandledDevices': ['ThrustMasterHOTAS4','TFlightHotasOne']}),
    ('T-Rudder', {'Template': 'tfrp', 'HandledDevices': ['T-Rudder']}),
    ('TPR-Rudder', {'Template': 'tpr-rudder', 'HandledDevices': ['044FB68F']}),
    ('TFlightStickX', {'Template': 'stickx', 'HandledDevices': ['044FB106']}),
    ('Warthog', {'Template': 'warthog', 'HandledDevices': ['ThrustMasterWarthogJoystick', 'ThrustMasterWarthogThrottle', 'ThrustMasterWarthogCombined']}),
    ('CobraM5', {'Template': 'cobram5', 'HandledDevices': ['11C05603', '11C05605']}),
    ('Gladiator', {'Template': 'gladiator', 'HandledDevices': ['231D0121']}),
    ('Cougar', {'Template': 'cougar', 'HandledDevices': ['044FB351', '044FB352']}),
    ('SaitekFLY5', {'Template': 'fly5', 'HandledDevices': ['SaitekFLY5', '06A30836']}),
    ('SaitekX45', {'Template': 'x45', 'HandledDevices': ['SaitekX45']}),
    ('SaitekX52', {'Template': 'x52', 'HandledDevices': ['SaitekX52']}),
    ('SaitekX52Pro', {'Template': 'x52pro', 'HandledDevices': ['SaitekX52Pro']}),
    ('SaitekX55', {'Template': 'x55', 'HandledDevices': ['SaitekX55Joystick', 'SaitekX55Throttle']}),
    ('SaitekX56', {'Template': 'x56', 'HandledDevices': ['SaitekX56Joystick', 'SaitekX56Throttle', '07382221', '0738A221']}),
    ('SaitekProFlightPedals', {'Template': 'proflightpedals', 'HandledDevices': ['SaitekProFlightRudderPedals', '06A30765']}),
    ('SaitekProFlightCombatPedals', {'Template': 'proflightcombatpedals', 'HandledDevices': ['SaitekProFlightCombatRudderPedals']}),
    ('CHFighterStick', {'Template': 'chfighter', 'KeyDevices': ['CHFighterStick', '068EC0F3'], 'HandledDevices': ['CHFighterStick', '068EC0F3', 'CHProThrottle1', 'CHProThrottle2', '068EC010']}),
    ('CHCombatStick', {'Template': 'chcombat', 'KeyDevices': ['CHCombatStick'], 'HandledDevices': ['CHCombatStick', 'CHProThrottle1', 'CHProThrottle2', '068EC010']}),
    ('CHProThrottle', {'Template': 'chfighter', 'HandledDevices': ['CHProThrottle1', 'CHProThrottle2', '068EC010']}),
    ('CHThrottleQuadrant', {'Template': 'chquadrant', 'HandledDevices': ['068E00FA']}),
    ('CHProFlightThrottleQuadrant', {'Template': 'chproflightquadrant', 'HandledDevices': ['06A30C2D']}),
    ('CHProPedals', {'Template': 'chpropedals', 'HandledDevices': ['CHProPedals', '068E00F2']}),
    ('SidePanelControlDeck', {'Template': 'sidepanelcontroldeck', 'HandledDevices': ['07382218']}),
    ('XBox', {'Template': 'xbox', 'HandledDevices': ['XB360 Pad', '045E02FF', '045E02DD','28DE11FF','045E02E0','045E02FD']}),
    ('XBoxElite', {'Template': 'xboxelite', 'HandledDevices': ['045E02E3','045E0B22']}),
    ('GamePad', {'Template': 'xbox', 'HandledDevices': ['GamePad']}),
    ('Sabretooth', {'Template': 'sabretooth', 'HandledDevices': ['1689FE00']}),
    ('LogitechG940Pedals', {'Template': 'g940pedals', 'HandledDevices': ['LogitechG940Pedals']}),
    ('SlawBF109Pedals', {'Template': 'slawbf109pedals', 'HandledDevices': ['SlawFlightControlRudder']}),
    ('MFGCrosswind', {'Template': 'crosswind', 'HandledDevices': ['16D00A38', '85640203']}),
    ('DS4', {'Template': 'ds4', 'HandledDevices': ['DS4', 'DualShock4']}),
    ('VPC-WarBRD-DELTA-Left', {'Template': 'vpc-warbrd-delta-left', 'HandledDevices': ['03EB2042']}),
    ('VPC-WarBRD-DELTA-Right', {'Template': 'vpc-warbrd-delta-right', 'HandledDevices': ['03EB2044']}),
    ('VPC-ALPHA-Left', {'Template': 'vpc-alpha-left', 'HandledDevices': ['03EB2046','334483EB', '334480CB','3344C0CB']}),
    ('VPC-ALPHA-Right', {'Template': 'vpc-alpha-right', 'HandledDevices': ['03EB2048','334443EB','334440CB','334400CB','3344412F']}),
    ('VPC-ALPHA-Left-Custom', {'Template': 'vpc-alpha-left', 'HandledDevices': ['03EB9901']}),
    ('VPC-ALPHA-Right-Custom', {'Template': 'vpc-alpha-right', 'HandledDevices': ['03EB9902']}),
    ('VPC-ALPHA-Prime-Left', {'Template': 'vpc-alpha-prime-left', 'HandledDevices': ['334483F3','3344838F','334403F3','3344038F','334443F5']}),
    ('VPC-ALPHA-Prime-Right', {'Template': 'vpc-alpha-prime-right', 'HandledDevices': ['334443F4','33444390','3344C3F3','334483F4','334403F4','334440D4','33440390']}),
    ('VPC-FLNKR-Right', {'Template': 'vpc-flnkr-grip', 'HandledDevices': ['33444393']}),
    ('VPC-MongoosT-50CM2-Throttle', {'Template': 'vpc-mongoost-50cm2-throttle', 'HandledDevices': ['33448195']}),
    ('VPC-MongoosT-50CM3-Throttle', {'Template': 'vpc-mongoost-50cm3-throttle', 'HandledDevices': ['33448197','33440197','33448198','VPCThrottle']}),
    ('VPC-MongoosT-50CM3-Throttle-32B', {'Template': 'vpc-mongoost-50cm3-throttle-32b', 'KeyDevices': ['VPC-MongoosT-50CM3-Throttle-32B0', 'VPC-MongoosT-50CM3-Throttle-32B1', 'VPC-MongoosT-50CM3-Throttle-32B2'], 'HandledDevices': ['VPC-MongoosT-50CM3-Throttle-32B0', 'VPC-MongoosT-50CM3-Throttle-32B1', 'VPC-MongoosT-50CM3-Throttle-32B2']}),
    ('VPC-MongoosT-50CM3-Throttle-32B-No-Shift', {'Template': 'vpc-mongoost-50cm3-throttle-32b-no-shift', 'KeyDevices': ['VPC-MongoosT-50CM3-Throttle-32B-NS0', 'VPC-MongoosT-50CM3-Throttle-32B-NS1'], 'HandledDevices': ['VPC-MongoosT-50CM3-Throttle-32B-NS0', 'VPC-MongoosT-50CM3-Throttle-32B-NS1']}),
    ('VPC-Control-Panel-2', {'Template': 'vpc-controlpanel2', 'HandledDevices': ['3344825A']}),
    ('VKB-Kosmosima-SCG-Left', {'Template': 'vkb-kosmosima-scg-left', 'HandledDevices': ['231D0127']}),
    ('VKB-Kosmosima-SCG-Right', {'Template': 'vkb-kosmosima-scg-right', 'HandledDevices': ['231D0126']}),
    ('VKB-Gladiator-NXT-Premium-Right', {'Template': 'vkb-gladiator-nxt-premium-right', 'HandledDevices': ['231D0200']}),
    ('VKB-Gladiator-NXT-Premium-Left', {'Template': 'vkb-gladiator-nxt-premium-left', 'HandledDevices': ['231D0201']}),
    ('VKB-Gladiator-NXT-Premium-Right-OTA', {'Template': 'vkb-gladiator-nxt-premium-right-ota', 'HandledDevices': ['231D3200']}),
    ('VKB-Gladiator-NXT-Premium-Left-OTA', {'Template': 'vkb-gladiator-nxt-premium-left-ota', 'HandledDevices': ['231D3201']}),
    ('VKB-STECS-VC1', {'Template': 'vkb-stecs-1', 'HandledDevices': ['231D012D::0']}),
    ('VKB-STECS-VC2', {'Template': 'vkb-stecs-2', 'HandledDevices': ['231D012D::1']}),
    ('VKB-GNX-WWII-Throttle', {'Template': 'vkb-gnx-ww2-throttle', 'HandledDevices': ['231D2214']}),
    ('Winwing-Orion-Throttle-2-F18-Handle', {'Template': 'winwing-orion-throttle2-f18-handle', 'HandledDevices': ['4098BE62']}),
    ('Winwing-Ursa-Minor-Fighter-Right', {'Template': 'winwing-ursa-minor-fighter-right', 'HandledDevices': ['4098BC2A']}),
    ('Winwing-Ursa-Minor-Fighter-Left', {'Template': 'winwing-ursa-minor-fighter-left', 'HandledDevices': ['4098BC29']}),
    ('Keyboard', {'Template': 'keyboard', 'HandledDevices': ['Keyboard']})
])

#controls went in here!

hotasMap = {    # map aliases to rendering box definitions - DRY code out
    #'XB360 Pad' : 'XB360 Pad',
    '045E02FF' : 'XB360 Pad',
    '045E02DD' : 'XB360 Pad',
    '28DE11FF' : 'XB360 Pad',
    '045E02E0' : 'XB360 Pad'
}


# default height is 54 (px)
hotasDetails = {
        '044F0400': {
        'displayName': 'HotasCougar',
        'Joy_1': {'Type': 'Digital', 'x': 2003, 'y': 557, 'width': 670}, # Primary trigger half press
        'Joy_2': {'Type': 'Digital', 'x': 1948, 'y': 218, 'width': 892}, # Top trigger red button
        'Joy_3': {'Type': 'Digital', 'x': 2080, 'y': 1094, 'width': 592}, # Pinky button
        'Joy_4': {'Type': 'Digital', 'x': 2080, 'y': 1004, 'width': 592}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 2881, 'y': 218, 'width': 892}, # Top side button
        'Joy_6': {'Type': 'Digital', 'x': 2003, 'y': 611, 'width': 670}, # Primary trigger full press
        'Joy_7': {'Type': 'Digital', 'x': 1995, 'y': 302, 'width': 676}, # Left hat up
        'Joy_8': {'Type': 'Digital', 'x': 1995, 'y': 356, 'width': 676}, # Left hat right
        'Joy_9': {'Type': 'Digital', 'x': 1995, 'y': 410, 'width': 676}, # Left hat down
        'Joy_10': {'Type': 'Digital', 'x': 1995, 'y': 464, 'width': 676}, # Left hat left
        'Joy_11': {'Type': 'Digital', 'x': 3042, 'y': 562, 'width': 774}, # Right hat up
        'Joy_12': {'Type': 'Digital', 'x': 3042, 'y': 616, 'width': 774}, # Right hat right
        'Joy_13': {'Type': 'Digital', 'x': 3042, 'y': 670, 'width': 774}, # Right hat down
        'Joy_14': {'Type': 'Digital', 'x': 3042, 'y': 724, 'width': 774}, # Right hat left
        'Joy_15': {'Type': 'Digital', 'x': 2004, 'y': 700, 'width': 667}, # Thumb hat up
        'Joy_16': {'Type': 'Digital', 'x': 2004, 'y': 754, 'width': 667}, # Thumb hat right
        'Joy_17': {'Type': 'Digital', 'x': 2004, 'y': 808, 'width': 667}, # Thumb hat down
        'Joy_18': {'Type': 'Digital', 'x': 2004, 'y': 862, 'width': 667}, # Thumb hat left
        'Joy_19': {'Type': 'Digital', 'x': 372, 'y': 1640, 'width': 683}, # Rdr Cursor button
        'Joy_20': {'Type': 'Digital', 'x': 1495, 'y': 1679, 'width': 772}, #Radio select down
        'Joy_21': {'Type': 'Digital', 'x': 1495, 'y': 1733, 'width': 772}, #Radio select up
        'Joy_22': {'Type': 'Digital', 'x': 1495, 'y': 1787, 'width': 772}, #Radio select right
        'Joy_23': {'Type': 'Digital', 'x': 1495, 'y': 1841, 'width': 772}, #Radio select left
        'Joy_24': {'Type': 'Digital', 'x': 1220, 'y': 649, 'width': 633}, #Man RNG/Uncage button
        'Joy_25': {'Type': 'Digital', 'x': 1310, 'y': 1022, 'width': 690}, #Dog fight up
        'Joy_26': {'Type': 'Digital', 'x': 1310, 'y': 1076, 'width': 690}, #Dog fight down
        'Joy_27': {'Type': 'Digital', 'x': 1310, 'y': 1214, 'width': 690}, #SPD BRK up
        'Joy_28': {'Type': 'Digital', 'x': 1310, 'y': 1268, 'width': 690}, #SPD BRK down
        'Joy_POV1Up': {'Type': 'Digital', 'x': 3042, 'y': 304, 'width': 774}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 3042, 'y': 358, 'width': 774}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 3042, 'y': 412, 'width': 774}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 3042, 'y': 466, 'width': 774}, # PoV hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3124, 'y': 870, 'width': 692}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3124, 'y': 816, 'width': 692}, # Stick up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 108, 'y': 364, 'width': 682}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1220, 'y': 595, 'width': 633}, # Man RNG/Uncage
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1310, 'y': 1424, 'width': 690}, # Ant Elev
        'Joy_VAxis': {'Type': 'Analogue', 'x': 372, 'y': 1586, 'width': 683}, # Rdr Cursor
    },
    'LogitechExtreme3DPro': {
        'Joy_1': {'Type': 'Digital', 'x': 474, 'y': 904, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 474, 'y': 1004, 'width': 1092}, # Side trigger
        'Joy_3': {'Type': 'Digital', 'x': 424, 'y': 784, 'width': 1092}, # Bottom-left button
        'Joy_4': {'Type': 'Digital', 'x': 2124, 'y': 784, 'width': 1092}, # Bottom-right button
        'Joy_5': {'Type': 'Digital', 'x': 424, 'y': 654, 'width': 1092}, # Top-left button
        'Joy_6': {'Type': 'Digital', 'x': 2124, 'y': 654, 'width': 1092}, # Top-right button
        'Joy_7': {'Type': 'Digital', 'x': 244, 'y': 1434, 'width': 542, 'height': 108}, # Left bank top-left button
        'Joy_8': {'Type': 'Digital', 'x': 794, 'y': 1434, 'width': 542, 'height': 108}, # Left bank top-right button
        'Joy_9': {'Type': 'Digital', 'x': 244, 'y': 1550, 'width': 542, 'height': 108}, # Left bank middle-left button
        'Joy_10': {'Type': 'Digital', 'x': 794, 'y': 1550, 'width': 542, 'height': 108}, # Left bank middle-right button
        'Joy_11': {'Type': 'Digital', 'x': 244, 'y': 1666, 'width': 542, 'height': 108}, # Left bank bottom-left button
        'Joy_12': {'Type': 'Digital', 'x': 794, 'y': 1666, 'width': 542, 'height': 108}, # Left bank bottom-right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 864, 'y': 374, 'width': 1932}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 864, 'y': 430, 'width': 1932}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 864, 'y': 486, 'width': 1932}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 864, 'y': 542, 'width': 1932}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2357, 'y': 980, 'width': 1132}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2864, 'y': 1574, 'width': 832}, # Stick throttle slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2357, 'y': 924, 'width': 1132}, # Stick pitch
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2357, 'y': 868, 'width': 1132}, # Stick roll
    },
    'T16000M': {
        'Joy_1': {'Type': 'Digital', 'x': 2124, 'y': 624, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 474, 'y': 624, 'width': 1092}, # Bottom button
        'Joy_3': {'Type': 'Digital', 'x': 474, 'y': 494, 'width': 1092}, # Left-hand button
        'Joy_4': {'Type': 'Digital', 'x': 2124, 'y': 494, 'width': 1092}, # Right-hand button
        'Joy_5': {'Type': 'Digital', 'x': 24, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-left button
        'Joy_6': {'Type': 'Digital', 'x': 574, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-middle button
        'Joy_7': {'Type': 'Digital', 'x': 1124, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-right button
        'Joy_8': {'Type': 'Digital', 'x': 1124, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-right button
        'Joy_9': {'Type': 'Digital', 'x': 574, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-middle button
        'Joy_10': {'Type': 'Digital', 'x': 24, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-left button
        'Joy_11': {'Type': 'Digital', 'x': 3264, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-right button
        'Joy_12': {'Type': 'Digital', 'x': 2714, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-middle button
        'Joy_13': {'Type': 'Digital', 'x': 2164, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-left button
        'Joy_14': {'Type': 'Digital', 'x': 2164, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-left button
        'Joy_15': {'Type': 'Digital', 'x': 2714, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-middle button
        'Joy_16': {'Type': 'Digital', 'x': 3264, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1542, 'y': 214, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1542, 'y': 270, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1542, 'y': 326, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1542, 'y': 382, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2357, 'y': 980, 'width': 1132}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2584, 'y': 1750, 'width': 832}, # Stick throttle slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2357, 'y': 924, 'width': 1132}, # Stick pitch
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2357, 'y': 868, 'width': 1132}, # Stick roll
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2357, 'y': 980, 'width': 1132}, # Stick twist    
    },
    'T16000MFCS': {
        'Joy_1': {'Type': 'Digital', 'x': 1804, 'y': 844, 'width': 642, 'height': 108}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2764, 'y': 604, 'width': 992}, # Bottom button
        'Joy_3': {'Type': 'Digital', 'x': 1754, 'y': 484, 'width': 692}, # Left-hand button
        'Joy_4': {'Type': 'Digital', 'x': 2764, 'y': 504, 'width': 992}, # Right-hand button
        'Joy_5': {'Type': 'Digital', 'x': 1254, 'y': 1244, 'width': 292, 'height': 108}, # Left bank top-left button
        'Joy_6': {'Type': 'Digital', 'x': 1554, 'y': 1244, 'width': 292, 'height': 108}, # Left bank top-middle button
        'Joy_7': {'Type': 'Digital', 'x': 1854, 'y': 1244, 'width': 292, 'height': 108}, # Left bank top-right button
        'Joy_8': {'Type': 'Digital', 'x': 1854, 'y': 1360, 'width': 292, 'height': 108}, # Left bank bottom-right button
        'Joy_9': {'Type': 'Digital', 'x': 1554, 'y': 1360, 'width': 292, 'height': 108}, # Left bank bottom-middle button
        'Joy_10': {'Type': 'Digital', 'x': 1254, 'y': 1360, 'width': 292, 'height': 108}, # Left bank bottom-left button
        'Joy_11': {'Type': 'Digital', 'x': 3484, 'y': 992, 'width': 292, 'height': 108}, # Right bank top-right button
        'Joy_12': {'Type': 'Digital', 'x': 3184, 'y': 992, 'width': 292, 'height': 108}, # Right bank top-middle button
        'Joy_13': {'Type': 'Digital', 'x': 2884, 'y': 992, 'width': 292, 'height': 108}, # Right bank top-left button
        'Joy_14': {'Type': 'Digital', 'x': 2884, 'y': 1108, 'width': 292, 'height': 108}, # Right bank bottom-left button
        'Joy_15': {'Type': 'Digital', 'x': 3184, 'y': 1108, 'width': 292, 'height': 108}, # Right bank bottom-middle button
        'Joy_16': {'Type': 'Digital', 'x': 3484, 'y': 1108, 'width': 292, 'height': 108}, # Right bank bottom-right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2524, 'y': 214, 'width': 1192}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2524, 'y': 270, 'width': 1192}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2524, 'y': 326, 'width': 1192}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2524, 'y': 382, 'width': 1192}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2824, 'y': 856, 'width': 932}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2944, 'y': 1593, 'width': 832}, # Stick throttle slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2824, 'y': 800, 'width': 932}, # Stick pitch
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2824, 'y': 744, 'width': 932}, # Stick roll
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2824, 'y': 856, 'width': 932},  # Stick twist
    },
    'T16000MTHROTTLE': {
        'Joy_1': {'Type': 'Digital', 'x': 294, 'y': 1244, 'width': 792}, # Thumb button
        'Joy_2': {'Type': 'Digital', 'x': 1774, 'y': 1774, 'width': 892}, # Pinky button
        'Joy_3': {'Type': 'Digital', 'x': 1714, 'y': 1664, 'width': 892}, # Ring finger button
        'Joy_4': {'Type': 'Digital', 'x': 1484, 'y': 1514, 'width': 692}, # Middle finger rocker up
        'Joy_5': {'Type': 'Digital', 'x': 1484, 'y': 1570, 'width': 692}, # Middle finger rocker down
        'Joy_6': {'Type': 'Digital', 'x': 244, 'y': 1866, 'width': 732}, # Index finger mouse push
        'Joy_7': {'Type': 'Digital', 'x': 1024, 'y': 654, 'width': 692}, # Middle hat up
        'Joy_8': {'Type': 'Digital', 'x': 1024, 'y': 710, 'width': 692}, # Middle hat right
        'Joy_9': {'Type': 'Digital', 'x': 1024, 'y': 766, 'width': 692}, # Middle hat down
        'Joy_10': {'Type': 'Digital', 'x': 1024, 'y': 820, 'width': 692}, # Middle hat left
        'Joy_11': {'Type': 'Digital', 'x': 1034, 'y': 929, 'width': 692}, # Middle hat up
        'Joy_12': {'Type': 'Digital', 'x': 1034, 'y': 985, 'width': 692}, # Castle hat right
        'Joy_13': {'Type': 'Digital', 'x': 1034, 'y': 1041, 'width': 692}, # Castle hat down
        'Joy_14': {'Type': 'Digital', 'x': 1034, 'y': 1097, 'width': 692}, # Castle hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1014, 'y': 364, 'width': 692}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1014, 'y': 420, 'width': 692}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1014, 'y': 476, 'width': 692}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1014, 'y': 532, 'width': 692}, # PoV hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 244, 'y': 1810, 'width': 732}, # Index finger mouse X
        'Joy_YAxis': {'Type': 'Analogue', 'x': 244, 'y': 1754, 'width': 732}, # Index finger mouse Y
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 84, 'y': 555, 'width': 572}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1874, 'y': 1914, 'width': 832}, # Pinky dial
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1954, 'y': 2054, 'width': 832}, # Paddle
    },
    '044F0405': {
        'Joy_1': {'Type': 'Digital', 'x': 2124, 'y': 494, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 474, 'y': 494, 'width': 1092}, # Back button
        'Joy_3': {'Type': 'Digital', 'x': 474, 'y': 624, 'width': 1092}, # Left-hand button
        'Joy_4': {'Type': 'Digital', 'x': 2124, 'y': 624, 'width': 1092}, # Right-hand button
        'Joy_5': {'Type': 'Digital', 'x': 24, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-left button
        'Joy_6': {'Type': 'Digital', 'x': 574, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-middle button
        'Joy_7': {'Type': 'Digital', 'x': 1124, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-right button
        'Joy_8': {'Type': 'Digital', 'x': 1124, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-right button
        'Joy_9': {'Type': 'Digital', 'x': 574, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-middle button
        'Joy_10': {'Type': 'Digital', 'x': 24, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-left button
        'Joy_11': {'Type': 'Digital', 'x': 3264, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-right button
        'Joy_12': {'Type': 'Digital', 'x': 2714, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-middle button
        'Joy_13': {'Type': 'Digital', 'x': 2164, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-left button
        'Joy_14': {'Type': 'Digital', 'x': 2164, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-left button
        'Joy_15': {'Type': 'Digital', 'x': 2714, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-middle button
        'Joy_16': {'Type': 'Digital', 'x': 3264, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1542, 'y': 214, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1542, 'y': 270, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1542, 'y': 326, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1542, 'y': 382, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2357, 'y': 980, 'width': 1132}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2584, 'y': 1750, 'width': 832}, # Stick throttle slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2357, 'y': 924, 'width': 1132}, # Stick pitch
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2357, 'y': 868, 'width': 1132}, # Stick roll
    },
    '044F0406': {
        'Joy_1': {'Type': 'Digital', 'x': 2124, 'y': 494, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 474, 'y': 494, 'width': 1092}, # Back button
        'Joy_3': {'Type': 'Digital', 'x': 474, 'y': 624, 'width': 1092}, # Left-hand button
        'Joy_4': {'Type': 'Digital', 'x': 2124, 'y': 624, 'width': 1092}, # Right-hand button
        'Joy_5': {'Type': 'Digital', 'x': 24, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-left button
        'Joy_6': {'Type': 'Digital', 'x': 574, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-middle button
        'Joy_7': {'Type': 'Digital', 'x': 1124, 'y': 1104, 'width': 542, 'height': 108}, # Left bank top-right button
        'Joy_8': {'Type': 'Digital', 'x': 1124, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-right button
        'Joy_9': {'Type': 'Digital', 'x': 574, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-middle button
        'Joy_10': {'Type': 'Digital', 'x': 24, 'y': 1220, 'width': 542, 'height': 108}, # Left bank bottom-left button
        'Joy_11': {'Type': 'Digital', 'x': 3264, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-right button
        'Joy_12': {'Type': 'Digital', 'x': 2714, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-middle button
        'Joy_13': {'Type': 'Digital', 'x': 2164, 'y': 1104, 'width': 542, 'height': 108}, # Right bank top-left button
        'Joy_14': {'Type': 'Digital', 'x': 2164, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-left button
        'Joy_15': {'Type': 'Digital', 'x': 2714, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-middle button
        'Joy_16': {'Type': 'Digital', 'x': 3264, 'y': 1220, 'width': 542, 'height': 108}, # Right bank bottom-right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1542, 'y': 214, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1542, 'y': 270, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1542, 'y': 326, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1542, 'y': 382, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2357, 'y': 980, 'width': 1132}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2584, 'y': 1750, 'width': 832}, # Stick throttle slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2357, 'y': 924, 'width': 1132}, # Stick pitch
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2357, 'y': 868, 'width': 1132}, # Stick roll
    },    
    'SaitekFLY5': {
        'Joy_1': {'Type': 'Digital', 'x': 684, 'y': 794, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 734, 'y': 874, 'width': 1092}, # Bottom-left button
        'Joy_3': {'Type': 'Digital', 'x': 2414, 'y': 744, 'width': 1092}, # Bottom-right button
        'Joy_4': {'Type': 'Digital', 'x': 624, 'y': 704, 'width': 1092}, # Top-left button
        'Joy_5': {'Type': 'Digital', 'x': 2414, 'y': 594, 'width': 1092}, # Top-right button
        'Joy_6': {'Type': 'Digital', 'x': 584, 'y': 1847, 'width': 1092}, # Bottom bank first button
        'Joy_7': {'Type': 'Digital', 'x': 734, 'y': 1927, 'width': 1092}, # Bottom bank second button
        'Joy_8': {'Type': 'Digital', 'x': 884, 'y': 2007, 'width': 1092}, # Bottom bank third button
        'Joy_9': {'Type': 'Digital', 'x': 1034, 'y': 2090, 'width': 1092}, # Bottom bank fourth button
        'Joy_10': {'Type': 'Digital', 'x': 304, 'y': 1604, 'width': 1092}, # Rear left button
        'Joy_11': {'Type': 'Digital', 'x': 664, 'y': 1204, 'width': 1092}, # Rear right button
        'Joy_12': {'Type': 'Digital', 'x': 2474, 'y': 864, 'width': 1132}, # Scroll wheel up
        'Joy_13': {'Type': 'Digital', 'x': 2474, 'y': 920, 'width': 1132}, # Scroll wheel down
        'Joy_14': {'Type': 'Digital', 'x': 2594, 'y': 1504, 'width': 1092}, # Base button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 990, 'y': 304, 'width': 1932}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 990, 'y': 360, 'width': 1932}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 990, 'y': 416, 'width': 1932}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 990, 'y': 472, 'width': 1932}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1136, 'width': 1132}, # Stick twist
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1080, 'width': 1132}, # Stick roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1024, 'width': 1132}, # Stick pitch
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 264, 'y': 1404, 'width': 1032}, # Throttle
    },
    '06A30836': { # TODO collapse alias
        'displayName': 'SaitekFLY5',
        'Joy_1': {'Type': 'Digital', 'x': 684, 'y': 794, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 734, 'y': 874, 'width': 1092}, # Bottom-left button
        'Joy_3': {'Type': 'Digital', 'x': 2414, 'y': 744, 'width': 1092}, # Bottom-right button
        'Joy_4': {'Type': 'Digital', 'x': 624, 'y': 704, 'width': 1092}, # Top-left button
        'Joy_5': {'Type': 'Digital', 'x': 2414, 'y': 594, 'width': 1092}, # Top-right button
        'Joy_6': {'Type': 'Digital', 'x': 584, 'y': 1847, 'width': 1092}, # Bottom bank first button
        'Joy_7': {'Type': 'Digital', 'x': 734, 'y': 1927, 'width': 1092}, # Bottom bank second button
        'Joy_8': {'Type': 'Digital', 'x': 884, 'y': 2007, 'width': 1092}, # Bottom bank third button
        'Joy_9': {'Type': 'Digital', 'x': 1034, 'y': 2090, 'width': 1092}, # Bottom bank fourth button
        'Joy_10': {'Type': 'Digital', 'x': 304, 'y': 1604, 'width': 1092}, # Rear left button
        'Joy_11': {'Type': 'Digital', 'x': 664, 'y': 1204, 'width': 1092}, # Rear right button
        'Joy_12': {'Type': 'Digital', 'x': 2474, 'y': 864, 'width': 1132}, # Scroll wheel up
        'Joy_13': {'Type': 'Digital', 'x': 2474, 'y': 920, 'width': 1132}, # Scroll wheel down
        'Joy_14': {'Type': 'Digital', 'x': 2594, 'y': 1504, 'width': 1092}, # Base button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 990, 'y': 304, 'width': 1932}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 990, 'y': 360, 'width': 1932}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 990, 'y': 416, 'width': 1932}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 990, 'y': 472, 'width': 1932}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1136, 'width': 1132}, # Stick twist
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1080, 'width': 1132}, # Stick roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2484, 'y': 1024, 'width': 1132}, # Stick pitch
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 264, 'y': 1404, 'width': 1032}, # Throttle
    },
    'SaitekX45': {
        'Joy_1': {'Type': 'Digital', 'x': 4260, 'y': 1040, 'width': 600}, # Stick Trigger button
        'Joy_2': {'Type': 'Digital', 'x': 2900, 'y': 810, 'width': 600}, # Stick Fire button 'A'
        'Joy_3': {'Type': 'Digital', 'x': 4100, 'y': 640, 'width': 600}, # Stick Fire button 'B'
        'Joy_4': {'Type': 'Digital', 'x': 3710, 'y': 410, 'width': 600}, # Stick Launch button
        'Joy_5': {'Type': 'Digital', 'x': 1880, 'y': 1410, 'width': 600}, # Throttle Fire button 'D'
        'Joy_6': {'Type': 'Digital', 'x': 1630, 'y': 2400, 'width': 600}, # Throttle Mouse Fire button
        'Joy_7': {'Type': 'Digital', 'x': 4200, 'y': 1370, 'width': 600}, # Stick Pinkie button
        'Joy_8': {'Type': 'Digital', 'x': 4260, 'y': 800, 'width': 600}, # Stick Fire button 'C'
        'Joy_9': {'Type': 'Digital', 'x': 1630, 'y': 1556, 'width': 600}, # Stick first switch up
        'Joy_10': {'Type': 'Digital', 'x': 1630, 'y': 1608, 'width': 600}, # Stick first switch down
        'Joy_11': {'Type': 'Digital', 'x': 1785, 'y': 1716, 'width': 600}, # Stick second switch up
        'Joy_12': {'Type': 'Digital', 'x': 1785, 'y': 1768, 'width': 600}, # Stick second switch down
        'Joy_13': {'Type': 'Digital', 'x': 2110, 'y': 1872, 'width': 600}, # Stick third switch up
        'Joy_14': {'Type': 'Digital', 'x': 2110, 'y': 1924, 'width': 600}, # Stick third switch down
        'Joy_15': {'Type': 'Digital', 'x': 2940, 'y': 370, 'width': 600}, # Stick PoV2 Up
        'Joy_16': {'Type': 'Digital', 'x': 2940, 'y': 450, 'width': 600}, # Stick PoV2 Right
        'Joy_17': {'Type': 'Digital', 'x': 2940, 'y': 540, 'width': 600}, # Stick PoV2 Down
        'Joy_18': {'Type': 'Digital', 'x': 2940, 'y': 630, 'width': 600}, # Stick PoV2 Left
        'Joy_19': {'Type': 'Digital', 'x': 1630, 'y': 530, 'width': 600}, # Throttle rear hat up
        'Joy_20': {'Type': 'Digital', 'x': 1630, 'y': 610, 'width': 600}, # Throttle rear hat right
        'Joy_21': {'Type': 'Digital', 'x': 1630, 'y': 700, 'width': 600}, # Throttle rear hat down
        'Joy_22': {'Type': 'Digital', 'x': 1630, 'y': 790, 'width': 600}, # Throttle rear hat left
        'Joy_23': {'Type': 'Digital', 'x': 2180, 'y': 1930, 'width': 600}, # Throttle Mouse Hat Up
        'Joy_24': {'Type': 'Digital', 'x': 2180, 'y': 2010, 'width': 600}, # Throttle Mouse Hat Right
        'Joy_25': {'Type': 'Digital', 'x': 2180, 'y': 2100, 'width': 600}, # Throttle Mouse Hat Down
        'Joy_26': {'Type': 'Digital', 'x': 2180, 'y': 2190, 'width': 600}, # Throttle Mouse Hat Left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2810, 'y': 1050, 'width': 600}, # Stick PoV1 hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2810, 'y': 1130, 'width': 600}, # Stick PoV1 hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2810, 'y': 1220, 'width': 600}, # Stick PoV1 hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2810, 'y': 1315, 'width': 600}, # Stick PoV1 hat left
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1890, 'y': 1620, 'width': 600}, # Throttle bottom rotary
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1940, 'y': 1120, 'width': 600}, # Throttle top rotary
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 730, 'y': 880, 'width': 600}, # Throttle yaw rocker
        'Joy_XAxis': {'Type': 'Analogue', 'x': 4210, 'y': 2310, 'width': 600}, # Stick roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 4210, 'y': 2400, 'width': 600}, # Stick pitch
        'Joy_UAxis': {'Type': 'Analogue', 'x': 140, 'y': 1600, 'width': 600}, # Throttle main slider
    },
    'SaitekX52': {
        'Joy_1': {'Type': 'Digital', 'x': 3164, 'y': 858, 'width': 600}, # Stick primary trigger half press
        'Joy_2': {'Type': 'Digital', 'x': 2524, 'y': 210, 'width': 560}, # Stick 'Safe'
        'Joy_3': {'Type': 'Digital', 'x': 3108, 'y': 478, 'width': 560}, # Stick blue button right of Safe
        'Joy_4': {'Type': 'Digital', 'x': 3118, 'y': 662, 'width': 560}, # Stick blue button right of hat
        'Joy_5': {'Type': 'Digital', 'x': 2071, 'y': 674, 'width': 570}, # Stick black button left of hat
        'Joy_6': {'Type': 'Digital', 'x': 3102, 'y': 1148, 'width': 570}, # Stick pinky trigger
        'Joy_7': {'Type': 'Digital', 'x': 1334, 'y': 1038, 'width': 740}, # Throttle blue button
        'Joy_8': {'Type': 'Digital', 'x': 1142, 'y': 656, 'width': 760}, # Throttle top rotary button
        'Joy_9': {'Type': 'Digital', 'x': 1630, 'y': 1556, 'width': 560}, # Stick first switch up
        'Joy_10': {'Type': 'Digital', 'x': 1630, 'y': 1608, 'width': 560}, # Stick first switch down
        'Joy_11': {'Type': 'Digital', 'x': 1785, 'y': 1716, 'width': 560}, # Stick second switch up
        'Joy_12': {'Type': 'Digital', 'x': 1785, 'y': 1768, 'width': 560}, # Stick second switch down
        'Joy_13': {'Type': 'Digital', 'x': 2110, 'y': 1872, 'width': 560}, # Stick third switch up
        'Joy_14': {'Type': 'Digital', 'x': 2110, 'y': 1924, 'width': 560}, # Stick third switch down
        'Joy_15': {'Type': 'Digital', 'x': 3164, 'y': 910, 'width': 600}, # Stick primary trigger full press
        'Joy_16': {'Type': 'Digital', 'x': 2044, 'y': 422, 'width': 740}, # Stick top hat down
        'Joy_17': {'Type': 'Digital', 'x': 2044, 'y': 370, 'width': 740}, # Stick top hat right
        'Joy_18': {'Type': 'Digital', 'x': 2044, 'y': 318, 'width': 740}, # Stick top hat up
        'Joy_19': {'Type': 'Digital', 'x': 2044, 'y': 476, 'width': 740}, # Stick top hat left
        'Joy_20': {'Type': 'Digital', 'x': 254, 'y': 330, 'width': 750}, # Throttle rear hat up
        'Joy_21': {'Type': 'Digital', 'x': 254, 'y': 382, 'width': 750}, # Throttle rear hat right
        'Joy_22': {'Type': 'Digital', 'x': 254, 'y': 434, 'width': 750}, # Throttle rear hat down
        'Joy_23': {'Type': 'Digital', 'x': 254, 'y': 486, 'width': 750}, # Throttle rear hat left
        'Joy_27': {'Type': 'Digital', 'x': 26, 'y': 1748, 'width': 570}, # Throttle bottom left button (RST)
        'Joy_28': {'Type': 'Digital', 'x': 198, 'y': 1850, 'width': 570}, # Throttle bottom middle button
        'Joy_29': {'Type': 'Digital', 'x': 355, 'y': 1954, 'width': 570}, # Throttle bottom right button (FUN)
        'Joy_30': {'Type': 'Digital', 'x': 1498, 'y': 1316, 'width': 750}, # Throttle bottom rotary button
        'Joy_31': {'Type': 'Digital', 'x': 1114, 'y': 2014, 'width': 620}, # Throttle mouse click
        'Joy_32': {'Type': 'Digital', 'x': 124, 'y': 752, 'width': 650}, # Throttle rear wheel click
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1878, 'y': 786, 'width': 740}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1878, 'y': 838, 'width': 740}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1878, 'y': 890, 'width': 740}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1878, 'y': 942, 'width': 740}, # PoV hat left
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1498, 'y': 1264, 'width': 750}, # Throttle bottom rotary
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1142, 'y': 604, 'width': 740}, # Throttle top rotary
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3074, 'y': 1946, 'width': 720}, # Stick yaw
        'Joy_UAxis': {'Type': 'Analogue', 'x': 422, 'y': 584, 'width': 460}, # Throttle 'volume' slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3074, 'y': 1894, 'width': 720}, # Stick roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3074, 'y': 1842, 'width': 720}, # Stick pitch
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 102, 'y': 1224, 'width': 460}, # Throttle main slider
        '?Wheel': {'Type': 'Analogue', 'x': 120, 'y': 694, 'width': 660}, # Throttle rear wheel
    },
    'SaitekX52Pro': {
        'Joy_1': {'Type': 'Digital', 'x': 3164, 'y': 824, 'width': 652}, # Stick primary trigger half press
        'Joy_2': {'Type': 'Digital', 'x': 2404, 'y': 214, 'width': 792}, # Stick 'Safe'
        'Joy_3': {'Type': 'Digital', 'x': 3104, 'y': 484, 'width': 692}, # Stick red button right of Safe
        'Joy_4': {'Type': 'Digital', 'x': 3104, 'y': 674, 'width': 692}, # Stick red button right of hat
        'Joy_5': {'Type': 'Digital', 'x': 1964, 'y': 674, 'width': 692}, # Stick black button left of hat
        'Joy_6': {'Type': 'Digital', 'x': 3092, 'y': 1144, 'width': 732}, # Stick pinky trigger
        'Joy_7': {'Type': 'Digital', 'x': 1364, 'y': 1054, 'width': 792}, # Throttle red button
        'Joy_8': {'Type': 'Digital', 'x': 1144, 'y': 660, 'width': 772}, # Throttle top rotary button
        'Joy_9': {'Type': 'Digital', 'x': 1624, 'y': 1554, 'width': 572}, # Stick first switch up
        'Joy_10': {'Type': 'Digital', 'x': 1624, 'y': 1610, 'width': 572}, # Stick first switch down
        'Joy_11': {'Type': 'Digital', 'x': 1784, 'y': 1724, 'width': 572}, # Stick second switch up
        'Joy_12': {'Type': 'Digital', 'x': 1784, 'y': 1780, 'width': 572}, # Stick second switch down
        'Joy_13': {'Type': 'Digital', 'x': 2084, 'y': 1864, 'width': 572}, # Stick third switch up
        'Joy_14': {'Type': 'Digital', 'x': 2084, 'y': 1920, 'width': 572}, # Stick third switch down
        'Joy_15': {'Type': 'Digital', 'x': 3164, 'y': 880, 'width': 652}, # Stick primary trigger full press
        'Joy_16': {'Type': 'Digital', 'x': 1004, 'y': 2016, 'width': 932}, # Throttle mouse click
        'Joy_17': {'Type': 'Digital', 'x': 104, 'y': 700, 'width': 732}, # Throttle rear wheel down
        'Joy_18': {'Type': 'Digital', 'x': 104, 'y': 644, 'width': 732}, # Throttle rear wheel up
        'Joy_19': {'Type': 'Digital', 'x': 104, 'y': 756, 'width': 732}, # Throttle rear wheel click
        'Joy_20': {'Type': 'Digital', 'x': 1814, 'y': 304, 'width': 932}, # Stick top hat up
        'Joy_21': {'Type': 'Digital', 'x': 1814, 'y': 360, 'width': 932}, # Stick top hat right
        'Joy_22': {'Type': 'Digital', 'x': 1814, 'y': 416, 'width': 932}, # Stick top hat down
        'Joy_23': {'Type': 'Digital', 'x': 1814, 'y': 472, 'width': 932}, # Stick top hat left
        'Joy_24': {'Type': 'Digital', 'x': 244, 'y': 284, 'width': 972}, # Throttle rear hat up
        'Joy_25': {'Type': 'Digital', 'x': 244, 'y': 340, 'width': 972}, # Throttle rear hat right
        'Joy_26': {'Type': 'Digital', 'x': 244, 'y': 396, 'width': 972}, # Throttle rear hat down
        'Joy_27': {'Type': 'Digital', 'x': 244, 'y': 452, 'width': 972}, # Throttle rear hat left
        'Joy_31': {'Type': 'Digital', 'x': 1494, 'y': 1320, 'width': 772}, # Throttle bottom rotary button
        'Joy_32': {'Type': 'Digital', 'x': 44, 'y': 1864, 'width': 752}, # Left-hand MFD button
        #'Joy_???': {'Type': 'Digital', 'x': 26, 'y': 1748, 'width': 570}, # Throttle bottom left button
        #'Joy_???': {'Type': 'Digital', 'x': 198, 'y': 1850, 'width': 570}, # Throttle bottom middle button
        #'Joy_???': {'Type': 'Digital', 'x': 355, 'y': 1954, 'width': 570}, # Throttle bottom right button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1694, 'y': 774, 'width': 932}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1694, 'y': 830, 'width': 932}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1694, 'y': 886, 'width': 932}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1694, 'y': 942, 'width': 932}, # PoV hat left
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1494, 'y': 1264, 'width': 772}, # Throttle bottom rotary
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1144, 'y': 604, 'width': 772}, # Throttle top rotary
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3034, 'y': 1956, 'width': 792}, # Stick yaw
        'Joy_UAxis': {'Type': 'Analogue', 'x': 264, 'y': 554, 'width': 632}, # Throttle 'volume' slider
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3034, 'y': 1900, 'width': 792}, # Stick roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3034, 'y': 1844, 'width': 792}, # Stick pitch
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 84, 'y': 1054, 'width': 472, 'height': 108}, # Throttle main slider
        #'?Wheel': {'Type': 'Analogue', 'x': 120, 'y': 694, 'width': 660}, # Throttle rear wheel
    },
    'SaitekX55Joystick': {
        'Joy_1': {'Type': 'Digital', 'x': 2044, 'y': 604, 'width': 642, 'height': 108}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2144, 'y': 224, 'width': 792}, # Top trigger
        'Joy_3': {'Type': 'Digital', 'x': 3064, 'y': 554, 'width': 692}, # Side trigger
        'Joy_4': {'Type': 'Digital', 'x': 2044, 'y': 744, 'width': 642, 'height': 108}, # Secondary trigger
        'Joy_5': {'Type': 'Digital', 'x': 3024, 'y': 974, 'width': 792}, # Pinky button
        'Joy_6': {'Type': 'Digital', 'x': 2044, 'y': 884, 'width': 642, 'height': 108}, # Pinky trigger
        'Joy_7': {'Type': 'Digital', 'x': 3054, 'y': 224, 'width': 772}, # Witch hat up
        'Joy_8': {'Type': 'Digital', 'x': 3054, 'y': 280, 'width': 772}, # Witch hat right
        'Joy_9': {'Type': 'Digital', 'x': 3054, 'y': 336, 'width': 772}, # Witch hat down
        'Joy_10': {'Type': 'Digital', 'x': 3054, 'y': 392, 'width': 772}, # Witch hat left
        'Joy_11': {'Type': 'Digital', 'x': 3074, 'y': 724, 'width': 742}, # Castle hat up
        'Joy_12': {'Type': 'Digital', 'x': 3074, 'y': 780, 'width': 742}, # Castle hat right
        'Joy_13': {'Type': 'Digital', 'x': 3074, 'y': 836, 'width': 742}, # Castle hat down
        'Joy_14': {'Type': 'Digital', 'x': 3074, 'y': 892, 'width': 742}, # Castle hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1744, 'y': 304, 'width': 1072}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1744, 'y': 360, 'width': 1072}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1744, 'y': 416, 'width': 1072}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1744, 'y': 472, 'width': 1072}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1166, 'width': 632},
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1110, 'width': 632},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1054, 'width': 632}
    },
    'SaitekX55Throttle': {
        'Joy_1': {'Type': 'Digital', 'x': 44, 'y': 604, 'width': 852},  # E button
        'Joy_2': {'Type': 'Digital', 'x': 1874, 'y': 1660, 'width': 672}, # F push
        'Joy_3': {'Type': 'Digital', 'x': 1534, 'y': 1810, 'width': 672}, # G push
        'Joy_4': {'Type': 'Digital', 'x': 2574, 'y': 1694, 'width': 892}, # H button
        'Joy_5': {'Type': 'Digital', 'x': 2744, 'y': 1784, 'width': 892}, # I button
        'Joy_6': {'Type': 'Digital', 'x': 74, 'y': 1604, 'width': 572}, # Switch 1
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 1660, 'width': 572}, # Switch 2
        'Joy_8': {'Type': 'Digital', 'x': 94, 'y': 1754, 'width': 572}, # Switch 3
        'Joy_9': {'Type': 'Digital', 'x': 94, 'y': 1810, 'width': 572}, # Switch 4
        'Joy_10': {'Type': 'Digital', 'x': 764, 'y': 1754, 'width': 572}, # Switch 5
        'Joy_11': {'Type': 'Digital', 'x': 764, 'y': 1810, 'width': 572}, # Switch 6
        'Joy_12': {'Type': 'Digital', 'x': 1104, 'y': 1424, 'width': 572}, # TGL 1 up
        'Joy_13': {'Type': 'Digital', 'x': 1104, 'y': 1480, 'width': 572}, # TGL 1 down
        'Joy_14': {'Type': 'Digital', 'x': 1164, 'y': 1284, 'width': 572}, # TGL 2 up
        'Joy_15': {'Type': 'Digital', 'x': 1164, 'y': 1340, 'width': 572}, # TGL 2 down
        'Joy_16': {'Type': 'Digital', 'x': 1224, 'y': 1154, 'width': 572}, # TGL 3 up
        'Joy_17': {'Type': 'Digital', 'x': 1224, 'y': 1210, 'width': 572}, # TGL 3 down
        'Joy_18': {'Type': 'Digital', 'x': 1244, 'y': 1014, 'width': 572}, # TGL 4 up
        'Joy_19': {'Type': 'Digital', 'x': 1244, 'y': 1070, 'width': 572}, # TGL 4 down
        'Joy_20': {'Type': 'Digital', 'x': 1154, 'y': 564, 'width': 772}, # H3 up
        'Joy_21': {'Type': 'Digital', 'x': 1154, 'y': 620, 'width': 772}, # H3 right
        'Joy_22': {'Type': 'Digital', 'x': 1154, 'y': 676, 'width': 772}, # H3 down
        'Joy_23': {'Type': 'Digital', 'x': 1154, 'y': 732, 'width': 772}, # H3 left
        'Joy_24': {'Type': 'Digital', 'x': 1364, 'y': 1924, 'width': 772}, # H4 up
        'Joy_25': {'Type': 'Digital', 'x': 1364, 'y': 1980, 'width': 772}, # H4 right
        'Joy_26': {'Type': 'Digital', 'x': 1364, 'y': 2036, 'width': 772}, # H4 down
        'Joy_27': {'Type': 'Digital', 'x': 1364, 'y': 2092, 'width': 772}, # H4 left
        'Joy_28': {'Type': 'Digital', 'x': 3124, 'y': 2034, 'width': 692}, # Pinky rocker up
        'Joy_29': {'Type': 'Digital', 'x': 3124, 'y': 2090, 'width': 692}, # Pinky rocker down
        'Joy_30': {'Type': 'Digital', 'x': 3134, 'y': 1884, 'width': 692}, # Pinky spin up
        'Joy_31': {'Type': 'Digital', 'x': 3134, 'y': 1940, 'width': 692}, # Pinky spin down
        'Joy_XAxis': {'Type': 'Analogue', 'x': 164, 'y': 680, 'width': 572}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1194, 'y': 870, 'width': 732}, # Mouse left/right
        'Joy_VAxis': {'Type': 'Analogue', 'x': 1194, 'y': 814, 'width': 732}, # Mouse up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1874, 'y': 1604, 'width': 672}, # F spin
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1534, 'y': 1754, 'width': 672}, # G spin
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1014, 'y': 1574, 'width': 692}, # RTY2 axis
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 854, 'y': 1654, 'width': 692}, # RTY1 axis
    },
    'SaitekX56Joystick':
    {
        'Joy_1': {'Type': 'Digital', 'x': 1964, 'y': 618, 'width': 642, 'height': 108}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2084, 'y': 208, 'width': 792}, # 'R' button
        'Joy_3': {'Type': 'Digital', 'x': 3014, 'y': 604, 'width': 792}, # Side button
        'Joy_4': {'Type': 'Digital', 'x': 2024, 'y': 904, 'width': 642}, # Stick press
        'Joy_5': {'Type': 'Digital', 'x': 3024, 'y': 974, 'width': 792}, # Pinky button
        'Joy_6': {'Type': 'Digital', 'x': 1964, 'y': 1038, 'width': 642, 'height': 108}, # Pinky trigger
        'Joy_7': {'Type': 'Digital', 'x': 3054, 'y': 224, 'width': 772}, # Witch hat up
        'Joy_8': {'Type': 'Digital', 'x': 3054, 'y': 280, 'width': 772}, # Witch hat right
        'Joy_9': {'Type': 'Digital', 'x': 3054, 'y': 336, 'width': 772}, # Witch hat down
        'Joy_10': {'Type': 'Digital', 'x': 3054, 'y': 392, 'width': 772}, # Witch hat left
        'Joy_11': {'Type': 'Digital', 'x': 3074, 'y': 724, 'width': 742}, # Castle hat up
        'Joy_12': {'Type': 'Digital', 'x': 3074, 'y': 780, 'width': 742}, # Castle hat right
        'Joy_13': {'Type': 'Digital', 'x': 3074, 'y': 836, 'width': 742}, # Castle hat down
        'Joy_14': {'Type': 'Digital', 'x': 3074, 'y': 892, 'width': 742}, # Castle hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1684, 'y': 288, 'width': 1072}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1684, 'y': 344, 'width': 1072}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1684, 'y': 400, 'width': 1072}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1684, 'y': 456, 'width': 1072}, # PoV hat left
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2024, 'y': 848, 'width': 642}, # Stick x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2024, 'y': 792, 'width': 642}, # Stick y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1166, 'width': 632}, # z
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1110, 'width': 632}, # x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1054, 'width': 632} # y
    },
    '07382221': # Old name for Saitek X56 joystick TODO merge
    {
        'displayName': 'SaitekX56Joystick',
        'Joy_1': {'Type': 'Digital', 'x': 1964, 'y': 618, 'width': 642, 'height': 108}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2084, 'y': 208, 'width': 792}, # 'R' button
        'Joy_3': {'Type': 'Digital', 'x': 3014, 'y': 604, 'width': 792}, # Side button
        'Joy_4': {'Type': 'Digital', 'x': 2024, 'y': 904, 'width': 642}, # Stick press
        'Joy_5': {'Type': 'Digital', 'x': 3024, 'y': 974, 'width': 792}, # Pinky button
        'Joy_6': {'Type': 'Digital', 'x': 1964, 'y': 1038, 'width': 642, 'height': 108}, # Pinky trigger
        'Joy_7': {'Type': 'Digital', 'x': 3054, 'y': 224, 'width': 772}, # Witch hat up
        'Joy_8': {'Type': 'Digital', 'x': 3054, 'y': 280, 'width': 772}, # Witch hat right
        'Joy_9': {'Type': 'Digital', 'x': 3054, 'y': 336, 'width': 772}, # Witch hat down
        'Joy_10': {'Type': 'Digital', 'x': 3054, 'y': 392, 'width': 772}, # Witch hat left
        'Joy_11': {'Type': 'Digital', 'x': 3074, 'y': 724, 'width': 742}, # Castle hat up
        'Joy_12': {'Type': 'Digital', 'x': 3074, 'y': 780, 'width': 742}, # Castle hat right
        'Joy_13': {'Type': 'Digital', 'x': 3074, 'y': 836, 'width': 742}, # Castle hat down
        'Joy_14': {'Type': 'Digital', 'x': 3074, 'y': 892, 'width': 742}, # Castle hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1684, 'y': 288, 'width': 1072}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1684, 'y': 344, 'width': 1072}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1684, 'y': 400, 'width': 1072}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1684, 'y': 456, 'width': 1072}, # PoV hat left
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2024, 'y': 848, 'width': 642}, # Stick x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2024, 'y': 792, 'width': 642}, # Stick y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1166, 'width': 632}, # z
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1110, 'width': 632}, # x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1054, 'width': 632} # y
    },
    'SaitekX56Throttle':
    {
        'Joy_1': {'Type': 'Digital', 'x': 24, 'y': 604, 'width': 752},  # E button
        'Joy_2': {'Type': 'Digital', 'x': 1874, 'y': 1660, 'width': 672}, # F push
        'Joy_3': {'Type': 'Digital', 'x': 1534, 'y': 1810, 'width': 672}, # G push
        'Joy_4': {'Type': 'Digital', 'x': 2744, 'y': 1784, 'width': 892}, # I button
        'Joy_5': {'Type': 'Digital', 'x': 2574, 'y': 1694, 'width': 892}, # H button
        'Joy_6': {'Type': 'Digital', 'x': 74, 'y': 1604, 'width': 532}, # Switch 1
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 1660, 'width': 532}, # Switch 2
        'Joy_8': {'Type': 'Digital', 'x': 94, 'y': 1754, 'width': 572}, # Switch 3
        'Joy_9': {'Type': 'Digital', 'x': 94, 'y': 1810, 'width': 572}, # Switch 4
        'Joy_10': {'Type': 'Digital', 'x': 764, 'y': 1754, 'width': 572}, # Switch 5
        'Joy_11': {'Type': 'Digital', 'x': 764, 'y': 1810, 'width': 572}, # Switch 6
        'Joy_12': {'Type': 'Digital', 'x': 1104, 'y': 1444, 'width': 572}, # TGL 1 up
        'Joy_13': {'Type': 'Digital', 'x': 1104, 'y': 1500, 'width': 572}, # TGL 1 down
        'Joy_14': {'Type': 'Digital', 'x': 1164, 'y': 1304, 'width': 572}, # TGL 2 up
        'Joy_15': {'Type': 'Digital', 'x': 1164, 'y': 1360, 'width': 572}, # TGL 2 down
        'Joy_16': {'Type': 'Digital', 'x': 1224, 'y': 1168, 'width': 572}, # TGL 3 up
        'Joy_17': {'Type': 'Digital', 'x': 1224, 'y': 1224, 'width': 572}, # TGL 3 down
        'Joy_18': {'Type': 'Digital', 'x': 1224, 'y': 1026, 'width': 572}, # TGL 4 up
        'Joy_19': {'Type': 'Digital', 'x': 1224, 'y': 1082, 'width': 572}, # TGL 4 down
        'Joy_20': {'Type': 'Digital', 'x': 1154, 'y': 534, 'width': 772}, # H3 up
        'Joy_21': {'Type': 'Digital', 'x': 1154, 'y': 590, 'width': 772}, # H3 right
        'Joy_22': {'Type': 'Digital', 'x': 1154, 'y': 646, 'width': 772}, # H3 down
        'Joy_23': {'Type': 'Digital', 'x': 1154, 'y': 702, 'width': 772}, # H3 left
        'Joy_24': {'Type': 'Digital', 'x': 1364, 'y': 1924, 'width': 772}, # H4 up
        'Joy_25': {'Type': 'Digital', 'x': 1364, 'y': 1980, 'width': 772}, # H4 right
        'Joy_26': {'Type': 'Digital', 'x': 1364, 'y': 2036, 'width': 772}, # H4 down
        'Joy_27': {'Type': 'Digital', 'x': 1364, 'y': 2092, 'width': 772}, # H4 left
        'Joy_28': {'Type': 'Digital', 'x': 3124, 'y': 2034, 'width': 692}, # Pinky rocker up
        'Joy_29': {'Type': 'Digital', 'x': 3124, 'y': 2090, 'width': 692}, # Pinky rocker down
        'Joy_30': {'Type': 'Digital', 'x': 3134, 'y': 1884, 'width': 692}, # Pinky spin up
        'Joy_31': {'Type': 'Digital', 'x': 3134, 'y': 1940, 'width': 692}, # Pinky spin down
        'Joy_32': {'Type': 'Digital', 'x': 1224, 'y': 894, 'width': 642}, # Stick press
        'Joy_33': {'Type': 'Digital', 'x': 104, 'y': 525, 'width': 748}, # Slider press
        'Joy_XAxis': {'Type': 'Analogue', 'x': 84, 'y': 784, 'width': 572}, # Throttle (left/both)
        'Joy_YAxis': {'Type': 'Analogue', 'x': 124, 'y': 694, 'width': 572}, # Throttle (right)
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1874, 'y': 1604, 'width': 672}, # F spin
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1224, 'y': 838, 'width': 642}, # Stick x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1224, 'y': 782, 'width': 642}, # Stick y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1534, 'y': 1754, 'width': 672}, # G spin
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1014, 'y': 1588, 'width': 692}, # RTY3 axis
        'Joy_VAxis': {'Type': 'Analogue', 'x': 854, 'y': 1668, 'width': 692}, # RTY4 axis
    },
    '0738A221': # Old name for Saitek X56 throttle
    {
        'displayName': 'SaitekX56Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 24, 'y': 604, 'width': 752},  # E button
        'Joy_2': {'Type': 'Digital', 'x': 1874, 'y': 1660, 'width': 672}, # F push
        'Joy_3': {'Type': 'Digital', 'x': 1534, 'y': 1810, 'width': 672}, # G push
        'Joy_4': {'Type': 'Digital', 'x': 2574, 'y': 1694, 'width': 892}, # H button
        'Joy_5': {'Type': 'Digital', 'x': 2744, 'y': 1784, 'width': 892}, # I button
        'Joy_6': {'Type': 'Digital', 'x': 74, 'y': 1604, 'width': 532}, # Switch 1
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 1660, 'width': 532}, # Switch 2
        'Joy_8': {'Type': 'Digital', 'x': 94, 'y': 1754, 'width': 572}, # Switch 3
        'Joy_9': {'Type': 'Digital', 'x': 94, 'y': 1810, 'width': 572}, # Switch 4
        'Joy_10': {'Type': 'Digital', 'x': 764, 'y': 1754, 'width': 572}, # Switch 5
        'Joy_11': {'Type': 'Digital', 'x': 764, 'y': 1810, 'width': 572}, # Switch 6
        'Joy_12': {'Type': 'Digital', 'x': 1104, 'y': 1444, 'width': 572}, # TGL 1 up
        'Joy_13': {'Type': 'Digital', 'x': 1104, 'y': 1500, 'width': 572}, # TGL 1 down
        'Joy_14': {'Type': 'Digital', 'x': 1164, 'y': 1304, 'width': 572}, # TGL 2 up
        'Joy_15': {'Type': 'Digital', 'x': 1164, 'y': 1360, 'width': 572}, # TGL 2 down
        'Joy_16': {'Type': 'Digital', 'x': 1224, 'y': 1168, 'width': 572}, # TGL 3 up
        'Joy_17': {'Type': 'Digital', 'x': 1224, 'y': 1224, 'width': 572}, # TGL 3 down
        'Joy_18': {'Type': 'Digital', 'x': 1224, 'y': 1026, 'width': 572}, # TGL 4 up
        'Joy_19': {'Type': 'Digital', 'x': 1224, 'y': 1082, 'width': 572}, # TGL 4 down
        'Joy_20': {'Type': 'Digital', 'x': 1154, 'y': 534, 'width': 772}, # H3 up
        'Joy_21': {'Type': 'Digital', 'x': 1154, 'y': 590, 'width': 772}, # H3 right
        'Joy_22': {'Type': 'Digital', 'x': 1154, 'y': 646, 'width': 772}, # H3 down
        'Joy_23': {'Type': 'Digital', 'x': 1154, 'y': 702, 'width': 772}, # H3 left
        'Joy_24': {'Type': 'Digital', 'x': 1364, 'y': 1924, 'width': 772}, # H4 up
        'Joy_25': {'Type': 'Digital', 'x': 1364, 'y': 1980, 'width': 772}, # H4 right
        'Joy_26': {'Type': 'Digital', 'x': 1364, 'y': 2036, 'width': 772}, # H4 down
        'Joy_27': {'Type': 'Digital', 'x': 1364, 'y': 2092, 'width': 772}, # H4 left
        'Joy_28': {'Type': 'Digital', 'x': 3124, 'y': 2034, 'width': 692}, # Pinky rocker up
        'Joy_29': {'Type': 'Digital', 'x': 3124, 'y': 2090, 'width': 692}, # Pinky rocker down
        'Joy_30': {'Type': 'Digital', 'x': 3134, 'y': 1884, 'width': 692}, # Pinky spin up
        'Joy_31': {'Type': 'Digital', 'x': 3134, 'y': 1940, 'width': 692}, # Pinky spin down
        'Joy_32': {'Type': 'Digital', 'x': 1224, 'y': 894, 'width': 642}, # Stick press
        'Joy_33': {'Type': 'Digital', 'x': 104, 'y': 525, 'width': 748}, # Slider press
        'Joy_XAxis': {'Type': 'Analogue', 'x': 84, 'y': 784, 'width': 572}, # Throttle (left/both)
        'Joy_YAxis': {'Type': 'Analogue', 'x': 124, 'y': 694, 'width': 572}, # Throttle (right)
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1874, 'y': 1604, 'width': 672}, # F spin
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1224, 'y': 838, 'width': 642}, # Stick x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1224, 'y': 782, 'width': 642}, # Stick y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1534, 'y': 1754, 'width': 672}, # G spin
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1014, 'y': 1588, 'width': 692}, # RTY3 axis
        'Joy_VAxis': {'Type': 'Analogue', 'x': 854, 'y': 1668, 'width': 692}, # RTY4 axis
    },
    'CHCombatStick': {
        'Joy_1': {'Type': 'Digital', 'x': 1974, 'y': 854, 'width': 592}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2984, 'y': 944, 'width': 832}, # Thumb button
        'Joy_3': {'Type': 'Digital', 'x': 2964, 'y': 654, 'width': 832}, # Top button
        'Joy_4': {'Type': 'Digital', 'x': 2084, 'y': 1159, 'width': 592}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 1754, 'y': 234, 'width': 892}, # Side trigger
        'Joy_6': {'Type': 'Digital', 'x': 1664, 'y': 334, 'width': 892}, # Top trigger
        'Joy_7': {'Type': 'Digital', 'x': 1689, 'y': 464, 'width': 832}, # PoV hat up
        'Joy_8': {'Type': 'Digital', 'x': 1689, 'y': 520, 'width': 832}, # PoV hat right
        'Joy_9': {'Type': 'Digital', 'x': 1689, 'y': 576, 'width': 832}, # PoV hat down
        'Joy_10': {'Type': 'Digital', 'x': 1689, 'y': 632, 'width': 832}, # PoV hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2964, 'y': 212, 'width': 832}, # Right hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2964, 'y': 268, 'width': 832}, # Right hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2964, 'y': 324, 'width': 832}, # Right hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2964, 'y': 380, 'width': 832}, # Right hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1168, 'width': 692}, # Stick X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1112, 'width': 692}, # Stick Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2254, 'y': 1894, 'width': 692}, # Wheel on left of base
    },
    'CHFighterStick': {
        'Joy_1': {'Type': 'Digital', 'x': 1974, 'y': 854, 'width': 592}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 1664, 'y': 334, 'width': 892}, # Top trigger
        'Joy_3': {'Type': 'Digital', 'x': 1754, 'y': 234, 'width': 892}, # Side trigger
        'Joy_4': {'Type': 'Digital', 'x': 2084, 'y': 1159, 'width': 592}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 1689, 'y': 464, 'width': 832}, # Left hat up
        'Joy_6': {'Type': 'Digital', 'x': 1689, 'y': 520, 'width': 832}, # Left hat right
        'Joy_7': {'Type': 'Digital', 'x': 1689, 'y': 576, 'width': 832}, # Left hat down
        'Joy_8': {'Type': 'Digital', 'x': 1689, 'y': 632, 'width': 832}, # Left hat left
        'Joy_9': {'Type': 'Digital', 'x': 2994, 'y': 494, 'width': 832}, # Castle hat up
        'Joy_10': {'Type': 'Digital', 'x': 2994, 'y': 550, 'width': 832}, # Castle hat right
        'Joy_11': {'Type': 'Digital', 'x': 2994, 'y': 606, 'width': 832}, # Castle hat down
        'Joy_12': {'Type': 'Digital', 'x': 2994, 'y': 662, 'width': 832}, # Castle hat left
        'Joy_13': {'Type': 'Digital', 'x': 3058, 'y': 810, 'width': 772}, # Thumb hat up
        'Joy_14': {'Type': 'Digital', 'x': 3058, 'y': 866, 'width': 772}, # Thumb hat right
        'Joy_15': {'Type': 'Digital', 'x': 3058, 'y': 922, 'width': 772}, # Thumb hat down
        'Joy_16': {'Type': 'Digital', 'x': 3058, 'y': 978, 'width': 772}, # Thumb hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2964, 'y': 212, 'width': 832}, # POV hat up (looks like witch hat)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2964, 'y': 268, 'width': 832}, # POV hat right (looks like witch hat)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2964, 'y': 324, 'width': 832}, # POV hat down (looks like witch hat)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2964, 'y': 380, 'width': 832}, # POV hat left (looks like witch hat)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1112, 'width': 692}, # Stick X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1168, 'width': 692}, # Stick Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2254, 'y': 1894, 'width': 692}, # Wheel on left of base
    },
    '068EC0F3': { # CH FighterStick with CH manager
        'displayName': 'CH FighterStick with CH manager',
        'Joy_1': {'Type': 'Digital', 'x': 1974, 'y': 854, 'width': 592}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 1664, 'y': 334, 'width': 892}, # Top trigger
        'Joy_3': {'Type': 'Digital', 'x': 1754, 'y': 234, 'width': 892}, # Side trigger
        'Joy_4': {'Type': 'Digital', 'x': 2084, 'y': 1159, 'width': 592}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 1689, 'y': 464, 'width': 832}, # Left hat up
        'Joy_6': {'Type': 'Digital', 'x': 1689, 'y': 520, 'width': 832}, # Left hat right
        'Joy_7': {'Type': 'Digital', 'x': 1689, 'y': 576, 'width': 832}, # Left hat down
        'Joy_8': {'Type': 'Digital', 'x': 1689, 'y': 632, 'width': 832}, # Left hat left
        'Joy_9': {'Type': 'Digital', 'x': 2994, 'y': 494, 'width': 832}, # Castle hat up
        'Joy_10': {'Type': 'Digital', 'x': 2994, 'y': 550, 'width': 832}, # Castle hat right
        'Joy_11': {'Type': 'Digital', 'x': 2994, 'y': 606, 'width': 832}, # Castle hat down
        'Joy_12': {'Type': 'Digital', 'x': 2994, 'y': 662, 'width': 832}, # Castle hat left
        'Joy_13': {'Type': 'Digital', 'x': 3058, 'y': 810, 'width': 772}, # Thumb hat up
        'Joy_14': {'Type': 'Digital', 'x': 3058, 'y': 866, 'width': 772}, # Thumb hat right
        'Joy_15': {'Type': 'Digital', 'x': 3058, 'y': 922, 'width': 772}, # Thumb hat down
        'Joy_16': {'Type': 'Digital', 'x': 3058, 'y': 978, 'width': 772}, # Thumb hat left
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2964, 'y': 212, 'width': 832}, # POV hat up (looks like witch hat)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2964, 'y': 268, 'width': 832}, # POV hat right (looks like witch hat)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2964, 'y': 324, 'width': 832}, # POV hat down (looks like witch hat)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2964, 'y': 380, 'width': 832}, # POV hat left (looks like witch hat)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1112, 'width': 692}, # Stick X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3124, 'y': 1168, 'width': 692}, # Stick Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2254, 'y': 1894, 'width': 692}, # Wheel on left of base
    },
    'CHProThrottle1': {
        'Joy_1': {'Type': 'Digital', 'x': 1114, 'y': 966, 'width': 832}, # Castle hat right
        'Joy_2': {'Type': 'Digital', 'x': 1114, 'y': 1022, 'width': 832}, # Castle hat down
        'Joy_3': {'Type': 'Digital', 'x': 1114, 'y': 1078, 'width': 832}, # Castle hat left
        'Joy_4': {'Type': 'Digital', 'x': 1114, 'y': 910, 'width': 832}, # Castle hat up
        'Joy_5': {'Type': 'Digital', 'x': 1189, 'y': 1696, 'width': 1032}, # Bottom hat right
        'Joy_6': {'Type': 'Digital', 'x': 1189, 'y': 1752, 'width': 1032}, # Bottom hat down
        'Joy_7': {'Type': 'Digital', 'x': 1189, 'y': 1808, 'width': 1032}, # Bottom hat left
        'Joy_8': {'Type': 'Digital', 'x': 1189, 'y': 1640, 'width': 1032}, # Bottom hat up
        'Joy_9': {'Type': 'Digital', 'x': 1198, 'y': 1275, 'width': 832}, # Rear hat down
        'Joy_10': {'Type': 'Digital', 'x': 1198, 'y': 1219, 'width': 832}, # Rear hat right
        'Joy_11': {'Type': 'Digital', 'x': 1198, 'y': 1163, 'width': 832}, # Rear hat up
        'Joy_12': {'Type': 'Digital', 'x': 1198, 'y': 1331, 'width': 832}, # Rear hat left
        'Joy_13': {'Type': 'Digital', 'x': 1261, 'y': 1549, 'width': 932}, # Mouse button
        'Joy_14': {'Type': 'Digital', 'x': 1042, 'y': 814, 'width': 892}, # Right back
        'Joy_15': {'Type': 'Digital', 'x': 904, 'y': 724, 'width': 892}, # Middle back
        'Joy_16': {'Type': 'Digital', 'x': 684, 'y': 634, 'width': 892}, # Left back
        'Joy_POV1Up': {'Type': 'Digital', 'x': 132, 'y': 1896, 'width': 932}, # PoV hat up (looks like witch hat)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 132, 'y': 1952, 'width': 932}, # PoV hat right (looks like witch hat)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 132, 'y': 2008, 'width': 932}, # PoV hat down (looks like witch hat)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 132, 'y': 1840, 'width': 932}, # PoV hat left (looks like witch hat)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1493, 'width': 932}, # Mouse X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1437, 'width': 932}, # Mouse Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 80, 'y': 714, 'width': 692}, # Throttle
    },
    'CHProThrottle2': { # CH Pro Throttle with CH manager
        'Joy_1': {'Type': 'Digital', 'x': 1261, 'y': 1549, 'width': 932}, # Mouse button
        'Joy_2': {'Type': 'Digital', 'x': 1042, 'y': 814, 'width': 892}, # Right back
        'Joy_3': {'Type': 'Digital', 'x': 904, 'y': 724, 'width': 892}, # Middle back
        'Joy_4': {'Type': 'Digital', 'x': 684, 'y': 634, 'width': 892}, # Left back
        'Joy_5': {'Type': 'Digital', 'x': 1198, 'y': 1275, 'width': 832}, # Rear hat down
        'Joy_6': {'Type': 'Digital', 'x': 1198, 'y': 1219, 'width': 832}, # Rear hat right
        'Joy_7': {'Type': 'Digital', 'x': 1198, 'y': 1163, 'width': 832}, # Rear hat up
        'Joy_8': {'Type': 'Digital', 'x': 1198, 'y': 1331, 'width': 832}, # Rear hat left
        'Joy_9': {'Type': 'Digital', 'x': 1114, 'y': 966, 'width': 832}, # Castle hat right
        'Joy_10': {'Type': 'Digital', 'x': 1114, 'y': 1022, 'width': 832}, # Castle hat down
        'Joy_11': {'Type': 'Digital', 'x': 1114, 'y': 1078, 'width': 832}, # Castle hat left
        'Joy_12': {'Type': 'Digital', 'x': 1114, 'y': 910, 'width': 832}, # Castle hat up
        'Joy_13': {'Type': 'Digital', 'x': 1189, 'y': 1696, 'width': 1032}, # Bottom hat right
        'Joy_14': {'Type': 'Digital', 'x': 1189, 'y': 1752, 'width': 1032}, # Bottom hat down
        'Joy_15': {'Type': 'Digital', 'x': 1189, 'y': 1808, 'width': 1032}, # Bottom hat left
        'Joy_16': {'Type': 'Digital', 'x': 1189, 'y': 1640, 'width': 1032}, # Bottom hat up
        'Joy_POV1Up': {'Type': 'Digital', 'x': 132, 'y': 1896, 'width': 932}, # PoV hat up (looks like witch hat)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 132, 'y': 1952, 'width': 932}, # PoV hat right (looks like witch hat)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 132, 'y': 2008, 'width': 932}, # PoV hat down (looks like witch hat)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 132, 'y': 1840, 'width': 932}, # PoV hat left (looks like witch hat)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1493, 'width': 932}, # Mouse X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1437, 'width': 932}, # Mouse Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 80, 'y': 714, 'width': 692}, # Throttle
    },
    '068EC010': { # CH Pro Throttle with CH manager, alternate
        'displayName': 'CH Pro Throttle with CH manager, alternate',
        'Joy_1': {'Type': 'Digital', 'x': 1261, 'y': 1549, 'width': 932}, # Mouse button
        'Joy_2': {'Type': 'Digital', 'x': 1042, 'y': 814, 'width': 892}, # Right back
        'Joy_3': {'Type': 'Digital', 'x': 904, 'y': 724, 'width': 892}, # Middle back
        'Joy_4': {'Type': 'Digital', 'x': 684, 'y': 634, 'width': 892}, # Left back
        'Joy_5': {'Type': 'Digital', 'x': 1198, 'y': 1275, 'width': 832}, # Rear hat down
        'Joy_6': {'Type': 'Digital', 'x': 1198, 'y': 1219, 'width': 832}, # Rear hat right
        'Joy_7': {'Type': 'Digital', 'x': 1198, 'y': 1163, 'width': 832}, # Rear hat up
        'Joy_8': {'Type': 'Digital', 'x': 1198, 'y': 1331, 'width': 832}, # Rear hat left
        'Joy_9': {'Type': 'Digital', 'x': 1114, 'y': 966, 'width': 832}, # Castle hat right
        'Joy_10': {'Type': 'Digital', 'x': 1114, 'y': 1022, 'width': 832}, # Castle hat down
        'Joy_11': {'Type': 'Digital', 'x': 1114, 'y': 1078, 'width': 832}, # Castle hat left
        'Joy_12': {'Type': 'Digital', 'x': 1114, 'y': 910, 'width': 832}, # Castle hat up
        'Joy_13': {'Type': 'Digital', 'x': 1189, 'y': 1696, 'width': 1032}, # Bottom hat right
        'Joy_14': {'Type': 'Digital', 'x': 1189, 'y': 1752, 'width': 1032}, # Bottom hat down
        'Joy_15': {'Type': 'Digital', 'x': 1189, 'y': 1808, 'width': 1032}, # Bottom hat left
        'Joy_16': {'Type': 'Digital', 'x': 1189, 'y': 1640, 'width': 1032}, # Bottom hat up
        'Joy_POV1Up': {'Type': 'Digital', 'x': 132, 'y': 1896, 'width': 932}, # PoV hat up (looks like witch hat)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 132, 'y': 1952, 'width': 932}, # PoV hat right (looks like witch hat)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 132, 'y': 2008, 'width': 932}, # PoV hat down (looks like witch hat)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 132, 'y': 1840, 'width': 932}, # PoV hat left (looks like witch hat)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1493, 'width': 932}, # Mouse X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1261, 'y': 1437, 'width': 932}, # Mouse Y axis
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 80, 'y': 714, 'width': 692}, # Throttle
    },
    '068E00FA': { # CH Quadrant throttle
        'displayName': 'CH Quadrant throttle',
        'Joy_XAxis': {'Type': 'Analogue', 'x': 354, 'y': 804, 'width': 932}, # Throttle 1
        'Joy_YAxis': {'Type': 'Analogue', 'x': 554, 'y': 564, 'width': 932}, # Throttle 2
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 754, 'y': 324, 'width': 932}, # Throttle 3
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2214, 'y': 324, 'width': 932}, # Throttle 4
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2414, 'y': 564, 'width': 932}, # Throttle 5
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2614, 'y': 804, 'width': 932}, # Throttle 6
        'Joy_1': {'Type': 'Digital', 'x': 354, 'y': 1484, 'width': 932}, # Switch 1 up
        'Joy_2': {'Type': 'Digital', 'x': 354, 'y': 1540, 'width': 932}, # Switch 1 down
        'Joy_3': {'Type': 'Digital', 'x': 554, 'y': 1724, 'width': 932}, # Switch 2 up
        'Joy_4': {'Type': 'Digital', 'x': 554, 'y': 1780, 'width': 932}, # Switch 2 down
        'Joy_5': {'Type': 'Digital', 'x': 754, 'y': 1964, 'width': 932}, # Switch 3 up
        'Joy_6': {'Type': 'Digital', 'x': 754, 'y': 2020, 'width': 932}, # Switch 3 down
        'Joy_7': {'Type': 'Digital', 'x': 2214, 'y': 1964, 'width': 932}, # Switch 4 up
        'Joy_8': {'Type': 'Digital', 'x': 2214, 'y': 2020, 'width': 932}, # Switch 4 down
        'Joy_9': {'Type': 'Digital', 'x': 2414, 'y': 1724, 'width': 932}, # Switch 5 up
        'Joy_10': {'Type': 'Digital', 'x': 2414, 'y': 1780, 'width': 932}, # Switch 5 down
        'Joy_11': {'Type': 'Digital', 'x': 2614, 'y': 1484, 'width': 932}, # Switch 6 up
        'Joy_12': {'Type': 'Digital', 'x': 2614, 'y': 1540, 'width': 932}, # Switch 6 down
    },
    '06A30C2D': { # CH Pro Flight Quadrant throttle
        'displayName': 'CH Pro Flight Quadrant throttle',
        'Joy_XAxis': {'Type': 'Analogue', 'x': 554, 'y': 564, 'width': 932}, # Throttle 1
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1474, 'y': 324, 'width': 932}, # Throttle 2
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2414, 'y': 564, 'width': 932}, # Throttle 3
        'Joy_1': {'Type': 'Digital', 'x': 354, 'y': 1484, 'width': 932}, # Switch 1 up
        'Joy_2': {'Type': 'Digital', 'x': 354, 'y': 1540, 'width': 932}, # Switch 1 down
        'Joy_3': {'Type': 'Digital', 'x': 1474, 'y': 1754, 'width': 932}, # Switch 2 up
        'Joy_4': {'Type': 'Digital', 'x': 1474, 'y': 1810, 'width': 932}, # Switch 2 down
        'Joy_5': {'Type': 'Digital', 'x': 2614, 'y': 1484, 'width': 932}, # Switch 3 up
        'Joy_6': {'Type': 'Digital', 'x': 2614, 'y': 1540, 'width': 932}, # Switch 3 down
    },
    'ThrustMasterHOTAS4': {
        'Joy_1': {'Type': 'Digital', 'x': 1394, 'y': 614, 'width': 1082}, # Stick primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2114, 'y': 264, 'width': 1192}, # Stick L1 button
        'Joy_3': {'Type': 'Digital', 'x': 2954, 'y': 544, 'width': 792, 'height': 108}, # Stick R3 button
        'Joy_4': {'Type': 'Digital', 'x': 2754, 'y': 374, 'width': 832, 'height': 108}, # Stick L3 button
        'Joy_5': {'Type': 'Digital', 'x': 950, 'y': 734, 'width': 592, 'height': 108}, # Throttle 'square'
        'Joy_6': {'Type': 'Digital', 'x': 950, 'y': 898, 'width': 592, 'height': 108}, # Throttle 'cross'
        'Joy_7': {'Type': 'Digital', 'x': 950, 'y': 1046, 'width': 592, 'height': 108}, # Throttle 'circle'
        'Joy_8': {'Type': 'Digital', 'x': 1044, 'y': 1374, 'width': 592, 'height': 108}, # Throttle 'triangle'
        'Joy_9': {'Type': 'Digital', 'x': 1628, 'y': 710, 'width': 832}, # Throttle R2 button
        'Joy_10': {'Type': 'Digital', 'x': 1928, 'y': 790, 'width': 532, 'height': 108}, # Throttle L2 button
        'Joy_11': {'Type': 'Digital', 'x': 284, 'y': 2044, 'width': 592}, # Throttle SE button
        'Joy_12': {'Type': 'Digital', 'x': 984, 'y': 2044, 'width': 592}, # Throttle ST button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 994, 'y': 354, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 994, 'y': 410, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 994, 'y': 466, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 994, 'y': 522, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1988, 'width': 792, 'height': 108}, # Stick twist
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1878, 'width': 792, 'height': 108}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1768, 'width': 792, 'height': 108}, # Stick up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 96, 'y': 736, 'width': 692}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1114, 'y': 1504, 'width': 932, 'height': 108}, # Throttle rocker
    },
    'TFlightHotasOne': {
        'Joy_1': {'Type': 'Digital', 'x': 1394, 'y': 614, 'width': 1082}, # Stick primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2114, 'y': 264, 'width': 1192}, # Stick L1 button
        'Joy_3': {'Type': 'Digital', 'x': 2954, 'y': 544, 'width': 792, 'height': 108}, # Stick R3 button
        'Joy_4': {'Type': 'Digital', 'x': 2754, 'y': 374, 'width': 832, 'height': 108}, # Stick L3 button
        'Joy_5': {'Type': 'Digital', 'x': 950, 'y': 734, 'width': 592, 'height': 108}, # Throttle 'square'
        'Joy_6': {'Type': 'Digital', 'x': 950, 'y': 898, 'width': 592, 'height': 108}, # Throttle 'cross'
        'Joy_7': {'Type': 'Digital', 'x': 950, 'y': 1046, 'width': 592, 'height': 108}, # Throttle 'circle'
        'Joy_8': {'Type': 'Digital', 'x': 1044, 'y': 1374, 'width': 592, 'height': 108}, # Throttle 'triangle'
        'Joy_9': {'Type': 'Digital', 'x': 1628, 'y': 710, 'width': 832}, # Throttle R2 button
        'Joy_10': {'Type': 'Digital', 'x': 1928, 'y': 790, 'width': 532, 'height': 108}, # Throttle L2 button
        'Joy_11': {'Type': 'Digital', 'x': 284, 'y': 2044, 'width': 592}, # Throttle SE button
        'Joy_12': {'Type': 'Digital', 'x': 984, 'y': 2044, 'width': 592}, # Throttle ST button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 994, 'y': 354, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 994, 'y': 410, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 994, 'y': 466, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 994, 'y': 522, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1988, 'width': 792, 'height': 108}, # Stick twist
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1878, 'width': 792, 'height': 108}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3018, 'y': 1768, 'width': 792, 'height': 108}, # Stick up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 96, 'y': 736, 'width': 692}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1114, 'y': 1504, 'width': 932, 'height': 108}, # Throttle rocker
    },
    'ThrustMasterTFlightHOTASX': {
        'Joy_1': {'Type': 'Digital', 'x': 1394, 'y': 614, 'width': 1082}, # Stick primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2114, 'y': 264, 'width': 1192}, # Stick L1 button
        'Joy_3': {'Type': 'Digital', 'x': 2954, 'y': 544, 'width': 792, 'height': 108}, # Stick R3 button
        'Joy_4': {'Type': 'Digital', 'x': 2754, 'y': 374, 'width': 832, 'height': 108}, # Stick L3 button
        'Joy_5': {'Type': 'Digital', 'x': 950, 'y': 734, 'width': 592, 'height': 108}, # Throttle 'square'
        'Joy_6': {'Type': 'Digital', 'x': 950, 'y': 898, 'width': 592, 'height': 108}, # Throttle 'cross'
        'Joy_7': {'Type': 'Digital', 'x': 950, 'y': 1046, 'width': 592, 'height': 108}, # Throttle 'circle'
        'Joy_8': {'Type': 'Digital', 'x': 1044, 'y': 1374, 'width': 592, 'height': 108}, # Throttle 'triangle'
        'Joy_9': {'Type': 'Digital', 'x': 1628, 'y': 710, 'width': 832}, # Throttle R2 button
        'Joy_10': {'Type': 'Digital', 'x': 1928, 'y': 790, 'width': 532, 'height': 108}, # Throttle L2 button
        'Joy_11': {'Type': 'Digital', 'x': 284, 'y': 2004, 'width': 592}, # Throttle SE button
        'Joy_12': {'Type': 'Digital', 'x': 984, 'y': 2004, 'width': 592}, # Throttle ST button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 994, 'y': 354, 'width': 1532}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 994, 'y': 410, 'width': 1532}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 994, 'y': 466, 'width': 1532}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 994, 'y': 522, 'width': 1532}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 3018, 'y': 947, 'width': 792, 'height': 108}, # Stick twist
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3018, 'y': 837, 'width': 792, 'height': 108}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3018, 'y': 727, 'width': 792, 'height': 108}, # Stick up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 96, 'y': 736, 'width': 692}, # Throttle
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1114, 'y': 1504, 'width': 932, 'height': 108}, # Throttle rocker
    },
    '044FB106': {
        'Joy_1': {'Type': 'Digital', 'x': 684, 'y': 822, 'width': 1092}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2204, 'y': 744, 'width': 1092}, # Secondary trigger
        'Joy_3': {'Type': 'Digital', 'x': 2124, 'y': 564, 'width': 1092}, # Button 3
        'Joy_4': {'Type': 'Digital', 'x': 2174, 'y': 654, 'width': 1092}, # Button 4
        'Joy_5': {'Type': 'Digital', 'x': 474, 'y': 1564, 'width': 1092}, # Button 5
        'Joy_6': {'Type': 'Digital', 'x': 544, 'y': 1424, 'width': 1092}, # Button 6
        'Joy_7': {'Type': 'Digital', 'x': 584, 'y': 1266, 'width': 1092}, # Button 7
        'Joy_8': {'Type': 'Digital', 'x': 584, 'y': 1204, 'width': 1092}, # Button 8
        'Joy_9': {'Type': 'Digital', 'x': 554, 'y': 1704, 'width': 1092}, # Button 9
        'Joy_10': {'Type': 'Digital', 'x': 554, 'y': 1766, 'width': 1092}, # Button 10
        'Joy_11': {'Type': 'Digital', 'x': 2824, 'y': 1428, 'width': 692}, # Button 11
        'Joy_12': {'Type': 'Digital', 'x': 2824, 'y': 1338, 'width': 692}, # Button 12
        'Joy_POV1Up': {'Type': 'Digital', 'x': 990, 'y': 304, 'width': 1932}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 990, 'y': 360, 'width': 1932}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 990, 'y': 416, 'width': 1932}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 990, 'y': 472, 'width': 1932}, # PoV hat left
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2364, 'y': 966, 'width': 1132}, # Stick twist
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2584, 'y': 1833, 'width': 892}, # Throttle axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2364, 'y': 910, 'width': 1132}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2364, 'y': 854, 'width': 1132}, # Stick up/down
    },
    'ThrustMasterWarthogJoystick': {
        'Joy_1': {'Type': 'Digital', 'x': 2042, 'y': 548, 'width': 620}, # Primary trigger half press
        'Joy_2': {'Type': 'Digital', 'x': 1952, 'y': 214, 'width': 880}, # Top trigger red button
        'Joy_3': {'Type': 'Digital', 'x': 2084, 'y': 1102, 'width': 580}, # Pinky button
        'Joy_4': {'Type': 'Digital', 'x': 2084, 'y': 1012, 'width': 580}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 2886, 'y': 212, 'width': 880}, # Top side button
        'Joy_6': {'Type': 'Digital', 'x': 2042, 'y': 602, 'width': 620}, # Primary trigger full press
        'Joy_7': {'Type': 'Digital', 'x': 1916, 'y': 300, 'width': 760}, # Left hat up
        'Joy_8': {'Type': 'Digital', 'x': 1916, 'y': 354, 'width': 760}, # Left hat right
        'Joy_9': {'Type': 'Digital', 'x': 1916, 'y': 408, 'width': 760}, # Left hat down
        'Joy_10': {'Type': 'Digital', 'x': 1916, 'y': 462, 'width': 760}, # Left hat left
        'Joy_11': {'Type': 'Digital', 'x': 3048, 'y': 562, 'width': 760}, # Right hat up
        'Joy_12': {'Type': 'Digital', 'x': 3048, 'y': 616, 'width': 760}, # Right hat right
        'Joy_13': {'Type': 'Digital', 'x': 3048, 'y': 670, 'width': 760}, # Right hat down
        'Joy_14': {'Type': 'Digital', 'x': 3048, 'y': 724, 'width': 760}, # Right hat left
        'Joy_15': {'Type': 'Digital', 'x': 2004, 'y': 700, 'width': 660}, # Thumb hat up
        'Joy_16': {'Type': 'Digital', 'x': 2004, 'y': 754, 'width': 660}, # Thumb hat right
        'Joy_17': {'Type': 'Digital', 'x': 2004, 'y': 808, 'width': 660}, # Thumb hat down
        'Joy_18': {'Type': 'Digital', 'x': 2004, 'y': 862, 'width': 660}, # Thumb hat left
        'Joy_19': {'Type': 'Digital', 'x': 2004, 'y': 914, 'width': 660}, # Thumb hat push
        'Joy_POV1Up': {'Type': 'Digital', 'x': 3048, 'y': 308, 'width': 760}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 3048, 'y': 362, 'width': 760}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 3048, 'y': 416, 'width': 760}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 3048, 'y': 470, 'width': 760}, # PoV hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3126, 'y': 872, 'width': 680}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3126, 'y': 818, 'width': 680}, # Stick up/down
    },
    'ThrustMasterWarthogThrottle': {
        'Joy_1': {'Type': 'Digital', 'x': 2870, 'y': 1422, 'width': 680}, # Rear analogue push
        'Joy_2': {'Type': 'Digital', 'x': 1674, 'y': 1672, 'width': 660}, # Side hat push
        'Joy_3': {'Type': 'Digital', 'x': 1674, 'y': 1456, 'width': 660}, # Side hat up
        'Joy_4': {'Type': 'Digital', 'x': 1674, 'y': 1510, 'width': 660}, # Side hat right
        'Joy_5': {'Type': 'Digital', 'x': 1674, 'y': 1564, 'width': 660}, # Side hat down
        'Joy_6': {'Type': 'Digital', 'x': 1674, 'y': 1618, 'width': 660}, # Side hat left
        'Joy_7': {'Type': 'Digital', 'x': 1694, 'y': 1810, 'width': 640}, # Side top switch right
        'Joy_8': {'Type': 'Digital', 'x': 1694, 'y': 1756, 'width': 640}, # Side top switch left
        'Joy_9': {'Type': 'Digital', 'x': 1694, 'y': 1950, 'width': 640}, # Side middle switch right
        'Joy_10': {'Type': 'Digital', 'x': 1694, 'y': 1896, 'width': 640}, # Side middle switch left
        'Joy_11': {'Type': 'Digital', 'x': 1694, 'y': 2088, 'width': 640}, # Side bottom switch right
        'Joy_12': {'Type': 'Digital', 'x': 1694, 'y': 2034, 'width': 640}, # Side bottom switch left
        'Joy_13': {'Type': 'Digital', 'x': 3386, 'y': 1976, 'width': 420}, # Side toggle up
        'Joy_14': {'Type': 'Digital', 'x': 3386, 'y': 2030, 'width': 420}, # Side toggle down
        'Joy_15': {'Type': 'Digital', 'x': 3196, 'y': 1514, 'width': 620}, # Rear red button
        'Joy_16': {'Type': 'Digital', 'x': 1080, 'y': 566, 'width': 620}, # ENG left button
        'Joy_17': {'Type': 'Digital', 'x': 1200, 'y': 666, 'width': 620}, # ENG right button
        'Joy_18': {'Type': 'Digital', 'x': 1316, 'y': 1000, 'width': 420}, # ENG operate left down
        'Joy_19': {'Type': 'Digital', 'x': 1354, 'y': 844, 'width': 420}, # ENG operate right down
        'Joy_20': {'Type': 'Digital', 'x': 1140, 'y': 1118, 'width': 620}, # APU start button
        'Joy_21': {'Type': 'Digital', 'x': 960, 'y': 1362, 'width': 620}, # LDGH silence button
        'Joy_22': {'Type': 'Digital', 'x': 88, 'y': 750, 'width': 320}, # Flaps up
        'Joy_23': {'Type': 'Digital', 'x': 88, 'y': 804, 'width': 320}, # Flaps down
        'Joy_24': {'Type': 'Digital', 'x': 36, 'y': 1428, 'width': 480}, # EAC
        'Joy_25': {'Type': 'Digital', 'x': 218, 'y': 1542, 'width': 480}, # RDR ALT
        'Joy_26': {'Type': 'Digital', 'x': 436, 'y': 1646, 'width': 480}, # Autopilot
        'Joy_27': {'Type': 'Digital', 'x': 1020, 'y': 1460, 'width': 420}, # Autopilot select up
        'Joy_28': {'Type': 'Digital', 'x': 1020, 'y': 1514, 'width': 420}, # Autopilot select down
        'Joy_31': {'Type': 'Digital', 'x': 1316, 'y': 946, 'width': 420}, # ENG operate left up
        'Joy_32': {'Type': 'Digital', 'x': 1354, 'y': 790, 'width': 420}, # ENG operate right up
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1964, 'y': 1214, 'width': 760}, # Rear PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1964, 'y': 1268, 'width': 760}, # Rear PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1964, 'y': 1322, 'width': 760}, # Rear PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1964, 'y': 1376, 'width': 760}, # Rear PoV hat left
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1082, 'y': 1252, 'width': 520}, # Throttle friction control
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2870, 'y': 1368, 'width': 680}, # Rear analogue left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2870, 'y': 1314, 'width': 680}, # Rear analogue up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 530, 'y': 316, 'width': 540}, # Throttle
    },
    'ThrustMasterWarthogCombined': {
        # Stick
        'Joy_1': {'Type': 'Digital', 'x': 2042, 'y': 548, 'width': 620}, # Primary trigger half press
        'Joy_2': {'Type': 'Digital', 'x': 1952, 'y': 214, 'width': 880}, # Top trigger red button
        'Joy_3': {'Type': 'Digital', 'x': 2084, 'y': 1102, 'width': 580}, # Pinky button
        'Joy_4': {'Type': 'Digital', 'x': 2084, 'y': 1012, 'width': 580}, # Pinky trigger
        'Joy_5': {'Type': 'Digital', 'x': 2886, 'y': 212, 'width': 880}, # Top side button
        'Joy_6': {'Type': 'Digital', 'x': 2042, 'y': 602, 'width': 620}, # Primary trigger full press
        'Joy_7': {'Type': 'Digital', 'x': 1916, 'y': 300, 'width': 760}, # Left hat up
        'Joy_8': {'Type': 'Digital', 'x': 1916, 'y': 354, 'width': 760}, # Left hat right
        'Joy_9': {'Type': 'Digital', 'x': 1916, 'y': 408, 'width': 760}, # Left hat down
        'Joy_10': {'Type': 'Digital', 'x': 1916, 'y': 462, 'width': 760}, # Left hat left
        'Joy_11': {'Type': 'Digital', 'x': 3048, 'y': 562, 'width': 760}, # Right hat up
        'Joy_12': {'Type': 'Digital', 'x': 3048, 'y': 616, 'width': 760}, # Right hat right
        'Joy_13': {'Type': 'Digital', 'x': 3048, 'y': 670, 'width': 760}, # Right hat down
        'Joy_14': {'Type': 'Digital', 'x': 3048, 'y': 724, 'width': 760}, # Right hat left
        'Joy_15': {'Type': 'Digital', 'x': 2004, 'y': 700, 'width': 660}, # Thumb hat up
        'Joy_16': {'Type': 'Digital', 'x': 2004, 'y': 754, 'width': 660}, # Thumb hat right
        'Joy_17': {'Type': 'Digital', 'x': 2004, 'y': 808, 'width': 660}, # Thumb hat down
        'Joy_18': {'Type': 'Digital', 'x': 2004, 'y': 862, 'width': 660}, # Thumb hat left
        'Joy_19': {'Type': 'Digital', 'x': 2004, 'y': 914, 'width': 660}, # Thumb hat push
        'Joy_POV1Up': {'Type': 'Digital', 'x': 3048, 'y': 308, 'width': 760}, # PoV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 3048, 'y': 362, 'width': 760}, # PoV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 3048, 'y': 416, 'width': 760}, # PoV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 3048, 'y': 470, 'width': 760}, # PoV hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3126, 'y': 872, 'width': 680}, # Stick left/right
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3126, 'y': 818, 'width': 680}, # Stick up/down
        # Throttle
        'Joy_20': {'Type': 'Digital', 'x': 3196, 'y': 1514, 'width': 620}, # Rear red button
        'Joy_21': {'Type': 'Digital', 'x': 960, 'y': 1362, 'width': 620}, # LDGH silence button
        'Joy_22': {'Type': 'Digital', 'x': 1964, 'y': 1214, 'width': 760}, # Rear PoV hat up
        'Joy_23': {'Type': 'Digital', 'x': 1964, 'y': 1268, 'width': 760}, # Rear PoV hat right
        'Joy_24': {'Type': 'Digital', 'x': 1964, 'y': 1322, 'width': 760}, # Rear PoV hat down
        'Joy_25': {'Type': 'Digital', 'x': 1964, 'y': 1376, 'width': 760}, # Rear PoV hat left
        #'Joy_25': {'Type': 'Digital', 'x': 2870, 'y': 1422, 'width': 680}, # Rear analogue push
        'Joy_26': {'Type': 'Digital', 'x': 1674, 'y': 1672, 'width': 660}, # Side hat push
        'Joy_27': {'Type': 'Digital', 'x': 1674, 'y': 1456, 'width': 660}, # Side hat up
        'Joy_28': {'Type': 'Digital', 'x': 1674, 'y': 1510, 'width': 660}, # Side hat right
        'Joy_29': {'Type': 'Digital', 'x': 1674, 'y': 1564, 'width': 660}, # Side hat down
        'Joy_30': {'Type': 'Digital', 'x': 1674, 'y': 1618, 'width': 660}, # Side hat left
        #'Joy_31': {'Type': 'Digital', 'x': 1694, 'y': 1810, 'width': 640}, # Side top switch right
        #'Joy_32': {'Type': 'Digital', 'x': 1694, 'y': 1756, 'width': 640}, # Side top switch left
        #'Joy_33': {'Type': 'Digital', 'x': 1694, 'y': 1950, 'width': 640}, # Side middle switch right
        #'Joy_34': {'Type': 'Digital', 'x': 1694, 'y': 1896, 'width': 640}, # Side middle switch left
        #'Joy_35': {'Type': 'Digital', 'x': 1694, 'y': 2088, 'width': 640}, # Side bottom switch right
        #'Joy_36': {'Type': 'Digital', 'x': 1694, 'y': 2034, 'width': 640}, # Side bottom switch left
        #'Joy_37': {'Type': 'Digital', 'x': 3386, 'y': 1976, 'width': 420}, # Side toggle up
        #'Joy_38': {'Type': 'Digital', 'x': 3386, 'y': 2030, 'width': 420}, # Side toggle down
        #'Joy_40': {'Type': 'Digital', 'x': 1080, 'y': 566, 'width': 620}, # ENG left button
        #'Joy_41': {'Type': 'Digital', 'x': 1200, 'y': 666, 'width': 620}, # ENG right button
        'Joy_31': {'Type': 'Digital', 'x': 1316, 'y': 1000, 'width': 420}, # ENG operate left down
        'Joy_32': {'Type': 'Digital', 'x': 1354, 'y': 844, 'width': 420}, # ENG operate right down
        #'Joy_44': {'Type': 'Digital', 'x': 1140, 'y': 1118, 'width': 620}, # APU start button
        #'Joy_46': {'Type': 'Digital', 'x': 88, 'y': 750, 'width': 320}, # Flaps up
        #'Joy_47': {'Type': 'Digital', 'x': 88, 'y': 804, 'width': 320}, # Flaps down
        #'Joy_48': {'Type': 'Digital', 'x': 36, 'y': 1428, 'width': 480}, # EAC
        #'Joy_49': {'Type': 'Digital', 'x': 218, 'y': 1542, 'width': 480}, # RDR ALT
        #'Joy_50': {'Type': 'Digital', 'x': 436, 'y': 1646, 'width': 480}, # Autopilot
        #'Joy_51': {'Type': 'Digital', 'x': 1020, 'y': 1460, 'width': 420}, # Autopilot select up
        #'Joy_52': {'Type': 'Digital', 'x': 1020, 'y': 1514, 'width': 420}, # Autopilot select down
        #'Joy_53': {'Type': 'Digital', 'x': 1316, 'y': 946, 'width': 420}, # ENG operate left up
        #'Joy_54': {'Type': 'Digital', 'x': 1354, 'y': 790, 'width': 420}, # ENG operate right up
        'Joy_VAxis': {'Type': 'Analogue', 'x': 1082, 'y': 1252, 'width': 520}, # Throttle friction control
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2870, 'y': 1368, 'width': 680}, # Rear analogue left/right
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2870, 'y': 1314, 'width': 680}, # Rear analogue up/down
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 530, 'y': 316, 'width': 540}, # Throttle
    },
    '07382218': { # Saitek Side Panel Control Deck
        'displayName': 'SidePanelControlDeck',
        'Joy_1': {'Type': 'Digital', 'x': 34, 'y': 584, 'width': 592},
        'Joy_2': {'Type': 'Digital', 'x': 634, 'y': 584, 'width': 592},
        'Joy_3': {'Type': 'Digital', 'x': 1234, 'y': 584, 'width': 592},
        'Joy_4': {'Type': 'Digital', 'x': 2629, 'y': 584, 'width': 592},
        'Joy_5': {'Type': 'Digital', 'x': 3229, 'y': 584, 'width': 592},
        'Joy_6': {'Type': 'Digital', 'x': 34, 'y': 646, 'width': 592},
        'Joy_7': {'Type': 'Digital', 'x': 634, 'y': 646, 'width': 592},
        'Joy_8': {'Type': 'Digital', 'x': 1234, 'y': 646, 'width': 592},
        'Joy_9': {'Type': 'Digital', 'x': 2629, 'y': 646, 'width': 592},
        'Joy_10': {'Type': 'Digital', 'x': 3229, 'y': 646, 'width': 592},
        'Joy_11': {'Type': 'Digital', 'x': 34, 'y': 884, 'width': 592},
        'Joy_12': {'Type': 'Digital', 'x': 34, 'y': 946, 'width': 592},
        'Joy_13': {'Type': 'Digital', 'x': 634, 'y': 884, 'width': 592},
        'Joy_14': {'Type': 'Digital', 'x': 634, 'y': 946, 'width': 592},
        'Joy_15': {'Type': 'Digital', 'x': 1234, 'y': 884, 'width': 592},
        'Joy_16': {'Type': 'Digital', 'x': 1234, 'y': 946, 'width': 592},
        'Joy_17': {'Type': 'Digital', 'x': 2629, 'y': 884, 'width': 592},
        'Joy_18': {'Type': 'Digital', 'x': 3229, 'y': 884, 'width': 592},
        'Joy_19': {'Type': 'Digital', 'x': 2629, 'y': 946, 'width': 592},
        'Joy_20': {'Type': 'Digital', 'x': 3229, 'y': 946, 'width': 592},
        'Joy_21': {'Type': 'Digital', 'x': 2624, 'y': 1132, 'width': 992},
        'Joy_22': {'Type': 'Digital', 'x': 2624, 'y': 1222, 'width': 992},
        'Joy_23': {'Type': 'Digital', 'x': 2624, 'y': 1284, 'width': 992},
        'Joy_24': {'Type': 'Digital', 'x': 2624, 'y': 1344, 'width': 992},
        'Joy_25': {'Type': 'Digital', 'x': 1060, 'y': 1371, 'width': 772}, # Scroll wheel press
        'Joy_26': {'Type': 'Digital', 'x': 1060, 'y': 1259, 'width': 772},
        'Joy_27': {'Type': 'Digital', 'x': 1060, 'y': 1315, 'width': 772},
        'Joy_28': {'Type': 'Digital', 'x': 835, 'y': 1160, 'width': 992}, # Stick red button
        'Joy_XAxis': {'Type': 'Analogue', 'x': 695, 'y': 1556, 'width': 1132, 'height': 108},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 695, 'y': 1666, 'width': 1132, 'height': 108},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 695, 'y': 1776, 'width': 1132, 'height': 108},
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2685, 'y': 1556, 'width': 1132, 'height': 108},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2685, 'y': 1666, 'width': 1132, 'height': 108},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2685, 'y': 1776, 'width': 1132, 'height': 108},
    },
    'XB360 Pad': {
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E02FF': { # Copy of XB360 controls
        'displayName': 'XB360',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E02DD': { # Copy of XB360 controls
        'displayName': 'XB360',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    'GamePad': { # Copy of XBox controls
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '28DE11FF': { # Copy of XB360 controls
        'displayName': 'XB360',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E02E0': { # Copy of XB360 controls - EasySMX X10 Game Controller
        'displayName': 'XB360',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E02E3': { # XBox Elite controller
        'displayName': 'XBox Elite controller',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E0B22': { # XBox Elite Series 2 controller
        'displayName': 'XBox Elite Series 2 Controller',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '1689FE00': { # Razer Sabretooth (xbox-like pad)
        'displayName': 'Razer Sabretooth',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    '045E02FD': { # PB Tails Metal Crush Defender (xbox pad clone)
        'displayName': 'Razer Sabretooth',
        'Pad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'Pad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'Pad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'Pad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'Pad_Y': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'Pad_B': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'Pad_A': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'Pad_X': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'Pad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'Pad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'Pad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'Pad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'Pad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'Pad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'Pad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Pad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Pad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'Pad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'Pad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'Pad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
        # 2.3 appears to have renamed 'Pad' to 'GamePad'
        'GamePad_LBumper': {'Type': 'Digital', 'x': 74, 'y': 624, 'width': 1392, 'height': 108},
        'GamePad_LTrigger': {'Type': 'Digital', 'x': 74, 'y': 518, 'width': 1392},
        'GamePad_RBumper': {'Type': 'Digital', 'x': 2368, 'y': 624, 'width': 1442, 'height': 108},
        'GamePad_RTrigger': {'Type': 'Digital', 'x': 2368, 'y': 520, 'width': 1442},
        'GamePad_FaceUp': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192},
        'GamePad_FaceRight': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192},
        'GamePad_FaceDown': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192},
        'GamePad_FaceLeft': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192},
        'GamePad_Back': {'Type': 'Digital', 'x': 74, 'y': 786, 'width': 1192},
        'GamePad_Start': {'Type': 'Digital', 'x': 2625, 'y': 786, 'width': 1192},
        'GamePad_DPadUp': {'Type': 'Digital', 'x': 134, 'y': 1308, 'width': 1032, 'height': 108},
        'GamePad_DPadRight': {'Type': 'Digital', 'x': 134, 'y': 1418, 'width': 1032, 'height': 108},
        'GamePad_DPadDown': {'Type': 'Digital', 'x': 134, 'y': 1528, 'width': 1032, 'height': 108},
        'GamePad_DPadLeft': {'Type': 'Digital', 'x': 134, 'y': 1638, 'width': 1032, 'height': 108},
        'GamePad_RStickY': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'GamePad_RStickX': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'GamePad_RThumb': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108},
        'GamePad_LStickY': {'Type': 'Analogue', 'x': 134, 'y': 930, 'width': 1032, 'height': 108},
        'GamePad_LStickX': {'Type': 'Analogue', 'x': 134, 'y': 1040, 'width': 1032, 'height': 108},
        'GamePad_LThumb': {'Type': 'Digital', 'x': 134, 'y': 1150, 'width': 1032, 'height': 108},
    },
    'Logitech710WirelessGamepad': { # Logitech F710 (xbox-like pad)
        'Joy_1': {'Type': 'Digital', 'x': 2625, 'y': 1178, 'width': 1192}, # X
        'Joy_2': {'Type': 'Digital', 'x': 2625, 'y': 1083, 'width': 1192}, # A
        'Joy_3': {'Type': 'Digital', 'x': 2625, 'y': 988, 'width': 1192}, # B
        'Joy_4': {'Type': 'Digital', 'x': 2625, 'y': 894, 'width': 1192}, # Y
        'Joy_5': {'Type': 'Digital', 'x': 74, 'y': 510, 'width': 1392, 'height': 108}, # Left bumper
        'Joy_6': {'Type': 'Digital', 'x': 2368, 'y': 510, 'width': 1442, 'height': 108}, # Right bumper
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 406, 'width': 1392}, # Left trigger
        'Joy_8': {'Type': 'Digital', 'x': 2368, 'y': 406, 'width': 1442}, # Right trigger
        'Joy_9': {'Type': 'Digital', 'x': 74, 'y': 706, 'width': 1192}, # Back
        'Joy_10': {'Type': 'Digital', 'x': 2625, 'y': 706, 'width': 1192}, # Start
        'Joy_11': {'Type': 'Digital', 'x': 134, 'y': 1542, 'width': 1032, 'height': 108}, # Left stick button
        'Joy_12': {'Type': 'Digital', 'x': 2765, 'y': 1542, 'width': 1052, 'height': 108}, # Right stick button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 134, 'y': 864, 'width': 1032, 'height': 108},
        'Joy_POV1Right': {'Type': 'Digital', 'x': 134, 'y': 974, 'width': 1032, 'height': 108},
        'Joy_POV1Down': {'Type': 'Digital', 'x': 134, 'y': 1084, 'width': 1032, 'height': 108},
        'Joy_POV1Left': {'Type': 'Digital', 'x': 134, 'y': 1194, 'width': 1032, 'height': 108},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1322, 'width': 1052, 'height': 108},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1432, 'width': 1052, 'height': 108},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 134, 'y': 1322, 'width': 1032, 'height': 108},
        'Joy_XAxis': {'Type': 'Analogue', 'x': 134, 'y': 1432, 'width': 1032, 'height': 108},
    },
    'DS4': {
        'Joy_1': {'Type': 'Digital', 'x': 2625, 'y': 1378, 'width': 1192}, # Square
        'Joy_2': {'Type': 'Digital', 'x': 2625, 'y': 1283, 'width': 1192}, # Cross
        'Joy_3': {'Type': 'Digital', 'x': 2625, 'y': 1188, 'width': 1192}, # Circle
        'Joy_4': {'Type': 'Digital', 'x': 2625, 'y': 1094, 'width': 1192}, # Triangle
        'Joy_5': {'Type': 'Digital', 'x': 74, 'y': 824, 'width': 1392, 'height': 108}, # Left bumper
        'Joy_6': {'Type': 'Digital', 'x': 2368, 'y': 824, 'width': 1442, 'height': 108}, # Right bumper
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 986, 'width': 1192}, # Share (?)
        'Joy_8': {'Type': 'Digital', 'x': 2625, 'y': 986, 'width': 1192}, # Options (?)
        'Joy_9': {'Type': 'Digital', 'x': 1428, 'y': 551, 'width': 1052, 'height': 108}, # Trackpad press (?)
        'Joy_10': {'Type': 'Digital', 'x': 1328, 'y': 1866, 'width': 1192}, # PS button (?)
        'Joy_11': {'Type': 'Digital', 'x': 134, 'y': 1824, 'width': 1032, 'height': 108}, # Press of left stick
        'Joy_12': {'Type': 'Digital', 'x': 2765, 'y': 1824, 'width': 1052, 'height': 108}, # Press of right stick
        'Joy_POV1Up': {'Type': 'Digital', 'x': 134, 'y': 1104, 'width': 1032, 'height': 108},
        'Joy_POV1Right': {'Type': 'Digital', 'x': 134, 'y': 1214, 'width': 1032, 'height': 108},
        'Joy_POV1Down': {'Type': 'Digital', 'x': 134, 'y': 1324, 'width': 1032, 'height': 108},
        'Joy_POV1Left': {'Type': 'Digital', 'x': 134, 'y': 1434, 'width': 1032, 'height': 108},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 134, 'y': 1604, 'width': 1032, 'height': 108}, # Vertical axis of left stick
        'Joy_XAxis': {'Type': 'Analogue', 'x': 134, 'y': 1714, 'width': 1032, 'height': 108}, # Horizontal axis of left stick
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1604, 'width': 1052, 'height': 108}, # Vertical axis of right stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1714, 'width': 1052, 'height': 108}, # Horizontal axis of right stick
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 74, 'y': 718, 'width': 1392}, # Left trigger
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2368, 'y': 720, 'width': 1442}, # Right trigger
        #'?': {'Type': 'Analogue', 'x': 1428, 'y': 331, 'width': 1052, 'height': 108}, # Vertical axis of trackpad
        #'?': {'Type': 'Analogue', 'x': 1428, 'y': 441, 'width': 1052, 'height': 108}, # Horizontal axis of trackpad
    },
    'DualShock4': { # a copy of DS4
        'Joy_1': {'Type': 'Digital', 'x': 2625, 'y': 1378, 'width': 1192}, # Square
        'Joy_2': {'Type': 'Digital', 'x': 2625, 'y': 1283, 'width': 1192}, # Cross
        'Joy_3': {'Type': 'Digital', 'x': 2625, 'y': 1188, 'width': 1192}, # Circle
        'Joy_4': {'Type': 'Digital', 'x': 2625, 'y': 1094, 'width': 1192}, # Triangle
        'Joy_5': {'Type': 'Digital', 'x': 74, 'y': 824, 'width': 1392, 'height': 108}, # Left bumper
        'Joy_6': {'Type': 'Digital', 'x': 2368, 'y': 824, 'width': 1442, 'height': 108}, # Right bumper
        'Joy_7': {'Type': 'Digital', 'x': 74, 'y': 986, 'width': 1192}, # Share (?)
        'Joy_8': {'Type': 'Digital', 'x': 2625, 'y': 986, 'width': 1192}, # Options (?)
        'Joy_9': {'Type': 'Digital', 'x': 1428, 'y': 551, 'width': 1052, 'height': 108}, # Trackpad press (?)
        'Joy_10': {'Type': 'Digital', 'x': 1328, 'y': 1866, 'width': 1192}, # PS button (?)
        'Joy_11': {'Type': 'Digital', 'x': 134, 'y': 1824, 'width': 1032, 'height': 108}, # Press of left stick
        'Joy_12': {'Type': 'Digital', 'x': 2765, 'y': 1824, 'width': 1052, 'height': 108}, # Press of right stick
        'Joy_POV1Up': {'Type': 'Digital', 'x': 134, 'y': 1104, 'width': 1032, 'height': 108},
        'Joy_POV1Right': {'Type': 'Digital', 'x': 134, 'y': 1214, 'width': 1032, 'height': 108},
        'Joy_POV1Down': {'Type': 'Digital', 'x': 134, 'y': 1324, 'width': 1032, 'height': 108},
        'Joy_POV1Left': {'Type': 'Digital', 'x': 134, 'y': 1434, 'width': 1032, 'height': 108},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 134, 'y': 1604, 'width': 1032, 'height': 108}, # Vertical axis of left stick
        'Joy_XAxis': {'Type': 'Analogue', 'x': 134, 'y': 1714, 'width': 1032, 'height': 108}, # Horizontal axis of left stick
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1604, 'width': 1052, 'height': 108}, # Vertical axis of right stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2765, 'y': 1714, 'width': 1052, 'height': 108}, # Horizontal axis of right stick
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 74, 'y': 718, 'width': 1392}, # Left trigger
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2368, 'y': 720, 'width': 1442}, # Right trigger
        #'?': {'Type': 'Analogue', 'x': 1428, 'y': 331, 'width': 1052, 'height': 108}, # Vertical axis of trackpad
        #'?': {'Type': 'Analogue', 'x': 1428, 'y': 441, 'width': 1052, 'height': 108}, # Horizontal axis of trackpad
    },
    'CHProPedals': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    '068E00F2': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    'LogitechG940Joystick': {
        'Joy_1': {'Type': 'Digital', 'x': 2034, 'y': 604, 'width': 652}, # Primary trigger half-press
        'Joy_2': {'Type': 'Digital', 'x': 2044, 'y': 424, 'width': 642, 'height': 108}, # Fire button
        'Joy_3': {'Type': 'Digital', 'x': 2124, 'y': 234, 'width': 642, 'height': 108}, # S1 button
        'Joy_4': {'Type': 'Digital', 'x': 3064, 'y': 496, 'width': 752}, # S2 button
        'Joy_5': {'Type': 'Digital', 'x': 3064, 'y': 584, 'width': 752}, # S3 button
        'Joy_6': {'Type': 'Digital', 'x': 2044, 'y': 764, 'width': 642, 'height': 108}, # S4 button
        'Joy_7': {'Type': 'Digital', 'x': 2044, 'y': 1018, 'width': 642, 'height': 108}, # S5 button
        'Joy_8': {'Type': 'Digital', 'x': 2954, 'y': 386, 'width': 832}, # Ministick button
        'Joy_VAxis': {'Type': 'Analogue', 'x': 2954, 'y': 330, 'width': 832}, # Ministick X
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2954, 'y': 274, 'width': 832}, # Ministick Y
        'Joy_9': {'Type': 'Digital', 'x': 2034, 'y': 660, 'width': 652}, # Primary trigger full-press
        'Joy_POV1Up': {'Type': 'Digital', 'x': 3124, 'y': 694, 'width': 692}, # POV hat up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 3124, 'y': 750, 'width': 692}, # POV hat right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 3124, 'y': 806, 'width': 692}, # POV hat down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 3124, 'y': 862, 'width': 692}, # POV hat left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3144, 'y': 1060, 'width': 672}, # Stick X axis
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3144, 'y': 1004, 'width': 672}, # Stick Y axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 3084, 'y': 1824, 'width': 592}, # Trim 2
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 3224, 'y': 1744, 'width': 592}, # Trim 3
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2934, 'y': 1904, 'width': 592}, # Trim 1
    },
    'LogitechG940Throttle': {
    },
    'LogitechG940Pedals': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal (unconfirmed)
        'Joy_YAxis': {'Type': 'Digital', 'x': 168, 'y': 591, 'width': 1332, 'height': 162}, # Left pedal (unconfirmed)
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1314, 'height': 151}, # Rudder
    },
    'T-Rudder': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2269, 'y': 594, 'width': 1323, 'height': 152}, # Right pedal
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1213, 'y': 343, 'width': 1323, 'height': 152}, # Rudder
    },
    '044FB68F': { # TM TPR Rudder
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 169, 'y': 593, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 593, 'width': 1332, 'height': 162}, # Right pedal
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    'SaitekProFlightRudderPedals': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    '06A30765': { # Copy of SaitekProFlightRudderPedals (although actually Cessna pedals)
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'displayName': 'Cessna pedals',
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    'SaitekProFlightCombatRudderPedals': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal (unconfirmed)
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal (unconfirmed)
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    'SlawFlightControlRudder': {
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal (unconfirmed)
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal (unconfirmed)
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    '16D00A38': { # MFG Crosswind
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'displayName': 'MFG Crosswind',
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal (unconfirmed)
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal (unconfirmed)
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    '85640203': { # MFG Crosswind (alternate address)
        # Although the individual pedals are analogue, they often have digital binds due to their nature so we pretend they are digital
        'displayName': 'MFG Crosswind',
        'Joy_XAxis': {'Type': 'Digital', 'x': 164, 'y': 588, 'width': 1332, 'height': 162}, # Left pedal (unconfirmed)
        'Joy_YAxis': {'Type': 'Digital', 'x': 2264, 'y': 588, 'width': 1332, 'height': 162}, # Right pedal (unconfirmed)
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1208, 'y': 331, 'width': 1332, 'height': 162}, # Rudder
    },
    '046DC29A': { # Logitech GT Wheel
        'displayName': 'Logitech GT Wheel',
        'Joy_1': {'Type': 'Digital', 'x': 2624, 'y': 1089, 'width': 1192, 'height': 54}, # Cross button
        'Joy_2': {'Type': 'Digital', 'x': 2624, 'y': 1184, 'width': 1192, 'height': 54}, # Square button
        'Joy_3': {'Type': 'Digital', 'x': 2624, 'y': 994, 'width': 1192, 'height': 54}, # Circle button
        'Joy_4': {'Type': 'Digital', 'x': 2624, 'y': 900, 'width': 1192, 'height': 54}, # Triangle button
        'Joy_5': {'Type': 'Digital', 'x': 2404, 'y': 594, 'width': 992, 'height': 108}, # Right back paddle
        'Joy_6': {'Type': 'Digital', 'x': 24, 'y': 594, 'width': 992, 'height': 108}, # Left back paddle
        'Joy_7': {'Type': 'Digital', 'x': 2404, 'y': 484, 'width': 992, 'height': 54}, # Right shoulder button
        'Joy_8': {'Type': 'Digital', 'x': 24, 'y': 484, 'width': 992, 'height': 54}, # Left shoulder button
        'Joy_9': {'Type': 'Digital', 'x': 484, 'y': 1720, 'width': 1192, 'height': 54}, # Select button
        'Joy_10': {'Type': 'Digital', 'x': 1744, 'y': 1720, 'width': 1192, 'height': 54}, # Start button
        'Joy_11': {'Type': 'Digital', 'x': 2404, 'y': 354, 'width': 992, 'height': 54}, # R3 button
        'Joy_12': {'Type': 'Digital', 'x': 24, 'y': 354, 'width': 992, 'height': 54}, # L3 button
        'Joy_13': {'Type': 'Digital', 'x': 2684, 'y': 808, 'width': 1132, 'height': 54}, # Gear stick towards
        'Joy_14': {'Type': 'Digital', 'x': 2684, 'y': 752, 'width': 1132, 'height': 54}, # Gear stick away
        'Joy_15': {'Type': 'Digital', 'x': 2684, 'y': 1494, 'width': 1132, 'height': 108}, # Dial button
        'Joy_16': {'Type': 'Digital', 'x': 84, 'y': 1554, 'width': 1132, 'height': 54}, # Plus button
        'Joy_17': {'Type': 'Digital', 'x': 2684, 'y': 1274, 'width': 1132, 'height': 108}, # Dial clockwise
        'Joy_18': {'Type': 'Digital', 'x': 2684, 'y': 1384, 'width': 1132, 'height': 108}, # Dial anticlockwise
        'Joy_19': {'Type': 'Digital', 'x': 84, 'y': 1610, 'width': 1132, 'height': 54}, # Minus button
        'Joy_20': {'Type': 'Digital', 'x': 1544, 'y': 554, 'width': 332, 'height': 108}, # Horn
        'Joy_21': {'Type': 'Digital', 'x': 1114, 'y': 1824, 'width': 1192, 'height': 54}, # Central button
        'Joy_POV1Up': {'Type': 'Digital', 'x': 84, 'y': 870, 'width': 932, 'height': 108}, # PoV up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 84, 'y': 980, 'width': 932, 'height': 108}, # PoV right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 84, 'y': 1090, 'width': 932, 'height': 108}, # PoV down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 84, 'y': 1200, 'width': 932, 'height': 108}, # PoV left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1284, 'y': 304, 'width': 932, 'height': 54}, # Steering wheel
    },
    '044FB351': { # Cougar MFD 1
        'displayName': 'Cougar MFD 1',
        'Joy_1': {'Type': 'Digital', 'x': 134, 'y': 604, 'width': 592, 'height': 100},
        'Joy_2': {'Type': 'Digital', 'x': 239, 'y': 464, 'width': 592, 'height': 100},
        'Joy_3': {'Type': 'Digital', 'x': 644, 'y': 320, 'width': 592, 'height': 100},
        'Joy_4': {'Type': 'Digital', 'x': 1054, 'y': 464, 'width': 592, 'height': 100},
        'Joy_5': {'Type': 'Digital', 'x': 1161, 'y': 604, 'width': 592, 'height': 100},
        'Joy_6': {'Type': 'Digital', 'x': 1424, 'y': 932, 'width': 452, 'height': 100},
        'Joy_7': {'Type': 'Digital', 'x': 1424, 'y': 1040, 'width': 452, 'height': 100},
        'Joy_8': {'Type': 'Digital', 'x': 1424, 'y': 1148, 'width': 452, 'height': 100},
        'Joy_9': {'Type': 'Digital', 'x': 1424, 'y': 1256, 'width': 452, 'height': 100},
        'Joy_10': {'Type': 'Digital', 'x': 1424, 'y': 1364, 'width': 452, 'height': 100},
        'Joy_11': {'Type': 'Digital', 'x': 1161, 'y': 1694, 'width': 592, 'height': 100},
        'Joy_12': {'Type': 'Digital', 'x': 1054, 'y': 1834, 'width': 592, 'height': 100},
        'Joy_13': {'Type': 'Digital', 'x': 644, 'y': 1974, 'width': 592, 'height': 100},
        'Joy_14': {'Type': 'Digital', 'x': 239, 'y': 1834, 'width': 592, 'height': 100},
        'Joy_15': {'Type': 'Digital', 'x': 134, 'y': 1694, 'width': 592, 'height': 100},
        'Joy_16': {'Type': 'Digital', 'x': 24, 'y': 1364, 'width': 452, 'height': 100},
        'Joy_17': {'Type': 'Digital', 'x': 24, 'y': 1256, 'width': 452, 'height': 100},
        'Joy_18': {'Type': 'Digital', 'x': 24, 'y': 1148, 'width': 452, 'height': 100},
        'Joy_19': {'Type': 'Digital', 'x': 24, 'y': 1040, 'width': 452, 'height': 100},
        'Joy_20': {'Type': 'Digital', 'x': 24, 'y': 932, 'width': 452, 'height': 100},
        'Joy_21': {'Type': 'Digital', 'x': 1484, 'y': 762, 'width': 392, 'height': 80},
        'Joy_22': {'Type': 'Digital', 'x': 1484, 'y': 844, 'width': 392, 'height': 80},
        'Joy_23': {'Type': 'Digital', 'x': 1484, 'y': 1472, 'width': 392, 'height': 80},
        'Joy_24': {'Type': 'Digital', 'x': 1484, 'y': 1554, 'width': 392, 'height': 80},
        'Joy_25': {'Type': 'Digital', 'x': 84, 'y': 1472, 'width': 392, 'height': 80},
        'Joy_26': {'Type': 'Digital', 'x': 84, 'y': 1554, 'width': 392, 'height': 80},
        'Joy_27': {'Type': 'Digital', 'x': 84, 'y': 762, 'width': 392, 'height': 80},
        'Joy_28': {'Type': 'Digital', 'x': 84, 'y': 844, 'width': 392, 'height': 80},
    },
    '044FB352': { # Cougar MFD 2
        'displayName': 'Cougar MFD 2',
        'Joy_1': {'Type': 'Digital', 'x': 2068, 'y': 604, 'width': 592, 'height': 100},
        'Joy_2': {'Type': 'Digital', 'x': 2173, 'y': 464, 'width': 592, 'height': 100},
        'Joy_3': {'Type': 'Digital', 'x': 2578, 'y': 320, 'width': 592, 'height': 100},
        'Joy_4': {'Type': 'Digital', 'x': 2988, 'y': 464, 'width': 592, 'height': 100},
        'Joy_5': {'Type': 'Digital', 'x': 3095, 'y': 604, 'width': 592, 'height': 100},
        'Joy_6': {'Type': 'Digital', 'x': 3358, 'y': 932, 'width': 452, 'height': 100},
        'Joy_7': {'Type': 'Digital', 'x': 3358, 'y': 1040, 'width': 452, 'height': 100},
        'Joy_8': {'Type': 'Digital', 'x': 3358, 'y': 1148, 'width': 452, 'height': 100},
        'Joy_9': {'Type': 'Digital', 'x': 3358, 'y': 1256, 'width': 452, 'height': 100},
        'Joy_10': {'Type': 'Digital', 'x': 3358, 'y': 1364, 'width': 452, 'height': 100},
        'Joy_11': {'Type': 'Digital', 'x': 3095, 'y': 1694, 'width': 592, 'height': 100},
        'Joy_12': {'Type': 'Digital', 'x': 2988, 'y': 1834, 'width': 592, 'height': 100},
        'Joy_13': {'Type': 'Digital', 'x': 2578, 'y': 1974, 'width': 592, 'height': 100},
        'Joy_14': {'Type': 'Digital', 'x': 2173, 'y': 1834, 'width': 592, 'height': 100},
        'Joy_15': {'Type': 'Digital', 'x': 2068, 'y': 1694, 'width': 592, 'height': 100},
        'Joy_16': {'Type': 'Digital', 'x': 1958, 'y': 1364, 'width': 452, 'height': 100},
        'Joy_17': {'Type': 'Digital', 'x': 1958, 'y': 1256, 'width': 452, 'height': 100},
        'Joy_18': {'Type': 'Digital', 'x': 1958, 'y': 1148, 'width': 452, 'height': 100},
        'Joy_19': {'Type': 'Digital', 'x': 1958, 'y': 1040, 'width': 452, 'height': 100},
        'Joy_20': {'Type': 'Digital', 'x': 1958, 'y': 932, 'width': 452, 'height': 100},
        'Joy_21': {'Type': 'Digital', 'x': 3418, 'y': 762, 'width': 392, 'height': 80},
        'Joy_22': {'Type': 'Digital', 'x': 3418, 'y': 844, 'width': 392, 'height': 80},
        'Joy_23': {'Type': 'Digital', 'x': 3418, 'y': 1472, 'width': 392, 'height': 80},
        'Joy_24': {'Type': 'Digital', 'x': 3418, 'y': 1554, 'width': 392, 'height': 80},
        'Joy_25': {'Type': 'Digital', 'x': 2018, 'y': 1472, 'width': 392, 'height': 80},
        'Joy_26': {'Type': 'Digital', 'x': 2018, 'y': 1554, 'width': 392, 'height': 80},
        'Joy_27': {'Type': 'Digital', 'x': 2018, 'y': 762, 'width': 392, 'height': 80},
        'Joy_28': {'Type': 'Digital', 'x': 2018, 'y': 844, 'width': 392, 'height': 80},
    },
    '11C05603': { # Cobra M5
        'displayName': 'Cobra M5',
        'Joy_1': {'Type': 'Digital', 'x': 64, 'y': 1273, 'width': 1392, 'height': 54}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2264, 'y': 922, 'width': 1392, 'height': 54}, # Secondary trigger
        'Joy_3': {'Type': 'Digital', 'x': 124, 'y': 1124, 'width': 1332, 'height': 54}, # NAV left red button
        'Joy_4': {'Type': 'Digital', 'x': 2324, 'y': 734, 'width': 1332, 'height': 54}, # NAV right red button
        'Joy_5': {'Type': 'Digital', 'x': 184, 'y': 722, 'width': 1272, 'height': 54}, # NAV witch hat left
        'Joy_6': {'Type': 'Digital', 'x': 184, 'y': 554, 'width': 1272, 'height': 54}, # NAV witch hat up
        'Joy_7': {'Type': 'Digital', 'x': 184, 'y': 610, 'width': 1272, 'height': 54}, # NAV witch hat right
        'Joy_8': {'Type': 'Digital', 'x': 184, 'y': 666, 'width': 1272, 'height': 54}, # NAV witch hat down
        'Joy_9': {'Type': 'Digital', 'x': 124, 'y': 1414, 'width': 1332, 'height': 54}, # NAV pinky trigger
        'Joy_10': {'Type': 'Digital', 'x': 124, 'y': 1064, 'width': 1332, 'height': 54}, # BVR left red button
        'Joy_11': {'Type': 'Digital', 'x': 2324, 'y': 674, 'width': 1332, 'height': 54}, # BVR right red button
        'Joy_12': {'Type': 'Digital', 'x': 184, 'y': 492, 'width': 1272, 'height': 54}, # BVR witch hat left
        'Joy_13': {'Type': 'Digital', 'x': 184, 'y': 324, 'width': 1272, 'height': 54}, # BVR witch hat up
        'Joy_14': {'Type': 'Digital', 'x': 184, 'y': 380, 'width': 1272, 'height': 54}, # BVR witch hat right
        'Joy_15': {'Type': 'Digital', 'x': 184, 'y': 436, 'width': 1272, 'height': 54}, # BVR witch hat down
        'Joy_16': {'Type': 'Digital', 'x': 124, 'y': 1354, 'width': 1332, 'height': 54}, # BVR pinky trigger
        'Joy_17': {'Type': 'Digital', 'x': 124, 'y': 1184, 'width': 1332, 'height': 54}, # VIS left red button
        'Joy_18': {'Type': 'Digital', 'x': 2324, 'y': 794, 'width': 1332, 'height': 54}, # VIS right red button
        'Joy_19': {'Type': 'Digital', 'x': 184, 'y': 952, 'width': 1272, 'height': 54}, # VIS witch hat left
        'Joy_20': {'Type': 'Digital', 'x': 184, 'y': 784, 'width': 1272, 'height': 54}, # VIS witch hat up
        'Joy_21': {'Type': 'Digital', 'x': 184, 'y': 840, 'width': 1272, 'height': 54}, # VIS witch hat right
        'Joy_22': {'Type': 'Digital', 'x': 184, 'y': 896, 'width': 1272, 'height': 54}, # VIS witch hat down
        'Joy_23': {'Type': 'Digital', 'x': 124, 'y': 1474, 'width': 1332, 'height': 54}, # VIS pinky trigger
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1864, 'y': 324, 'width': 1932, 'height': 54}, # PoV up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1864, 'y': 380, 'width': 1932, 'height': 54}, # PoV right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1864, 'y': 436, 'width': 1932, 'height': 54}, # PoV down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1864, 'y': 492, 'width': 1932, 'height': 54}, # PoV left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1080, 'width': 1332, 'height': 54},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1024, 'width': 1332, 'height': 54},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1136, 'width': 1332, 'height': 54},
    },
    '11C05605': { # Cobra M5 variant
        'displayName': 'Cobra M5 variant',
        'Joy_1': {'Type': 'Digital', 'x': 64, 'y': 1273, 'width': 1392, 'height': 54}, # Primary trigger
        'Joy_2': {'Type': 'Digital', 'x': 2264, 'y': 922, 'width': 1392, 'height': 54}, # Secondary trigger
        'Joy_3': {'Type': 'Digital', 'x': 124, 'y': 1124, 'width': 1332, 'height': 54}, # NAV left red button
        'Joy_4': {'Type': 'Digital', 'x': 2324, 'y': 734, 'width': 1332, 'height': 54}, # NAV right red button
        'Joy_5': {'Type': 'Digital', 'x': 184, 'y': 722, 'width': 1272, 'height': 54}, # NAV witch hat left
        'Joy_6': {'Type': 'Digital', 'x': 184, 'y': 554, 'width': 1272, 'height': 54}, # NAV witch hat up
        'Joy_7': {'Type': 'Digital', 'x': 184, 'y': 610, 'width': 1272, 'height': 54}, # NAV witch hat right
        'Joy_8': {'Type': 'Digital', 'x': 184, 'y': 666, 'width': 1272, 'height': 54}, # NAV witch hat down
        'Joy_9': {'Type': 'Digital', 'x': 124, 'y': 1414, 'width': 1332, 'height': 54}, # NAV pinky trigger
        'Joy_10': {'Type': 'Digital', 'x': 124, 'y': 1064, 'width': 1332, 'height': 54}, # BVR left red button
        'Joy_11': {'Type': 'Digital', 'x': 2324, 'y': 674, 'width': 1332, 'height': 54}, # BVR right red button
        'Joy_12': {'Type': 'Digital', 'x': 184, 'y': 492, 'width': 1272, 'height': 54}, # BVR witch hat left
        'Joy_13': {'Type': 'Digital', 'x': 184, 'y': 324, 'width': 1272, 'height': 54}, # BVR witch hat up
        'Joy_14': {'Type': 'Digital', 'x': 184, 'y': 380, 'width': 1272, 'height': 54}, # BVR witch hat right
        'Joy_15': {'Type': 'Digital', 'x': 184, 'y': 436, 'width': 1272, 'height': 54}, # BVR witch hat down
        'Joy_16': {'Type': 'Digital', 'x': 124, 'y': 1354, 'width': 1332, 'height': 54}, # BVR pinky trigger
        'Joy_17': {'Type': 'Digital', 'x': 124, 'y': 1184, 'width': 1332, 'height': 54}, # VIS left red button
        'Joy_18': {'Type': 'Digital', 'x': 2324, 'y': 794, 'width': 1332, 'height': 54}, # VIS right red button
        'Joy_19': {'Type': 'Digital', 'x': 184, 'y': 952, 'width': 1272, 'height': 54}, # VIS witch hat left
        'Joy_20': {'Type': 'Digital', 'x': 184, 'y': 784, 'width': 1272, 'height': 54}, # VIS witch hat up
        'Joy_21': {'Type': 'Digital', 'x': 184, 'y': 840, 'width': 1272, 'height': 54}, # VIS witch hat right
        'Joy_22': {'Type': 'Digital', 'x': 184, 'y': 896, 'width': 1272, 'height': 54}, # VIS witch hat down
        'Joy_23': {'Type': 'Digital', 'x': 124, 'y': 1474, 'width': 1332, 'height': 54}, # VIS pinky trigger
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1864, 'y': 324, 'width': 1932, 'height': 54}, # PoV up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1864, 'y': 380, 'width': 1932, 'height': 54}, # PoV right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1864, 'y': 436, 'width': 1932, 'height': 54}, # PoV down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1864, 'y': 492, 'width': 1932, 'height': 54}, # PoV left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1080, 'width': 1332, 'height': 54},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1024, 'width': 1332, 'height': 54},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2324, 'y': 1136, 'width': 1332, 'height': 54},
    },
    '231D0121': { # VKB Gladiator
        'displayName': 'VKB Gladiator',
        'Joy_1': {'Type': 'Digital', 'x': 204, 'y': 1524, 'width': 992, 'height': 54}, # Flaps up
        'Joy_2': {'Type': 'Digital', 'x': 254, 'y': 1624, 'width': 992, 'height': 54}, # Flaps down
        'Joy_3': {'Type': 'Digital', 'x': 784, 'y': 1904, 'width': 992, 'height': 54}, # A1
        'Joy_4': {'Type': 'Digital', 'x': 2524, 'y': 1514, 'width': 992, 'height': 54}, # A2
        'Joy_5': {'Type': 'Digital', 'x': 2464, 'y': 1424, 'width': 992, 'height': 54}, # A3
        'Joy_6': {'Type': 'Digital', 'x': 1144, 'y': 1994, 'width': 992, 'height': 54}, # B1
        'Joy_7': {'Type': 'Digital', 'x': 2484, 'y': 1814, 'width': 992, 'height': 54}, # B2
        'Joy_8': {'Type': 'Digital', 'x': 2564, 'y': 1604, 'width': 992, 'height': 54}, # B3
        'Joy_9': {'Type': 'Digital', 'x': 2244, 'y': 1994, 'width': 992, 'height': 54}, # C1
        'Joy_10': {'Type': 'Digital', 'x': 2414, 'y': 1904, 'width': 992, 'height': 54}, # C2
        'Joy_11': {'Type': 'Digital', 'x': 2624, 'y': 1694, 'width': 992, 'height': 54}, # C3
        'Joy_12': {'Type': 'Digital', 'x': 2274, 'y': 1254, 'width': 1192, 'height': 54}, # Engine start
        'Joy_13': {'Type': 'Digital', 'x': 2204, 'y': 1114, 'width': 1192, 'height': 54}, # Eject
        'Joy_14': {'Type': 'Digital', 'x': 2184, 'y': 584, 'width': 1472, 'height': 54}, # Primary trigger (mode 1, unshifted)
        'Joy_15': {'Type': 'Digital', 'x': 2184, 'y': 640, 'width': 1472, 'height': 56}, # Primary trigger (mode 1, shifted)
        'Joy_16': {'Type': 'Digital', 'x': 2184, 'y': 704, 'width': 1472, 'height': 54}, # Primary trigger (mode 2, unshifted)
        'Joy_17': {'Type': 'Digital', 'x': 2184, 'y': 760, 'width': 1472, 'height': 56}, # Primary trigger (mode 2, shifted)
        'Joy_18': {'Type': 'Digital', 'x': 2124, 'y': 304, 'width': 1472, 'height': 54}, # Thumb trigger (mode 1, unshifted)
        'Joy_19': {'Type': 'Digital', 'x': 2124, 'y': 360, 'width': 1472, 'height': 56}, # Thumb trigger (mode 1, shifted)
        'Joy_20': {'Type': 'Digital', 'x': 2124, 'y': 424, 'width': 1472, 'height': 54}, # Thumb trigger (mode 2, unshifted)
        'Joy_21': {'Type': 'Digital', 'x': 2124, 'y': 480, 'width': 1472, 'height': 56}, # Thumb trigger (mode 2, shifted)
        'Joy_POV1Up': {'Type': 'Digital', 'x': 274, 'y': 304, 'width': 1112, 'height': 54}, # POV hat up (mode 1, unshifted)
        'Joy_22': {'Type': 'Digital', 'x': 274, 'y': 360, 'width': 1112, 'height': 54}, # POV hat up (mode 1, shifted)
        'Joy_POV1Down': {'Type': 'Digital', 'x': 274, 'y': 526, 'width': 1112, 'height': 52}, # POV hat down (mode 1, unshifted)
        'Joy_23': {'Type': 'Digital', 'x': 274, 'y': 580, 'width': 1112, 'height': 54}, # POV hat down (mode 1, shifted)
        'Joy_POV1Left': {'Type': 'Digital', 'x': 274, 'y': 636, 'width': 1112, 'height': 52}, # POV hat left (mode 1, unshifted)
        'Joy_24': {'Type': 'Digital', 'x': 274, 'y': 690, 'width': 1112, 'height': 66}, # POV hat left (mode 1, shifted)
        'Joy_POV1Right': {'Type': 'Digital', 'x': 274, 'y': 416, 'width': 1112, 'height': 52}, # POV hat right (mode 1, unshifted)
        'Joy_25': {'Type': 'Digital', 'x': 274, 'y': 470, 'width': 1112, 'height': 54}, # POV hat right (mode 1, shifted)
        'Joy_POV2Up': {'Type': 'Digital', 'x': 274, 'y': 764, 'width': 1112, 'height': 54}, # POV hat up (mode 2, unshifted)
        'Joy_26': {'Type': 'Digital', 'x': 274, 'y': 820, 'width': 1112, 'height': 54}, # POV hat up (mode 2, shifted)
        'Joy_POV2Down': {'Type': 'Digital', 'x': 274, 'y': 986, 'width': 1112, 'height': 52}, # POV hat down (mode 2, unshifted)
        'Joy_27': {'Type': 'Digital', 'x': 274, 'y': 1040, 'width': 1112, 'height': 54}, # POV hat down (mode 2, shifted)
        'Joy_POV2Left': {'Type': 'Digital', 'x': 274, 'y': 1096, 'width': 1112, 'height': 52}, # POV hat left (mode 2, unshifted)
        'Joy_28': {'Type': 'Digital', 'x': 274, 'y': 1150, 'width': 1112, 'height': 66}, # POV hat left (mode 2, shifted)
        'Joy_POV2Right': {'Type': 'Digital', 'x': 274, 'y': 876, 'width': 1112, 'height': 52}, # POV hat right (mode 2, unshifted)
        'Joy_29': {'Type': 'Digital', 'x': 274, 'y': 930, 'width': 1112, 'height': 54}, # POV hat right (mode 2, shifted)
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2164, 'y': 910, 'width': 1532, 'height': 54}, # Roll
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2164, 'y': 854, 'width': 1532, 'height': 54}, # Pitch
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2164, 'y': 966, 'width': 1532, 'height': 54}, # Yaw
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 564, 'y': 1402, 'width': 832, 'height': 54}, # Throttle
    },
    '03EB2042': { # VPC WarBRD Delta left
        'displayName': 'VPC WarBRD Delta left',
        'Joy_1': {'Type': 'Digital', 'x': 2470, 'y': 1100, 'width': 1180}, # Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2470, 'y': 1160, 'width': 1180}, # Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2470, 'y': 1300, 'width': 1180}, # Trigger button
        'Joy_4': {'Type': 'Digital', 'x': 270, 'y': 1000, 'width': 1180}, # Wheel up
        'Joy_5': {'Type': 'Digital', 'x': 270, 'y': 1060, 'width': 1180}, # Wheel down
        'Joy_6': {'Type': 'Digital', 'x': 270, 'y': 1120, 'width': 1180}, # Wheel push
        'Joy_7': {'Type': 'Digital', 'x': 270, 'y': 820, 'width': 1180}, # Mini-joystick push
		# 4-way hat right
        'Joy_8': {'Type': 'Digital', 'x': 2470, 'y': 700, 'width': 1180}, 
        'Joy_9': {'Type': 'Digital', 'x': 2470, 'y': 760, 'width': 1180},
        'Joy_10': {'Type': 'Digital', 'x': 2470, 'y': 820, 'width': 1180},
        'Joy_11': {'Type': 'Digital', 'x': 2470, 'y': 880, 'width': 1180},
        'Joy_12': {'Type': 'Digital', 'x': 2470, 'y': 940, 'width': 1180},
		# 4-way hat left
        'Joy_13': {'Type': 'Digital', 'x': 270, 'y': 300, 'width': 1180},
        'Joy_14': {'Type': 'Digital', 'x': 270, 'y': 360, 'width': 1180},
        'Joy_15': {'Type': 'Digital', 'x': 270, 'y': 420, 'width': 1180},
        'Joy_16': {'Type': 'Digital', 'x': 270, 'y': 480, 'width': 1180},
        'Joy_17': {'Type': 'Digital', 'x': 270, 'y': 540, 'width': 1180},
		# 8-way hat LED
        'Joy_18': {'Type': 'Digital', 'x': 2470, 'y': 300, 'width': 1180},
        'Joy_19': {'Type': 'Digital', 'x': 2470, 'y': 360, 'width': 1180},
        'Joy_20': {'Type': 'Digital', 'x': 2470, 'y': 420, 'width': 1180},
        'Joy_21': {'Type': 'Digital', 'x': 2470, 'y': 480, 'width': 1180},
        'Joy_22': {'Type': 'Digital', 'x': 2470, 'y': 540, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 270, 'y': 1400, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 270, 'y': 1460, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 270, 'y': 1520, 'width': 1180},
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 270, 'y': 700, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 270, 'y': 760, 'width': 1180},
    },
    '03EB2044': { # VPC WarBRD Delta right
        'displayName': 'VPC WarBRD Delta right',
        'Joy_1': {'Type': 'Digital', 'x': 270, 'y': 1100, 'width': 1180}, # Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 270, 'y': 1160, 'width': 1180}, # Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 270, 'y': 1300, 'width': 1180}, # Trigger button
        'Joy_4': {'Type': 'Digital', 'x': 2470, 'y': 1000, 'width': 1180}, # Wheel up
        'Joy_5': {'Type': 'Digital', 'x': 2470, 'y': 1060, 'width': 1180}, # Wheel down
        'Joy_6': {'Type': 'Digital', 'x': 2470, 'y': 1120, 'width': 1180}, # Wheel push
        'Joy_7': {'Type': 'Digital', 'x': 2470, 'y': 820, 'width': 1180}, # Mini-joystick push
		# 4-way hat right
        'Joy_8': {'Type': 'Digital', 'x': 2470, 'y': 300, 'width': 1180},
        'Joy_9': {'Type': 'Digital', 'x': 2470, 'y': 360, 'width': 1180},
        'Joy_10': {'Type': 'Digital', 'x': 2470, 'y': 420, 'width': 1180},
        'Joy_11': {'Type': 'Digital', 'x': 2470, 'y': 480, 'width': 1180},
        'Joy_12': {'Type': 'Digital', 'x': 2470, 'y': 540, 'width': 1180},
		# 4-way hat left
		'Joy_13': {'Type': 'Digital', 'x': 270, 'y': 700, 'width': 1180}, 
        'Joy_14': {'Type': 'Digital', 'x': 270, 'y': 760, 'width': 1180},
        'Joy_15': {'Type': 'Digital', 'x': 270, 'y': 820, 'width': 1180},
        'Joy_16': {'Type': 'Digital', 'x': 270, 'y': 880, 'width': 1180},
        'Joy_17': {'Type': 'Digital', 'x': 270, 'y': 940, 'width': 1180},
		# 8-way hat LED
        'Joy_18': {'Type': 'Digital', 'x': 270, 'y': 300, 'width': 1180},
        'Joy_19': {'Type': 'Digital', 'x': 270, 'y': 360, 'width': 1180},
        'Joy_20': {'Type': 'Digital', 'x': 270, 'y': 420, 'width': 1180},
        'Joy_21': {'Type': 'Digital', 'x': 270, 'y': 480, 'width': 1180},
        'Joy_22': {'Type': 'Digital', 'x': 270, 'y': 540, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2470, 'y': 1400, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2470, 'y': 1460, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2470, 'y': 1520, 'width': 1180},
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2470, 'y': 700, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2470, 'y': 760, 'width': 1180},
    },
        '03EB2046': { # VPC Alpha left
        'displayName': 'VPC Alpha left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '03EB2048': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button        
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
		# 4-way hat top
		'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '03EB9901': { # VPC Alpha left
        'displayName': 'VPC Alpha left',
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '03EB9902': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button        
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
		# 4-way hat top
		'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334483EB': { # VPC Alpha left
        'displayName': 'VPC Alpha left',
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '334480CB': { # VPC Alpha left
        'displayName': 'VPC Alpha left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '3344C0CB': { # VPC Alpha left
        'displayName': 'VPC Alpha left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '334443EB': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button        
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
		# 4-way hat top
		'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
		# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334440CB': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180},
	# 4-way hat top
	'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	# 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334400CB': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180},
	    # 4-way hat top
	    'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '3344412F': { # VPC Alpha right
        'displayName': 'VPC Alpha right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Black button
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push
        'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Red button
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180},
	    # 4-way hat top
	    'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},

        # Break axis
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334483F3': { # VPC Alpha Prime left
        'displayName': 'VPC Alpha Prime left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '3344838F': { # VPC Alpha Prime left
        'displayName': 'VPC Alpha Prime left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '334403F3': { # VPC Alpha Prime left
        'displayName': 'VPC Alpha Prime left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '3344038F': { # VPC Alpha Prime left
        'displayName': 'VPC Alpha Prime left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '334443F5': { # VPC Alpha Prime left
        'displayName': 'VPC Alpha Prime left',
        'Joy_1': {'Type': 'Digital', 'x': 2610, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 2610, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 2610, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 2610, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 2610, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 2610, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button
        'Joy_7': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Red button
        # 4-way hat top
   		'Joy_8': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 120, 'y': 570, 'width': 1180}, # Up
        'Joy_10': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 120, 'y': 690, 'width': 1180}, # Down 
        'Joy_12': {'Type': 'Digital', 'x': 120, 'y': 750, 'width': 1180}, # Left
        # Black button
        'Joy_13': {'Type': 'Digital', 'x': 120, 'y': 920, 'width': 1180},        
		# 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 120, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 120, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 120, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 120, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 120, 'y': 1280, 'width': 1180}, # Left
		# 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 120, 'y': 450, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 120, 'y': 390, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 120, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_20': {'Type': 'Digital', 'x': 120, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_22': {'Type': 'Digital', 'x': 120, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 120, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 2610, 'y': 1540, 'width': 1180}, # Push
        'Joy_26': {'Type': 'Digital', 'x': 2610, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 2610, 'y': 1360, 'width': 1180}, # Righ
        'Joy_24': {'Type': 'Digital', 'x': 2610, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 2610, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 2610, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 2610, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1690, 'width': 1180},
		# Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 120, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 120, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 120, 'y': 1980, 'width': 1180}, # Twist
		# Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2610, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2610, 'y': 570, 'width': 1180},
    },
    '334443F4': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '33444390': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '3344C3F3': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334483F4': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334403F4': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '334440D4': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '33440390': { # VPC Alpha Prime right
        'displayName': 'VPC Alpha Prime right',
        'Joy_1': {'Type': 'Digital', 'x': 120, 'y': 810, 'width': 1180}, # Flip Trigger first stage
        'Joy_2': {'Type': 'Digital', 'x': 120, 'y': 870, 'width': 1180}, # Flip Trigger second stage
        'Joy_3': {'Type': 'Digital', 'x': 120, 'y': 930, 'width': 1180}, # Flip Trigger third stage
        'Joy_4': {'Type': 'Digital', 'x': 120, 'y': 1060, 'width': 1180}, # Trigger first stage
        'Joy_5': {'Type': 'Digital', 'x': 120, 'y': 1120, 'width': 1180}, # Trigger second stage
        'Joy_6': {'Type': 'Digital', 'x': 120, 'y': 630, 'width': 1180}, # Mini-joystick push
        # Lower button        
        'Joy_13': {'Type': 'Digital', 'x': 2610, 'y': 920, 'width': 1180},
        # 4-way hat bottom
        'Joy_14': {'Type': 'Digital', 'x': 2610, 'y': 1340, 'width': 1180}, # Push		
        'Joy_15': {'Type': 'Digital', 'x': 2610, 'y': 1100, 'width': 1180}, # Up
        'Joy_18': {'Type': 'Digital', 'x': 2610, 'y': 1160, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2610, 'y': 1220, 'width': 1180}, # Down
        'Joy_16': {'Type': 'Digital', 'x': 2610, 'y': 1280, 'width': 1180}, # Left
        # Top button
        'Joy_7': {'Type': 'Digital', 'x': 120, 'y': 330, 'width': 1180}, 
	    # 4-way hat top
	    'Joy_8': {'Type': 'Digital', 'x': 2610, 'y': 740, 'width': 1180}, # Push
        'Joy_9': {'Type': 'Digital', 'x': 2610, 'y': 500, 'width': 1180}, # Up
        'Joy_12': {'Type': 'Digital', 'x': 2610, 'y': 560, 'width': 1180}, # Right
        'Joy_11': {'Type': 'Digital', 'x': 2610, 'y': 620, 'width': 1180}, # Down 
        'Joy_10': {'Type': 'Digital', 'x': 2610, 'y': 680, 'width': 1180}, # Left
	    # 2-way hat
        'Joy_28': {'Type': 'Digital', 'x': 2610, 'y': 330, 'width': 1180}, # Push
        'Joy_29': {'Type': 'Digital', 'x': 2610, 'y': 210, 'width': 1180}, # Up
        'Joy_30': {'Type': 'Digital', 'x': 2610, 'y': 270, 'width': 1180}, # Down
        # Wheel
        'Joy_19': {'Type': 'Digital', 'x': 2610, 'y': 1630, 'width': 1180}, # Push first stage
        'Joy_20': {'Type': 'Digital', 'x': 2610, 'y': 1690, 'width': 1180}, # Push second stage
        'Joy_22': {'Type': 'Digital', 'x': 2610, 'y': 1570, 'width': 1180}, # Down
        'Joy_21': {'Type': 'Digital', 'x': 2610, 'y': 1510, 'width': 1180}, # Up
        # Thumb hat
        'Joy_23': {'Type': 'Digital', 'x': 120, 'y': 1540, 'width': 1180}, # Push
        'Joy_24': {'Type': 'Digital', 'x': 120, 'y': 1300, 'width': 1180}, # Up
        'Joy_27': {'Type': 'Digital', 'x': 120, 'y': 1360, 'width': 1180}, # Righ
        'Joy_26': {'Type': 'Digital', 'x': 120, 'y': 1420, 'width': 1180}, # Down
        'Joy_25': {'Type': 'Digital', 'x': 120, 'y': 1480, 'width': 1180}, # Left
        # Pinky button
        'Joy_31': {'Type': 'Digital', 'x': 120, 'y': 1900, 'width': 1180},
        # Break axis
        'Joy_32': {'Type': 'Digital', 'x': 120, 'y': 1750, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 120, 'y': 1690, 'width': 1180},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1860, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1920, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 2610, 'y': 1980, 'width': 1180},
	    # Mini-joysticks axis
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 120, 'y': 510, 'width': 1180},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 120, 'y': 570, 'width': 1180},
    },
    '33444393': { # VPC FLNKR Grip
        'displayName': 'VPC FLNKR Grip',
        'Joy_1': {'Type': 'Digital', 'x': 25, 'y': 349, 'width': 561}, # Left Thumb button
        # centre hat
        'Joy_2': {'Type': 'Digital', 'x': 1155, 'y': 263, 'width': 1180}, # push
        'Joy_3': {'Type': 'Digital', 'x': 1155, 'y': 24, 'width': 1180}, # up
        'Joy_4': {'Type': 'Digital', 'x': 1155, 'y': 83, 'width': 1180}, # right
        'Joy_5': {'Type': 'Digital', 'x': 1155, 'y': 143, 'width': 1180}, # down
        'Joy_6': {'Type': 'Digital', 'x': 1155, 'y': 203, 'width': 1180}, # left
        # Right button        
        'Joy_7': {'Type': 'Digital', 'x': 1155, 'y': 373, 'width': 1215}, # Right Thumb button
        # 4-way hat right
        'Joy_9': {'Type': 'Digital', 'x': 1313, 'y': 1157, 'width': 1180}, # Push		
        'Joy_10': {'Type': 'Digital', 'x': 1313, 'y': 919, 'width': 1180}, # Up
        'Joy_11': {'Type': 'Digital', 'x': 1313, 'y': 977, 'width': 1180}, # Right
        'Joy_12': {'Type': 'Digital', 'x': 1313, 'y': 1038, 'width': 1180}, # Down
        'Joy_13': {'Type': 'Digital', 'x': 1313, 'y': 1092, 'width': 1180}, # Left
	    # 4-way hat right side
	    'Joy_20': {'Type': 'Digital', 'x': 1379, 'y': 710, 'width': 1180}, # Push
        'Joy_21': {'Type': 'Digital', 'x': 1379, 'y': 470, 'width': 1180}, # Up
        'Joy_22': {'Type': 'Digital', 'x': 1379, 'y': 529, 'width': 1180}, # Right
        'Joy_23': {'Type': 'Digital', 'x': 1379, 'y': 591, 'width': 1180}, # Down 
        'Joy_24': {'Type': 'Digital', 'x': 1379, 'y': 649, 'width': 1180}, # Left
	    # 2-way hat left
        'Joy_8': {'Type': 'Digital', 'x': 77, 'y': 977, 'width': 423}, # Push
        'Joy_RXAxis': {'Type': 'Digital', 'x': 77, 'y': 856, 'width': 423}, # Left/Right
        'Joy_RYAxis': {'Type': 'Digital', 'x': 77, 'y': 916, 'width': 423}, # Up/Down
        # two-stage trigger
        'Joy_27': {'Type': 'Digital', 'x': 1117, 'y': 1519, 'width': 1180}, # Push first stage
        'Joy_28': {'Type': 'Digital', 'x': 1117, 'y': 1579, 'width': 1180}, # Push second stage
        # combo trigger
        'Joy_25': {'Type': 'Digital', 'x': 1584, 'y': 1231, 'width': 1180}, # Up
        'Joy_26': {'Type': 'Digital', 'x': 1584, 'y': 1290, 'width': 1180}, # Push
        # Lower Thumb hat
        'Joy_14': {'Type': 'Digital', 'x': 2593, 'y': 382, 'width': 1180}, # Push
        'Joy_15': {'Type': 'Digital', 'x': 2593, 'y': 144, 'width': 1180}, # Up
        'Joy_16': {'Type': 'Digital', 'x': 2593, 'y': 202, 'width': 1180}, # Right
        'Joy_17': {'Type': 'Digital', 'x': 2593, 'y': 264, 'width': 1180}, # Down
        'Joy_18': {'Type': 'Digital', 'x': 2593, 'y': 322, 'width': 1180}, # Left
        # Lower left side thumb button
        'Joy_19': {'Type': 'Digital', 'x': 1813, 'y': 1440, 'width': 1215},
        # Break axis
        'Joy_30': {'Type': 'Digital', 'x': 1822, 'y': 1747, 'width': 1180},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 1822, 'y': 1792, 'width': 1180}, #TODO: verify this one's name in binds file!
        # Trigger
        'Joy_29': {'Type': 'Digital', 'x': 1882, 'y': 1370, 'width': 1215},
	    # Joystick axis
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1000, 'y': 1951, 'width': 1180},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1000, 'y': 2010, 'width': 1180},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1000, 'y': 2073, 'width': 1180},
    },
    '33448195': { # VPC MongoosT-50CM2 Throttle
        'displayName': 'VPC MongoosT-50CM2 Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},       # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        # As of update 18.02 of Elite Dangerous 4.0 support for 128 buttons per device was added. - 2024-04-10
        'Joy_33': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},        # Throttle Right Back Button Lower
        'Joy_34': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},      # T1
        'Joy_35': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},      # T2
        'Joy_36': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},       # T3
        'Joy_37': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},       # T4
        'Joy_38': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},       # B1 - Mode 1
        'Joy_39': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},       # B2 - Mode 1
        'Joy_40': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},       # B3 - Mode 1
        'Joy_41': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},       # B4 - Mode 1
        'Joy_42': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},       # B5 - Mode 1
        'Joy_43': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},       # B6 - Mode 1
        'Joy_44': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},       # T5 Forwards
        'Joy_45': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},       # T5 Backwards
        'Joy_46': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},       # T6 Forwards
        'Joy_47': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},       # T6 Backwards
        'Joy_48': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},       # T7 Forwards
        'Joy_49': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},       # T7 Backwards
        'Joy_50': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},      # E1 Button
        'Joy_51': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},      # E1 Anti-Clockwise
        'Joy_52': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},      # E1 Clockwise
        'Joy_53': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},      # E2 Button
        'Joy_54': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},      # E2 Anti-Clockwise
        'Joy_55': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},      # E2 Clockwise
        'Joy_56': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},       # B1 - Mode 2
        'Joy_57': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},       # B2 - Mode 2
        'Joy_58': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},       # B3 - Mode 2
        'Joy_59': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},       # B4 - Mode 2
        'Joy_60': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},       # B5 - Mode 2
        'Joy_61': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},       # B6 - Mode 2
        'Joy_62': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},      # B1 - Mode 3
        'Joy_63': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},      # B2 - Mode 3
        'Joy_64': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},      # B3 - Mode 3

        'Joy_65': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},      # B4 - Mode 3
        'Joy_66': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},      # B5 - Mode 3
        'Joy_67': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},      # B6 - Mode 3
        'Joy_68': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},      # B1 - Mode 4
        'Joy_69': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},      # B2 - Mode 4
        'Joy_70': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},      # B3 - Mode 4
        'Joy_71': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},      # B4 - Mode 4
        'Joy_72': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},      # B5 - Mode 4
        'Joy_73': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},      # B6 - Mode 4
        'Joy_74': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180},      # B1 - Mode 5
        'Joy_75': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180},      # B2 - Mode 5
        'Joy_76': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180},      # B3 - Mode 5
        'Joy_77': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180},      # B4 - Mode 5
        'Joy_79': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180},      # B5 - Mode 5
        'Joy_80': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180},      # B6 - Mode 5

        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },
    '33448197': { # VPC MongoosT-50CM3 Throttle
        'displayName': 'VPC MongoosT-50CM3 Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},       # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        # As of update 18.02 of Elite Dangerous 4.0 support for 128 buttons per device was added. - 2024-04-10
        'Joy_33': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},        # Throttle Right Back Button Lower
        'Joy_34': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},      # T1
        'Joy_35': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},      # T2
        'Joy_36': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},       # T3
        'Joy_37': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},       # T4
        'Joy_38': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},       # B1 - Mode 1
        'Joy_39': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},       # B2 - Mode 1
        'Joy_40': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},       # B3 - Mode 1
        'Joy_41': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},       # B4 - Mode 1
        'Joy_42': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},       # B5 - Mode 1
        'Joy_43': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},       # B6 - Mode 1
        'Joy_44': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},       # T5 Forwards
        'Joy_45': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},       # T5 Backwards
        'Joy_46': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},       # T6 Forwards
        'Joy_47': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},       # T6 Backwards
        'Joy_48': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},       # T7 Forwards
        'Joy_49': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},       # T7 Backwards
        'Joy_50': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},      # E1 Button
        'Joy_51': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},      # E1 Anti-Clockwise
        'Joy_52': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},      # E1 Clockwise
        'Joy_53': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},      # E2 Button
        'Joy_54': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},      # E2 Anti-Clockwise
        'Joy_55': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},      # E2 Clockwise
        'Joy_56': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},       # B1 - Mode 2
        'Joy_57': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},       # B2 - Mode 2
        'Joy_58': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},       # B3 - Mode 2
        'Joy_59': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},       # B4 - Mode 2
        'Joy_60': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},       # B5 - Mode 2
        'Joy_61': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},       # B6 - Mode 2
        'Joy_62': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},      # B1 - Mode 3
        'Joy_63': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},      # B2 - Mode 3
        'Joy_64': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},      # B3 - Mode 3

        'Joy_65': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},      # B4 - Mode 3
        'Joy_66': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},      # B5 - Mode 3
        'Joy_67': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},      # B6 - Mode 3
        'Joy_68': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},      # B1 - Mode 4
        'Joy_69': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},      # B2 - Mode 4
        'Joy_70': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},      # B3 - Mode 4
        'Joy_71': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},      # B4 - Mode 4
        'Joy_72': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},      # B5 - Mode 4
        'Joy_73': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},      # B6 - Mode 4
        'Joy_74': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180},      # B1 - Mode 5
        'Joy_75': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180},      # B2 - Mode 5
        'Joy_76': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180},      # B3 - Mode 5
        'Joy_77': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180},      # B4 - Mode 5
        'Joy_79': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180},      # B5 - Mode 5
        'Joy_80': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180},      # B6 - Mode 5

        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },
    'VPCThrottle': { # VPC MongoosT-50CM3 Throttle
        'displayName': 'VPC MongoosT-50CM3 Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},       # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        # As of update 18.02 of Elite Dangerous 4.0 support for 128 buttons per device was added. - 2024-04-10
        'Joy_33': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},        # Throttle Right Back Button Lower
        'Joy_34': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},      # T1
        'Joy_35': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},      # T2
        'Joy_36': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},       # T3
        'Joy_37': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},       # T4
        'Joy_38': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},       # B1 - Mode 1
        'Joy_39': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},       # B2 - Mode 1
        'Joy_40': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},       # B3 - Mode 1
        'Joy_41': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},       # B4 - Mode 1
        'Joy_42': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},       # B5 - Mode 1
        'Joy_43': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},       # B6 - Mode 1
        'Joy_44': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},       # T5 Forwards
        'Joy_45': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},       # T5 Backwards
        'Joy_46': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},       # T6 Forwards
        'Joy_47': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},       # T6 Backwards
        'Joy_48': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},       # T7 Forwards
        'Joy_49': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},       # T7 Backwards
        'Joy_50': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},      # E1 Button
        'Joy_51': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},      # E1 Anti-Clockwise
        'Joy_52': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},      # E1 Clockwise
        'Joy_53': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},      # E2 Button
        'Joy_54': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},      # E2 Anti-Clockwise
        'Joy_55': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},      # E2 Clockwise
        'Joy_56': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},       # B1 - Mode 2
        'Joy_57': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},       # B2 - Mode 2
        'Joy_58': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},       # B3 - Mode 2
        'Joy_59': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},       # B4 - Mode 2
        'Joy_60': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},       # B5 - Mode 2
        'Joy_61': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},       # B6 - Mode 2
        'Joy_62': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},      # B1 - Mode 3
        'Joy_63': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},      # B2 - Mode 3
        'Joy_64': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},      # B3 - Mode 3

        'Joy_65': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},      # B4 - Mode 3
        'Joy_66': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},      # B5 - Mode 3
        'Joy_67': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},      # B6 - Mode 3
        'Joy_68': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},      # B1 - Mode 4
        'Joy_69': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},      # B2 - Mode 4
        'Joy_70': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},      # B3 - Mode 4
        'Joy_71': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},      # B4 - Mode 4
        'Joy_72': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},      # B5 - Mode 4
        'Joy_73': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},      # B6 - Mode 4
        'Joy_74': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180},      # B1 - Mode 5
        'Joy_75': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180},      # B2 - Mode 5
        'Joy_76': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180},      # B3 - Mode 5
        'Joy_77': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180},      # B4 - Mode 5
        'Joy_79': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180},      # B5 - Mode 5
        'Joy_80': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180},      # B6 - Mode 5

        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },
    '33440197': { # VPC MongoosT-50CM3 Throttle
        'displayName': 'VPC MongoosT-50CM3 Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},       # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        # As of update 18.02 of Elite Dangerous 4.0 support for 128 buttons per device was added. - 2024-04-10
        'Joy_33': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},        # Throttle Right Back Button Lower
        'Joy_34': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},      # T1
        'Joy_35': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},      # T2
        'Joy_36': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},       # T3
        'Joy_37': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},       # T4
        'Joy_38': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},       # B1 - Mode 1
        'Joy_39': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},       # B2 - Mode 1
        'Joy_40': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},       # B3 - Mode 1
        'Joy_41': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},       # B4 - Mode 1
        'Joy_42': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},       # B5 - Mode 1
        'Joy_43': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},       # B6 - Mode 1
        'Joy_44': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},       # T5 Forwards
        'Joy_45': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},       # T5 Backwards
        'Joy_46': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},       # T6 Forwards
        'Joy_47': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},       # T6 Backwards
        'Joy_48': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},       # T7 Forwards
        'Joy_49': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},       # T7 Backwards
        'Joy_50': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},      # E1 Button
        'Joy_51': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},      # E1 Anti-Clockwise
        'Joy_52': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},      # E1 Clockwise
        'Joy_53': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},      # E2 Button
        'Joy_54': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},      # E2 Anti-Clockwise
        'Joy_55': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},      # E2 Clockwise
        'Joy_56': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},       # B1 - Mode 2
        'Joy_57': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},       # B2 - Mode 2
        'Joy_58': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},       # B3 - Mode 2
        'Joy_59': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},       # B4 - Mode 2
        'Joy_60': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},       # B5 - Mode 2
        'Joy_61': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},       # B6 - Mode 2
        'Joy_62': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},      # B1 - Mode 3
        'Joy_63': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},      # B2 - Mode 3
        'Joy_64': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},      # B3 - Mode 3

        'Joy_65': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},      # B4 - Mode 3
        'Joy_66': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},      # B5 - Mode 3
        'Joy_67': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},      # B6 - Mode 3
        'Joy_68': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},      # B1 - Mode 4
        'Joy_69': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},      # B2 - Mode 4
        'Joy_70': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},      # B3 - Mode 4
        'Joy_71': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},      # B4 - Mode 4
        'Joy_72': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},      # B5 - Mode 4
        'Joy_73': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},      # B6 - Mode 4
        'Joy_74': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180},      # B1 - Mode 5
        'Joy_75': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180},      # B2 - Mode 5
        'Joy_76': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180},      # B3 - Mode 5
        'Joy_77': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180},      # B4 - Mode 5
        'Joy_79': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180},      # B5 - Mode 5
        'Joy_80': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180},      # B6 - Mode 5

        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },
    '33440198': { # VPC MongoosT-50CM3 Throttle
        'displayName': 'VPC MongoosT-50CM3 Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},       # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        # As of update 18.02 of Elite Dangerous 4.0 support for 128 buttons per device was added. - 2024-04-10
        'Joy_33': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},        # Throttle Right Back Button Lower
        'Joy_34': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},      # T1
        'Joy_35': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},      # T2
        'Joy_36': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},       # T3
        'Joy_37': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},       # T4
        'Joy_38': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},       # B1 - Mode 1
        'Joy_39': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},       # B2 - Mode 1
        'Joy_40': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},       # B3 - Mode 1
        'Joy_41': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},       # B4 - Mode 1
        'Joy_42': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},       # B5 - Mode 1
        'Joy_43': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},       # B6 - Mode 1
        'Joy_44': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},       # T5 Forwards
        'Joy_45': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},       # T5 Backwards
        'Joy_46': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},       # T6 Forwards
        'Joy_47': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},       # T6 Backwards
        'Joy_48': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},       # T7 Forwards
        'Joy_49': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},       # T7 Backwards
        'Joy_50': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},      # E1 Button
        'Joy_51': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},      # E1 Anti-Clockwise
        'Joy_52': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},      # E1 Clockwise
        'Joy_53': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},      # E2 Button
        'Joy_54': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},      # E2 Anti-Clockwise
        'Joy_55': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},      # E2 Clockwise
        'Joy_56': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},       # B1 - Mode 2
        'Joy_57': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},       # B2 - Mode 2
        'Joy_58': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},       # B3 - Mode 2
        'Joy_59': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},       # B4 - Mode 2
        'Joy_60': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},       # B5 - Mode 2
        'Joy_61': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},       # B6 - Mode 2
        'Joy_62': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},      # B1 - Mode 3
        'Joy_63': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},      # B2 - Mode 3
        'Joy_64': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},      # B3 - Mode 3

        'Joy_65': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},      # B4 - Mode 3
        'Joy_66': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},      # B5 - Mode 3
        'Joy_67': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},      # B6 - Mode 3
        'Joy_68': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},      # B1 - Mode 4
        'Joy_69': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},      # B2 - Mode 4
        'Joy_70': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},      # B3 - Mode 4
        'Joy_71': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},      # B4 - Mode 4
        'Joy_72': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},      # B5 - Mode 4
        'Joy_73': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},      # B6 - Mode 4
        'Joy_74': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180},      # B1 - Mode 5
        'Joy_75': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180},      # B2 - Mode 5
        'Joy_76': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180},      # B3 - Mode 5
        'Joy_77': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180},      # B4 - Mode 5
        'Joy_79': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180},      # B5 - Mode 5
        'Joy_80': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180},      # B6 - Mode 5

        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },    
    'VPC-MongoosT-50CM3-Throttle-32B0': { # VPC MongoosT-50CM3 Throttle - 32 Button Split Mode - Device 0
        'displayName': 'VPC MongoosT-50CM3 Throttle - 32 Button Split',
        'Joy_1': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},     # Throttle Right Back Button Lower
        'Joy_2': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},   # T1
        'Joy_3': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},   # T2
        'Joy_4': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},    # T3
        'Joy_5': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},    # T4
        'Joy_6': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},    # B1 - Mode 1
        'Joy_7': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},    # B2 - Mode 1
        'Joy_8': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},    # B3 - Mode 1
        'Joy_9': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},    # B4 - Mode 1
        'Joy_10': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},   # B5 - Mode 1
        'Joy_11': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},   # B6 - Mode 1
        'Joy_12': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},   # T5 Forwards
        'Joy_13': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},   # T5 Backwards
        'Joy_14': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},   # T6 Forwards
        'Joy_15': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},   # T6 Backwards
        'Joy_16': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},   # T7 Forwards
        'Joy_17': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},   # T7 Backwards
        'Joy_18': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},  # E1 Button
        'Joy_19': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},  # E1 Anti-Clockwise
        'Joy_20': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},  # E1 Clockwise
        'Joy_21': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},  # E2 Button
        'Joy_22': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},  # E2 Anti-Clockwise
        'Joy_23': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},  # E2 Clockwise
        'Joy_24': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},   # B1 - Mode 2
        'Joy_25': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},   # B2 - Mode 2
        'Joy_26': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},   # B3 - Mode 2
        'Joy_27': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},   # B4 - Mode 2
        'Joy_28': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},   # B5 - Mode 2
        'Joy_29': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},   # B6 - Mode 2
        'Joy_30': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},  # B1 - Mode 3
        'Joy_31': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},  # B2 - Mode 3
        'Joy_32': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},  # B3 - Mode 3

    },

    'VPC-MongoosT-50CM3-Throttle-32B1': { # VPC MongoosT-50CM3 Throttle - 32 Button Split Mode - Device 1
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},        # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },

    'VPC-MongoosT-50CM3-Throttle-32B2': { # VPC MongoosT-50CM3 Throttle - 32 Button Split Mode - Device 2
        'Joy_1': {'Type': 'Digital', 'x': 2732, 'y': 1220, 'width': 180},  # B4 - Mode 3
        'Joy_2': {'Type': 'Digital', 'x': 2920, 'y': 1220, 'width': 180},  # B5 - Mode 3
        'Joy_3': {'Type': 'Digital', 'x': 3110, 'y': 1220, 'width': 180},  # B6 - Mode 3
        'Joy_4': {'Type': 'Digital', 'x': 2732, 'y': 1470, 'width': 180},  # B1 - Mode 4
        'Joy_5': {'Type': 'Digital', 'x': 2920, 'y': 1470, 'width': 180},  # B2 - Mode 4
        'Joy_6': {'Type': 'Digital', 'x': 3110, 'y': 1470, 'width': 180},  # B3 - Mode 4
        'Joy_7': {'Type': 'Digital', 'x': 2732, 'y': 1600, 'width': 180},  # B4 - Mode 4
        'Joy_8': {'Type': 'Digital', 'x': 2920, 'y': 1600, 'width': 180},  # B5 - Mode 4
        'Joy_9': {'Type': 'Digital', 'x': 3110, 'y': 1600, 'width': 180},  # B6 - Mode 4
        'Joy_10': {'Type': 'Digital', 'x': 2732, 'y': 1840, 'width': 180}, # B1 - Mode 5
        'Joy_11': {'Type': 'Digital', 'x': 2920, 'y': 1840, 'width': 180}, # B2 - Mode 5
        'Joy_12': {'Type': 'Digital', 'x': 3110, 'y': 1840, 'width': 180}, # B3 - Mode 5
        'Joy_13': {'Type': 'Digital', 'x': 2732, 'y': 1980, 'width': 180}, # B4 - Mode 5
        'Joy_14': {'Type': 'Digital', 'x': 2920, 'y': 1980, 'width': 180}, # B5 - Mode 5
        'Joy_15': {'Type': 'Digital', 'x': 3110, 'y': 1980, 'width': 180}, # B6 - Mode 5
    },
    'VPC-MongoosT-50CM3-Throttle-32B-NS0': { # VPC MongoosT-50CM3 Throttle - 32 Button Split Mode - No mode shift - Device 0
        'displayName': 'VPC MongoosT-50CM3 Throttle - 32 Button Split - No mode shift',
        'Joy_1': {'Type': 'Digital', 'x': 2066, 'y': 602, 'width': 450},        # Throttle Left Encoder Button
        'Joy_2': {'Type': 'Digital', 'x': 2066, 'y': 546, 'width': 450},        # Throttle Left Encoder Backwards
        'Joy_3': {'Type': 'Digital', 'x': 2066, 'y': 492, 'width': 450},        # Throttle Left Encoder Forwards
        'Joy_4': {'Type': 'Digital', 'x': 1440, 'y': 622, 'width': 450},        # Throttle Left Pinkie Button
        'Joy_5': {'Type': 'Digital', 'x': 1988, 'y': 348, 'width': 450},        # Throttle Left 2W Hat Button
        'Joy_6': {'Type': 'Digital', 'x': 1988, 'y': 292, 'width': 450},        # Throttle Left 2W Hat Down
        'Joy_7': {'Type': 'Digital', 'x': 1988, 'y': 238, 'width': 450},        # Throttle Left 2W Hat Up
        'Joy_8': {'Type': 'Digital', 'x': 804, 'y': 710, 'width': 450},         # Throttle Middle 4W HAT Button
        'Joy_9': {'Type': 'Digital', 'x': 804, 'y': 602, 'width': 450},         # Throttle Middle 4W HAT Down
        'Joy_10': {'Type': 'Digital', 'x': 804, 'y': 546, 'width': 450},        # Throttle Middle 4W HAT Right
        'Joy_11': {'Type': 'Digital', 'x': 804, 'y': 491, 'width': 450},        # Throttle Middle 4W HAT Up
        'Joy_12': {'Type': 'Digital', 'x': 804, 'y': 656, 'width': 450},        # Throttle Middle 4W HAT Left
        'Joy_13': {'Type': 'Digital', 'x': 170, 'y': 480, 'width': 474},        # Throttle Analog Stick Button
        'Joy_14': {'Type': 'Digital', 'x': 2238, 'y': 1016, 'width': 450},      # Throttle Right Encoder forwards
        'Joy_15': {'Type': 'Digital', 'x': 2238, 'y': 1070, 'width': 450},      # Throttle Right Encoder backwards
        'Joy_16': {'Type': 'Digital', 'x': 2238, 'y': 960, 'width': 450},       # Throttle Right 4W HAT 1 Button
        'Joy_17': {'Type': 'Digital', 'x': 2238, 'y': 795, 'width': 450},       # Throttle Right 4W HAT 1 Forwards
        'Joy_18': {'Type': 'Digital', 'x': 2238, 'y': 850, 'width': 450},       # Throttle Right 4W HAT 1 Down
        'Joy_19': {'Type': 'Digital', 'x': 2238, 'y': 906, 'width': 450},       # Throttle Right 4W HAT 1 Backwards
        'Joy_20': {'Type': 'Digital', 'x': 2238, 'y': 740, 'width': 450},       # Throttle Right 4W HAT 1 Up
        'Joy_21': {'Type': 'Digital', 'x': 2170, 'y': 1508, 'width': 425},      # Throttle Right Forward Button
        'Joy_22': {'Type': 'Digital', 'x': 1624, 'y': 974, 'width': 450},       # Throttle Right 4W HAT 2 Button
        'Joy_23': {'Type': 'Digital', 'x': 1624, 'y': 864, 'width': 450},       # Throttle Right 4W HAT 2 Down
        'Joy_24': {'Type': 'Digital', 'x': 1624, 'y': 918, 'width': 450},       # Throttle Right 4W HAT 2 Backwards
        'Joy_25': {'Type': 'Digital', 'x': 1624, 'y': 754, 'width': 450},       # Throttle Right 4W HAT 2 Up
        'Joy_26': {'Type': 'Digital', 'x': 1624, 'y': 808, 'width': 450},       # Throttle Right 4W HAT 2 Forwards
        'Joy_27': {'Type': 'Digital', 'x': 2210, 'y': 1432, 'width': 450},      # Throttle Right 4W HAT 3 Button
        'Joy_28': {'Type': 'Digital', 'x': 2210, 'y': 1322, 'width': 450},      # Throttle Right 4W HAT 3 Down
        'Joy_29': {'Type': 'Digital', 'x': 2210, 'y': 1378, 'width': 450},      # Throttle Right 4W HAT 3 Backwards
        'Joy_30': {'Type': 'Digital', 'x': 2210, 'y': 1212, 'width': 450},      # Throttle Right 4W HAT 3 Up
        'Joy_31': {'Type': 'Digital', 'x': 2210, 'y': 1268, 'width': 450},      # Throttle Right 4W HAT 3 Forwards
        'Joy_32': {'Type': 'Digital', 'x': 842, 'y': 814, 'width': 380},        # Throttle Right Back Button
        'Joy_XAxis': {'Type': 'Analogue', 'x': 170, 'y': 370, 'width': 474},    # Throttle Analog Stick
        'Joy_YAxis': {'Type': 'Analogue', 'x': 170, 'y': 425, 'width': 474},    # Throttle Analog Stick
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1435, 'y': 194, 'width': 394},   # Throttle Handle Slider
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 1850, 'width': 450},   # Throttle Left
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 1900, 'width': 450},   # Throttle Right
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2200, 'y': 1594, 'width': 350}, # Flaps
    },

    'VPC-MongoosT-50CM3-Throttle-32B-NS1': { # VPC MongoosT-50CM3 Throttle - 32 Button Split Mode - No mode shift - Device 1
        'Joy_1': {'Type': 'Digital', 'x': 842, 'y': 894, 'width': 380},     # Throttle Right Back Button Lower
        'Joy_2': {'Type': 'Digital', 'x': 2200, 'y': 1731, 'width': 325},   # T1
        'Joy_3': {'Type': 'Digital', 'x': 2200, 'y': 1914, 'width': 325},   # T2
        'Joy_4': {'Type': 'Digital', 'x': 720, 'y': 1046, 'width': 370},    # T3
        'Joy_5': {'Type': 'Digital', 'x': 720, 'y': 1238, 'width': 370},    # T4
        'Joy_6': {'Type': 'Digital', 'x': 2732, 'y': 340, 'width': 180},    # B1 - Mode 1
        'Joy_7': {'Type': 'Digital', 'x': 2920, 'y': 340, 'width': 180},    # B2 - Mode 1
        'Joy_8': {'Type': 'Digital', 'x': 3110, 'y': 340, 'width': 180},    # B3 - Mode 1
        'Joy_9': {'Type': 'Digital', 'x': 2732, 'y': 470, 'width': 180},    # B4 - Mode 1
        'Joy_10': {'Type': 'Digital', 'x': 2920, 'y': 470, 'width': 180},   # B5 - Mode 1
        'Joy_11': {'Type': 'Digital', 'x': 3110, 'y': 470, 'width': 180},   # B6 - Mode 1
        'Joy_12': {'Type': 'Digital', 'x': 672, 'y': 1464, 'width': 300},   # T5 Forwards
        'Joy_13': {'Type': 'Digital', 'x': 672, 'y': 1518, 'width': 300},   # T5 Backwards
        'Joy_14': {'Type': 'Digital', 'x': 672, 'y': 1660, 'width': 300},   # T6 Forwards
        'Joy_15': {'Type': 'Digital', 'x': 672, 'y': 1716, 'width': 300},   # T6 Backwards
        'Joy_16': {'Type': 'Digital', 'x': 672, 'y': 1856, 'width': 300},   # T7 Forwards
        'Joy_17': {'Type': 'Digital', 'x': 672, 'y': 1910, 'width': 300},   # T7 Backwards
        'Joy_18': {'Type': 'Digital', 'x': 1196, 'y': 2074, 'width': 325},  # E1 Button
        'Joy_19': {'Type': 'Digital', 'x': 1196, 'y': 1964, 'width': 325},  # E1 Anti-Clockwise
        'Joy_20': {'Type': 'Digital', 'x': 1196, 'y': 2020, 'width': 325},  # E1 Clockwise
        'Joy_21': {'Type': 'Digital', 'x': 1662, 'y': 2076, 'width': 325},  # E2 Button
        'Joy_22': {'Type': 'Digital', 'x': 1662, 'y': 1966, 'width': 325},  # E2 Anti-Clockwise
        'Joy_23': {'Type': 'Digital', 'x': 1662, 'y': 2022, 'width': 325},  # E2 Clockwise
        'Joy_24': {'Type': 'Digital', 'x': 2732, 'y': 710, 'width': 180},   # B1 - Mode 2
        'Joy_25': {'Type': 'Digital', 'x': 2920, 'y': 710, 'width': 180},   # B2 - Mode 2
        'Joy_26': {'Type': 'Digital', 'x': 3110, 'y': 710, 'width': 180},   # B3 - Mode 2
        'Joy_27': {'Type': 'Digital', 'x': 2732, 'y': 860, 'width': 180},   # B4 - Mode 2
        'Joy_28': {'Type': 'Digital', 'x': 2920, 'y': 860, 'width': 180},   # B5 - Mode 2
        'Joy_29': {'Type': 'Digital', 'x': 3110, 'y': 860, 'width': 180},   # B6 - Mode 2
#        'Joy_30': {'Type': 'Digital', 'x': 2732, 'y': 1090, 'width': 180},  # B1 - Mode 3
#        'Joy_31': {'Type': 'Digital', 'x': 2920, 'y': 1090, 'width': 180},  # B2 - Mode 3
#        'Joy_32': {'Type': 'Digital', 'x': 3110, 'y': 1090, 'width': 180},  # B3 - Mode 3

    },

    '3344825A': { # VPC control panel #2
        'displayName': 'VPC control panel #2',
        'Joy_1': {'Type': 'Digital', 'x': 2412 , 'y': 175, 'width': 390},       #B1
        'Joy_2': {'Type': 'Digital', 'x': 2532 , 'y': 435, 'width': 390},       #B2
        'Joy_3': {'Type': 'Digital', 'x': 2412 , 'y': 95, 'width': 390},        #B3
        'Joy_4': {'Type': 'Digital', 'x': 2532, 'y': 355, 'width': 390},        #B4
        'Joy_5': {'Type': 'Digital', 'x': 3102, 'y': 1415, 'width': 390},       #B5
        'Joy_6': {'Type': 'Digital', 'x': 3102, 'y': 1503, 'width': 390},       #B6
        'Joy_7': {'Type': 'Digital', 'x': 3102, 'y': 1585, 'width': 390},       #B7
        'Joy_8': {'Type': 'Digital', 'x': 3102, 'y': 1669, 'width': 390},       #B8
        'Joy_9': {'Type': 'Digital', 'x': 3102, 'y': 1749, 'width': 390},       #B9
        'Joy_10': {'Type': 'Digital', 'x': 3102, 'y': 1833, 'width': 390},      #B10
        'Joy_11': {'Type': 'Digital', 'x': 135, 'y': 855, 'width': 390},        #T1 - up
        'Joy_12': {'Type': 'Digital', 'x': 135, 'y': 915, 'width': 390},        #T1 - down
        'Joy_13': {'Type': 'Digital', 'x': 131, 'y': 997, 'width': 390},        #T2 - up
        'Joy_14': {'Type': 'Digital', 'x': 131, 'y': 1057, 'width': 390},       #T2 - down
        'Joy_15': {'Type': 'Digital', 'x': 131, 'y': 1141, 'width': 390},       #T3 - up
        'Joy_16': {'Type': 'Digital', 'x': 131, 'y': 1201, 'width': 390},       #T3 - down
        'Joy_17': {'Type': 'Digital', 'x': 131, 'y': 1355, 'width': 390},       #T4 - up
        'Joy_18': {'Type': 'Digital', 'x': 131, 'y': 1415, 'width': 390},       #T4 - down
        'Joy_19': {'Type': 'Digital', 'x': 131, 'y': 1525, 'width': 390},       #T5 - up
        'Joy_20': {'Type': 'Digital', 'x': 131, 'y': 1585, 'width': 390},       #T5 - down
        'Joy_21': {'Type': 'Digital', 'x': 131, 'y': 1685, 'width': 390},       #T6 - up
        'Joy_22': {'Type': 'Digital', 'x': 131, 'y': 1745, 'width': 390},       #T6 - down
        'Joy_23': {'Type': 'Digital', 'x': 3062, 'y': 385, 'width': 390},       #T7 - up
        'Joy_24': {'Type': 'Digital', 'x': 3062, 'y': 445, 'width': 390},       #T7 - down
        'Joy_25': {'Type': 'Digital', 'x': 3062, 'y': 523, 'width': 390},       #T8 - up
        'Joy_26': {'Type': 'Digital', 'x': 3062, 'y': 583, 'width': 390},       #T8 - down
        'Joy_27': {'Type': 'Digital', 'x': 3102, 'y': 1060, 'width': 390},      #T9 - left
        'Joy_28': {'Type': 'Digital', 'x': 3102, 'y': 1120, 'width': 390},      #T9 - right
        'Joy_29': {'Type': 'Digital', 'x': 3102, 'y': 1220, 'width': 390},      #T10 - left
        'Joy_30': {'Type': 'Digital', 'x': 3102, 'y': 1280, 'width': 390},      #T10 - right
        'Joy_31': {'Type': 'Digital', 'x': 645, 'y': 785, 'width': 390},        #E1 - Press
        'Joy_32': {'Type': 'Digital', 'x': 645, 'y': 725, 'width': 390},        #E1 - Clockwise
        'Joy_33': {'Type': 'Digital', 'x': 645, 'y': 845, 'width': 390},        #E1 - Anti-Clockwise
        'Joy_34': {'Type': 'Digital', 'x': 135, 'y': 641, 'width': 390},        #E2 - Press
        'Joy_35': {'Type': 'Digital', 'x': 135, 'y': 581, 'width': 390},        #E2 - Clockwise
        'Joy_36': {'Type': 'Digital', 'x': 135, 'y': 701, 'width': 390},        #E2 - Anti-Clockwise
        'Joy_37': {'Type': 'Digital', 'x': 648, 'y': 514, 'width': 390},        #E3 - Press
        'Joy_38': {'Type': 'Digital', 'x': 648, 'y': 454, 'width': 390},        #E3 - Clockwise
        'Joy_39': {'Type': 'Digital', 'x': 648, 'y': 574, 'width': 390},        #E3 - Anti-Clockwise
        'Joy_40': {'Type': 'Digital', 'x': 135, 'y': 276, 'width': 390},        #Gear Toggle
        'Joy_41': {'Type': 'Digital', 'x': 135, 'y': 336, 'width': 390},        #Gear Up
        'Joy_42': {'Type': 'Digital', 'x': 135, 'y': 396, 'width': 390},        #Gear Middle
        'Joy_43': {'Type': 'Digital', 'x': 135, 'y': 456, 'width': 390},        #Gear Down
    },
    '231D0127': { # VKB Kosmosima SCG Left
        'displayName': 'VKB Kosmosima SCG Left',
        'Joy_1': {'Type': 'Digital', 'x': 2052, 'y': 1798, 'width': 739, 'height': 68}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 2052, 'y': 1876, 'width': 739, 'height': 68}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 658, 'y': 1384, 'width': 724, 'height': 68}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 2100, 'y': 1088, 'width': 709, 'height': 68}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 2142, 'y': 2060, 'width': 740, 'height': 68}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 886, 'y': 388, 'width': 782, 'height': 68}, # A4 up
        'Joy_7': {'Type': 'Digital', 'x': 886, 'y': 626, 'width': 782, 'height': 68}, # A4 right
        'Joy_8': {'Type': 'Digital', 'x': 886, 'y': 468, 'width': 782, 'height': 68}, # A4 down
        'Joy_9': {'Type': 'Digital', 'x': 886, 'y': 546, 'width': 782, 'height': 68}, # A4 left
        'Joy_10': {'Type': 'Digital', 'x': 886, 'y': 702, 'width': 782, 'height': 68}, # A4 push
        'Joy_11': {'Type': 'Digital', 'x': 782, 'y': 882, 'width': 772, 'height': 68}, # A3 up
        'Joy_12': {'Type': 'Digital', 'x': 782, 'y': 1118, 'width': 772, 'height': 68}, # A3 right
        'Joy_13': {'Type': 'Digital', 'x': 782, 'y': 960, 'width': 772, 'height': 68}, # A3 down
        'Joy_14': {'Type': 'Digital', 'x': 782, 'y': 1040, 'width': 772, 'height': 68}, # A3 left
        'Joy_15': {'Type': 'Digital', 'x': 782, 'y': 1196, 'width': 772, 'height': 68}, # A3 push
        'Joy_24': {'Type': 'Digital', 'x': 748, 'y': 1568, 'width': 632, 'height': 68}, # C1 up
        'Joy_21': {'Type': 'Digital', 'x': 748, 'y': 1806, 'width': 632, 'height': 68}, # C1 right
        'Joy_22': {'Type': 'Digital', 'x': 748, 'y': 1648, 'width': 632, 'height': 68}, # C1 down
        'Joy_23': {'Type': 'Digital', 'x': 748, 'y': 1726, 'width': 632, 'height': 68}, # C1 left
        'Joy_25': {'Type': 'Digital', 'x': 748, 'y': 1882, 'width': 632, 'height': 68}, # C1 push
        'Joy_26': {'Type': 'Digital', 'x': 2028, 'y': 1540, 'width': 718, 'height': 68}, # B2 up
        'Joy_27': {'Type': 'Digital', 'x': 2028, 'y': 1616, 'width': 718, 'height': 68}, # B2 down
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1986, 'y': 386, 'width': 639, 'height': 68}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1986, 'y': 464, 'width': 639, 'height': 68}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 706, 'y': 2064, 'width': 671, 'height': 68}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2752, 'y': 542, 'width': 571, 'height': 68}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2752, 'y': 778, 'width': 571, 'height': 68}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2752, 'y': 620, 'width': 571, 'height': 68}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2752, 'y': 698, 'width': 571, 'height': 68}, # A1 POV Switch left
    },
    '231D0126': { # VKB Kosmosima SCG Right
        'displayName': 'VKB Kosmosima SCG Right',
        'Joy_1': {'Type': 'Digital', 'x': 1139, 'y': 1777, 'width': 739, 'height': 68}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 1139, 'y': 1852, 'width': 739, 'height': 68}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 2571, 'y': 1364, 'width': 724, 'height': 68}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 1223, 'y': 1091, 'width': 709, 'height': 68}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 1059, 'y': 2030, 'width': 740, 'height': 68}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 2427, 'y': 388, 'width': 782, 'height': 68}, # A4 up
        'Joy_7': {'Type': 'Digital', 'x': 2427, 'y': 623, 'width': 782, 'height': 68}, # A4 right
        'Joy_8': {'Type': 'Digital', 'x': 2427, 'y': 466, 'width': 782, 'height': 68}, # A4 down
        'Joy_9': {'Type': 'Digital', 'x': 2427, 'y': 544, 'width': 782, 'height': 68}, # A4 left
        'Joy_10': {'Type': 'Digital', 'x': 2427, 'y': 699, 'width': 782, 'height': 68}, # A4 push
        'Joy_11': {'Type': 'Digital', 'x': 2518, 'y': 876, 'width': 772, 'height': 68}, # A3 up
        'Joy_12': {'Type': 'Digital', 'x': 2518, 'y': 1107, 'width': 772, 'height': 68}, # A3 right
        'Joy_13': {'Type': 'Digital', 'x': 2518, 'y': 953, 'width': 772, 'height': 68}, # A3 down
        'Joy_14': {'Type': 'Digital', 'x': 2518, 'y': 1029, 'width': 772, 'height': 68}, # A3 left
        'Joy_15': {'Type': 'Digital', 'x': 2518, 'y': 1184, 'width': 772, 'height': 68}, # A3 push
        'Joy_21': {'Type': 'Digital', 'x': 2658, 'y': 1534, 'width': 632, 'height': 68}, # C1 up
        'Joy_22': {'Type': 'Digital', 'x': 2658, 'y': 1768, 'width': 632, 'height': 68}, # C1 right
        'Joy_23': {'Type': 'Digital', 'x': 2658, 'y': 1612, 'width': 632, 'height': 68}, # C1 down
        'Joy_24': {'Type': 'Digital', 'x': 2658, 'y': 1690, 'width': 632, 'height': 68}, # C1 left
        'Joy_25': {'Type': 'Digital', 'x': 2658, 'y': 1845, 'width': 632, 'height': 68}, # C1 push
        'Joy_26': {'Type': 'Digital', 'x': 1153, 'y': 1519, 'width': 718, 'height': 68}, # B2 up
        'Joy_27': {'Type': 'Digital', 'x': 1153, 'y': 1597, 'width': 718, 'height': 68}, # B2 down
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 732, 'y': 406, 'width': 639, 'height': 68}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 732, 'y': 484, 'width': 639, 'height': 68}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2622, 'y': 2025, 'width': 671, 'height': 68}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 1488, 'y': 561, 'width': 571, 'height': 68}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 1488, 'y': 795, 'width': 571, 'height': 68}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 1488, 'y': 638, 'width': 571, 'height': 68}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 1488, 'y': 717, 'width': 571, 'height': 68}, # A1 POV Switch left
    },
    '231D0200': { # VKB Gladiator NXT Premium Right
        'displayName': 'VKB Gladiator NXT Premium Right',
        'Joy_1': {'Type': 'Digital', 'x': 460, 'y': 1390, 'width': 842, 'height': 56}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 460, 'y': 1452, 'width': 842, 'height': 56}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 384, 'y': 1018, 'width': 918, 'height': 56}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 2636, 'y': 546, 'width': 918, 'height': 56}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 384, 'y': 2028, 'width': 918, 'height': 56}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 2636, 'y': 1136, 'width': 918, 'height': 56}, # A3 up
        'Joy_POV3Up': {'Type': 'Digital', 'x': 2636, 'y': 1136, 'width': 918, 'height': 56}, # A3 up (rebind)
        'Joy_7': {'Type': 'Digital', 'x': 2636, 'y': 1196, 'width': 918, 'height': 56}, # A3 right
        'Joy_POV3Right': {'Type': 'Digital', 'x': 2636, 'y': 1196, 'width': 918, 'height': 56}, # A3 right (rebind)
        'Joy_8': {'Type': 'Digital', 'x': 2636, 'y': 1258, 'width': 918, 'height': 56}, # A3 down
        'Joy_POV3Down': {'Type': 'Digital', 'x': 2636, 'y': 1258, 'width': 918, 'height': 56}, # A3 down (rebind)
        'Joy_9': {'Type': 'Digital', 'x': 2636, 'y': 1320, 'width': 918, 'height': 56}, # A3 left
        'Joy_POV3Left': {'Type': 'Digital', 'x': 2636, 'y': 1320, 'width': 918, 'height': 56}, # A3 left (rebind)
        'Joy_10': {'Type': 'Digital', 'x': 2636, 'y': 1382, 'width': 918, 'height': 56}, # A3 push
        'Joy_11': {'Type': 'Digital', 'x': 2636, 'y': 720, 'width': 918, 'height': 56}, # A4 up
        'Joy_POV2Up': {'Type': 'Digital', 'x': 2636, 'y': 720, 'width': 918, 'height': 56}, # A4 up (rebind)
        'Joy_12': {'Type': 'Digital', 'x': 2636, 'y': 786, 'width': 918, 'height': 56}, # A4 right
        'Joy_POV2Right': {'Type': 'Digital', 'x': 2636, 'y': 786, 'width': 918, 'height': 56}, # A4 right (rebind)
        'Joy_13': {'Type': 'Digital', 'x': 2636, 'y': 850, 'width': 918, 'height': 56}, # A4 down
        'Joy_POV2Down': {'Type': 'Digital', 'x': 2636, 'y': 850, 'width': 918, 'height': 56}, # A4 down (rebind)
        'Joy_14': {'Type': 'Digital', 'x': 2636, 'y': 916, 'width': 918, 'height': 56}, # A4 left
        'Joy_POV2Left': {'Type': 'Digital', 'x': 2636, 'y': 916, 'width': 918, 'height': 56}, # A4 left (rebind)
        'Joy_15': {'Type': 'Digital', 'x': 2636, 'y': 982, 'width': 918, 'height': 56}, # A4 push
        'Joy_16': {'Type': 'Digital', 'x': 384, 'y': 1624, 'width': 918, 'height': 56}, # C1 up
        'Joy_POV4Up': {'Type': 'Digital', 'x': 384, 'y': 1624, 'width': 918, 'height': 56}, # C1 up (rebind)
        'Joy_17': {'Type': 'Digital', 'x': 384, 'y': 1690, 'width': 918, 'height': 56}, # C1 right
        'Joy_POV4Right': {'Type': 'Digital', 'x': 384, 'y': 1690, 'width': 918, 'height': 56}, # C1 right (rebind)
        'Joy_18': {'Type': 'Digital', 'x': 384, 'y': 1754, 'width': 918, 'height': 56}, # C1 down
        'Joy_POV4Down': {'Type': 'Digital', 'x': 384, 'y': 1754, 'width': 918, 'height': 56}, # C1 down (rebind)
        'Joy_19': {'Type': 'Digital', 'x': 384, 'y': 1820, 'width': 918, 'height': 56}, # C1 left
        'Joy_POV4Left': {'Type': 'Digital', 'x': 384, 'y': 1820, 'width': 918, 'height': 56}, # C1 left (rebind)
        'Joy_20': {'Type': 'Digital', 'x': 384, 'y': 1886, 'width': 918, 'height': 56}, # C1 push
        'Joy_21': {'Type': 'Digital', 'x': 460, 'y': 1158, 'width': 842, 'height': 56}, # Rapid fire push
        'Joy_22': {'Type': 'Digital', 'x': 460, 'y': 1220, 'width': 842, 'height': 56}, # Rapid fire pull
        'Joy_23': {'Type': 'Digital', 'x': 2718, 'y': 1826, 'width': 842, 'height': 56}, # En1 up
        'Joy_24': {'Type': 'Digital', 'x': 2718, 'y': 1888, 'width': 842, 'height': 56}, # En1 down
        'Joy_25': {'Type': 'Digital', 'x': 2718, 'y': 1948, 'width': 842, 'height': 56}, # En2 up
        'Joy_26': {'Type': 'Digital', 'x': 2718, 'y': 2010, 'width': 842, 'height': 56}, # En2 down
        'Joy_27': {'Type': 'Digital', 'x': 2656, 'y': 1540, 'width': 902, 'height': 56}, # F1
        'Joy_28': {'Type': 'Digital', 'x': 2656, 'y': 1600, 'width': 902, 'height': 56}, # F2
        'Joy_29': {'Type': 'Digital', 'x': 2656, 'y': 1662, 'width': 902, 'height': 56}, # F3
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1598, 'y': 320, 'width': 758, 'height': 56}, # Joystick x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1598, 'y': 382, 'width': 758, 'height': 56}, # Joystick y
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 446, 'width': 758, 'height': 56}, # Throttle
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1598, 'y': 508, 'width': 758, 'height': 56}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1598, 'y': 572, 'width': 758, 'height': 56}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 634, 'width': 758, 'height': 56}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 384, 'y': 598, 'width': 918, 'height': 56}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 384, 'y': 664, 'width': 918, 'height': 56}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 384, 'y': 730, 'width': 918, 'height': 56}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 384, 'y': 796, 'width': 918, 'height': 56}, # A1 POV Switch left
    },
    '231D0201': { # VKB Gladiator NXT Premium Left
        'displayName': 'VKB Gladiator NXT Premium Left',
        'Joy_1': {'Type': 'Digital', 'x': 2692, 'y': 1390, 'width': 842, 'height': 56}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 2692, 'y': 1452, 'width': 842, 'height': 56}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 2616, 'y': 1018, 'width': 918, 'height': 56}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 374, 'y': 546, 'width': 918, 'height': 56}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 2616, 'y': 2028, 'width': 918, 'height': 56}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 374, 'y': 1136, 'width': 918, 'height': 56}, # A3 up
        'Joy_POV3Up': {'Type': 'Digital', 'x': 374, 'y': 1136, 'width': 918, 'height': 56}, # A3 up (rebind)
        'Joy_7': {'Type': 'Digital', 'x': 374, 'y': 1196, 'width': 918, 'height': 56}, # A3 right
        'Joy_POV3Right': {'Type': 'Digital', 'x': 374, 'y': 1196, 'width': 918, 'height': 56}, # A3 right (rebind)
        'Joy_8': {'Type': 'Digital', 'x': 374, 'y': 1258, 'width': 918, 'height': 56}, # A3 down
        'Joy_POV3Down': {'Type': 'Digital', 'x': 374, 'y': 1258, 'width': 918, 'height': 56}, # A3 down (rebind)
        'Joy_9': {'Type': 'Digital', 'x': 374, 'y': 1320, 'width': 918, 'height': 56}, # A3 left
        'Joy_POV3Left': {'Type': 'Digital', 'x': 374, 'y': 1320, 'width': 918, 'height': 56}, # A3 left (rebind)
        'Joy_10': {'Type': 'Digital', 'x': 374, 'y': 1382, 'width': 918, 'height': 56}, # A3 push
        'Joy_11': {'Type': 'Digital', 'x': 374, 'y': 720, 'width': 918, 'height': 56}, # A4 up
        'Joy_POV2Up': {'Type': 'Digital', 'x': 374, 'y': 720, 'width': 918, 'height': 56}, # A4 up (rebind)
        'Joy_12': {'Type': 'Digital', 'x': 374, 'y': 786, 'width': 918, 'height': 56}, # A4 right
        'Joy_POV2Right': {'Type': 'Digital', 'x': 374, 'y': 786, 'width': 918, 'height': 56}, # A4 right (rebind)
        'Joy_13': {'Type': 'Digital', 'x': 374, 'y': 850, 'width': 918, 'height': 56}, # A4 down
        'Joy_POV2Down': {'Type': 'Digital', 'x': 374, 'y': 850, 'width': 918, 'height': 56}, # A4 down (rebind)
        'Joy_14': {'Type': 'Digital', 'x': 374, 'y': 916, 'width': 918, 'height': 56}, # A4 left
        'Joy_POV2Left': {'Type': 'Digital', 'x': 374, 'y': 916, 'width': 918, 'height': 56}, # A4 left (rebind)
        'Joy_15': {'Type': 'Digital', 'x': 374, 'y': 982, 'width': 918, 'height': 56}, # A4 push
        'Joy_16': {'Type': 'Digital', 'x': 2616, 'y': 1624, 'width': 918, 'height': 56}, # C1 up
        'Joy_POV4Up': {'Type': 'Digital', 'x': 2616, 'y': 1624, 'width': 918, 'height': 56}, # C1 up (rebind)
        'Joy_17': {'Type': 'Digital', 'x': 2616, 'y': 1690, 'width': 918, 'height': 56}, # C1 right
        'Joy_POV4Right': {'Type': 'Digital', 'x': 2616, 'y': 1690, 'width': 918, 'height': 56}, # C1 right (rebind)
        'Joy_18': {'Type': 'Digital', 'x': 2616, 'y': 1754, 'width': 918, 'height': 56}, # C1 down
        'Joy_POV4Down': {'Type': 'Digital', 'x': 2616, 'y': 1754, 'width': 918, 'height': 56}, # C1 down (rebind)
        'Joy_19': {'Type': 'Digital', 'x': 2616, 'y': 1820, 'width': 918, 'height': 56}, # C1 left
        'Joy_POV4Left': {'Type': 'Digital', 'x': 2616, 'y': 1820, 'width': 918, 'height': 56}, # C1 left (rebind)
        'Joy_20': {'Type': 'Digital', 'x': 2616, 'y': 1886, 'width': 918, 'height': 56}, # C1 push
        'Joy_21': {'Type': 'Digital', 'x': 2692, 'y': 1158, 'width': 842, 'height': 56}, # Rapid fire push
        'Joy_22': {'Type': 'Digital', 'x': 2692, 'y': 1220, 'width': 842, 'height': 56}, # Rapid fire pull
        'Joy_23': {'Type': 'Digital', 'x': 456, 'y': 1826, 'width': 842, 'height': 56}, # En1 up
        'Joy_24': {'Type': 'Digital', 'x': 456, 'y': 1888, 'width': 842, 'height': 56}, # En1 down
        'Joy_25': {'Type': 'Digital', 'x': 456, 'y': 1948, 'width': 842, 'height': 56}, # En2 up
        'Joy_26': {'Type': 'Digital', 'x': 456, 'y': 2010, 'width': 842, 'height': 56}, # En2 down
        'Joy_27': {'Type': 'Digital', 'x': 394, 'y': 1540, 'width': 902, 'height': 56}, # F1
        'Joy_28': {'Type': 'Digital', 'x': 394, 'y': 1600, 'width': 902, 'height': 56}, # F2
        'Joy_29': {'Type': 'Digital', 'x': 394, 'y': 1662, 'width': 902, 'height': 56}, # F3
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1598, 'y': 320, 'width': 758, 'height': 56}, # Joystick x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1598, 'y': 382, 'width': 758, 'height': 56}, # Joystick y
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 446, 'width': 758, 'height': 56}, # Throttle
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1598, 'y': 508, 'width': 758, 'height': 56}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1598, 'y': 572, 'width': 758, 'height': 56}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 634, 'width': 758, 'height': 56}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2616, 'y': 598, 'width': 918, 'height': 56}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2616, 'y': 664, 'width': 918, 'height': 56}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2616, 'y': 730, 'width': 918, 'height': 56}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2616, 'y': 796, 'width': 918, 'height': 56}, # A1 POV Switch left
    },
    '231D3200': { # VKB Gladiator NXT Premium Right OTA
        'displayName': 'VKB Gladiator NXT Premium Right OTA',
        'Joy_1': {'Type': 'Digital', 'x': 460, 'y': 1390, 'width': 842, 'height': 56}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 460, 'y': 1452, 'width': 842, 'height': 56}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 384, 'y': 1018, 'width': 918, 'height': 56}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 2636, 'y': 546, 'width': 918, 'height': 56}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 384, 'y': 2028, 'width': 918, 'height': 56}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 2636, 'y': 1136, 'width': 918, 'height': 56}, # A3 up
        'Joy_POV3Up': {'Type': 'Digital', 'x': 2636, 'y': 1136, 'width': 918, 'height': 56}, # A3 up (rebind)
        'Joy_7': {'Type': 'Digital', 'x': 2636, 'y': 1196, 'width': 918, 'height': 56}, # A3 right
        'Joy_POV3Right': {'Type': 'Digital', 'x': 2636, 'y': 1196, 'width': 918, 'height': 56}, # A3 right (rebind)
        'Joy_8': {'Type': 'Digital', 'x': 2636, 'y': 1258, 'width': 918, 'height': 56}, # A3 down
        'Joy_POV3Down': {'Type': 'Digital', 'x': 2636, 'y': 1258, 'width': 918, 'height': 56}, # A3 down (rebind)
        'Joy_9': {'Type': 'Digital', 'x': 2636, 'y': 1320, 'width': 918, 'height': 56}, # A3 left
        'Joy_POV3Left': {'Type': 'Digital', 'x': 2636, 'y': 1320, 'width': 918, 'height': 56}, # A3 left (rebind)
        'Joy_10': {'Type': 'Digital', 'x': 2636, 'y': 1382, 'width': 918, 'height': 56}, # A3 push
        'Joy_11': {'Type': 'Digital', 'x': 2636, 'y': 720, 'width': 918, 'height': 56}, # A4 up
        'Joy_POV2Up': {'Type': 'Digital', 'x': 2636, 'y': 720, 'width': 918, 'height': 56}, # A4 up (rebind)
        'Joy_12': {'Type': 'Digital', 'x': 2636, 'y': 786, 'width': 918, 'height': 56}, # A4 right
        'Joy_POV2Right': {'Type': 'Digital', 'x': 2636, 'y': 786, 'width': 918, 'height': 56}, # A4 right (rebind)
        'Joy_13': {'Type': 'Digital', 'x': 2636, 'y': 850, 'width': 918, 'height': 56}, # A4 down
        'Joy_POV2Down': {'Type': 'Digital', 'x': 2636, 'y': 850, 'width': 918, 'height': 56}, # A4 down (rebind)
        'Joy_14': {'Type': 'Digital', 'x': 2636, 'y': 916, 'width': 918, 'height': 56}, # A4 left
        'Joy_POV2Left': {'Type': 'Digital', 'x': 2636, 'y': 916, 'width': 918, 'height': 56}, # A4 left (rebind)
        'Joy_15': {'Type': 'Digital', 'x': 2636, 'y': 982, 'width': 918, 'height': 56}, # A4 push
        'Joy_16': {'Type': 'Digital', 'x': 384, 'y': 1624, 'width': 918, 'height': 56}, # C1 up
        'Joy_POV4Up': {'Type': 'Digital', 'x': 384, 'y': 1624, 'width': 918, 'height': 56}, # C1 up (rebind)
        'Joy_17': {'Type': 'Digital', 'x': 384, 'y': 1690, 'width': 918, 'height': 56}, # C1 right
        'Joy_POV4Right': {'Type': 'Digital', 'x': 384, 'y': 1690, 'width': 918, 'height': 56}, # C1 right (rebind)
        'Joy_18': {'Type': 'Digital', 'x': 384, 'y': 1754, 'width': 918, 'height': 56}, # C1 down
        'Joy_POV4Down': {'Type': 'Digital', 'x': 384, 'y': 1754, 'width': 918, 'height': 56}, # C1 down (rebind)
        'Joy_19': {'Type': 'Digital', 'x': 384, 'y': 1820, 'width': 918, 'height': 56}, # C1 left
        'Joy_POV4Left': {'Type': 'Digital', 'x': 384, 'y': 1820, 'width': 918, 'height': 56}, # C1 left (rebind)
        'Joy_20': {'Type': 'Digital', 'x': 384, 'y': 1886, 'width': 918, 'height': 56}, # C1 push
        'Joy_21': {'Type': 'Digital', 'x': 460, 'y': 1158, 'width': 842, 'height': 56}, # Rapid fire push
        'Joy_22': {'Type': 'Digital', 'x': 460, 'y': 1220, 'width': 842, 'height': 56}, # Rapid fire pull
        'Joy_23': {'Type': 'Digital', 'x': 2718, 'y': 1826, 'width': 842, 'height': 56}, # En1 up
        'Joy_24': {'Type': 'Digital', 'x': 2718, 'y': 1888, 'width': 842, 'height': 56}, # En1 down
        'Joy_25': {'Type': 'Digital', 'x': 2718, 'y': 1948, 'width': 842, 'height': 56}, # En2 up
        'Joy_26': {'Type': 'Digital', 'x': 2718, 'y': 2010, 'width': 842, 'height': 56}, # En2 down
        'Joy_27': {'Type': 'Digital', 'x': 2656, 'y': 1540, 'width': 902, 'height': 56}, # F1
        'Joy_28': {'Type': 'Digital', 'x': 2656, 'y': 1600, 'width': 902, 'height': 56}, # F2
        'Joy_29': {'Type': 'Digital', 'x': 2656, 'y': 1662, 'width': 902, 'height': 56}, # F3
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1598, 'y': 320, 'width': 758, 'height': 56}, # Joystick x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1598, 'y': 382, 'width': 758, 'height': 56}, # Joystick y
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 446, 'width': 758, 'height': 56}, # Throttle
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1598, 'y': 508, 'width': 758, 'height': 56}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1598, 'y': 572, 'width': 758, 'height': 56}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 634, 'width': 758, 'height': 56}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 384, 'y': 598, 'width': 918, 'height': 56}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 384, 'y': 664, 'width': 918, 'height': 56}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 384, 'y': 730, 'width': 918, 'height': 56}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 384, 'y': 796, 'width': 918, 'height': 56}, # A1 POV Switch left
    },
    '231D3201': { # VKB Gladiator NXT Premium Left OTA
        'displayName': 'VKB Gladiator NXT Premium Left OTA',
        'Joy_1': {'Type': 'Digital', 'x': 2692, 'y': 1390, 'width': 842, 'height': 56}, # Fire first stage
        'Joy_2': {'Type': 'Digital', 'x': 2692, 'y': 1452, 'width': 842, 'height': 56}, # Fire second stage
        'Joy_3': {'Type': 'Digital', 'x': 2616, 'y': 1018, 'width': 918, 'height': 56}, # A2
        'Joy_4': {'Type': 'Digital', 'x': 374, 'y': 546, 'width': 918, 'height': 56}, # B1
        'Joy_5': {'Type': 'Digital', 'x': 2616, 'y': 2028, 'width': 918, 'height': 56}, # D1
        'Joy_6': {'Type': 'Digital', 'x': 374, 'y': 1136, 'width': 918, 'height': 56}, # A3 up
        'Joy_POV3Up': {'Type': 'Digital', 'x': 374, 'y': 1136, 'width': 918, 'height': 56}, # A3 up (rebind)
        'Joy_7': {'Type': 'Digital', 'x': 374, 'y': 1196, 'width': 918, 'height': 56}, # A3 right
        'Joy_POV3Right': {'Type': 'Digital', 'x': 374, 'y': 1196, 'width': 918, 'height': 56}, # A3 right (rebind)
        'Joy_8': {'Type': 'Digital', 'x': 374, 'y': 1258, 'width': 918, 'height': 56}, # A3 down
        'Joy_POV3Down': {'Type': 'Digital', 'x': 374, 'y': 1258, 'width': 918, 'height': 56}, # A3 down (rebind)
        'Joy_9': {'Type': 'Digital', 'x': 374, 'y': 1320, 'width': 918, 'height': 56}, # A3 left
        'Joy_POV3Left': {'Type': 'Digital', 'x': 374, 'y': 1320, 'width': 918, 'height': 56}, # A3 left (rebind)
        'Joy_10': {'Type': 'Digital', 'x': 374, 'y': 1382, 'width': 918, 'height': 56}, # A3 push
        'Joy_11': {'Type': 'Digital', 'x': 374, 'y': 720, 'width': 918, 'height': 56}, # A4 up
        'Joy_POV2Up': {'Type': 'Digital', 'x': 374, 'y': 720, 'width': 918, 'height': 56}, # A4 up (rebind)
        'Joy_12': {'Type': 'Digital', 'x': 374, 'y': 786, 'width': 918, 'height': 56}, # A4 right
        'Joy_POV2Right': {'Type': 'Digital', 'x': 374, 'y': 786, 'width': 918, 'height': 56}, # A4 right (rebind)
        'Joy_13': {'Type': 'Digital', 'x': 374, 'y': 850, 'width': 918, 'height': 56}, # A4 down
        'Joy_POV2Down': {'Type': 'Digital', 'x': 374, 'y': 850, 'width': 918, 'height': 56}, # A4 down (rebind)
        'Joy_14': {'Type': 'Digital', 'x': 374, 'y': 916, 'width': 918, 'height': 56}, # A4 left
        'Joy_POV2Left': {'Type': 'Digital', 'x': 374, 'y': 916, 'width': 918, 'height': 56}, # A4 left (rebind)
        'Joy_15': {'Type': 'Digital', 'x': 374, 'y': 982, 'width': 918, 'height': 56}, # A4 push
        'Joy_16': {'Type': 'Digital', 'x': 2616, 'y': 1624, 'width': 918, 'height': 56}, # C1 up
        'Joy_POV4Up': {'Type': 'Digital', 'x': 2616, 'y': 1624, 'width': 918, 'height': 56}, # C1 up (rebind)
        'Joy_17': {'Type': 'Digital', 'x': 2616, 'y': 1690, 'width': 918, 'height': 56}, # C1 right
        'Joy_POV4Right': {'Type': 'Digital', 'x': 2616, 'y': 1690, 'width': 918, 'height': 56}, # C1 right (rebind)
        'Joy_18': {'Type': 'Digital', 'x': 2616, 'y': 1754, 'width': 918, 'height': 56}, # C1 down
        'Joy_POV4Down': {'Type': 'Digital', 'x': 2616, 'y': 1754, 'width': 918, 'height': 56}, # C1 down (rebind)
        'Joy_19': {'Type': 'Digital', 'x': 2616, 'y': 1820, 'width': 918, 'height': 56}, # C1 left
        'Joy_POV4Left': {'Type': 'Digital', 'x': 2616, 'y': 1820, 'width': 918, 'height': 56}, # C1 left (rebind)
        'Joy_20': {'Type': 'Digital', 'x': 2616, 'y': 1886, 'width': 918, 'height': 56}, # C1 push
        'Joy_21': {'Type': 'Digital', 'x': 2692, 'y': 1158, 'width': 842, 'height': 56}, # Rapid fire push
        'Joy_22': {'Type': 'Digital', 'x': 2692, 'y': 1220, 'width': 842, 'height': 56}, # Rapid fire pull
        'Joy_23': {'Type': 'Digital', 'x': 456, 'y': 1826, 'width': 842, 'height': 56}, # En1 up
        'Joy_24': {'Type': 'Digital', 'x': 456, 'y': 1888, 'width': 842, 'height': 56}, # En1 down
        'Joy_25': {'Type': 'Digital', 'x': 456, 'y': 1948, 'width': 842, 'height': 56}, # En2 up
        'Joy_26': {'Type': 'Digital', 'x': 456, 'y': 2010, 'width': 842, 'height': 56}, # En2 down
        'Joy_27': {'Type': 'Digital', 'x': 394, 'y': 1540, 'width': 902, 'height': 56}, # F1
        'Joy_28': {'Type': 'Digital', 'x': 394, 'y': 1600, 'width': 902, 'height': 56}, # F2
        'Joy_29': {'Type': 'Digital', 'x': 394, 'y': 1662, 'width': 902, 'height': 56}, # F3
        'Joy_XAxis': {'Type': 'Analogue', 'x': 1598, 'y': 320, 'width': 758, 'height': 56}, # Joystick x
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1598, 'y': 382, 'width': 758, 'height': 56}, # Joystick y
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 446, 'width': 758, 'height': 56}, # Throttle
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 1598, 'y': 508, 'width': 758, 'height': 56}, # A1 Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 1598, 'y': 572, 'width': 758, 'height': 56}, # A1 Ministick R y
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 1598, 'y': 634, 'width': 758, 'height': 56}, # Twist R z
        'Joy_POV1Up': {'Type': 'Digital', 'x': 2616, 'y': 598, 'width': 918, 'height': 56}, # A1 POV Switch up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 2616, 'y': 664, 'width': 918, 'height': 56}, # A1 POV Switch right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 2616, 'y': 730, 'width': 918, 'height': 56}, # A1 POV Switch down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 2616, 'y': 796, 'width': 918, 'height': 56}, # A1 POV Switch left
    },
    '231D012D::0': { # VKB STECS VC 1
        'displayName': 'VKB STECS VC 1',
        'Joy_1': {'Type': 'Digital', 'x': 50, 'y': 388, 'width': 842, 'height': 56}, # White Button
        'Joy_2': {'Type': 'Digital', 'x': 50, 'y': 466, 'width': 842, 'height': 56}, # Red Button
        'Joy_3': {'Type': 'Digital', 'x': 50, 'y': 544, 'width': 918, 'height': 56}, # White Dial 1
        'Joy_4': {'Type': 'Digital', 'x': 50, 'y': 622, 'width': 918, 'height': 56}, # White Dial 2
        'Joy_5': {'Type': 'Digital', 'x': 50, 'y': 700, 'width': 918, 'height': 56}, # White Dial 3
        'Joy_6': {'Type': 'Digital', 'x': 50, 'y': 788, 'width': 918, 'height': 56}, # White Dial 4
        'Joy_7': {'Type': 'Digital', 'x': 50, 'y': 856, 'width': 918, 'height': 56}, # White Dial 5
        'Joy_8': {'Type': 'Digital', 'x': 50, 'y': 934, 'width': 918, 'height': 56}, # TRIG L
        'Joy_9': {'Type': 'Digital', 'x': 50, 'y': 1012, 'width': 918, 'height': 56}, # Left Index Trigger
        'Joy_10': {'Type': 'Digital', 'x': 50, 'y': 1090, 'width': 918, 'height': 56}, # Weapon Select
        'Joy_11': {'Type': 'Digital', 'x': 50, 'y': 1168, 'width': 918, 'height': 56}, # RST
        'Joy_12': {'Type': 'Digital', 'x': 50, 'y': 1246, 'width': 918, 'height': 56}, # Left Dial Up
        'Joy_13': {'Type': 'Digital', 'x': 50, 'y': 1324, 'width': 918, 'height': 56}, # Left Dial Down
        'Joy_14': {'Type': 'Digital', 'x': 50, 'y': 1402, 'width': 918, 'height': 56}, # Left Side Dial Forward
        'Joy_15': {'Type': 'Digital', 'x': 50, 'y': 1480, 'width': 918, 'height': 56}, # Left Side Dial Back
        'Joy_16': {'Type': 'Digital', 'x': 50, 'y': 1558, 'width': 918, 'height': 56}, # TRIG R
        'Joy_17': {'Type': 'Digital', 'x': 50, 'y': 1636, 'width': 918, 'height': 56}, # Right Index Trigger
        'Joy_18': {'Type': 'Digital', 'x': 50, 'y': 1714, 'width': 918, 'height': 56}, # ENT
        'Joy_19': {'Type': 'Digital', 'x': 50, 'y': 1792, 'width': 918, 'height': 56}, # Right Ministick Push
        'Joy_20': {'Type': 'Digital', 'x': 50, 'y': 1870, 'width': 918, 'height': 56}, # BRK Push
        'Joy_21': {'Type': 'Digital', 'x': 50, 'y': 1948, 'width': 842, 'height': 56}, # MB1 Hat Push
        'Joy_22': {'Type': 'Digital', 'x': 50, 'y': 2026, 'width': 842, 'height': 56}, # Radio Click
        'Joy_23': {'Type': 'Digital', 'x': 50, 'y': 2104, 'width': 842, 'height': 56}, # MB2
        'Joy_24': {'Type': 'Digital', 'x': 50, 'y': 2182, 'width': 842, 'height': 56}, # OP EXEC
        'Joy_25': {'Type': 'Digital', 'x': 50, 'y': 2260, 'width': 842, 'height': 56}, # BRK Up
        'Joy_26': {'Type': 'Digital', 'x': 50, 'y': 2338, 'width': 842, 'height': 56}, # BRK Down
        'Joy_27': {'Type': 'Digital', 'x': 50, 'y': 2416, 'width': 902, 'height': 56}, # BRK Right
        'Joy_28': {'Type': 'Digital', 'x': 50, 'y': 2494, 'width': 902, 'height': 56}, # BRK Left
        'Joy_29': {'Type': 'Digital', 'x': 50, 'y': 2572, 'width': 902, 'height': 56}, # MB1 Hat Left
        'Joy_30': {'Type': 'Digital', 'x': 50, 'y': 2650, 'width': 902, 'height': 56}, # MB1 Hat Right
        'Joy_31': {'Type': 'Digital', 'x': 50, 'y': 2728, 'width': 902, 'height': 56}, # MB1 Hat Down
        'Joy_32': {'Type': 'Digital', 'x': 50, 'y': 2806, 'width': 902, 'height': 56}, # MB1 Hat Up
        'Joy_XAxis': {'Type': 'Analogue', 'x': 50, 'y': 2884, 'width': 758, 'height': 56}, # Right Throttle
        'Joy_YAxis': {'Type': 'Analogue', 'x': 50, 'y': 2962, 'width': 758, 'height': 56}, # Left Throttle
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 50, 'y': 3040, 'width': 758, 'height': 56}, # Right Dial
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 50, 'y': 3118, 'width': 758, 'height': 56}, # Right Ministick R x
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 50, 'y': 3196, 'width': 758, 'height': 56}, # Right Ministick R y
    },
    '231D012D::1': { # VKB STECS VC 2
        'displayName': 'VKB STECS VC 2',
        'Joy_1': {'Type': 'Digital', 'x': 50, 'y': 388, 'width': 842, 'height': 56}, # Radio Down
        'Joy_2': {'Type': 'Digital', 'x': 50, 'y': 466, 'width': 842, 'height': 56}, # Radio Up
        'Joy_3': {'Type': 'Digital', 'x': 50, 'y': 544, 'width': 918, 'height': 56}, # A1
        'Joy_4': {'Type': 'Digital', 'x': 50, 'y': 622, 'width': 918, 'height': 56}, # A2
        'Joy_5': {'Type': 'Digital', 'x': 50, 'y': 700, 'width': 918, 'height': 56}, # C1
        'Joy_6': {'Type': 'Digital', 'x': 50, 'y': 778, 'width': 918, 'height': 56}, # B1
        'Joy_7': {'Type': 'Digital', 'x': 50, 'y': 856, 'width': 918, 'height': 56}, # B2
        'Joy_8': {'Type': 'Digital', 'x': 50, 'y': 934, 'width': 918, 'height': 56}, # B3
        'Joy_9': {'Type': 'Digital', 'x': 50, 'y': 1012, 'width': 918, 'height': 56}, # B4
        'Joy_10': {'Type': 'Digital', 'x': 50, 'y': 1090, 'width': 918, 'height': 56}, # B5
        'Joy_11': {'Type': 'Digital', 'x': 50, 'y': 1168, 'width': 918, 'height': 56}, # SW1 Up
        'Joy_12': {'Type': 'Digital', 'x': 50, 'y': 1246, 'width': 918, 'height': 56}, # SW1 Button
        'Joy_13': {'Type': 'Digital', 'x': 50, 'y': 1324, 'width': 918, 'height': 56}, # SW1 Down
        'Joy_14': {'Type': 'Digital', 'x': 50, 'y': 1402, 'width': 918, 'height': 56}, # SW2 Up
        'Joy_15': {'Type': 'Digital', 'x': 50, 'y': 1480, 'width': 918, 'height': 56}, # SW2 Button
        'Joy_16': {'Type': 'Digital', 'x': 50, 'y': 1558, 'width': 918, 'height': 56}, # SW2 Down
        'Joy_17': {'Type': 'Digital', 'x': 50, 'y': 1636, 'width': 918, 'height': 56}, # TGL UP
        'Joy_18': {'Type': 'Digital', 'x': 50, 'y': 1714, 'width': 918, 'height': 56}, # TGL DOWN
        'Joy_19': {'Type': 'Digital', 'x': 50, 'y': 1792, 'width': 918, 'height': 56}, # EN1 Left
        'Joy_20': {'Type': 'Digital', 'x': 50, 'y': 1870, 'width': 918, 'height': 56}, # EN1 Right
        'Joy_21': {'Type': 'Digital', 'x': 50, 'y': 1948, 'width': 842, 'height': 56}, # EN2 Left
        'Joy_22': {'Type': 'Digital', 'x': 50, 'y': 2026, 'width': 842, 'height': 56}, # EN2 Right
        'Joy_23': {'Type': 'Digital', 'x': 50, 'y': 2104, 'width': 842, 'height': 56}, # EN1 Click
        'Joy_24': {'Type': 'Digital', 'x': 50, 'y': 2182, 'width': 842, 'height': 56}, # EN2 Click
        'Joy_25': {'Type': 'Digital', 'x': 50, 'y': 2260, 'width': 842, 'height': 56}, # 3-Position Switch Up
        'Joy_26': {'Type': 'Digital', 'x': 50, 'y': 2338, 'width': 842, 'height': 56}, # 3-Position Switch Down
    },
    '231D2214': { # VKB GNX WWII Throttle 
        'displayName': 'VKB GNX WWII Throttle',
        'Joy_1': {'Type': 'Digital', 'x': 3152, 'y': 932, 'width': 548, 'height': 44}, # A1
        'Joy_2': {'Type': 'Digital', 'x': 3152, 'y': 986, 'width': 548, 'height': 44}, # A2
        'Joy_3': {'Type': 'Digital', 'x': 2292, 'y': 638, 'width': 548, 'height': 44}, # B1
        'Joy_4': {'Type': 'Digital', 'x': 2292, 'y': 692, 'width': 548, 'height': 44}, # B2
        'Joy_5': {'Type': 'Digital', 'x': 2292, 'y': 742, 'width': 548, 'height': 44}, # B3
        'Joy_6': {'Type': 'Digital', 'x': 3152, 'y': 1134, 'width': 548, 'height': 44}, # White Right Rocker Up
        'Joy_7': {'Type': 'Digital', 'x': 3152, 'y': 1186, 'width': 548, 'height': 44}, # White Right Rocker Middle
        'Joy_8': {'Type': 'Digital', 'x': 3152, 'y': 1240, 'width': 548, 'height': 44}, # White Right Rocker Down
        'Joy_9': {'Type': 'Digital', 'x': 3152, 'y': 1388, 'width': 548, 'height': 44}, # White Left Rocker Up
        'Joy_10': {'Type': 'Digital', 'x': 3152, 'y': 1442, 'width': 548, 'height': 44}, # White Left Rocker Middle
        'Joy_11': {'Type': 'Digital', 'x': 3152, 'y': 1496, 'width': 548, 'height': 44}, # White Left Rocker Down
        'Joy_12': {'Type': 'Digital', 'x': 3152, 'y': 778, 'width': 548, 'height': 44}, # Red Start
        'Joy_13': {'Type': 'Digital', 'x': 3152, 'y': 630, 'width': 548, 'height': 44}, # Mode 1
        'Joy_14': {'Type': 'Digital', 'x': 3152, 'y': 576, 'width': 548, 'height': 44}, # Mode 2
        'Joy_15': {'Type': 'Digital', 'x': 3152, 'y': 522, 'width': 548, 'height': 44}, # Mode 3
        'Joy_16': {'Type': 'Digital', 'x': 3152, 'y': 470, 'width': 548, 'height': 44}, # Mode 4
        'Joy_17': {'Type': 'Digital', 'x': 2292, 'y': 472, 'width': 548, 'height': 44}, # C1
        'Joy_18': {'Type': 'Digital', 'x': 1350, 'y': 878, 'width': 548, 'height': 44}, # Flaps 1
        'Joy_19': {'Type': 'Digital', 'x': 1350, 'y': 824, 'width': 548, 'height': 44}, # Flaps 2
        'Joy_20': {'Type': 'Digital', 'x': 1350, 'y': 772, 'width': 548, 'height': 44}, # Flaps 3
        'Joy_21': {'Type': 'Digital', 'x': 1350, 'y': 720, 'width': 548, 'height': 44}, # Flaps 4
        'Joy_22': {'Type': 'Digital', 'x': 1350, 'y': 572, 'width': 548, 'height': 44}, # Landing Gear Down
        'Joy_23': {'Type': 'Digital', 'x': 1350, 'y': 520, 'width': 548, 'height': 44}, # Landing Gear Middle
        'Joy_24': {'Type': 'Digital', 'x': 1350, 'y': 468, 'width': 548, 'height': 44}, # Landing Gear Up
        'Joy_25': {'Type': 'Digital', 'x': 412, 'y': 1336, 'width': 548, 'height': 44}, # A1 (THQ)
        'Joy_26': {'Type': 'Digital', 'x': 412, 'y': 1388, 'width': 548, 'height': 44}, # A2
        'Joy_27': {'Type': 'Digital', 'x': 412, 'y': 1440, 'width': 548, 'height': 44}, # A3
        'Joy_28': {'Type': 'Digital', 'x': 412, 'y': 1492, 'width': 548, 'height': 44}, # A4
        'Joy_29': {'Type': 'Digital', 'x': 412, 'y': 1636, 'width': 548, 'height': 44}, # B1
        'Joy_30': {'Type': 'Digital', 'x': 412, 'y': 1828, 'width': 548, 'height': 44}, # C1
        'Joy_31': {'Type': 'Digital', 'x': 412, 'y': 1880, 'width': 548, 'height': 44}, # C2
        'Joy_32': {'Type': 'Digital', 'x': 412, 'y': 1686, 'width': 548, 'height': 44}, # B2
        'Joy_33': {'Type': 'Digital', 'x': 412, 'y': 472, 'width': 548, 'height': 44}, # <
        'Joy_34': {'Type': 'Digital', 'x': 412, 'y': 522, 'width': 548, 'height': 44}, # >
        'Joy_35': {'Type': 'Digital', 'x': 412, 'y': 712, 'width': 548, 'height': 44}, # V
        'Joy_36': {'Type': 'Digital', 'x': 412, 'y': 662, 'width': 548, 'height': 44}, # ^
        'Joy_37': {'Type': 'Digital', 'x': 412, 'y': 856, 'width': 548, 'height': 44}, # Black
        'Joy_38': {'Type': 'Digital', 'x': 412, 'y': 1002, 'width': 548, 'height': 44}, # Red

        'Joy_XAxis': {'Type': 'Analogue', 'x': 1328, 'y': 1942, 'width': 548, 'height': 44},
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 1328, 'y': 1994, 'width': 548, 'height': 44}, # Not used for THQ-WW2
        'Joy_YAxis': {'Type': 'Analogue', 'x': 1328, 'y': 2046, 'width': 548, 'height': 44},

        'Joy_RXAxis': {'Type': 'Analogue', 'x': 2304, 'y': 1944, 'width': 548, 'height': 44},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2304, 'y': 1996, 'width': 548, 'height': 44},
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 2304, 'y': 2048, 'width': 548, 'height': 44},
    },
    
    '4098BE62': { # Winwing Orion Throttle Base II + F18 Handle
        'displayName': 'Winwing Orion Throttle Base II + F18 Handle',
        # Handle
        'Joy_1': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_2': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_3': {'Type': 'Digital', 'x': 164, 'y': 540, 'width': 400, 'height': 60},
        'Joy_4': {'Type': 'Digital', 'x': 164, 'y': 600, 'width': 400, 'height': 60},
        'Joy_5': {'Type': 'Digital', 'x': 164, 'y': 660, 'width': 400, 'height': 60},
        'Joy_6': {'Type': 'Digital', 'x': 764, 'y': 450, 'width': 400, 'height': 60},
        'Joy_7': {'Type': 'Digital', 'x': 764, 'y': 370, 'width': 400, 'height': 60},
        'Joy_8': {'Type': 'Digital', 'x': 2824, 'y': 92, 'width': 400, 'height': 60},
        'Joy_9': {'Type': 'Digital', 'x': 2824, 'y': 152, 'width': 400, 'height': 60},
        'Joy_10': {'Type': 'Digital', 'x': 2824, 'y': 212, 'width': 400, 'height': 60},
        'Joy_11': {'Type': 'Digital', 'x': 2824, 'y': 272, 'width': 400, 'height': 60},
        'Joy_12': {'Type': 'Digital', 'x': 2824, 'y': 332, 'width': 400, 'height': 60},
        'Joy_13': {'Type': 'Digital', 'x': 164, 'y': 796, 'width': 400, 'height': 60},
        'Joy_14': {'Type': 'Digital', 'x': 164, 'y': 856, 'width': 400, 'height': 60},
        'Joy_15': {'Type': 'Digital', 'x': 164, 'y': 916, 'width': 400, 'height': 60},
        'Joy_16': {'Type': 'Digital', 'x': 164, 'y': 976, 'width': 400, 'height': 60},
        'Joy_17': {'Type': 'Digital', 'x': 164, 'y': 1036, 'width': 400, 'height': 60},
        'Joy_18': {'Type': 'Digital', 'x': 3324, 'y': 212, 'width': 400, 'height': 60},
        'Joy_19': {'Type': 'Digital', 'x': 3324, 'y': 272, 'width': 400, 'height': 60},
        'Joy_20': {'Type': 'Digital', 'x': 3324, 'y': 332, 'width': 400, 'height': 60},
        'Joy_21': {'Type': 'Digital', 'x': 764, 'y': 938, 'width': 400, 'height': 60},
        'Joy_22': {'Type': 'Digital', 'x': 2298, 'y': 154, 'width': 400, 'height': 60},
        'Joy_23': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_24': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_25': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_26': {'Type': 'Digital', 'x': 2298, 'y': 214, 'width': 400, 'height': 60},
        'Joy_27': {'Type': 'Digital', 'x': 2298, 'y': 274, 'width': 400, 'height': 60},
        'Joy_28': {'Type': 'Digital', 'x': 2298, 'y': 334, 'width': 400, 'height': 60},
        'Joy_29': {'Type': 'Digital', 'x': 2298, 'y': 394, 'width': 400, 'height': 60},
        
        'Joy_ZAxis': {'Type': 'Analogue', 'x': 764, 'y': 293, 'width': 880, 'height': 60},
        # End of handle
        # Base
        'Joy_30': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_31': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_32': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_33': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_34': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_35': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_36': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_37': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_38': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_39': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_40': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_41': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_42': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_43': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_44': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_45': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_46': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_47': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_48': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_49': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_50': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_51': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_52': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_53': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_54': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_55': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_56': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_57': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_58': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_59': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_60': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_61': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_62': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_63': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_64': {'Type': 'Digital', 'x': 3320, 'y': 2020, 'width': 400, 'height': 60},     # Not sure
        'Joy_65': {'Type': 'Digital', 'x': 3324, 'y': 594, 'width': 400, 'height': 60},
        'Joy_66': {'Type': 'Digital', 'x': 3324, 'y': 664, 'width': 400, 'height': 60},
        'Joy_67': {'Type': 'Digital', 'x': 3324, 'y': 752, 'width': 400, 'height': 60},
        'Joy_68': {'Type': 'Digital', 'x': 3324, 'y': 812, 'width': 400, 'height': 60},
        'Joy_69': {'Type': 'Digital', 'x': 2684, 'y': 654, 'width': 400, 'height': 60},
        'Joy_70': {'Type': 'Digital', 'x': 2684, 'y': 714, 'width': 400, 'height': 60},
        'Joy_71': {'Type': 'Digital', 'x': 2684, 'y': 774, 'width': 400, 'height': 60},
        'Joy_72': {'Type': 'Digital', 'x': 2684, 'y': 834, 'width': 400, 'height': 60},
        'Joy_73': {'Type': 'Digital', 'x': 3324, 'y': 908, 'width': 400, 'height': 60},
        'Joy_74': {'Type': 'Digital', 'x': 3324, 'y': 964, 'width': 400, 'height': 60},
        'Joy_75': {'Type': 'Digital', 'x': 3324, 'y': 1068, 'width': 400, 'height': 60},
        'Joy_76': {'Type': 'Digital', 'x': 3324, 'y': 1128, 'width': 400, 'height': 60},
        'Joy_77': {'Type': 'Digital', 'x': 3324, 'y': 1236, 'width': 400, 'height': 60},
        'Joy_78': {'Type': 'Digital', 'x': 3324, 'y': 1296, 'width': 400, 'height': 60},
        'Joy_79': {'Type': 'Digital', 'x': 3324, 'y': 1356, 'width': 400, 'height': 60},
        'Joy_80': {'Type': 'Digital', 'x': 3324, 'y': 1466, 'width': 400, 'height': 60},
        'Joy_81': {'Type': 'Digital', 'x': 2804, 'y': 1782, 'width': 400, 'height': 60},
        'Joy_82': {'Type': 'Digital', 'x': 2804, 'y': 1842, 'width': 400, 'height': 60},
        'Joy_83': {'Type': 'Digital', 'x': 2804, 'y': 1576, 'width': 400, 'height': 60},
        'Joy_84': {'Type': 'Digital', 'x': 2804, 'y': 1696, 'width': 400, 'height': 60},
        'Joy_85': {'Type': 'Digital', 'x': 2804, 'y': 1636, 'width': 400, 'height': 60},
        'Joy_86': {'Type': 'Digital', 'x': 164, 'y': 1272, 'width': 400, 'height': 60},
        'Joy_87': {'Type': 'Digital', 'x': 164, 'y': 1332, 'width': 400, 'height': 60},
        'Joy_88': {'Type': 'Digital', 'x': 164, 'y': 1392, 'width': 400, 'height': 60},
        'Joy_89': {'Type': 'Digital', 'x': 164, 'y': 1510, 'width': 400, 'height': 60},
        'Joy_90': {'Type': 'Digital', 'x': 164, 'y': 1570, 'width': 400, 'height': 60},
        'Joy_91': {'Type': 'Digital', 'x': 164, 'y': 1630, 'width': 400, 'height': 60},
        'Joy_92': {'Type': 'Digital', 'x': 764, 'y': 1554, 'width': 400, 'height': 60},
        'Joy_93': {'Type': 'Digital', 'x': 2124, 'y': 1964, 'width': 400, 'height': 60},
        'Joy_94': {'Type': 'Digital', 'x': 2124, 'y': 2024, 'width': 400, 'height': 60},
        'Joy_95': {'Type': 'Digital', 'x': 2124, 'y': 2084, 'width': 400, 'height': 60},
        'Joy_96': {'Type': 'Digital', 'x': 2264, 'y': 1844, 'width': 400, 'height': 60},
        'Joy_97': {'Type': 'Digital', 'x': 164, 'y': 1752, 'width': 400, 'height': 60},
        'Joy_98': {'Type': 'Digital', 'x': 164, 'y': 1872, 'width': 400, 'height': 60},
        'Joy_99': {'Type': 'Digital', 'x': 164, 'y': 1812, 'width': 400, 'height': 60},
        'Joy_100': {'Type': 'Digital', 'x': 644, 'y': 1932, 'width': 400, 'height': 60},
        'Joy_101': {'Type': 'Digital', 'x': 644, 'y': 2052, 'width': 400, 'height': 60},
        'Joy_102': {'Type': 'Digital', 'x': 644, 'y': 1992, 'width': 400, 'height': 60},
        'Joy_103': {'Type': 'Digital', 'x': 1164, 'y': 1932, 'width': 400, 'height': 60},
        'Joy_104': {'Type': 'Digital', 'x': 1164, 'y': 2052, 'width': 400, 'height': 60},
        'Joy_105': {'Type': 'Digital', 'x': 1164, 'y': 1992, 'width': 400, 'height': 60},
        'Joy_106': {'Type': 'Digital', 'x': 3324, 'y': 1570, 'width': 400, 'height': 60},
        'Joy_107': {'Type': 'Digital', 'x': 3324, 'y': 1630, 'width': 400, 'height': 60},
        'Joy_108': {'Type': 'Digital', 'x': 3324, 'y': 1690, 'width': 400, 'height': 60},
        'Joy_109': {'Type': 'Digital', 'x': 2804, 'y': 1928, 'width': 400, 'height': 60},
        'Joy_110': {'Type': 'Digital', 'x': 2804, 'y': 1988, 'width': 400, 'height': 60},
        'Joy_111': {'Type': 'Digital', 'x': 2804, 'y': 2048, 'width': 400, 'height': 60},
                       
    },
    
    '4098BC2A': { # Wingwin Ursa Minor Fighter (Right)
        'displayName': 'Wingwin Ursa Minor Fighter (Right)',
        'Joy_1': {'Type': 'Digital', 'x': 644, 'y': 1205, 'width': 400, 'height': 80},
        'Joy_2': {'Type': 'Digital', 'x': 1044, 'y': 1205, 'width': 400, 'height': 80},
        'Joy_3': {'Type': 'Digital', 'x': 644, 'y': 1285, 'width': 400, 'height': 80},
        'Joy_4': {'Type': 'Digital', 'x': 1044, 'y': 1285, 'width': 400, 'height': 80},
        'Joy_5': {'Type': 'Digital', 'x': 644, 'y': 1399, 'width': 400, 'height': 80},
        'Joy_6': {'Type': 'Digital', 'x': 124, 'y': 1672, 'width': 400, 'height': 80},
        'Joy_7': {'Type': 'Digital', 'x': 124, 'y': 1749, 'width': 400, 'height': 80},
        'Joy_8': {'Type': 'Digital', 'x': 3284, 'y': 1190, 'width': 400, 'height': 80},
        'Joy_9': {'Type': 'Digital', 'x': 2884, 'y': 1190, 'width': 400, 'height': 80},
        'Joy_10': {'Type': 'Digital', 'x': 3284, 'y': 1270, 'width': 400, 'height': 80},
        'Joy_11': {'Type': 'Digital', 'x': 2884, 'y': 1270, 'width': 400, 'height': 80},
        'Joy_12': {'Type': 'Digital', 'x': 3284, 'y': 1790, 'width': 400, 'height': 80},
        'Joy_13': {'Type': 'Digital', 'x': 3284, 'y': 1408, 'width': 400, 'height': 80},
        'Joy_14': {'Type': 'Digital', 'x': 3284, 'y': 1485, 'width': 400, 'height': 80},
        'Joy_15': {'Type': 'Digital', 'x': 2000, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        'Joy_16': {'Type': 'Digital', 'x': 2884, 'y': 1190 , 'width': 400, 'height': 80},  #Not sure
        'Joy_17': {'Type': 'Digital', 'x': 2400, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        'Joy_18': {'Type': 'Digital', 'x': 2600, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        'Joy_19': {'Type': 'Digital', 'x': 2800, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        'Joy_20': {'Type': 'Digital', 'x': 864, 'y': 390, 'width': 400, 'height': 80},
        'Joy_21': {'Type': 'Digital', 'x': 124, 'y': 327, 'width': 400, 'height': 80},
        'Joy_22': {'Type': 'Digital', 'x': 2724, 'y': 159, 'width': 400, 'height': 80},
        'Joy_23': {'Type': 'Digital', 'x': 3284, 'y': 159, 'width': 400, 'height':80},
        'Joy_24': {'Type': 'Digital', 'x': 3284, 'y': 239, 'width': 400, 'height': 80},
        'Joy_25': {'Type': 'Digital', 'x': 3284, 'y': 319, 'width': 400, 'height': 80},
        'Joy_26': {'Type': 'Digital', 'x': 3284, 'y': 399, 'width': 400, 'height': 80},
        'Joy_27': {'Type': 'Digital', 'x': 3284, 'y': 479, 'width': 400, 'height': 80},
        'Joy_28': {'Type': 'Digital', 'x': 2724, 'y': 257, 'width': 400, 'height': 80},
        'Joy_29': {'Type': 'Digital', 'x': 864, 'y': 680, 'width': 400, 'height': 80},
        'Joy_30': {'Type': 'Digital', 'x': 864, 'y': 760, 'width': 400, 'height': 80},
        'Joy_31': {'Type': 'Digital', 'x': 864, 'y': 840, 'width': 400, 'height': 80},
        'Joy_32': {'Type': 'Digital', 'x': 864, 'y': 920, 'width': 400, 'height': 80},
        'Joy_33': {'Type': 'Digital', 'x': 864, 'y': 1000, 'width': 400, 'height': 80},
        'Joy_34': {'Type': 'Digital', 'x': 124, 'y': 755, 'width': 400, 'height': 80},
        'Joy_35': {'Type': 'Digital', 'x': 3284, 'y': 619, 'width': 400, 'height': 80},
        'Joy_36': {'Type': 'Digital', 'x': 3284, 'y': 699, 'width': 400, 'height': 80},
        'Joy_37': {'Type': 'Digital', 'x': 2724, 'y': 723, 'width': 400, 'height': 80},
        'Joy_38': {'Type': 'Digital', 'x': 2724, 'y': 803, 'width': 400, 'height': 80},
        'Joy_39': {'Type': 'Digital', 'x': 2884, 'y': 1030, 'width': 400, 'height': 80},
        'Joy_40': {'Type': 'Digital', 'x': 124, 'y': 1202, 'width': 400, 'height': 80},
        'Joy_41': {'Type': 'Digital', 'x': 124, 'y': 1282, 'width': 400, 'height': 80},
        'Joy_42': {'Type': 'Digital', 'x': 124, 'y': 1362, 'width': 400, 'height': 80},
        'Joy_43': {'Type': 'Digital', 'x': 124, 'y': 1442, 'width': 400, 'height': 80},
        'Joy_44': {'Type': 'Digital', 'x': 124, 'y': 1522, 'width': 400, 'height': 80},
        'Joy_45': {'Type': 'Digital', 'x': 124, 'y': 835, 'width': 400, 'height': 80},
        'Joy_46': {'Type': 'Digital', 'x': 124, 'y': 915, 'width': 400, 'height': 80},
        'Joy_47': {'Type': 'Digital', 'x': 124, 'y': 995, 'width': 400, 'height': 80},
        'Joy_48': {'Type': 'Digital', 'x': 124, 'y': 1075, 'width': 400, 'height': 80},

        'Joy_POV1Up': {'Type': 'Digital', 'x': 124, 'y': 407, 'width': 400, 'height': 80}, # PoV up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 124, 'y': 487, 'width': 400, 'height': 80}, # PoV right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 124, 'y': 567, 'width': 400, 'height': 80}, # PoV down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 124, 'y': 647, 'width': 400, 'height': 80}, # PoV left
        'Joy_XAxis': {'Type': 'Analogue', 'x': 524, 'y': 2040, 'width': 400, 'height': 80},
        'Joy_YAxis': {'Type': 'Analogue', 'x': 84, 'y': 2040, 'width': 400, 'height': 80},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 974, 'y': 2040, 'width': 400, 'height': 80},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 644, 'y': 1732, 'width': 400, 'height': 80}, # Slider?
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 124, 'y': 835, 'width': 400, 'height': 80}, # Pov Axis up/down
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 124, 'y': 915, 'width': 400, 'height': 80}, # Pov Axis left/right
    },
    '4098BC29': { # Wingwin Ursa Minor Fighter (Left)
        'displayName': 'Wingwin Ursa Minor Fighter (Left)',
        'Joy_1': {'Type': 'Digital', 'x': 367, 'y': 1398, 'width': 400, 'height': 80},
        'Joy_2': {'Type': 'Digital', 'x': 767, 'y': 1398, 'width': 400, 'height': 80},
        'Joy_3': {'Type': 'Digital', 'x': 367, 'y': 1478, 'width': 400, 'height': 80},
        'Joy_4': {'Type': 'Digital', 'x': 767, 'y': 1478, 'width': 400, 'height': 80},
        'Joy_5': {'Type': 'Digital', 'x': 767, 'y': 1825, 'width': 400, 'height': 80},
        'Joy_6': {'Type': 'Digital', 'x': 767, 'y': 1986, 'width': 400, 'height': 80},
        'Joy_7': {'Type': 'Digital', 'x': 767, 'y': 2066, 'width': 400, 'height': 80},
        'Joy_8': {'Type': 'Digital', 'x': 3388, 'y': 1209, 'width': 400, 'height': 80},
        'Joy_9': {'Type': 'Digital', 'x': 2987, 'y': 1209, 'width': 400, 'height': 80},
        'Joy_10': {'Type': 'Digital', 'x': 3386, 'y': 1290, 'width': 400, 'height': 80},
        'Joy_11': {'Type': 'Digital', 'x': 2989, 'y': 1290, 'width': 400, 'height': 80},
        'Joy_12': {'Type': 'Digital', 'x': 2989, 'y': 1402, 'width': 400, 'height': 80},
        'Joy_13': {'Type': 'Digital', 'x': 3947, 'y': 1637, 'width': 400, 'height': 80},
        'Joy_14': {'Type': 'Digital', 'x': 3947, 'y': 1717, 'width': 400, 'height': 80},
        # 'Joy_15': {'Type': 'Digital', 'x': 2000, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        # 'Joy_16': {'Type': 'Digital', 'x': 2884, 'y': 1190 , 'width': 400, 'height': 80},  #Not sure
        # 'Joy_17': {'Type': 'Digital', 'x': 2400, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        # 'Joy_18': {'Type': 'Digital', 'x': 2600, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        # 'Joy_19': {'Type': 'Digital', 'x': 2800, 'y': 2030, 'width': 400, 'height': 80},  #Not sure
        'Joy_20': {'Type': 'Digital', 'x': 2989, 'y': 363, 'width': 400, 'height': 80},
        'Joy_21': {'Type': 'Digital', 'x': 3948, 'y': 293, 'width': 400, 'height': 80},
        'Joy_22': {'Type': 'Digital', 'x': 846, 'y': 343, 'width': 400, 'height': 80},
        'Joy_23': {'Type': 'Digital', 'x': 357, 'y': 343, 'width': 400, 'height':80},
        'Joy_24': {'Type': 'Digital', 'x': 357, 'y': 423, 'width': 400, 'height': 80},
        'Joy_25': {'Type': 'Digital', 'x': 357, 'y': 503, 'width': 400, 'height': 80},
        'Joy_26': {'Type': 'Digital', 'x': 357, 'y': 583, 'width': 400, 'height': 80},
        'Joy_27': {'Type': 'Digital', 'x': 357, 'y': 663, 'width': 400, 'height': 80},
        'Joy_28': {'Type': 'Digital', 'x': 846, 'y': 442, 'width': 400, 'height': 80},
        'Joy_29': {'Type': 'Digital', 'x': 2997, 'y': 643, 'width': 400, 'height': 80},
        'Joy_30': {'Type': 'Digital', 'x': 2997, 'y': 723, 'width': 400, 'height': 80},
        'Joy_31': {'Type': 'Digital', 'x': 2997, 'y': 803, 'width': 400, 'height': 80},
        'Joy_32': {'Type': 'Digital', 'x': 2997, 'y': 883, 'width': 400, 'height': 80},
        'Joy_33': {'Type': 'Digital', 'x': 2997, 'y': 963, 'width': 400, 'height': 80},
        'Joy_34': {'Type': 'Digital', 'x': 3947, 'y': 721, 'width': 400, 'height': 80},
        'Joy_35': {'Type': 'Digital', 'x': 357, 'y': 803, 'width': 400, 'height': 80},
        'Joy_36': {'Type': 'Digital', 'x': 357, 'y': 883, 'width': 400, 'height': 80},
        'Joy_37': {'Type': 'Digital', 'x': 847, 'y': 907, 'width': 400, 'height': 80},
        'Joy_38': {'Type': 'Digital', 'x': 847, 'y': 987, 'width': 400, 'height': 80},
        'Joy_39': {'Type': 'Digital', 'x': 367, 'y': 1237, 'width': 400, 'height': 80},
        'Joy_40': {'Type': 'Digital', 'x': 3947, 'y': 1169, 'width': 400, 'height': 80},
        'Joy_41': {'Type': 'Digital', 'x': 3947, 'y': 1249, 'width': 400, 'height': 80},
        'Joy_42': {'Type': 'Digital', 'x': 3947, 'y': 1329, 'width': 400, 'height': 80},
        'Joy_43': {'Type': 'Digital', 'x': 3947, 'y': 1404, 'width': 400, 'height': 80},
        'Joy_44': {'Type': 'Digital', 'x': 3947, 'y': 1485, 'width': 400, 'height': 80},
        'Joy_45': {'Type': 'Digital', 'x': 3947, 'y': 801, 'width': 400, 'height': 80},
        'Joy_46': {'Type': 'Digital', 'x': 3947, 'y': 881, 'width': 400, 'height': 80},
        'Joy_47': {'Type': 'Digital', 'x': 3947, 'y': 961, 'width': 400, 'height': 80},
        'Joy_48': {'Type': 'Digital', 'x': 3947, 'y': 1041, 'width': 400, 'height': 80},

        'Joy_POV1Up': {'Type': 'Digital', 'x': 3947, 'y': 373, 'width': 400, 'height': 80}, # PoV up
        'Joy_POV1Right': {'Type': 'Digital', 'x': 3947, 'y': 453, 'width': 400, 'height': 80}, # PoV right
        'Joy_POV1Down': {'Type': 'Digital', 'x': 3947, 'y': 533, 'width': 400, 'height': 80}, # PoV down
        'Joy_POV1Left': {'Type': 'Digital', 'x': 3947, 'y': 613, 'width': 400, 'height': 80}, # PoV left
        'Joy_YAxis': {'Type': 'Analogue', 'x': 3467, 'y': 2013, 'width': 400, 'height': 80},
        'Joy_XAxis': {'Type': 'Analogue', 'x': 3957, 'y': 2013, 'width': 400, 'height': 80},
        'Joy_RZAxis': {'Type': 'Analogue', 'x': 2977, 'y': 2013, 'width': 400, 'height': 80},
        'Joy_UAxis': {'Type': 'Analogue', 'x': 2987, 'y': 1735, 'width': 400, 'height': 80}, # Slider?
        'Joy_RXAxis': {'Type': 'Analogue', 'x': 3547, 'y': 801, 'width': 400, 'height': 80}, # Pov Axis up/down
        'Joy_RYAxis': {'Type': 'Analogue', 'x': 3547, 'y': 881, 'width': 400, 'height': 80}, # Pov Axis left/right
    },
}

keymap = {
    'Key_Comma': ',',
    'Key_SemiColon': ';',
    'Key_LeftAlt': 'Left Alt',
    'Key_LeftBracket': '[',
    'Key_LeftControl': 'Left Ctrl',
    'Key_LeftShift': 'Left Shift',
    'Key_Minus': '-',
    'Key_Plus': '+',
    'Key_Equals': '=',
    'Key_Period': '.',
    'Key_RightAlt': 'Right Alt',
    'Key_RightBracket': ']',
    'Key_RightControl': 'Right Ctrl',
    'Key_RightShift': 'Right Shift',
    'Key_RightArrow': 'Right',
    'Key_UpArrow': 'Up',
    'Key_LeftArrow': 'Left',
    'Key_DownArrow': 'Down',
    'Key_LessThan': '<',
    'Key_GreaterThan': '>',
    'Key_LeftParenthesis': '(',
    'Key_RightParenthesis': ')',
    'Key_Numpad_0': 'Num 0',
    'Key_Numpad_1': 'Num 1',
    'Key_Numpad_2': 'Num 2',
    'Key_Numpad_3': 'Num 3',
    'Key_Numpad_4': 'Num 4',
    'Key_Numpad_5': 'Num 5',
    'Key_Numpad_6': 'Num 6',
    'Key_Numpad_7': 'Num 7',
    'Key_Numpad_8': 'Num 8',
    'Key_Numpad_9': 'Num 9',
    'Key_Numpad_Decimal': 'Num .',
    'Key_Numpad_Multiply': 'Num *',
    'Key_Numpad_Divide': 'Num /',
    'Key_Numpad_Add': 'Num +',
    'Key_Numpad_Subtract': 'Num -',
    'Key_Numpad_Enter': 'Num Enter',
    'Key_Numpad_Equals': 'Num =',
    'Key_Numpad_Comma': 'Num ,',
    'Key_Numpad_Period': 'Num .',
    'Key_PageDown': 'PgDn',
    'Key_PageUp': 'PgUp',
    'Key_Grave': '`',
    'Key_BackSlash': '\\',
    'Key_Slash': '/',
    'Key_Apostrophe': '\'',
    'Key_Hash': '#',
}
