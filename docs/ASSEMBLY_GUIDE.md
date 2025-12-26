# Assembly Guide - 7-Way Trailer Tester

Step-by-step instructions for assembling the trailer tester on a breadboard.

**⚠️ SAFETY WARNINGS:**
- This device connects to 12V automotive power - use proper fusing (10A recommended)
- Always disconnect power before making wiring changes
- Use proper wire gauge for 12V connections (18-22 AWG minimum)
- Verify polarity before applying power
- Work in a well-ventilated area

---

## Required Components

See [`SHOPPING_LIST.md`](SHOPPING_LIST.md) for complete parts list and Adafruit part numbers.

**Core Components:**
- Adafruit Feather RP2040
- 128x64 OLED FeatherWing
- NeoPixel Stick (8x LEDs)
- 2x ADS1115 16-bit ADC boards
- 2x 4-channel STEMMA relay boards
- Breadboard (full or half size)
- Jumper wires

**Power:**
- 12V automotive input (fused)
- Buck converter (12V → 5V, 3A minimum)

**Input Stage (per channel, x7):**
- 10kΩ resistor (R1)
- 2.7kΩ resistor (R2)
- 3.3V Zener diode

**Connectors:**
- Male 7-way connector (vehicle side)
- Female 7-way connector (trailer side)

---

## Assembly Steps

### Step 1: Prepare the Feather RP2040

1. **Solder stacking headers** to the Feather RP2040
   - Use the tall stacking headers (included with FeatherWing)
   - Solder from the bottom side
   - Ensure headers are perpendicular to the board

2. **Attach OLED FeatherWing**
   - Stack the OLED on top of the Feather
   - Headers should click into place
   - No soldering needed if using stacking headers

### Step 2: Power Supply

1. **Mount buck converter** on breadboard
   - Leave space for other components
   - Orient so input/output terminals are accessible

2. **Wire 12V input with inline fuse:**
   ```
   12V+ (vehicle) → 10A Fuse → Buck converter VIN+
   12V- (ground)  → Buck converter VIN-
   ```

3. **Connect 5V output to Feather:**
   ```
   Buck converter VOUT+ → Feather USB pin
   Buck converter VOUT- → Feather GND
   ```

**⚠️ Verify voltage before connecting!** Use multimeter to confirm buck converter outputs 5V.

### Step 3: I2C Bus Setup

All I2C devices share SDA and SCL lines with 4.7kΩ pull-up resistors.

1. **Connect I2C bus on breadboard:**
   ```
   Feather SDA → Bus rail (with 4.7kΩ to 3.3V)
   Feather SCL → Bus rail (with 4.7kΩ to 3.3V)
   ```

2. **Connect ADS1115 boards:**
   - **ADS1115 #1** (address 0x48):
     - ADDR pin → GND
     - VDD → 3.3V
     - GND → GND
     - SDA → I2C SDA bus
     - SCL → I2C SCL bus

   - **ADS1115 #2** (address 0x49):
     - ADDR pin → VDD (sets address to 0x49)
     - VDD → 3.3V
     - GND → GND
     - SDA → I2C SDA bus
     - SCL → I2C SCL bus

3. **OLED FeatherWing** automatically connects via stacking headers

### Step 4: Voltage Divider Input Circuits (x6 channels)

Build this circuit for each of the 6 trailer signal inputs:

```
12V Input ----[10K]----+----[2.7K]---- GND
                       |
                       +---- To ADC channel
                       |
                    [3.3V Zener]
                       |
                      GND
```

**Channel mapping:**

| Channel | Wire Color | ADC Board | ADC Channel | RV 7-Way Pin |
|---------|------------|-----------|-------------|--------------|
| Brake   | Blue       | Board #1  | A0          | Pin 2        |
| Tail    | Green      | Board #1  | A1          | Pin 3        |
| Left    | Red        | Board #1  | A2          | Pin 4        |
| Right   | Brown      | Board #1  | A3          | Pin 5        |
| Aux     | Black      | Board #2  | A0          | Pin 6        |
| Reverse | Yellow     | Board #2  | A1          | Pin 7        |

**For each channel:**
1. Connect 10kΩ resistor from input to breadboard row
2. Connect 2.7kΩ resistor from that row to GND
3. Connect 3.3V Zener diode across 2.7kΩ (cathode to resistor, anode to GND)
4. Connect midpoint (between resistors) to corresponding ADC channel

### Step 5: Relay Outputs

**STEMMA Relay Boards** (recommended - easiest):

Connect relay boards to Feather GPIO pins:

| Relay | Function | Feather Pin | Wire Color (Output) |
|-------|----------|-------------|---------------------|
| 0     | Brake    | D6          | Blue                |
| 1     | Tail     | D9          | Green               |
| 2     | Left     | D10         | Red                 |
| 3     | Right    | D11         | Brown               |
| 4     | Aux      | D12         | Black               |
| 5     | Reverse  | D13         | Yellow              |

**Wiring each relay:**
1. Connect relay signal pin to corresponding Feather GPIO
2. Connect relay VCC to 5V
3. Connect relay GND to GND
4. Wire relay NO (Normally Open) terminal to output connector
5. Wire relay COM (Common) terminal to 12V power

### Step 6: NeoPixel Strip

1. **Mount NeoPixel stick** on breadboard
2. **Connect power:**
   - VCC → 5V
   - GND → GND
3. **Connect data:**
   - DIN → Feather D5

**⚠️ NeoPixels draw significant current!** Ensure buck converter can supply at least 200mA for LEDs.

### Step 7: Control Buttons

1. **Mode button (D24):**
   - One terminal → D24
   - Other terminal → GND
   - Internal pull-up used (no external resistor needed)

2. **Test button (D25):**
   - One terminal → D25
   - Other terminal → GND
   - Internal pull-up used

### Step 8: 7-Way Connectors

**Male connector (vehicle input side):**
- Wire each pin to its corresponding voltage divider input
- Pin 1 (Ground/White) → Common GND

**Female connector (trailer output side):**
- Wire each pin to its corresponding relay NO terminal
- Pin 1 (Ground/White) → Common GND

**Color coding (RV 7-Way Standard):**
| Pin | Function | Color  |
|-----|----------|--------|
| 1   | Ground   | White  |
| 2   | Brake    | Blue   |
| 3   | Tail     | Green  |
| 4   | Left     | Red    |
| 5   | Right    | Brown  |
| 6   | Aux      | Black  |
| 7   | Reverse  | Yellow |

---

## Final Assembly Checklist

Before applying power:

- [ ] All solder joints are clean and solid
- [ ] No shorts between power rails (test with multimeter)
- [ ] Buck converter outputs 5V (verify with multimeter)
- [ ] All I2C devices have correct addresses (use I2C scanner if needed)
- [ ] Voltage dividers properly scaled (10K + 2.7K = 12.7K total)
- [ ] Zener diodes oriented correctly (cathode to signal, anode to GND)
- [ ] 10A fuse installed on 12V input
- [ ] All connections are mechanically secure
- [ ] Feather and FeatherWing properly seated

---

## Common Assembly Mistakes

### Power Issues
- **Buck converter backwards:** Verify polarity before connecting
- **Insufficient current capacity:** Use 3A minimum buck converter
- **No fusing:** Always fuse the 12V input!

### I2C Issues
- **Missing pull-ups:** I2C won't work without 4.7kΩ pull-ups on SDA/SCL
- **Wrong addresses:** Verify ADDR pin connections (0x48 vs 0x49)
- **Loose connections:** I2C is sensitive to connection quality

### Voltage Divider Issues
- **Wrong resistor values:** Double-check with multimeter
- **Zener backwards:** Cathode (marked end) goes to signal side
- **Missing zener:** ADC inputs can be damaged without protection

### Relay Issues
- **Wrong relay terminals:** Use NO (Normally Open), not NC
- **Insufficient 5V:** Relays draw significant current when energized
- **Contact ratings:** Ensure relays rated for at least 5A

---

## Testing the Assembly

### Initial Power-On Test

1. **Connect 12V power** (with inline fuse)
2. **Check Feather power LED** - should be lit
3. **Check OLED splash screen** - should display "7-Way Trailer Tester"
4. **Check NeoPixel startup animation** - should light up sequentially

If any of these fail, **immediately disconnect power** and troubleshoot.

### Relay Test

In Trailer Tester mode:
1. Press Mode button until "TRAILER_TESTER" shows on OLED
2. Press Test button
3. **Listen for relay clicks** - each relay should click on/off
4. **Watch NeoPixels** - should light up in sequence
5. **Measure relay outputs** - should show 12V when active

### Input Test

In Vehicle Tester mode:
1. Press Mode button until "VEHICLE_TESTER" shows on OLED
2. Connect a 12V test voltage to Brake input (Pin 2, Blue)
3. **Check OLED display** - should show approximately 12V for Brake channel
4. **Check NeoPixel** - LED #1 (Brake) should be bright blue
5. Repeat for each channel

**Expected reading:** 11.5V - 12.5V (depending on supply and calibration)

---

## Next Steps

After successful assembly and testing:

1. **Read [`USER_MANUAL.md`](USER_MANUAL.md)** - Learn how to operate the device
2. **Review [`HARDWARE_DESIGN.md`](HARDWARE_DESIGN.md)** - Understand circuit design
3. **Perform voltage calibration** (see `CALIBRATION_PROCEDURE.md`)
4. **Field test** with actual vehicle and trailer

---

## Support

Having issues? Check the troubleshooting section in [`USER_MANUAL.md`](USER_MANUAL.md).

---

*Assembly guide v1.0 - December 2024*
