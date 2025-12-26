# 7-Way Trailer Tester Simulator

Desktop simulation environment for developing and testing the trailer tester firmware without physical hardware.

## Quick Start

```bash
# Run the automated tests
python3 simulator/test_firmware.py

# Run the interactive terminal simulator
python3 simulator/run_simulator.py
```

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

## Architecture

The simulator works by mocking all CircuitPython hardware modules:

```
simulator/
├── mock_board.py              # GPIO pin definitions
├── mock_digitalio.py          # Digital I/O (buttons, relays)
├── mock_neopixel.py           # NeoPixel LED strip
├── mock_displayio.py          # Display framework
├── mock_terminalio.py         # Terminal font
├── mock_adafruit_display_text.py  # Text labels
├── mock_adafruit_displayio_sh1107.py  # OLED driver
├── mock_adafruit_ads1x15.py   # ADC voltage reading
├── mock_busio.py              # I2C/SPI buses
├── mock_micropython.py        # MicroPython compat
├── sim_state.py               # Simulation state manager
├── run_simulator.py           # Interactive terminal UI
└── test_firmware.py           # Automated tests
```

## Interactive Simulator Controls

When running `run_simulator.py`:

| Key | Action |
|-----|--------|
| `m` | Press mode button (cycle: Vehicle -> Trailer -> Pass-through) |
| `t` | Press test button (trigger test sequence in trailer mode) |
| `1` | Toggle brake signal (12V / 0V) |
| `2` | Toggle tail light signal |
| `3` | Toggle left turn signal |
| `4` | Toggle right turn signal |
| `5` | Toggle aux power signal |
| `6` | Toggle reverse signal |
| `a` | All signals ON (12V) |
| `o` | All signals OFF |
| `r` | Running lights preset (tail + aux) |
| `b` | Braking preset (tail + aux + brake + left + right) |
| `q` | Quit |

## Simulation State

The `SimulationState` class provides programmatic control:

```python
from sim_state import get_simulation_state

sim = get_simulation_state()

# Set vehicle signals
sim.set_vehicle_signal("brake", 11.8)  # 11.8V on brake wire
sim.set_vehicle_signal("tail", 12.0)

# Presets
sim.set_running_lights()  # tail + aux on
sim.set_braking()         # all brake lights on
sim.set_left_turn()
sim.set_right_turn()
sim.set_reverse()

# Read relay outputs (what tester is sending to trailer)
states = sim.get_relay_states()
# {'brake': False, 'tail': True, 'left': False, ...}

# Simulate button presses
sim.press_mode_button()
sim.release_mode_button()

# Get NeoPixel display for visualization
display = sim.get_neopixel_display()
# "[C] [b] [Y] [y] [g] [r] [p] [G]"
```

## Writing Tests

```python
from sim_state import get_simulation_state
import sys, os
sys.path.insert(0, "simulator")
sys.path.insert(0, "firmware")

# Import simulation state first (patches sys.modules)
sim = get_simulation_state()

# Now import firmware
from code import TrailerTester

# Create app and test
app = TrailerTester()
sim.set_vehicle_signal("left", 12.0)
readings = app._read_all_channels()
assert readings["left"] > 10.0

app.shutdown()
```

## Limitations

The simulator cannot test:
- Actual timing-sensitive behavior (uses desktop Python timing)
- Real I2C/GPIO electrical characteristics
- Power consumption
- EMI/noise behavior

Always verify with real hardware before deployment.
