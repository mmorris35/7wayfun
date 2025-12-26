# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock busio module for desktop simulation.

Author: Mike Morris
License: GNU GPL v3
"""


class I2C:
    """Mock I2C bus."""
    
    def __init__(self, scl=None, sda=None, frequency=100000):
        self.scl = scl
        self.sda = sda
        self.frequency = frequency
        self._locked = False
    
    def try_lock(self):
        if not self._locked:
            self._locked = True
            return True
        return False
    
    def unlock(self):
        self._locked = False
    
    def scan(self):
        """Return list of detected I2C addresses."""
        return [0x3C, 0x48, 0x49]  # OLED + 2x ADS1115
    
    def writeto(self, address, buffer):
        pass
    
    def readfrom_into(self, address, buffer):
        pass


class SPI:
    """Mock SPI bus."""
    
    def __init__(self, clock, MOSI=None, MISO=None):
        self.clock = clock
        self.MOSI = MOSI
        self.MISO = MISO
    
    def try_lock(self):
        return True
    
    def unlock(self):
        pass
    
    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        pass


class UART:
    """Mock UART."""
    
    def __init__(self, tx=None, rx=None, baudrate=9600):
        self.tx = tx
        self.rx = rx
        self.baudrate = baudrate
