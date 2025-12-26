# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock digitalio module for desktop simulation.

Simulates CircuitPython's digitalio module for GPIO control.

Author: Mike Morris
License: GNU GPL v3
"""

from enum import Enum


class Direction(Enum):
    """Pin direction constants."""
    INPUT = 0
    OUTPUT = 1


class Pull(Enum):
    """Pull-up/down constants."""
    UP = 0
    DOWN = 1


class DigitalInOut:
    """
    Mock digital I/O pin.
    
    Tracks state and can be connected to a simulation state manager
    for coordinated testing.
    """
    
    # Class-level registry of all pins for simulation access
    _pins = {}
    
    def __init__(self, pin):
        self.pin = pin
        self._direction = Direction.INPUT
        self._pull = None
        self._value = False
        
        # Register this pin
        DigitalInOut._pins[pin.name] = self
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = value
    
    @property
    def pull(self):
        return self._pull
    
    @pull.setter
    def pull(self, value):
        self._pull = value
        # If pull-up, default value is True (high)
        if value == Pull.UP:
            self._value = True
        elif value == Pull.DOWN:
            self._value = False
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if self._direction == Direction.OUTPUT:
            self._value = val
    
    @classmethod
    def get_pin(cls, name):
        """Get a pin instance by name for simulation control."""
        return cls._pins.get(name)
    
    @classmethod
    def set_input(cls, name, value):
        """Set an input pin value from simulation."""
        pin = cls._pins.get(name)
        if pin and pin._direction == Direction.INPUT:
            pin._value = value
    
    @classmethod
    def get_all_states(cls):
        """Get state of all pins for display."""
        states = {}
        for name, pin in cls._pins.items():
            states[name] = {
                "direction": "OUT" if pin._direction == Direction.OUTPUT else "IN",
                "value": pin._value,
                "pull": pin._pull.name if pin._pull else None
            }
        return states
