# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock board module for desktop simulation.

Simulates the CircuitPython board module with fake pin definitions
that work with the mock hardware classes.

Author: Mike Morris
License: GNU GPL v3
"""


class MockPin:
    """Mock GPIO pin that tracks its name for debugging."""
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"MockPin({self.name})"


# Feather RP2040 pin definitions
D5 = MockPin("D5")
D6 = MockPin("D6")
D9 = MockPin("D9")
D10 = MockPin("D10")
D11 = MockPin("D11")
D12 = MockPin("D12")
D13 = MockPin("D13")
D24 = MockPin("D24")
D25 = MockPin("D25")

# Analog pins
A0 = MockPin("A0")
A1 = MockPin("A1")
A2 = MockPin("A2")
A3 = MockPin("A3")

# I2C pins
SDA = MockPin("SDA")
SCL = MockPin("SCL")

# SPI pins
SCK = MockPin("SCK")
MOSI = MockPin("MOSI")
MISO = MockPin("MISO")

# Built-in LED
LED = MockPin("LED")


class MockI2C:
    """Mock I2C bus."""
    
    def __init__(self):
        self.devices = {}
    
    def scan(self):
        """Return list of detected I2C addresses."""
        return list(self.devices.keys())
    
    def try_lock(self):
        return True
    
    def unlock(self):
        pass


_i2c_instance = None


def I2C():
    """Get the shared I2C bus instance."""
    global _i2c_instance
    if _i2c_instance is None:
        _i2c_instance = MockI2C()
    return _i2c_instance


def STEMMA_I2C():
    """Alias for I2C on STEMMA connector."""
    return I2C()
