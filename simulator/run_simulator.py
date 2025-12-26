#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
7-Way Trailer Tester Simulator

Terminal-based simulator for developing and testing the trailer tester
firmware without physical hardware.

Usage:
    python run_simulator.py

Controls:
    m - Press mode button
    t - Press test button
    1-6 - Toggle vehicle signals (brake, tail, left, right, aux, reverse)
    a - All signals on (12V)
    o - All signals off
    r - Running lights preset
    b - Braking preset
    q - Quit

Author: Mike Morris
License: GNU GPL v3
"""

import sys
import os
import time
import threading
import select

# Set up paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "firmware")

# Import simulation state (this patches sys.modules)
sys.path.insert(0, SCRIPT_DIR)
from sim_state import get_simulation_state, SimulationState

# Now we can import firmware modules
sys.path.insert(0, FIRMWARE_DIR)


class TerminalUI:
    """Terminal-based UI for the simulator."""
    
    CHANNEL_KEYS = {
        '1': 'brake',
        '2': 'tail',
        '3': 'left',
        '4': 'right',
        '5': 'aux',
        '6': 'reverse',
    }
    
    def __init__(self, sim_state):
        self.sim_state = sim_state
        self.running = True
        self.last_update = 0
        self.update_interval = 0.1
    
    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")
    
    def draw_header(self):
        """Draw the header section."""
        print("=" * 60)
        print("  7-WAY TRAILER TESTER SIMULATOR")
        print("=" * 60)
    
    def draw_vehicle_signals(self):
        """Draw the simulated vehicle signals section."""
        print("\n[VEHICLE SIGNALS - Input to Tester]")
        print("-" * 40)
        
        signals = self.sim_state.vehicle_signals
        for idx, (name, voltage) in enumerate(signals.items(), 1):
            bar_len = int(voltage / 14.0 * 20)
            bar = "#" * bar_len + "." * (20 - bar_len)
            status = "ON " if voltage > 3.0 else "OFF"
            print(f"  {idx}) {name:8s}: {voltage:5.1f}V [{bar}] {status}")
    
    def draw_relay_outputs(self):
        """Draw the relay output states."""
        print("\n[RELAY OUTPUTS - From Tester to Trailer]")
        print("-" * 40)
        
        states = self.sim_state.get_relay_states()
        for name, is_on in states.items():
            status = "\033[92mON \033[0m" if is_on else "\033[90mOFF\033[0m"
            indicator = "[###]" if is_on else "[   ]"
            print(f"  {name:8s}: {indicator} {status}")
    
    def draw_neopixels(self):
        """Draw the NeoPixel strip state."""
        print("\n[NEOPIXEL STRIP]")
        print("-" * 40)
        display = self.sim_state.get_neopixel_display()
        labels = " STA  BRK  TAL  LFT  RGT  AUX  REV  GND"
        print(f"  {display}")
        print(f"  {labels}")
    
    def draw_oled(self):
        """Draw the OLED display content."""
        print("\n[OLED DISPLAY - 128x64]")
        print("-" * 40)
        print("+----------------------------+")
        text = self.sim_state.get_display_text()
        # Simple display - just show label text
        for line in text.split("\n")[:7]:
            print(f"|{line[:28]:28s}|")
        print("+----------------------------+")
    
    def draw_controls(self):
        """Draw the control help."""
        print("\n[CONTROLS]")
        print("-" * 40)
        print("  m = Mode button    t = Test button")
        print("  1-6 = Toggle signal (brake/tail/left/right/aux/rev)")
        print("  a = All signals ON    o = All signals OFF")
        print("  r = Running lights    b = Braking")
        print("  q = Quit")
    
    def draw(self):
        """Draw the complete UI."""
        self.clear_screen()
        self.draw_header()
        self.draw_vehicle_signals()
        self.draw_relay_outputs()
        self.draw_neopixels()
        self.draw_oled()
        self.draw_controls()
        print("\n> ", end="", flush=True)
    
    def handle_input(self, char):
        """Handle a single character input."""
        if char == 'q':
            self.running = False
            return
        
        elif char == 'm':
            # Mode button press
            self.sim_state.press_mode_button()
            time.sleep(0.05)
            self.sim_state.release_mode_button()
        
        elif char == 't':
            # Test button press
            self.sim_state.press_test_button()
            time.sleep(0.05)
            self.sim_state.release_test_button()
        
        elif char in self.CHANNEL_KEYS:
            # Toggle a vehicle signal
            channel = self.CHANNEL_KEYS[char]
            current = self.sim_state.vehicle_signals[channel]
            new_voltage = 0.0 if current > 3.0 else 12.0
            self.sim_state.set_vehicle_signal(channel, new_voltage)
        
        elif char == 'a':
            # All signals on
            for channel in self.CHANNEL_KEYS.values():
                self.sim_state.set_vehicle_signal(channel, 12.0)
        
        elif char == 'o':
            # All signals off
            self.sim_state.set_all_signals_off()
        
        elif char == 'r':
            # Running lights preset
            self.sim_state.set_all_signals_off()
            self.sim_state.set_running_lights()
        
        elif char == 'b':
            # Braking preset
            self.sim_state.set_all_signals_off()
            self.sim_state.set_running_lights()
            self.sim_state.set_braking()


def run_firmware_loop(app, stop_event):
    """Run the firmware main loop in a separate thread."""
    try:
        while not stop_event.is_set():
            app.check_buttons()
            
            # In vehicle tester mode, read inputs
            from test_modes import TestMode
            if app.current_mode in (TestMode.VEHICLE_TESTER, TestMode.PASS_THROUGH):
                app._read_all_channels()
            
            time.sleep(0.05)
    except Exception as error:
        print(f"\nFirmware error: {error}")


def main():
    """Main simulator entry point."""
    print("Initializing simulator...")
    
    # Get simulation state
    sim_state = get_simulation_state()
    
    # Import and create the firmware application
    # We need to patch 'time' module for CircuitPython compatibility
    import time as real_time
    
    # Patch time.monotonic if needed
    if not hasattr(real_time, 'monotonic'):
        real_time.monotonic = real_time.time
    
    # Now import firmware
    try:
        from code import TrailerTester as FirmwareApp
        print("Loading firmware...")
        app = FirmwareApp()
    except Exception as error:
        print(f"Failed to load firmware: {error}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Create UI
    ui = TerminalUI(sim_state)
    
    # Start firmware loop in background thread
    stop_event = threading.Event()
    firmware_thread = threading.Thread(
        target=run_firmware_loop,
        args=(app, stop_event),
        daemon=True
    )
    firmware_thread.start()
    
    print("Simulator ready. Press any key to start...")
    
    # Main UI loop
    try:
        # Set terminal to raw mode for single-char input
        import tty
        import termios
        
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while ui.running:
                ui.draw()
                
                # Wait for input with timeout
                if select.select([sys.stdin], [], [], 0.2)[0]:
                    char = sys.stdin.read(1)
                    ui.handle_input(char)
                
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        print("\nShutting down...")
        stop_event.set()
        firmware_thread.join(timeout=1.0)
        app.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
