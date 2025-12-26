#!/usr/bin/env python3
"""
Generate circuit diagrams for trailer-tester using Schemdraw.

This script generates SVG circuit diagrams that can be viewed
directly in GitHub.

Requirements:
    pip install schemdraw

Usage:
    python3 docs/diagrams/generate_diagrams.py
"""

import os
import sys

try:
    import schemdraw
    import schemdraw.elements as elm
except ImportError:
    print("ERROR: schemdraw not installed")
    print("Install with: pip install schemdraw")
    sys.exit(1)

# Output directory
DIAGRAM_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_voltage_divider():
    """Generate voltage divider circuit diagram."""
    print("Generating voltage_divider.svg...")

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=12, font='sans-serif')

        # Input from vehicle
        d += (vin := elm.SourceV().label('12V\nVehicle\nInput'))
        d += elm.Line().right(0.5)
        d += (r1 := elm.Resistor().right().label('R1\n10kΩ'))
        d += elm.Line().right(0.5)
        d += elm.Dot()
        d.push()  # Save position for output tap

        # Zener protection
        d += elm.Line().right(0.5)
        d += (zener := elm.Zener().down().reverse().label('3.6V\nZener', loc='bottom'))
        d += elm.Line().to(vin.start)

        # Output to ADC
        d.pop()  # Return to tap position
        d += elm.Line().down(0.5)
        d += elm.Gap().down().label(['+', 'To ADC\nInput', '−'])
        d += (r2 := elm.Resistor().down().label('R2\n2.7kΩ'))
        d += elm.Line().down(0.5)
        d += (gnd := elm.Ground())

        # Annotations
        d += elm.Label().at((r1.end[0] + 1.5, r1.end[1] + 1)).label(
            'Voltage Scaling:\nVout = Vin × (R2/(R1+R2))\nVout = 12V × 0.213 = 2.55V',
            fontsize=10
        )

        d.save(os.path.join(DIAGRAM_DIR, 'voltage_divider.svg'))


def generate_power_supply():
    """Generate power supply circuit diagram."""
    print("Generating power_supply.svg...")

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=12, font='sans-serif')

        # 12V input
        d += (vin := elm.SourceV().label('12V\nVehicle'))
        d += elm.Line().right(0.5)
        d += (fuse := elm.Fuse().right().label('10A\nFuse'))
        d += elm.Line().right(0.5)

        # Buck converter to 5V
        d += elm.Dot()
        d.push()
        d += elm.Ic(pins=[
            elm.IcPin(name='IN', side='left', pin='1'),
            elm.IcPin(name='OUT', side='right', pin='2'),
            elm.IcPin(name='GND', side='bottom', pin='3'),
        ], size=(2, 1.5)).right().label('Buck\nConverter\n12V→5V')

        # 5V output
        d += elm.Line().right(0.5)
        d += elm.Dot()
        d.push()
        d += elm.Label().label('5V\nLogic')
        d.pop()

        # LDO to 3.3V
        d += elm.Line().down(0.5)
        d += elm.Ic(pins=[
            elm.IcPin(name='IN', side='top', pin='1'),
            elm.IcPin(name='OUT', side='bottom', pin='2'),
            elm.IcPin(name='GND', side='left', pin='3'),
        ], size=(1.5, 1.5)).label('LDO\n5V→3.3V')
        d += elm.Line().down(0.5)
        d += elm.Label().label('3.3V\nAnalog')

        # Ground
        d.pop()
        d.pop()
        d += elm.Line().down(2)
        d += elm.Ground()

        d.save(os.path.join(DIAGRAM_DIR, 'power_supply.svg'))


def generate_i2c_bus():
    """Generate I2C bus topology diagram."""
    print("Generating i2c_bus.svg...")

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=12, font='sans-serif')

        # RP2040 I2C master
        d += (rp2040 := elm.Ic(pins=[
            elm.IcPin(name='SDA', side='right', pin='1'),
            elm.IcPin(name='SCL', side='right', pin='2'),
        ], size=(2, 2)).label('RP2040\nI2C Master'))

        # SDA line
        d += elm.Line().at(rp2040.SDA).right(1)
        d += elm.Dot()
        d.push()

        # ADC #1
        d += elm.Line().up(1)
        d += elm.Ic(pins=[
            elm.IcPin(name='SDA', side='left', pin='1'),
            elm.IcPin(name='SCL', side='left', pin='2'),
        ], size=(2, 1.5)).right().label('ADS1115\n0x48', loc='center')
        d.pop()

        # ADC #2
        d += elm.Dot()
        d.push()
        d += elm.Line().right(2.5)
        d += elm.Ic(pins=[
            elm.IcPin(name='SDA', side='left', pin='1'),
            elm.IcPin(name='SCL', side='left', pin='2'),
        ], size=(2, 1.5)).right().label('ADS1115\n0x49', loc='center')
        d.pop()

        # OLED Display
        d += elm.Line().down(1)
        d += elm.Ic(pins=[
            elm.IcPin(name='SDA', side='left', pin='1'),
            elm.IcPin(name='SCL', side='left', pin='2'),
        ], size=(2, 1.5)).right().label('SH1107\n0x3C', loc='center')

        # SCL line
        d += elm.Line().at(rp2040.SCL).right(5.5)
        d += elm.Dot()

        # Pull-up resistors
        d += elm.Line().at(rp2040.SDA).right(0.5).up(1.5)
        d += elm.Resistor().up().label('4.7kΩ\nPullup')
        d += elm.Line().up(0.5)
        d += elm.Vdd().label('3.3V')

        d += elm.Line().at(rp2040.SCL).right(0.5).up(1.5)
        d += elm.Resistor().up().label('4.7kΩ\nPullup')
        d += elm.Line().up(0.5)
        d += elm.Vdd().label('3.3V')

        d.save(os.path.join(DIAGRAM_DIR, 'i2c_bus.svg'))


def generate_relay_driver():
    """Generate relay driver circuit."""
    print("Generating relay_outputs.svg...")

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=12, font='sans-serif')

        # GPIO from RP2040
        d += elm.Line().right(0.5).label('GPIO\nD6-D13', loc='left')
        d += elm.Dot()
        d.push()

        # NPN transistor driver (optional - STEMMA relays have drivers)
        d += elm.Line().right(0.5)
        d += (relay := elm.Relay(unit=3, cyclinder=True).right().scale(1.5).label('STEMMA\nRelay\n10A'))
        d += elm.Line().right(0.5)
        d += elm.Dot()
        d.push()
        d += elm.Label().label('To Trailer\nConnector')

        # 12V power to relay
        d.pop()
        d += elm.Line().up(1)
        d += elm.Line().left(2)
        d += elm.Vdd().label('12V')

        # Flyback diode
        d.pop()
        d += elm.Line().down(0.5)
        d += elm.Diode().down().flip().label('Flyback\nDiode')
        d += elm.Line().down(0.5)
        d += elm.Ground()

        # Note
        d += elm.Label().at((4, 2)).label(
            'STEMMA Relay Board includes:\n- Driver transistor\n- Flyback diode\n- LED indicator',
            fontsize=10
        )

        d.save(os.path.join(DIAGRAM_DIR, 'relay_outputs.svg'))


def main():
    """Generate all circuit diagrams."""
    print("=" * 60)
    print("Generating Circuit Diagrams for trailer-tester")
    print("=" * 60)

    try:
        generate_voltage_divider()
        generate_power_supply()
        generate_i2c_bus()
        generate_relay_driver()

        print("=" * 60)
        print("All diagrams generated successfully!")
        print(f"Output directory: {DIAGRAM_DIR}")
        print("=" * 60)

    except Exception as e:
        print(f"ERROR: Failed to generate diagrams: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
