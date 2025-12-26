# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
ADC Manager for ADS1115 16-bit ADC boards.

Manages two ADS1115 boards via I2C to provide 8 channels of high-resolution
voltage measurement. Includes voltage scaling to account for the hardware
voltage dividers on the input stage.

Author: Mike Morris
License: GNU GPL v3
"""

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from logger import Logger, LogLevel


class ADCManager:
    """
    Manager for two ADS1115 16-bit ADC boards.
    
    Each ADS1115 provides 4 single-ended analog inputs. With two boards,
    we have 8 channels total, of which 6 are used for trailer signals.
    
    The input voltage dividers scale 15V max input to ~3.2V for the ADC.
    This class handles the reverse scaling to report actual input voltages.
    
    I2C Addresses:
        Board 0: 0x48 (ADDR pin to GND)
        Board 1: 0x49 (ADDR pin to VDD)
    
    Channel Mapping:
        Board 0, Channel 0: Brake (Blue)
        Board 0, Channel 1: Tail (Brown)
        Board 0, Channel 2: Left Turn (Yellow)
        Board 0, Channel 3: Right Turn (Green)
        Board 1, Channel 0: Aux 12V (Red)
        Board 1, Channel 1: Reverse (Purple)
        Board 1, Channel 2: Spare
        Board 1, Channel 3: Spare
    """
    
    # Voltage divider scaling factor
    # With R1=10K, R2=2.7K: ratio = (10K + 2.7K) / 2.7K = 4.7
    VOLTAGE_SCALE = 4.7
    
    # ADC reference voltage
    ADC_REF_VOLTAGE = 3.3
    
    # I2C addresses for the two ADS1115 boards
    BOARD_ADDRESSES = [0x48, 0x49]
    
    # Minimum voltage to consider as "detected" (noise floor)
    NOISE_FLOOR = 0.3
    
    def __init__(self, i2c=None):
        """
        Initialize the ADC manager with two ADS1115 boards.
        
        Args:
            i2c: I2C bus instance (uses board.I2C() if None)
        """
        self.logger = Logger(name="adc", level=LogLevel.DEBUG)
        self.logger.debug("Initializing ADC manager...")
        
        # Set up I2C bus
        if i2c is None:
            i2c = board.I2C()
        self.i2c = i2c
        
        # Initialize both ADS1115 boards
        self.adc_boards = []
        self.channels = {}
        
        self._init_boards()
        
        self.logger.info("ADC manager initialized", boards=len(self.adc_boards))
    
    def _init_boards(self):
        """Initialize both ADS1115 boards and create channel objects."""
        for board_idx, address in enumerate(self.BOARD_ADDRESSES):
            try:
                adc = ADS.ADS1115(self.i2c, address=address)
                
                # Set gain for 4.096V range (most appropriate for our divider output)
                adc.gain = 1  # +/- 4.096V
                
                self.adc_boards.append(adc)
                
                # Create AnalogIn objects for all 4 channels on this board
                for chan_idx in range(4):
                    channel_key = (board_idx, chan_idx)
                    self.channels[channel_key] = AnalogIn(adc, getattr(ADS, f"P{chan_idx}"))
                
                self.logger.debug(f"ADC board {board_idx} initialized at 0x{address:02X}")
                
            except Exception as error:
                self.logger.error(f"Failed to initialize ADC board at 0x{address:02X}: {error}")
                raise
    
    def read_raw(self, board_idx, channel):
        """
        Read raw ADC value from a specific channel.
        
        Args:
            board_idx: Index of the ADS1115 board (0 or 1)
            channel: Channel number on that board (0-3)
        
        Returns:
            Raw 16-bit ADC value
        """
        channel_key = (board_idx, channel)
        
        if channel_key not in self.channels:
            self.logger.error(f"Invalid channel: board={board_idx}, channel={channel}")
            return 0
        
        return self.channels[channel_key].value
    
    def read_voltage(self, board_idx, channel):
        """
        Read voltage from a channel, scaled to actual input voltage.
        
        This applies the voltage divider scaling factor to convert the
        ADC reading back to the original 12V-scale input voltage.
        
        Args:
            board_idx: Index of the ADS1115 board (0 or 1)
            channel: Channel number on that board (0-3)
        
        Returns:
            Actual input voltage (0-15V range, approximately)
        """
        channel_key = (board_idx, channel)
        
        if channel_key not in self.channels:
            self.logger.error(f"Invalid channel: board={board_idx}, channel={channel}")
            return 0.0
        
        # Get voltage at ADC input (after divider)
        adc_voltage = self.channels[channel_key].voltage
        
        # Scale back to original input voltage
        input_voltage = adc_voltage * self.VOLTAGE_SCALE
        
        # Apply noise floor - readings below this are considered zero
        if input_voltage < self.NOISE_FLOOR:
            input_voltage = 0.0
        
        return input_voltage
    
    def read_all_channels(self):
        """
        Read all 6 active channels and return as a dict.
        
        Returns:
            Dict mapping channel names to voltage readings
        """
        channel_map = {
            "brake": (0, 0),
            "tail": (0, 1),
            "left": (0, 2),
            "right": (0, 3),
            "aux": (1, 0),
            "reverse": (1, 1),
        }
        
        readings = {}
        for name, (board_idx, chan_idx) in channel_map.items():
            readings[name] = self.read_voltage(board_idx, chan_idx)
        
        return readings
    
    def is_channel_active(self, board_idx, channel, threshold=3.0):
        """
        Check if a channel has voltage above a threshold.
        
        Args:
            board_idx: Index of the ADS1115 board (0 or 1)
            channel: Channel number on that board (0-3)
            threshold: Voltage threshold (default 3.0V)
        
        Returns:
            True if voltage exceeds threshold
        """
        voltage = self.read_voltage(board_idx, channel)
        return voltage >= threshold
    
    def get_diagnostics(self):
        """
        Get diagnostic information about the ADC subsystem.
        
        Returns:
            Dict with diagnostic data
        """
        diagnostics = {
            "boards_detected": len(self.adc_boards),
            "channels_configured": len(self.channels),
            "voltage_scale": self.VOLTAGE_SCALE,
        }
        
        # Read all channels for current state
        diagnostics["current_readings"] = self.read_all_channels()
        
        return diagnostics
