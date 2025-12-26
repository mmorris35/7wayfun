# Circuit Diagrams

This directory contains circuit diagrams for the trailer-tester project. All diagrams are viewable directly in GitHub.

## Diagram Index

### System Architecture
- **system_architecture.md** - High-level Mermaid block diagram
- **system_architecture.svg** - Detailed SVG architecture diagram

### Circuit Schematics
- **voltage_divider.svg** - Voltage divider circuit for ADC inputs
- **power_supply.svg** - 12V to 5V/3.3V power conversion
- **i2c_bus.svg** - I2C topology showing ADCs and OLED
- **relay_outputs.svg** - Relay driver circuit
- **full_schematic.svg** - Complete breadboard schematic

### Connector Diagrams
- **connector_pinout.svg** - 7-way connector pinout (RV 7-Way Standard)

## Generation

Diagrams are generated using:
- **Schemdraw** - Python library for circuit diagrams
- **Mermaid** - Text-based diagrams in markdown
- **Manual SVG** - Hand-crafted for specific needs

To regenerate diagrams:
```bash
python3 docs/diagrams/generate_diagrams.py
```

## Viewing

All diagrams render directly in GitHub's web interface. Click on any `.svg` or `.md` file to view.
