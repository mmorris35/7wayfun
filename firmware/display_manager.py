# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
OLED Display Manager for 128x64 FeatherWing display.

Handles all display output including splash screen, mode indicators,
voltage readings, and status messages.

Author: Mike Morris
License: GNU GPL v3
"""

import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107
from logger import Logger, LogLevel


# Release any existing displays
displayio.release_displays()


class DisplayManager:
    """
    Manager for the 128x64 OLED FeatherWing display.
    
    The display uses the SH1107 controller and communicates via I2C.
    This class provides high-level methods for showing various screens
    and information relevant to the trailer tester.
    """
    
    WIDTH = 128
    HEIGHT = 64
    
    # Display layout constants
    HEADER_Y = 0
    CONTENT_START_Y = 12
    LINE_HEIGHT = 9
    
    # Channel display order and labels
    CHANNEL_ORDER = ["brake", "tail", "left", "right", "aux", "reverse"]
    CHANNEL_LABELS = {
        "brake": "BRK",
        "tail": "TAIL",
        "left": "LEFT",
        "right": "RGHT",
        "aux": "AUX",
        "reverse": "REV",
    }
    
    def __init__(self, i2c=None, address=0x3C):
        """
        Initialize the display manager.
        
        Args:
            i2c: I2C bus instance (uses board.I2C() if None)
            address: I2C address of the display (default 0x3C)
        """
        self.logger = Logger(name="display", level=LogLevel.DEBUG)
        self.logger.debug("Initializing display...")
        
        # Set up I2C and display bus
        if i2c is None:
            i2c = board.I2C()
        
        display_bus = displayio.I2CDisplay(i2c, device_address=address)
        
        # Initialize the SH1107 display
        self.display = SH1107(
            display_bus,
            width=self.WIDTH,
            height=self.HEIGHT,
            rotation=0
        )
        
        # Create the main display group
        self.root_group = displayio.Group()
        self.display.root_group = self.root_group
        
        # Create reusable text labels
        self._init_labels()
        
        self.logger.info("Display initialized", width=self.WIDTH, height=self.HEIGHT)
    
    def _init_labels(self):
        """Initialize reusable text label objects."""
        # Header label (mode indicator)
        self.header_label = label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            x=0,
            y=self.HEADER_Y + 6
        )
        self.root_group.append(self.header_label)
        
        # Channel labels (6 channels)
        self.channel_labels = []
        self.voltage_labels = []
        self.bar_rects = []
        
        for idx in range(6):
            y_pos = self.CONTENT_START_Y + (idx * self.LINE_HEIGHT) + 4
            
            # Channel name label
            chan_label = label.Label(
                terminalio.FONT,
                text="",
                color=0xFFFFFF,
                x=0,
                y=y_pos
            )
            self.channel_labels.append(chan_label)
            self.root_group.append(chan_label)
            
            # Voltage reading label
            volt_label = label.Label(
                terminalio.FONT,
                text="",
                color=0xFFFFFF,
                x=30,
                y=y_pos
            )
            self.voltage_labels.append(volt_label)
            self.root_group.append(volt_label)
        
        # Status message label (for temporary messages)
        self.status_label = label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            x=0,
            y=32
        )
        self.root_group.append(self.status_label)
    
    def clear(self):
        """Clear all display content."""
        self.header_label.text = ""
        self.status_label.text = ""
        for label_obj in self.channel_labels:
            label_obj.text = ""
        for label_obj in self.voltage_labels:
            label_obj.text = ""
    
    def show_splash(self):
        """Display the startup splash screen."""
        self.clear()
        self.header_label.text = "7-WAY TESTER"
        self.status_label.text = "v1.0 - Starting..."
        self.logger.debug("Showing splash screen")
    
    def show_mode(self, mode):
        """
        Display the current operating mode.
        
        Args:
            mode: TestMode enum value
        """
        from test_modes import TestMode
        
        mode_names = {
            TestMode.VEHICLE_TESTER: "MODE: VEHICLE TEST",
            TestMode.TRAILER_TESTER: "MODE: TRAILER TEST",
            TestMode.PASS_THROUGH: "MODE: PASS-THROUGH",
        }
        
        self.header_label.text = mode_names.get(mode, "MODE: UNKNOWN")
        self.status_label.text = ""
        
        # Clear voltage displays when changing modes
        for label_obj in self.voltage_labels:
            label_obj.text = ""
        
        self.logger.debug(f"Mode display updated: {TestMode.name(mode)}")
    
    def show_voltage_readings(self, readings):
        """
        Display voltage readings for all channels.
        
        Args:
            readings: Dict mapping channel names to voltage values
        """
        for idx, channel_name in enumerate(self.CHANNEL_ORDER):
            if channel_name in readings:
                voltage = readings[channel_name]
                
                # Channel name
                self.channel_labels[idx].text = self.CHANNEL_LABELS[channel_name]
                
                # Voltage value with simple bar indicator
                if voltage < 0.5:
                    bar = "[        ]"
                elif voltage < 6.0:
                    bar = "[==      ]"
                elif voltage < 10.0:
                    bar = "[=====   ]"
                elif voltage < 12.0:
                    bar = "[=======+]"
                else:
                    bar = "[========]"
                
                self.voltage_labels[idx].text = f"{voltage:5.1f}V {bar}"
    
    def show_test_channel(self, channel_name):
        """
        Display which channel is currently being tested.
        
        Args:
            channel_name: Human-readable channel name
        """
        self.status_label.text = f"Testing: {channel_name}"
        self.logger.debug(f"Testing channel: {channel_name}")
    
    def show_message(self, message):
        """
        Display a temporary status message.
        
        Args:
            message: Message text to display
        """
        # Clear channel displays
        for label_obj in self.channel_labels:
            label_obj.text = ""
        for label_obj in self.voltage_labels:
            label_obj.text = ""
        
        self.status_label.text = message
        self.logger.debug(f"Status message: {message}")
    
    def show_error(self, error_message):
        """
        Display an error message prominently.
        
        Args:
            error_message: Error text to display
        """
        self.header_label.text = "!! ERROR !!"
        self.status_label.text = error_message[:21]  # Truncate to fit
        self.logger.error(f"Display error: {error_message}")
