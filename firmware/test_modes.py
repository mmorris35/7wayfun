# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Test Mode definitions for the 7-way trailer tester.

Defines operating modes and test sequences for vehicle testing,
trailer testing, and pass-through monitoring.

Author: Mike Morris
License: GNU GPL v3
"""

from micropython import const


class TestMode:
    """
    Enumeration of operating modes for the trailer tester.
    
    Using class constants instead of enum for CircuitPython compatibility.
    """
    VEHICLE_TESTER = const(0)   # Read signals from tow vehicle
    TRAILER_TESTER = const(1)   # Send signals to test trailer
    PASS_THROUGH = const(2)     # Monitor signals passing through
    
    @classmethod
    def name(cls, mode):
        """Get the name of a mode value."""
        names = {
            cls.VEHICLE_TESTER: "VEHICLE_TESTER",
            cls.TRAILER_TESTER: "TRAILER_TESTER",
            cls.PASS_THROUGH: "PASS_THROUGH",
        }
        return names.get(mode, "UNKNOWN")
    
    @classmethod
    def all_modes(cls):
        """Return list of all mode values."""
        return [cls.VEHICLE_TESTER, cls.TRAILER_TESTER, cls.PASS_THROUGH]


class TestSequence:
    """
    Predefined test sequences for trailer testing mode.
    
    Each sequence is a list of (channel, duration) tuples that
    define which relay to activate and for how long.
    """
    
    # Standard full test - cycles through all circuits
    FULL_TEST = [
        ("tail", 2.0),      # Running lights first
        ("left", 1.5),      # Left turn signal (blink simulation)
        ("right", 1.5),     # Right turn signal
        ("brake", 2.0),     # Brake lights
        ("reverse", 1.5),   # Reverse lights
        ("aux", 1.0),       # Aux power
    ]
    
    # Quick test - faster cycle for rapid verification
    QUICK_TEST = [
        ("tail", 0.5),
        ("left", 0.5),
        ("right", 0.5),
        ("brake", 0.5),
        ("reverse", 0.5),
        ("aux", 0.5),
    ]
    
    # Turn signal test - alternating blink pattern
    TURN_SIGNAL_TEST = [
        ("left", 0.5),
        (None, 0.5),        # None = all off
        ("left", 0.5),
        (None, 0.5),
        ("left", 0.5),
        (None, 0.5),
        ("right", 0.5),
        (None, 0.5),
        ("right", 0.5),
        (None, 0.5),
        ("right", 0.5),
    ]
    
    # Brake test with hazards
    HAZARD_TEST = [
        ("left", 0.5),
        ("right", 0.5),     # Both on = hazards
        (None, 0.5),
        ("left", 0.5),
        ("right", 0.5),
        (None, 0.5),
        ("left", 0.5),
        ("right", 0.5),
        (None, 0.5),
    ]


class VehicleTester:
    """
    Vehicle testing mode handler.
    
    In this mode, the tester is connected to the tow vehicle's
    7-way connector. It reads and displays the signals the vehicle
    is outputting.
    """
    
    # Voltage thresholds for signal detection
    THRESHOLD_LOW = 3.0     # Below this = definitely off
    THRESHOLD_HIGH = 10.0   # Above this = definitely on
    THRESHOLD_FAULT = 16.0  # Above this = fault condition
    
    @staticmethod
    def interpret_voltage(voltage):
        """
        Interpret a voltage reading.
        
        Args:
            voltage: Measured voltage in volts
        
        Returns:
            Tuple of (status_string, is_active, is_fault)
        """
        if voltage < 0.5:
            return ("OFF", False, False)
        elif voltage < VehicleTester.THRESHOLD_LOW:
            return ("LOW", False, False)
        elif voltage < VehicleTester.THRESHOLD_HIGH:
            return ("WEAK", True, False)
        elif voltage < VehicleTester.THRESHOLD_FAULT:
            return ("OK", True, False)
        else:
            return ("HIGH!", True, True)
    
    @staticmethod
    def analyze_readings(readings):
        """
        Analyze a set of voltage readings.
        
        Args:
            readings: Dict of channel_name -> voltage
        
        Returns:
            Dict of channel_name -> (status, is_active, is_fault)
        """
        analysis = {}
        for channel, voltage in readings.items():
            analysis[channel] = VehicleTester.interpret_voltage(voltage)
        return analysis


class TrailerTester:
    """
    Trailer testing mode handler.
    
    In this mode, the tester is connected to the trailer. It outputs
    test signals to verify each trailer circuit functions correctly.
    """
    
    @staticmethod
    def get_test_sequence(sequence_name="full"):
        """
        Get a predefined test sequence.
        
        Args:
            sequence_name: One of "full", "quick", "turn", "hazard"
        
        Returns:
            List of (channel, duration) tuples
        """
        sequences = {
            "full": TestSequence.FULL_TEST,
            "quick": TestSequence.QUICK_TEST,
            "turn": TestSequence.TURN_SIGNAL_TEST,
            "hazard": TestSequence.HAZARD_TEST,
        }
        return sequences.get(sequence_name, TestSequence.FULL_TEST)


class PassThroughTester:
    """
    Pass-through monitoring mode handler.
    
    In this mode, both vehicle and trailer are connected. The tester
    monitors signals passing from vehicle to trailer in real-time.
    """
    
    @staticmethod
    def check_signal_integrity(vehicle_voltage, expected_at_trailer):
        """
        Check if a signal is passing through correctly.
        
        Args:
            vehicle_voltage: Voltage measured from vehicle side
            expected_at_trailer: What voltage should be at trailer
        
        Returns:
            Tuple of (is_ok, message)
        """
        diff = abs(vehicle_voltage - expected_at_trailer)
        
        if diff < 0.5:
            return (True, "OK")
        elif diff < 2.0:
            return (True, "VOLTAGE DROP")
        else:
            return (False, "SIGNAL LOSS")
