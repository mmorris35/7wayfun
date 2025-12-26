#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Simple test script for trailer tester firmware.

Runs basic tests without the full terminal UI to verify
firmware logic works correctly.

Author: Mike Morris
License: GNU GPL v3
"""

import sys
import os
import time

# Set up paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "firmware")

# Import simulation state (this patches sys.modules)
sys.path.insert(0, SCRIPT_DIR)
from sim_state import get_simulation_state

# Now we can import firmware modules
sys.path.insert(0, FIRMWARE_DIR)


def test_logger():
    """Test the logging module."""
    print("\n=== Testing Logger ===")
    
    from logger import Logger, LogLevel
    
    logger = Logger(name="test", level=LogLevel.DEBUG)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message", code=42)
    
    print("Logger test PASSED")


def test_neopixel_manager():
    """Test the NeoPixel manager."""
    print("\n=== Testing NeoPixel Manager ===")
    
    import mock_board as board
    from neopixel_manager import NeoPixelManager, Colors
    
    neopix = NeoPixelManager(pin=board.D5, num_pixels=8, brightness=0.5)
    
    # Test setting individual pixels
    neopix.set_pixel(0, Colors.RED)
    neopix.set_pixel(1, Colors.GREEN)
    neopix.set_pixel(2, Colors.BLUE)
    
    print(f"Pixel display: {neopix.pixels.get_display_string()}")
    
    # Test channel active/idle
    neopix.set_channel_active(3)
    neopix.set_channel_idle(4)
    
    print(f"After channel set: {neopix.pixels.get_display_string()}")
    
    # Test startup animation
    neopix.startup_animation()
    
    print("NeoPixel manager test PASSED")


def test_relay_manager():
    """Test the relay manager."""
    print("\n=== Testing Relay Manager ===")
    
    from relay_manager import RelayManager
    
    relays = RelayManager()
    
    # Test individual channels
    relays.set_channel(0, True)
    assert relays.get_channel(0) == True
    
    relays.set_channel(0, False)
    assert relays.get_channel(0) == False
    
    # Test by name
    relays.set_by_name("left", True)
    assert "left" in relays.get_active_channels()
    
    # Test all off
    relays.all_off()
    assert len(relays.get_active_channels()) == 0
    
    # Test pattern
    relays.set_pattern([True, False, True, False, True, False])
    active = relays.get_active_channels()
    assert "brake" in active
    assert "tail" not in active
    
    relays.all_off()
    
    print("Relay manager test PASSED")


def test_adc_manager():
    """Test the ADC manager with simulated voltages."""
    print("\n=== Testing ADC Manager ===")
    
    sim_state = get_simulation_state()
    
    # Set some simulated voltages
    sim_state.set_vehicle_signal("brake", 11.5)
    sim_state.set_vehicle_signal("tail", 12.0)
    sim_state.set_vehicle_signal("left", 0.0)
    
    from adc_manager import ADCManager
    
    adc = ADCManager()
    
    # Read voltages
    readings = adc.read_all_channels()
    
    print(f"Readings: {readings}")
    
    # Check brake is approximately correct (within tolerance of divider calculation)
    assert readings["brake"] > 10.0, f"Expected brake > 10V, got {readings['brake']}"
    assert readings["tail"] > 10.0, f"Expected tail > 10V, got {readings['tail']}"
    assert readings["left"] < 1.0, f"Expected left < 1V, got {readings['left']}"
    
    # Test channel active detection
    assert adc.is_channel_active(0, 0, threshold=3.0) == True
    assert adc.is_channel_active(0, 2, threshold=3.0) == False
    
    print("ADC manager test PASSED")


def test_display_manager():
    """Test the display manager."""
    print("\n=== Testing Display Manager ===")
    
    from display_manager import DisplayManager
    
    display = DisplayManager()
    
    # Test splash screen
    display.show_splash()
    
    # Test mode display
    from test_modes import TestMode
    display.show_mode(TestMode.VEHICLE_TESTER)
    
    # Test voltage readings
    readings = {
        "brake": 11.5,
        "tail": 12.0,
        "left": 0.0,
        "right": 12.1,
        "aux": 13.2,
        "reverse": 0.0,
    }
    display.show_voltage_readings(readings)
    
    # Test messages
    display.show_message("Test message")
    display.show_error("Test error")
    
    print("Display manager test PASSED")


def test_test_modes():
    """Test the test modes module."""
    print("\n=== Testing Test Modes ===")
    
    from test_modes import TestMode, TestSequence, VehicleTester
    
    # Test mode enumeration
    assert TestMode.name(TestMode.VEHICLE_TESTER) == "VEHICLE_TESTER"
    assert len(TestMode.all_modes()) == 3
    
    # Test voltage interpretation
    status, active, fault = VehicleTester.interpret_voltage(0.2)
    assert active == False
    
    status, active, fault = VehicleTester.interpret_voltage(12.0)
    assert active == True
    assert fault == False
    
    status, active, fault = VehicleTester.interpret_voltage(17.0)
    assert fault == True
    
    # Test analysis
    readings = {"brake": 12.0, "tail": 0.0}
    analysis = VehicleTester.analyze_readings(readings)
    assert analysis["brake"][1] == True  # is_active
    assert analysis["tail"][1] == False
    
    print("Test modes test PASSED")


def test_integration():
    """Test full integration of components."""
    print("\n=== Integration Test ===")
    
    sim_state = get_simulation_state()
    
    # Reset state
    sim_state.set_all_signals_off()
    
    # Simulate a vehicle with running lights and left turn
    sim_state.set_running_lights()
    sim_state.set_left_turn()
    
    # Import the full application
    # Note: This will print log messages
    print("Loading firmware application...")
    
    from code import TrailerTester as FirmwareApp
    
    app = FirmwareApp()
    
    # Manually trigger a read
    readings = app._read_all_channels()
    
    print(f"Integration readings: {readings}")
    
    # Check that readings match what we set
    assert readings["tail"] > 10.0, "Tail lights should be on"
    assert readings["left"] > 10.0, "Left turn should be on"
    assert readings["right"] < 1.0, "Right turn should be off"
    
    # Cleanup
    app.shutdown()
    
    print("Integration test PASSED")


def main():
    """Run all tests."""
    print("=" * 60)
    print("  TRAILER TESTER FIRMWARE TESTS")
    print("=" * 60)
    
    tests = [
        test_logger,
        test_neopixel_manager,
        test_relay_manager,
        test_adc_manager,
        test_display_manager,
        test_test_modes,
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as error:
            print(f"\nFAILED: {test_func.__name__}")
            print(f"  Error: {error}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"  RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
