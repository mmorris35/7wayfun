# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Simulation State Manager for the trailer tester.

Manages the simulated hardware state and provides methods for
setting up test scenarios.

Author: Mike Morris
License: GNU GPL v3
"""

import sys
import os

# Add simulator directory to path for mock imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Install mocks before importing firmware modules
import mock_board as board
import mock_digitalio as digitalio
import mock_neopixel as neopixel
import mock_displayio as displayio
import mock_terminalio as terminalio
import mock_adafruit_display_text as adafruit_display_text
import mock_adafruit_displayio_sh1107 as adafruit_displayio_sh1107
import mock_adafruit_ads1x15 as adafruit_ads1x15
import mock_micropython as micropython
import mock_busio as busio

# Patch sys.modules so firmware imports work
sys.modules['board'] = board
sys.modules['digitalio'] = digitalio
sys.modules['neopixel'] = neopixel
sys.modules['displayio'] = displayio
sys.modules['terminalio'] = terminalio
sys.modules['busio'] = busio
sys.modules['adafruit_display_text'] = adafruit_display_text
sys.modules['adafruit_displayio_sh1107'] = adafruit_displayio_sh1107
sys.modules['adafruit_ads1x15'] = adafruit_ads1x15
sys.modules['adafruit_ads1x15.ads1115'] = adafruit_ads1x15  # ADS1115 class is in this module
sys.modules['adafruit_ads1x15.analog_in'] = adafruit_ads1x15  # AnalogIn class is also here
sys.modules['micropython'] = micropython

# Make adafruit_ads1x15 behave like a package with ads1115 submodule
adafruit_ads1x15.ads1115 = adafruit_ads1x15


class SimulationState:
    """
    Manages the overall simulation state.
    
    Provides methods to:
    - Set simulated vehicle signals (for vehicle tester mode)
    - Monitor relay outputs (for trailer tester mode)
    - Simulate button presses
    - Get display state for visualization
    """
    
    # Channel to ADC mapping (matches firmware)
    CHANNEL_MAP = {
        "brake": (0x48, 0),
        "tail": (0x48, 1),
        "left": (0x48, 2),
        "right": (0x48, 3),
        "aux": (0x49, 0),
        "reverse": (0x49, 1),
    }
    
    # Voltage divider ratio (matches hardware design)
    VOLTAGE_DIVIDER_RATIO = 4.7
    
    def __init__(self):
        self.vehicle_signals = {
            "brake": 0.0,
            "tail": 0.0,
            "left": 0.0,
            "right": 0.0,
            "aux": 0.0,
            "reverse": 0.0,
        }
    
    def set_vehicle_signal(self, channel, voltage):
        """
        Set a simulated vehicle signal voltage.
        
        Args:
            channel: Channel name (brake, tail, left, right, aux, reverse)
            voltage: Actual vehicle voltage (0-14V range)
        """
        if channel not in self.CHANNEL_MAP:
            raise ValueError(f"Unknown channel: {channel}")
        
        self.vehicle_signals[channel] = voltage
        
        # Calculate voltage after divider
        adc_voltage = voltage / self.VOLTAGE_DIVIDER_RATIO
        
        # Set in mock ADC
        address, chan = self.CHANNEL_MAP[channel]
        adafruit_ads1x15.ADS1115.set_simulated_voltage(address, chan, adc_voltage)
    
    def set_all_signals_off(self):
        """Turn off all simulated vehicle signals."""
        for channel in self.CHANNEL_MAP:
            self.set_vehicle_signal(channel, 0.0)
    
    def set_running_lights(self):
        """Simulate running lights on (tail lights active)."""
        self.set_vehicle_signal("tail", 12.0)
        self.set_vehicle_signal("aux", 13.2)
    
    def set_left_turn(self):
        """Simulate left turn signal."""
        self.set_vehicle_signal("left", 12.0)
    
    def set_right_turn(self):
        """Simulate right turn signal."""
        self.set_vehicle_signal("right", 12.0)
    
    def set_braking(self):
        """Simulate braking."""
        self.set_vehicle_signal("brake", 11.8)
        self.set_vehicle_signal("left", 12.0)
        self.set_vehicle_signal("right", 12.0)
    
    def set_reverse(self):
        """Simulate reverse."""
        self.set_vehicle_signal("reverse", 12.0)
    
    def press_mode_button(self):
        """Simulate mode button press."""
        digitalio.DigitalInOut.set_input("D24", False)
    
    def release_mode_button(self):
        """Simulate mode button release."""
        digitalio.DigitalInOut.set_input("D24", True)
    
    def press_test_button(self):
        """Simulate test button press."""
        digitalio.DigitalInOut.set_input("D25", False)
    
    def release_test_button(self):
        """Simulate test button release."""
        digitalio.DigitalInOut.set_input("D25", True)
    
    def get_relay_states(self):
        """Get current state of all relay outputs."""
        states = {}
        relay_pins = ["D6", "D9", "D10", "D11", "D12", "D13"]
        relay_names = ["brake", "tail", "left", "right", "aux", "reverse"]
        
        for pin_name, relay_name in zip(relay_pins, relay_names):
            pin = digitalio.DigitalInOut.get_pin(pin_name)
            if pin:
                states[relay_name] = pin._value
            else:
                states[relay_name] = False
        
        return states
    
    def get_neopixel_state(self):
        """Get current NeoPixel colors."""
        neopix = neopixel.NeoPixel.get_instance()
        if neopix:
            return neopix.get_pixel_colors()
        return [(0, 0, 0)] * 8
    
    def get_neopixel_display(self):
        """Get terminal-friendly NeoPixel display."""
        neopix = neopixel.NeoPixel.get_instance()
        if neopix:
            return neopix.get_display_string()
        return ". . . . . . . ."
    
    def get_display_text(self):
        """Get all text currently shown on OLED."""
        labels = adafruit_display_text.label.Label.get_all_labels()
        text_items = []
        for lbl in labels:
            if lbl.text:
                text_items.append(f"  [{lbl.x:3d},{lbl.y:3d}] {lbl.text}")
        return "\n".join(text_items) if text_items else "  (empty)"


# Global simulation state instance
_sim_state = None


def get_simulation_state():
    """Get or create the simulation state manager."""
    global _sim_state
    if _sim_state is None:
        _sim_state = SimulationState()
    return _sim_state
