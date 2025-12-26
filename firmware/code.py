# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
7-Way Trailer Wiring Controller Tester

Main entry point for CircuitPython firmware.
Runs on Adafruit Feather RP2040 with:
- 128x64 OLED FeatherWing display
- 8x NeoPixel strip for status indication
- 2x ADS1115 16-bit ADC for voltage measurement
- 2x 4-channel relay boards for output driving

Author: Mike Morris
License: GNU GPL v3
"""

import time
import board
import digitalio
from logger import Logger, LogLevel
from display_manager import DisplayManager
from neopixel_manager import NeoPixelManager
from adc_manager import ADCManager
from relay_manager import RelayManager
from test_modes import TestMode, VehicleTester, TrailerTester, PassThroughTester


# Initialize logging first
logger = Logger(name="main", level=LogLevel.DEBUG)
logger.info("7-Way Trailer Tester starting up...")


class TrailerTester:
    """Main application class for the 7-way trailer tester."""

    # Button timing constants (in milliseconds)
    DEBOUNCE_MS = 50
    LONG_PRESS_MS = 2000

    # Channel definitions matching RV 7-Way standard
    CHANNELS = {
        "brake": {"pin": 2, "color": "blue", "relay_idx": 0, "adc_board": 0, "adc_chan": 0},
        "tail": {"pin": 3, "color": "green", "relay_idx": 1, "adc_board": 0, "adc_chan": 1},
        "left": {"pin": 4, "color": "red", "relay_idx": 2, "adc_board": 0, "adc_chan": 2},
        "right": {"pin": 5, "color": "brown", "relay_idx": 3, "adc_board": 0, "adc_chan": 3},
        "aux": {"pin": 6, "color": "black", "relay_idx": 4, "adc_board": 1, "adc_chan": 0},
        "reverse": {"pin": 7, "color": "yellow", "relay_idx": 5, "adc_board": 1, "adc_chan": 1},
    }
    
    def __init__(self):
        self.logger = Logger(name="app", level=LogLevel.DEBUG)
        self.logger.info("Initializing trailer tester application...")
        
        self.current_mode = TestMode.VEHICLE_TESTER
        self.running = True
        
        # Initialize hardware managers
        self._init_hardware()
        
        # Initialize mode button
        self._init_buttons()
        
        self.logger.info("Initialization complete")
    
    def _init_hardware(self):
        """Initialize all hardware components."""
        try:
            self.logger.debug("Initializing display...")
            self.display = DisplayManager()
            
            self.logger.debug("Initializing NeoPixels...")
            self.neopixels = NeoPixelManager(pin=board.D5, num_pixels=8)
            
            self.logger.debug("Initializing ADC boards...")
            self.adc = ADCManager()
            
            self.logger.debug("Initializing relay boards...")
            self.relays = RelayManager()
            
            # Show startup animation
            self.neopixels.startup_animation()
            self.display.show_splash()
            time.sleep(1.5)
            
        except Exception as error:
            self.logger.error(f"Hardware initialization failed: {error}")
            raise
    
    def _init_buttons(self):
        """Initialize control buttons."""
        # Mode button on D24
        self.mode_button = digitalio.DigitalInOut(board.D24)
        self.mode_button.direction = digitalio.Direction.INPUT
        self.mode_button.pull = digitalio.Pull.UP
        self.mode_button_last = True
        self._mode_press_time = 0

        # Test/Action button on D25
        self.test_button = digitalio.DigitalInOut(board.D25)
        self.test_button.direction = digitalio.Direction.INPUT
        self.test_button.pull = digitalio.Pull.UP
        self.test_button_last = True
        self._test_press_start = 0
        self._long_press_triggered = False

        self.logger.debug("Buttons initialized")
    
    def check_buttons(self):
        """Poll buttons with debounce and long-press detection."""
        current_time = time.monotonic() * 1000  # Convert to milliseconds

        # Mode button - simple press with debounce
        mode_current = self.mode_button.value
        if not mode_current and self.mode_button_last:
            # Button pressed (goes LOW when pressed due to pull-up)
            if current_time - self._mode_press_time > self.DEBOUNCE_MS:
                self._cycle_mode()
                # Visual feedback
                self.neopixels.blink_all((255, 255, 255), count=1, on_time=0.05, off_time=0.0)
                self._mode_press_time = current_time
        self.mode_button_last = mode_current

        # Test button - detect press start for long-press timing
        test_current = self.test_button.value
        if not test_current and self.test_button_last:
            # Button just pressed
            self._test_press_start = current_time
            self._long_press_triggered = False
        elif not test_current and not self.test_button_last:
            # Button held - check for long press
            hold_time = current_time - self._test_press_start
            if hold_time > self.LONG_PRESS_MS and not self._long_press_triggered:
                self._trigger_full_test()
                self._long_press_triggered = True
        elif test_current and not self.test_button_last:
            # Button released
            hold_time = current_time - self._test_press_start
            if hold_time < self.LONG_PRESS_MS and not self._long_press_triggered:
                self._trigger_test()
        self.test_button_last = test_current
    
    def _cycle_mode(self):
        """Cycle to the next operating mode."""
        modes = list(TestMode)
        current_idx = modes.index(self.current_mode)
        next_idx = (current_idx + 1) % len(modes)
        self.current_mode = modes[next_idx]
        
        self.logger.info(f"Mode changed to: {self.current_mode.name}")
        self.display.show_mode(self.current_mode)
        self.neopixels.set_mode_indicator(self.current_mode)
        
        # Turn off all relays when changing modes for safety
        self.relays.all_off()
    
    def _trigger_test(self):
        """Trigger test sequence based on current mode."""
        self.logger.info(f"Test triggered in mode: {self.current_mode.name}")

        if self.current_mode == TestMode.TRAILER_TESTER:
            self._run_trailer_test_sequence()
        elif self.current_mode == TestMode.VEHICLE_TESTER:
            # In vehicle mode, test button forces a refresh/detailed read
            self._read_all_channels(detailed=True)

    def _trigger_full_test(self):
        """Trigger comprehensive full system test (long press)."""
        self.logger.info("Full system test triggered (long press detected)")

        # Visual indication of full test starting
        self.neopixels.blink_all((0, 255, 255), count=3, on_time=0.1, off_time=0.1)
        self.display.show_message("FULL TEST")
        time.sleep(1.0)

        # Always run the full trailer test sequence for comprehensive testing
        self._run_trailer_test_sequence()

        # If in vehicle mode, also do a detailed channel read
        if self.current_mode == TestMode.VEHICLE_TESTER:
            time.sleep(0.5)
            self.display.show_message("Reading inputs...")
            time.sleep(1.0)
            self._read_all_channels(detailed=True)

        # Final indication
        self.neopixels.blink_all((0, 255, 0), count=2, on_time=0.15, off_time=0.15)
        self.logger.info("Full system test complete")

    def _run_trailer_test_sequence(self):
        """Run through all outputs to test trailer lights."""
        self.logger.info("Starting trailer test sequence...")
        self.display.show_message("Testing trailer...")
        
        test_sequence = [
            ("tail", "Tail Lights", 2.0),
            ("left", "Left Turn", 1.5),
            ("right", "Right Turn", 1.5),
            ("brake", "Brakes", 2.0),
            ("reverse", "Reverse", 1.5),
            ("aux", "Aux Power", 1.0),
        ]
        
        for channel_name, display_name, duration in test_sequence:
            channel = self.CHANNELS[channel_name]
            
            self.logger.debug(f"Testing {channel_name}...")
            self.display.show_test_channel(display_name)
            self.neopixels.set_channel_active(channel["relay_idx"] + 1)
            
            self.relays.set_channel(channel["relay_idx"], True)
            time.sleep(duration)
            self.relays.set_channel(channel["relay_idx"], False)
            
            self.neopixels.set_channel_idle(channel["relay_idx"] + 1)
            time.sleep(0.3)
        
        self.display.show_message("Test complete!")
        self.logger.info("Trailer test sequence complete")
    
    def _read_all_channels(self, detailed=False):
        """Read voltage on all input channels."""
        readings = {}
        
        for channel_name, channel_info in self.CHANNELS.items():
            voltage = self.adc.read_voltage(
                board_idx=channel_info["adc_board"],
                channel=channel_info["adc_chan"]
            )
            readings[channel_name] = voltage
            
            # Update NeoPixel based on voltage threshold
            is_active = voltage > 3.0  # Consider active if above 3V
            pixel_idx = channel_info["relay_idx"] + 1  # Offset by 1 for status LED
            
            if is_active:
                self.neopixels.set_channel_active(pixel_idx)
            else:
                self.neopixels.set_channel_idle(pixel_idx)
            
            if detailed:
                self.logger.debug(f"{channel_name}: {voltage:.2f}V")
        
        # Update display with readings
        self.display.show_voltage_readings(readings)
        
        return readings
    
    def run(self):
        """Main application loop."""
        self.logger.info("Entering main loop")
        self.display.show_mode(self.current_mode)
        self.neopixels.set_mode_indicator(self.current_mode)
        
        last_reading_time = 0
        reading_interval = 0.25  # Read voltages every 250ms
        
        try:
            while self.running:
                current_time = time.monotonic()
                
                # Check for button presses
                self.check_buttons()
                
                # In vehicle tester or pass-through mode, continuously read inputs
                if self.current_mode in (TestMode.VEHICLE_TESTER, TestMode.PASS_THROUGH):
                    if current_time - last_reading_time >= reading_interval:
                        self._read_all_channels()
                        last_reading_time = current_time
                
                # Small delay to prevent tight loop
                time.sleep(0.02)
                
        except KeyboardInterrupt:
            self.logger.info("Shutdown requested")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of all hardware."""
        self.logger.info("Shutting down...")
        self.relays.all_off()
        self.neopixels.clear()
        self.display.show_message("Goodbye!")
        time.sleep(0.5)
        self.display.clear()


# Main entry point
if __name__ == "__main__":
    try:
        app = TrailerTester()
        app.run()
    except Exception as error:
        logger.error(f"Fatal error: {error}")
        raise
