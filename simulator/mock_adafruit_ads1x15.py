# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock adafruit_ads1x15 module for desktop simulation.

Simulates the ADS1115 16-bit ADC with configurable voltage values
for testing.

Author: Mike Morris
License: GNU GPL v3
"""


# Channel constants (matching real library)
P0 = 0
P1 = 1
P2 = 2
P3 = 3


class ADS1115:
    """
    Mock ADS1115 16-bit ADC.
    
    Stores simulated voltage values that can be set externally
    for testing different scenarios.
    """
    
    # Class-level storage of all ADC instances
    _instances = {}
    
    # Simulated channel voltages (can be modified for testing)
    _simulated_voltages = {}
    
    def __init__(self, i2c, address=0x48):
        self.i2c = i2c
        self.address = address
        self._gain = 1
        
        # Initialize simulated voltages for this address
        key = address
        if key not in ADS1115._simulated_voltages:
            ADS1115._simulated_voltages[key] = {
                0: 0.0,
                1: 0.0,
                2: 0.0,
                3: 0.0
            }
        
        ADS1115._instances[address] = self
    
    @property
    def gain(self):
        return self._gain
    
    @gain.setter
    def gain(self, value):
        self._gain = value
    
    def get_voltage(self, channel):
        """Get the simulated voltage for a channel."""
        return ADS1115._simulated_voltages[self.address].get(channel, 0.0)
    
    @classmethod
    def set_simulated_voltage(cls, address, channel, voltage):
        """
        Set a simulated voltage value for testing.
        
        Args:
            address: I2C address (0x48 or 0x49)
            channel: Channel number (0-3)
            voltage: Voltage to simulate (after divider, so 0-3.3V range)
        """
        if address not in cls._simulated_voltages:
            cls._simulated_voltages[address] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
        cls._simulated_voltages[address][channel] = voltage
    
    @classmethod
    def get_all_voltages(cls):
        """Get all simulated voltages for display."""
        return dict(cls._simulated_voltages)
    
    @classmethod
    def get_instance(cls, address):
        """Get ADC instance by address."""
        return cls._instances.get(address)


class AnalogIn:
    """Mock analog input channel."""
    
    def __init__(self, adc, channel):
        self.adc = adc
        self.channel = channel
    
    @property
    def value(self):
        """Get raw ADC value (16-bit)."""
        voltage = self.adc.get_voltage(self.channel)
        # Convert voltage to 16-bit value (assuming 4.096V reference)
        return int((voltage / 4.096) * 32767)
    
    @property
    def voltage(self):
        """Get voltage reading."""
        return self.adc.get_voltage(self.channel)
