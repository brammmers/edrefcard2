# Guide: Creating Templates for the 5 Priority Controllers

## Controllers to Prioritize (40% of users)

1. **VKB Gladiator NXT Premium Right** (664 configs, 13.3%)
2. **Saitek X56 Throttle** (423 configs, 8.5%)
3. **Saitek X56 Joystick** (415 configs, 8.3%)
4. **VKB Gladiator NXT Premium Left** (266 configs, 5.3%)
5. **VKB Gladiator NXT Left OTA** (264 configs, 5.3%)

---

## 1. VKB Gladiator NXT Premium Right

### Official Resources

**Documentation:**
- Official website: https://vkb-sim.com/
- PDF manual: https://vkb-sim.com/download/manuals/ (search for "Gladiator NXT")
- Configuration tool: VKBDevCfg (free, downloadable from the website)

**High Resolution Images:**
- VKB website: https://vkb-sim.com/products/gladiator-evo-space-combat-edition/
- Professional review: https://www.youtube.com/watch?v=... (search for "VKB Gladiator NXT review")

### Device ID
- `231D0200` (already in supportedDevices, but no visual template)

### Button Mapping

**Quick Reference:**
```
Joy_1  → Main trigger (index finger)
Joy_2  → Red button on top (A1)
Joy_3  → Red side button (A2)
Joy_4  → Black button on top (A3)
Joy_5  → Ministick press

Hats:
Joy_POV1Up/Right/Down/Left → Main 8-way hat
Joy_7-10 → Upper hat (4-way)
Joy_11-14 → Side hat (4-way)

Axes:
Joy_XAxis → Roll (left-right)
Joy_YAxis → Pitch (forward-backward)
Joy_RZAxis → Twist (rotation)
Joy_UAxis → Throttle slider
```

### Creation Process

1. **Obtain the image:**
   - Download from VKB website
   - Or screenshot from a 4K YouTube review
   - Resize to 3840px width in GIMP

2. **Test the mapping:**
   - Install VKBDevCfg
   - Connect the joystick
   - Press each button and note the number

3. **Create the template:**
   - Use the admin tool (when available)
   - Or manually in GIMP, noting X,Y coordinates

4. **Python code:**
   ```python
   'VKB-Gladiator-NXT-Premium-Right': {
       'displayName': 'VKB Gladiator NXT Premium Right',
       'Joy_1': {'Type': 'Digital', 'x': 1234, 'y': 567, 'width': 800},
       # ... etc
   }
   ```

---

## 2. Saitek X56 Throttle

### Official Resources

**Documentation:**
- Logitech G website (current owner): https://www.logitechg.com/en-us/products/space/x56-space-flight-vr-simulator-controller.html
- PDF manual: Downloadable from the product page
- Legacy Saitek: https://support.logi.com/hc/en-us/articles/360025596274

**Images:**
- Logitech marketing: Official high-resolution images
- Guru3D review: https://www.guru3d.com/articles-pages/saitek-x-56-rhino-review,3.html

### Device IDs
- Throttle: `SaitekX56Throttle` or `0738A221`
- **Template already exists!** (line 578 bindingsData.py)

**NOTE:** This controller is ALREADY supported with complete visual template ✅

---

## 3. Saitek X56 Joystick

### Device ID
- `SaitekX56Joystick` or `07382221`

**Template already exists!** (line 525 bindingsData.py) ✅

---

## 4 & 5. VKB Gladiator NXT Premium Left / Left OTA

### Device IDs
- Left standard: `231D0201`
- Left OTA: `231d3201` (lowercase)

**NOTE:** Same configuration as the Right, but mirrored image

### Resources

Identical to Gladiator NXT Right, but:
- Left-hand configuration (inverted image)
- Identical mapping except for buttons
- OTA = "Over The Air" firmware updates

### Creation Tip

**Reuse the Right template:**
1. Copy the Right image
2. Flip horizontally in GIMP
3. Reuse the same coordinates (adjust X for the flip)
4. Different device ID, different template

---

## Detailed Manual Process

### Step 1: Preparation (15 min)

**Checklist:**
- [ ] Download PDF manual from manufacturer
- [ ] Download high-resolution image
- [ ] Install GIMP (if not already done)
- [ ] Access a test `.binds` file with this controller

### Step 2: Template Image (30 min)

**In GIMP:**

1. Open source image
2. `Image` → `Scale Image` → Width: 3840px
3. `Image` → `Flatten Image` (if transparent)
4. `File` → `Export As` → `www/layouts/controller-name.jpg`
5. Quality: 90%

### Step 3: Coordinate Mapping (1-2h)

**GIMP Method:**

1. Open template image
2. `Windows` → `Dockable Dialogs` → `Pointer`
3. Enable grid: `View` → `Show Grid`
4. For each button:
   - Position cursor at button center
   - Note X, Y in the pointer dialog
   - Estimate available width for text
   
**Mapping spreadsheet:**
```
Button      | X    | Y    | Width | Type
------------|------|------|-------|----------
Joy_1       | 2124 | 618  | 642   | Digital
Joy_2       | 2084 | 208  | 792   | Digital
Joy_POV1Up  | 1684 | 288  | 1072  | Digital
Joy_XAxis   | 3194 | 1110 | 632   | Analogue
```

### Step 4: Python Code (30 min)

**In `bindingsData.py`:**

1. Find the `hotasDetails = {` section
2. Add new entry:

```python
'231D0200': {  # Device ID
    'displayName': 'VKB Gladiator NXT Premium Right',
    
    # Digital buttons
    'Joy_1': {'Type': 'Digital', 'x': 2124, 'y': 618, 'width': 642},
    'Joy_2': {'Type': 'Digital', 'x': 2084, 'y': 208, 'width': 792},
    
    # Hats
    'Joy_POV1Up': {'Type': 'Digital', 'x': 1684, 'y': 288, 'width': 1072},
    'Joy_POV1Right': {'Type': 'Digital', 'x': 1684, 'y': 344, 'width': 1072},
    'Joy_POV1Down': {'Type': 'Digital', 'x': 1684, 'y': 400, 'width': 1072},
    'Joy_POV1Left': {'Type': 'Digital', 'x': 1684, 'y': 456, 'width': 1072},
    
    # Analog axes
    'Joy_XAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1110, 'width': 632},
    'Joy_YAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1054, 'width': 632},
    'Joy_RZAxis': {'Type': 'Analogue', 'x': 3194, 'y': 1166, 'width': 632},
    
    # ... continue for all buttons
},
```

### Step 5: Testing (15 min)

1. Upload a `.binds` file with the controller
2. Verify that the image displays
3. Verify that all texts are readable
4. Adjust if necessary

---

## Tips and Best Practices

### Text Spacing
- **Minimum width:** 400px for readability
- **Optimal width:** 600-800px
- **Avoid:** Less than 300px (text too tight)

### Button Types
- `Digital`: On/off buttons, hats
- `Analogue`: Axes, sliders, rotaries

### Custom Height
- Default: 54px
- If more space needed: `'height': 108`

### Hats (POV)
- Always 4 directions: `Up`, `Right`, `Down`, `Left`
- Vertical spacing: ~56px between each direction
- Identical width for all

### Code Organization
```python
# 1. Main buttons (trigger, etc.)
# 2. Hats organized by group
# 3. Analog axes
# 4. Secondary buttons
```

---

## Realistic Time Estimate

| Controller | Total Time | Comment |
|------------|-------------|----------------|
| VKB Glad NXT Right | 3h | First, learning curve |
| Saitek X56 Throttle | ✅ Already done | 0h |
| Saitek X56 Joystick | ✅ Already done | 0h |
| VKB Glad NXT Left | 1h | Reuse Right, just flip |
| VKB Glad NXT Left OTA | 30min | Identical to Left |

**Actual total needed: ~4.5 hours** to cover 40% of users (since 2/5 are already done!)

---

## Next Steps

1. **Immediate:** VKB Glad NXT Right (13% users)
2. **Then:** VKB Glad NXT Left (5%)  
3. **Bonus:** VKB Left OTA (5%) - almost free

Saitek X56 are already complete, so **VKB only priority**.

---

## Quick Links

**VKB:**
- Website: https://vkb-sim.com/
- Support: https://support.vkb-sim.pro/
- Forum: https://forum.vkb-sim.pro/

**Saitek/Logitech:**
- Support: https://support.logi.com/
- Drivers: https://support.logi.com/hc/en-us/articles/360025596274
