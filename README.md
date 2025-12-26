# trailer-tester

A bidirectional 7-way trailer wiring controller tester built with Adafruit CircuitPython hardware.

## Features

- **Vehicle Tester Mode** - Plug into tow vehicle, read and display voltage on all 6 trailer circuits
- **Trailer Tester Mode** - Plug into trailer, output 12V test signals to verify lights work
- **Pass-Through Mode** - Connect both, monitor signals in real-time
- **NeoPixel Status Display** - Color-coded LEDs show circuit status at a glance
- **OLED Information Display** - 128x64 screen shows mode, voltages, and status
- **Desktop Simulator** - Develop and test firmware without hardware

## Hardware

Built with Adafruit components:
- Feather RP2040 (main controller)
- 128x64 OLED FeatherWing (display)
- NeoPixel Stick 8x (status LEDs)
- ADS1115 16-bit ADC x2 (voltage sensing)
- 4-channel relay boards x2 (output switching)

See [`docs/HARDWARE_DESIGN.md`](docs/HARDWARE_DESIGN.md) for full specifications and [`docs/SHOPPING_LIST.md`](docs/SHOPPING_LIST.md) for part numbers.

## Quick Start

### Desktop Simulation (No Hardware Required)

```bash
# Clone the repo
git clone https://github.com/yourusername/trailer-tester.git
cd trailer-tester

# Run automated tests
python3 simulator/test_firmware.py

# Launch interactive simulator
python3 simulator/run_simulator.py
```

### On Hardware

1. Install CircuitPython 8.x on your Feather RP2040
2. Copy contents of `firmware/` to the CIRCUITPY drive
3. Install required CircuitPython libraries:
   - `adafruit_ads1x15`
   - `adafruit_displayio_sh1107`
   - `neopixel`

## Project Structure

```
trailer-tester/
├── firmware/           # CircuitPython firmware
│   ├── code.py        # Main entry point
│   ├── logger.py      # Centralized logging
│   ├── adc_manager.py # Voltage reading (ADS1115)
│   ├── relay_manager.py
│   ├── neopixel_manager.py
│   ├── display_manager.py
│   └── test_modes.py
├── simulator/          # Desktop simulation
│   ├── mock_*.py      # Mock hardware modules
│   ├── sim_state.py   # Simulation state
│   ├── test_firmware.py
│   └── run_simulator.py
├── docs/
│   ├── HARDWARE_DESIGN.md
│   └── SHOPPING_LIST.md
├── PROJECT_BRIEF.md
├── DEVELOPMENT_PLAN.md
└── CLAUDE.md
```

## 7-Way Connector Pinout

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | Ground | White |
| 2 | Electric Brakes | Blue |
| 3 | Tail/Running Lights | Brown |
| 4 | Left Turn/Brake | Yellow |
| 5 | Right Turn/Brake | Green |
| 6 | 12V Auxiliary | Red |
| 7 | Reverse Lights | Purple |

## Development

This project uses the DevPlan methodology for structured development.

```bash
# Run tests
make test

# Lint code
make lint

# Format code
make format
```

See [`DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md) for task tracking and [`CLAUDE.md`](CLAUDE.md) for coding standards.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Mike Morris - Quick SCIF LLC
