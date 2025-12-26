# 7-Way Trailer Wiring Controller Tester

## Design Overview

A bidirectional tester for standard 7-way RV/trailer connectors that can:
1. **Vehicle Mode**: Plug into a trailer to simulate loads and verify trailer wiring
2. **Trailer Mode**: Plug into a vehicle to read and display what signals the tow vehicle is sending

## 7-Way Connector Pinout (SAE J2863 Standard)

| Pin | Function              | Wire Color | Notes                          |
|-----|-----------------------|------------|--------------------------------|
| 1   | Ground                | White      | Common return, not tested      |
| 2   | Electric Brakes       | Blue       | 0-12V proportional (PWM-ish)   |
| 3   | Tail/Running Lights   | Brown      | 12V when headlights on         |
| 4   | Left Turn/Brake       | Yellow     | 12V pulsed or steady           |
| 5   | Right Turn/Brake      | Green      | 12V pulsed or steady           |
| 6   | 12V Auxiliary/Charge  | Red        | 12V-14.4V continuous           |
| 7   | Reverse Lights        | Purple     | 12V when in reverse            |

## System Architecture

```
                                    +------------------+
                                    |   NeoPixel Bar   |
                                    |   (8 LEDs)       |
                                    +--------+---------+
                                             |
+-------------+     +------------------+     |     +------------------+
|  7-Way      |     |                  |     |     |                  |
|  Connector  +---->+  Input Stage     +---->+---->+  Feather RP2040  |
|  (Vehicle)  |     |  (Voltage Div)   |     |     |                  |
+-------------+     +------------------+     |     +--------+---------+
                                             |              |
+-------------+     +------------------+     |              |
|  7-Way      |     |                  |     |     +--------+---------+
|  Connector  +<----+  Output Stage    +<----+     |   OLED Display   |
|  (Trailer)  |     |  (MOSFET/Relay)  |           |   (128x64)       |
+-------------+     +------------------+           +------------------+
                            ^
                            |
                    +-------+--------+
                    |  12V Vehicle   |
                    |  Power Input   |
                    +----------------+
```

## Operating Modes

### Mode 1: Trailer Tester (Output Mode)
- Connect female 7-way to trailer
- Microcontroller drives MOSFETs to send 12V test signals
- Cycles through: Left, Right, Brake, Running, Reverse, Aux
- NeoPixels show which output is active
- OLED shows test pattern status

### Mode 2: Vehicle Tester (Input Mode)  
- Connect male 7-way to vehicle's trailer connector
- Voltage dividers scale 12V signals to 3.3V for ADC
- Reads actual voltage on each pin
- NeoPixels show on/off status per pin (color-coded)
- OLED shows actual voltage readings

### Mode 3: Pass-Through Test
- Both connectors attached
- Vehicle signals pass through to trailer
- Tester monitors and displays all signals in real-time
- Useful for diagnosing intermittent issues

## Bill of Materials

### Core Electronics (Adafruit)

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 1   | 4884        | Feather RP2040                        | $11.95     | Main controller                 |
| 1   | 4650        | FeatherWing OLED 128x64               | $14.95     | Plugs directly onto Feather     |
| 1   | 1426        | NeoPixel Stick (8x WS2812B)           | $5.95      | 7 channels + 1 status           |
| 2   | 1085        | ADS1115 16-Bit ADC (4 channel)        | $14.95 ea  | 8 total ADC channels via I2C    |
| 1   | 2745        | STEMMA QT / Qwiic JST SH 4-pin Cable  | $0.95      | I2C daisy chain                 |
| 1   | 4210        | STEMMA QT SparkFun Qwiic / Breadboard | $1.50      | For breadboard prototyping      |
| 1   | 4399        | Feather Stacking Headers              | $1.25      | To stack OLED wing              |
| 1   | 2830        | USB-C to USB-C Cable                  | $4.95      | Programming/debugging           |

### Power Management

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 1   | 1385        | DC-DC Buck Converter 5V 3A (Mini560)  | $4.95      | 12V vehicle → 5V logic          |
| 1   | 3628        | Terminal Block 2-pin 5mm (5 pack)     | $2.50      | Power input connections         |

### Output Stage (MOSFET Switching)

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 2   | 5648        | 4-Channel STEMMA Relay Board          | $9.95 ea   | 8 relays total, 7 needed        |

**OR** (Alternative - individual MOSFETs, more advanced):

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 8   | 355         | N-Channel Power MOSFET (30V/60A)      | $1.75 ea   | IRLB8721 logic-level            |
| 8   | -           | 1N4007 Flyback Diode                  | $0.10 ea   | Inductive load protection       |
| 8   | -           | 10K Resistor (gate pulldown)          | $0.05 ea   | Default off state               |

**Recommendation**: Use the STEMMA relay boards for prototype. Much simpler, no heat issues, audible click for debugging.

### Input Stage (Voltage Sensing)

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 1   | 2892        | Through-Hole Resistor Kit             | $7.95      | Various values for dividers     |
| 7   | -           | 10K + 3.3K resistors (from kit)       | -          | 4:1 divider (12V → 3V)          |
| 7   | -           | 3.3V Zener Diode (1N4728)             | $0.10 ea   | Overvoltage protection          |

### Connectors and Wiring

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 1   | -           | 7-Way Trailer Plug (Male) - Vehicle   | ~$8        | Amazon/hardware store           |
| 1   | -           | 7-Way Trailer Socket (Female) - Trail | ~$8        | Amazon/hardware store           |
| 1   | 3314        | Silicone Wire 22AWG (various colors)  | $9.95      | Hook-up wire                    |
| 1   | 64          | Half-Size Breadboard                  | $5.00      | Main prototype board            |
| 1   | 239         | Full-Size Breadboard                  | $5.95      | If more space needed            |
| 1   | 153         | Breadboard Jumper Wires               | $6.95      | Connections                     |

### Enclosure and Misc

| Qty | Part Number | Description                           | Unit Price | Notes                           |
|-----|-------------|---------------------------------------|------------|---------------------------------|
| 1   | -           | Project Box (approx 6"x4"x2")         | ~$10       | Weather-resistant preferred     |
| 1   | -           | Automotive Blade Fuse Holder (inline) | ~$3        | 10A fuse for main power         |
| 1   | 3299        | Tactile Button Assortment             | $6.95      | Mode select, test trigger       |
| 1   | 4184        | SPDT Slide Switch                     | $0.95      | Power on/off                    |

## Voltage Divider Calculation

Vehicle systems can see 14.4V (alternator running) or transients higher. Design for 15V max input.

Target: Scale 15V → 3.0V (under 3.3V ADC reference)

Using R1 = 10K, R2 = 2.7K (close enough from kit):
- Vout = Vin * R2 / (R1 + R2)
- Vout = 15V * 2.7K / 12.7K = 3.19V  ✓

Actual ratio: 12.7K / 2.7K = 4.7:1
Software scaling factor: 4.7

Add 3.3V zener diode in parallel with R2 for overvoltage protection.

```
12V Input ----[10K]----+----[2.7K]---- GND
                       |
                       +---- To ADC
                       |
                    [3.3V Zener]
                       |
                      GND
```

## GPIO Pin Assignment (Feather RP2040)

| GPIO | Function              | Notes                               |
|------|-----------------------|-------------------------------------|
| D5   | NeoPixel Data Out     | 8-LED strip                         |
| D6   | Relay 1 (Brakes)      | Blue wire                           |
| D9   | Relay 2 (Tail)        | Brown wire                          |
| D10  | Relay 3 (Left Turn)   | Yellow wire                         |
| D11  | Relay 4 (Right Turn)  | Green wire                          |
| D12  | Relay 5 (Aux 12V)     | Red wire                            |
| D13  | Relay 6 (Reverse)     | Purple wire                         |
| D24  | Mode Button           | Cycle through modes                 |
| D25  | Test Button           | Trigger test sequence               |
| SDA  | I2C Data              | OLED + 2x ADS1115                   |
| SCL  | I2C Clock             | OLED + 2x ADS1115                   |
| A0   | Backup analog (brake) | Direct ADC if needed                |
| A1   | Backup analog         | Direct ADC if needed                |

### I2C Addresses
- OLED Display: 0x3C (or 0x3D)
- ADS1115 #1: 0x48 (ADDR → GND) - Channels: Brake, Tail, Left, Right
- ADS1115 #2: 0x49 (ADDR → VDD) - Channels: Aux, Reverse, spare, spare

## NeoPixel Color Coding

| LED # | Channel      | Off         | Active      | Fault       |
|-------|--------------|-------------|-------------|-------------|
| 0     | Status       | Dim white   | Mode color  | Red blink   |
| 1     | Brakes       | Dim blue    | Bright blue | Red         |
| 2     | Tail/Running | Dim brown   | Yellow      | Red         |
| 3     | Left Turn    | Dim yellow  | Bright yel  | Red         |
| 4     | Right Turn   | Dim green   | Bright grn  | Red         |
| 5     | Aux 12V      | Dim red     | Bright red  | Red blink   |
| 6     | Reverse      | Dim purple  | Bright purp | Red         |
| 7     | Ground       | Dim white   | Green       | Red         |

## OLED Display Layout (128x64)

```
+---------------------------+
| MODE: VEHICLE TESTER      |  <- Line 0: Current mode
|---------------------------|
| BRK: 11.8V  [====    ]    |  <- Line 1: Brake circuit
| TAIL: 0.0V  [        ]    |  <- Line 2: Tail lights
| LEFT: 12.1V [========]    |  <- Line 3: Left turn
| RIGHT: 0.0V [        ]    |  <- Line 4: Right turn
| AUX: 13.2V  [========]    |  <- Line 5: Aux power
| REV: 0.0V   [        ]    |  <- Line 6: Reverse
+---------------------------+
```

## Safety Considerations

1. **Fused Power Input**: 10A automotive fuse on main 12V input
2. **Reverse Polarity Protection**: Schottky diode or P-FET on power input
3. **Transient Protection**: TVS diode on 12V input rail (P6KE18A - 18V standoff)
4. **Ground Isolation**: Common ground between vehicle/trailer sides
5. **Current Limiting**: Relays rated for 10A, individual circuits unlikely to exceed 5A

## Assembly Order

1. Solder stacking headers to Feather RP2040
2. Attach OLED FeatherWing
3. Wire buck converter (12V in, 5V out to Feather USB)
4. Set up breadboard with voltage dividers and zener protection
5. Connect ADS1115 boards via I2C (STEMMA cables)
6. Wire relay boards to GPIO outputs
7. Connect NeoPixel stick
8. Wire 7-way connectors (use color-coded wires matching standard)
9. Add buttons for mode/test control
10. Load CircuitPython and test software

## Estimated Total Cost

| Category            | Approximate Cost |
|---------------------|------------------|
| Adafruit Electronics| $95-110          |
| Connectors/Wiring   | $30-40           |
| Protection/Misc     | $15-20           |
| Enclosure           | $10-15           |
| **Total**           | **$150-185**     |

## Next Steps

1. [ ] Order components
2. [ ] Write CircuitPython firmware
3. [ ] Breadboard prototype
4. [ ] Test with bench power supply first
5. [ ] Test with actual vehicle/trailer
6. [ ] Design PCB for production version
