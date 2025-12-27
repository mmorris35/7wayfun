# Project Brief: trailer-tester

## Overview

| Field | Value |
|-------|-------|
| **Project Name** | trailer-tester |
| **Project Type** | Embedded Firmware (CircuitPython) |
| **Goal** | Bidirectional 7-way trailer wiring tester that can test vehicle signals, trailer lights, and monitor pass-through connections |
| **Timeline** | 2 weeks |
| **Team Size** | 1 |

## Target Users

- RV owners diagnosing trailer lighting issues
- Trailer owners verifying wiring before trips
- Mobile mechanics servicing trailer electrical systems
- DIY automotive enthusiasts

## Features

### Must-Have (MVP)

1. **Vehicle Tester Mode** - Plug into tow vehicle's 7-way connector, read and display voltage on all 6 circuits (brake, tail, left, right, aux, reverse)
2. **Trailer Tester Mode** - Plug into trailer, output 12V test signals to cycle through and verify each trailer light circuit
3. **Pass-Through Mode** - Connect both vehicle and trailer, monitor signals in real-time as they pass through
4. **Automatic Fault Diagnosis** - Analyzes voltage readings to detect common wiring faults (voltage drops, weak signals, cross-wiring, ground faults) with confidence scoring and suggested fixes
5. **NeoPixel Status Display** - 8-LED strip showing color-coded status for each circuit (active, idle, fault)
6. **OLED Information Display** - 128x64 display showing current mode, voltage readings, and status messages
7. **Desktop Simulator** - Mock hardware for firmware development and testing without physical components

### Nice-to-Have (v2)

- Data logging to SD card for diagnostic history
- Bluetooth connectivity for mobile app integration
- Diagnostic trend analysis for intermittent faults
- Production PCB design (replace breadboard prototype)

## Technical Requirements

### Tech Stack

| Component | Technology |
|-----------|------------|
| Language | CircuitPython 8.x/9.x |
| MCU | Adafruit Feather RP2040 |
| ADC | ADS1115 16-bit (x2 via I2C) |
| Display | SH1107 128x64 OLED |
| LEDs | WS2812B NeoPixel (8x) |
| Relays | 4-channel STEMMA boards (x2) |
| Desktop Testing | Python 3.8+ with mock modules |

### Hardware Constraints

- Must handle 12-14.4V automotive voltages safely
- Voltage dividers scale input to 3.3V ADC range
- Zener diode protection on all inputs
- 10A fuse on main power input
- Relays rated for 10A per channel

### Software Constraints

- All firmware modules must be testable via desktop simulator
- No external dependencies beyond Adafruit CircuitPython libraries
- Centralized logging in all modules
- Descriptive variable names (no single letters)

## 7-Way Connector Pinout (RV 7-Way Standard)

| Pin | Function | Wire Color | Test Method |
|-----|----------|------------|-------------|
| 1 | Ground | White | Reference (not tested) |
| 2 | Electric Brakes | Blue | ADC + Relay |
| 3 | Tail/Running | Green | ADC + Relay |
| 4 | Left Turn/Brake | Red | ADC + Relay |
| 5 | Right Turn/Brake | Brown | ADC + Relay |
| 6 | 12V Auxiliary | Black | ADC + Relay |
| 7 | Reverse Lights | Yellow | ADC + Relay |

## Success Criteria

1. All three operating modes functional and switchable via button
2. Voltage readings accurate within 0.5V of actual
3. NeoPixels correctly indicate active/idle/fault states
4. OLED displays current mode and readings clearly
5. Desktop simulator passes all firmware tests
6. Documentation complete (hardware design, BOM, assembly guide)

## Out of Scope (MVP)

- Mobile app integration
- Cloud connectivity
- Production enclosure design
- Automated manufacturing documentation
- Compliance certifications

---

*Generated for DevPlan methodology*
