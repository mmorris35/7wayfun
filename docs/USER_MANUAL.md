# User Manual - 7-Way Trailer Tester

Complete operating guide for the 7-Way Trailer Wiring Tester.

---

## Quick Start

1. **Power on** - Connect 12V automotive power (fused)
2. **Mode select** - Press Mode button to cycle through operating modes
3. **Run test** - Press Test button (short press for quick test, long press for full test)
4. **Read display** - Check OLED for voltage readings or test status
5. **Watch LEDs** - NeoPixel strip shows channel status at a glance

---

## Operating Modes

The tester has three modes. Press the **Mode button** to cycle through them.

### 1. Vehicle Tester Mode

**Use case:** Testing tow vehicle's 7-way connector output

**Setup:**
1. Connect male 7-way connector to vehicle's trailer connector
2. Turn on vehicle
3. Activate vehicle lights (headlights, turn signals, brake, reverse, etc.)

**Operation:**
- OLED displays voltage for each channel in real-time
- NeoPixels light up when signals are active (above 3V)
- Readings update every 250ms
- Short press Test button for detailed voltage reading

**Interpreting readings:**
| Voltage | Status | Meaning |
|---------|--------|---------|
| 0.0V - 3.0V | OFF | No signal |
| 3.0V - 9.0V | WEAK | Poor connection or degraded wiring |
| 9.0V - 11.0V | WEAK | Below normal, check connections |
| 11.0V - 14.0V | OK | Normal signal (12V nominal) |
| Above 14.5V | HIGH | Potential fault, check alternator |

**Normal readings:**
- Running lights / Turn signals: 11.5V - 12.5V
- Brake lights: 11.5V - 12.5V
- Reverse lights: 11.5V - 12.5V
- Aux power: 12V - 14.4V (varies with alternator)

### 2. Trailer Tester Mode

**Use case:** Testing trailer lights and wiring

**Setup:**
1. Connect female 7-way connector to trailer
2. Ensure trailer ground is connected (Pin 1, White wire)

**Operation:**
- Press Test button to cycle through all channels
- Each circuit activates for 1-2 seconds
- Watch trailer lights to verify function
- NeoPixels show which circuit is being tested

**Test sequence (short press):**
1. Tail lights (Green) - 2 seconds
2. Left turn (Red) - 1.5 seconds
3. Right turn (Brown) - 1.5 seconds
4. Brakes (Blue) - 2 seconds
5. Reverse (Yellow) - 1.5 seconds
6. Aux power (Black) - 1 second

**Full test (long press - hold 2 seconds):**
- Runs complete sequence 3 times
- Provides visual confirmation with cyan blink
- Ends with green blink confirmation

### 3. Pass-Through Mode

**Use case:** Real-time monitoring while vehicle and trailer are connected

**Setup:**
1. Connect male connector to vehicle
2. Connect female connector to trailer
3. All signals pass through from vehicle to trailer

**Operation:**
- Tester monitors all signals in real-time
- OLED shows live voltage readings
- NeoPixels indicate active channels
- **Signal integrity checking active:**
  - Orange LED = degraded signal (below 9V)
  - Display shows "WEAK: channel" for problem circuits
  - Logs warnings for diagnostic purposes

**Useful for:**
- Diagnosing intermittent problems
- Verifying signal integrity under load
- Monitoring voltage drops
- Testing while driving (with passenger monitoring display)

---

## Display Reference

### OLED Screen Layout

```
+---------------------------+
| MODE: VEHICLE_TESTER      |  ← Current mode
|---------------------------|
| BRK: 11.8V  [====    ]    |  ← Brake (Pin 2, Blue)
| TAIL: 0.0V  [        ]    |  ← Tail (Pin 3, Green)
| LEFT: 12.1V [========]    |  ← Left (Pin 4, Red)
| RIGHT: 0.0V [        ]    |  ← Right (Pin 5, Brown)
| AUX: 13.2V  [========]    |  ← Aux (Pin 6, Black)
| REV: 0.0V   [        ]    |  ← Reverse (Pin 7, Yellow)
+---------------------------+
```

**Bar graph:** Visual representation of voltage (0-15V scale)

### NeoPixel LED Indicators

**LED positions (left to right):**
```
 0      1      2      3      4      5      6      7
STA   BRK   TAIL   LEFT  RIGHT  AUX    REV   GND
```

**LED colors and meanings:**

| LED | Channel | Off (Dim) | Active (Bright) | Degraded | Fault |
|-----|---------|-----------|-----------------|----------|-------|
| 0 | Status | Dim white | Mode color | - | Red blink |
| 1 | Brake | Dim blue | Bright blue | Orange | Red |
| 2 | Tail | Dim green | Bright green | Orange | Red |
| 3 | Left | Dim red | Bright red | Orange | Red |
| 4 | Right | Dim brown | Bright brown | Orange | Red |
| 5 | Aux | Dim white | Bright white | Orange | Red blink |
| 6 | Reverse | Dim yellow | Bright yellow | Orange | Red |
| 7 | Ground | Dim white | Green (OK) | - | Red |

**Mode indicator (LED 0) colors:**
- **Cyan** = Vehicle Tester mode
- **Magenta** = Trailer Tester mode
- **Yellow** = Pass-Through mode

---

## Control Buttons

### Mode Button (Left)

**Short press:** Cycle to next mode
- Vehicle Tester → Trailer Tester → Pass-Through → (repeat)
- White flash feedback on press
- Display and LEDs update immediately

**Mode transition behavior:**
- All relays turn off for safety
- Channel LEDs reset to idle state
- Display updates to show new mode

### Test Button (Right)

**Short press (<2 seconds):**
- **Vehicle Tester mode:** Force detailed voltage read (logged to console)
- **Trailer Tester mode:** Run test sequence once
- **Pass-Through mode:** No effect

**Long press (hold ≥2 seconds):**
- **All modes:** Run comprehensive full test
- Cyan blinks (3x) = test starting
- Runs complete trailer test sequence
- Green blinks (2x) = test complete

---

## 7-Way Connector Pinout

**RV 7-Way Standard** (for camping trailers, travel trailers, RVs)

| Pin | Function | Wire Color | Typical Current |
|-----|----------|------------|-----------------|
| 1 | Ground | White | Return path |
| 2 | Electric Brakes | Blue | 0-3A (PWM) |
| 3 | Tail/Running | Green | 2-5A |
| 4 | Left Turn/Brake | Red | 2-5A |
| 5 | Right Turn/Brake | Brown | 2-5A |
| 6 | 12V Auxiliary | Black | 0-10A |
| 7 | Reverse Lights | Yellow | 1-3A |

**Connector orientation:**
- View from rear of female connector (trailer side)
- Pin 1 (Ground) is in center
- Other pins arranged in circle around center

---

## Troubleshooting

### No Power / Display Dark

**Symptoms:** No OLED display, no LEDs, no relay clicks

**Possible causes:**
1. **No 12V input power**
   - Check fuse (replace if blown)
   - Verify 12V at input terminals with multimeter
   - Check battery/alternator

2. **Buck converter failure**
   - Verify 12V at buck converter input
   - Check 5V at buck converter output
   - Replace buck converter if no 5V output

3. **Feather not powered**
   - Check connection from buck converter to Feather USB pin
   - Verify 5V at Feather USB pin
   - Check Feather power LED

### No Voltage Readings

**Symptoms:** Display works, but all channels show 0.0V even with test voltage applied

**Possible causes:**
1. **ADC not initialized**
   - Check I2C connections (SDA, SCL, pull-ups)
   - Verify ADC boards are powered (3.3V)
   - Check I2C addresses (0x48 and 0x49)

2. **Voltage divider issue**
   - Verify 10K and 2.7K resistor values
   - Check connections at ADC input pins
   - Test voltage at ADC pin (should be ~2.5V for 12V input)

3. **Input not connected**
   - Verify test voltage is actually present
   - Check connections at input connector

### Readings Always 0.0V or Random

**Symptoms:** Channels show 0.0V or fluctuate randomly

**Likely cause:** **Zener diode backwards or missing**
- Zener cathode (marked end) should connect to signal
- Zener anode should connect to ground
- Check with multimeter in diode test mode

### Relays Not Clicking

**Symptoms:** In Trailer Tester mode, no relay activation sounds

**Possible causes:**
1. **Relays not powered**
   - Verify 5V at relay VCC pins
   - Check ground connections

2. **GPIO not connected**
   - Verify connections from Feather D6, D9-D13 to relay signal pins
   - Check for loose wires

3. **Wrong mode**
   - Relays only activate in Trailer Tester mode
   - Press Mode button to cycle to correct mode

### NeoPixels Not Lighting

**Symptoms:** No LED activity, or only some LEDs work

**Possible causes:**
1. **Data line issue**
   - Verify connection from Feather D5 to NeoPixel DIN
   - Check for breaks in data wire
   - First LED failure breaks entire strip

2. **Power issue**
   - NeoPixels need 5V power
   - Check VCC and GND connections
   - Verify buck converter can supply enough current (200mA minimum)

3. **Firmware issue**
   - Reinstall CircuitPython libraries
   - Reflash firmware

### Mode Button Not Responding

**Symptoms:** Pressing Mode button doesn't cycle modes

**Possible causes:**
1. **Button wiring**
   - Verify connection from button to D24
   - Check ground connection
   - Button should short D24 to GND when pressed

2. **Debounce timing**
   - Wait 50ms between presses (debounce period)
   - Ensure button makes clean contact

3. **Stuck in test mode**
   - Wait for test sequence to complete
   - Tests block mode changes temporarily

### Inaccurate Voltage Readings

**Symptoms:** Readings consistently off by more than 0.5V

**Likely cause:** **Needs calibration**
- See `CALIBRATION_PROCEDURE.md` for adjustment steps
- Adjust `VOLTAGE_SCALE` constant in `firmware/adc_manager.py`
- Typical range: 4.5 - 5.0

### Pass-Through Mode Shows "WEAK" Warnings

**Symptoms:** Orange LEDs and "WEAK: channel" messages

**Meaning:** Signal integrity check detected voltage drop

**Possible causes:**
1. **Bad connection**
   - Check connector pins for corrosion
   - Clean contacts with electrical contact cleaner
   - Verify solid mechanical connection

2. **Undersized wiring**
   - Check wire gauge (should be 16-18 AWG minimum)
   - Long wire runs cause voltage drop
   - Upgrade to heavier gauge wire

3. **Ground issue**
   - Verify Pin 1 (White, Ground) is solidly connected
   - Poor ground causes all circuits to read low
   - Check ground strap from trailer frame to connector

4. **High resistance**
   - Corroded terminals
   - Loose crimps
   - Damaged wire

---

## Maintenance and Care

### Regular Inspection

**Monthly (if in use):**
- Inspect 7-way connectors for corrosion
- Check fuse holder for tightness
- Verify all connections are secure
- Test in all three modes

**Before each use:**
- Visual inspection for damaged wires
- Check that display powers on
- Verify NeoPixels light during startup

### Cleaning

**Connectors:**
- Use electrical contact cleaner spray
- Brass wire brush for stubborn corrosion
- Apply dielectric grease to prevent future corrosion

**Display:**
- Wipe OLED with soft, dry cloth only
- Do not use solvents or cleaners

**Enclosure:**
- Clean with damp cloth
- Keep ventilation openings clear

### Storage

- Store in dry location
- Disconnect power when not in use
- Protect connectors with covers or caps
- Avoid extreme temperatures (0°C - 40°C recommended)

### Calibration

**Recommended:** Annually or if readings drift

See `CALIBRATION_PROCEDURE.md` for detailed steps.

---

## Technical Specifications

**Power Requirements:**
- Input: 10-15V DC (automotive)
- Fuse: 10A recommended
- Current draw: 200-500mA (depending on NeoPixel brightness)

**Voltage Measurement:**
- Range: 0-15V
- Resolution: 16-bit ADC (0.25mV steps)
- Accuracy: ±0.5V (after calibration)
- Update rate: 4 readings/second

**Relay Outputs:**
- Rating: 10A per channel
- Type: Electromechanical
- Response time: <10ms

**Environmental:**
- Operating temp: 0°C to 40°C
- Storage temp: -20°C to 60°C
- Humidity: Non-condensing

---

## Safety Information

### Warnings

⚠️ **Automotive voltage:** This device connects to 12V automotive electrical systems. Always use proper fusing and disconnect battery when making connections.

⚠️ **Electric brake systems:** Electric trailer brake circuits carry PWM signals with significant current. Do not short or miswire brake circuits.

⚠️ **Reversed polarity:** Connecting power backwards can damage electronic components. Always verify polarity before applying power.

⚠️ **Inductive loads:** Trailer lighting includes inductive loads that can cause voltage spikes. Ensure all relays have flyback protection.

### Proper Use

✅ **Do:**
- Use inline fuse on 12V input (10A recommended)
- Verify connections before applying power
- Test with known-good voltage source first
- Disconnect power when not in use
- Follow all local electrical codes

❌ **Don't:**
- Connect directly to trailer brakes without understanding brake controller systems
- Exceed relay current ratings
- Operate in wet conditions without waterproof enclosure
- Use damaged or corroded connectors
- Bypass safety fuses

---

## Getting Help

**Documentation:**
- `ASSEMBLY_GUIDE.md` - Build instructions
- `HARDWARE_DESIGN.md` - Circuit design details
- `CALIBRATION_PROCEDURE.md` - Voltage calibration steps

**Source Code:**
- GitHub: [trailer-tester repository](https://github.com/yourusername/trailer-tester)
- Report issues on GitHub Issues page

---

*User Manual v1.0 - December 2024*
