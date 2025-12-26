# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
NeoPixel Strip Manager for 8-LED status display.

Provides visual feedback for channel status using color-coded LEDs.
LED 0 is the mode/status indicator, LEDs 1-6 are channel status,
LED 7 is ground/overall status.

Author: Mike Morris
License: GNU GPL v3
"""

import time
import neopixel
from logger import Logger, LogLevel


class Colors:
    """Predefined color constants for the NeoPixel strip."""
    
    # Basic colors (RGB tuples)
    OFF = (0, 0, 0)
    WHITE = (255, 255, 255)
    WHITE_DIM = (20, 20, 20)
    RED = (255, 0, 0)
    RED_DIM = (30, 0, 0)
    GREEN = (0, 255, 0)
    GREEN_DIM = (0, 30, 0)
    BLUE = (0, 0, 255)
    BLUE_DIM = (0, 0, 30)
    YELLOW = (255, 255, 0)
    YELLOW_DIM = (30, 30, 0)
    PURPLE = (128, 0, 128)
    PURPLE_DIM = (20, 0, 20)
    ORANGE = (255, 165, 0)
    ORANGE_DIM = (30, 20, 0)
    CYAN = (0, 255, 255)
    
    # Mode indicator colors
    MODE_VEHICLE = CYAN
    MODE_TRAILER = ORANGE
    MODE_PASSTHROUGH = PURPLE
    
    # Channel colors (matching wire standards)
    CHANNEL_BRAKE_ACTIVE = BLUE
    CHANNEL_BRAKE_IDLE = BLUE_DIM
    CHANNEL_TAIL_ACTIVE = YELLOW
    CHANNEL_TAIL_IDLE = YELLOW_DIM
    CHANNEL_LEFT_ACTIVE = YELLOW
    CHANNEL_LEFT_IDLE = YELLOW_DIM
    CHANNEL_RIGHT_ACTIVE = GREEN
    CHANNEL_RIGHT_IDLE = GREEN_DIM
    CHANNEL_AUX_ACTIVE = RED
    CHANNEL_AUX_IDLE = RED_DIM
    CHANNEL_REVERSE_ACTIVE = PURPLE
    CHANNEL_REVERSE_IDLE = PURPLE_DIM
    
    # Fault indicator
    FAULT = RED


class NeoPixelManager:
    """
    Manager for the 8-LED NeoPixel strip.
    
    LED Layout:
        LED 0: Mode/Status indicator
        LED 1: Brake circuit (Blue)
        LED 2: Tail/Running lights (Yellow/Brown)
        LED 3: Left turn (Yellow)
        LED 4: Right turn (Green)
        LED 5: Aux 12V (Red)
        LED 6: Reverse (Purple)
        LED 7: Ground/Overall status
    """
    
    NUM_PIXELS = 8
    
    # Channel to LED index mapping (0 = status, 7 = ground)
    CHANNEL_LED_MAP = {
        "brake": 1,
        "tail": 2,
        "left": 3,
        "right": 4,
        "aux": 5,
        "reverse": 6,
    }
    
    # Active and idle colors for each channel
    CHANNEL_COLORS = {
        1: {"active": Colors.CHANNEL_BRAKE_ACTIVE, "idle": Colors.CHANNEL_BRAKE_IDLE},
        2: {"active": Colors.CHANNEL_TAIL_ACTIVE, "idle": Colors.CHANNEL_TAIL_IDLE},
        3: {"active": Colors.CHANNEL_LEFT_ACTIVE, "idle": Colors.CHANNEL_LEFT_IDLE},
        4: {"active": Colors.CHANNEL_RIGHT_ACTIVE, "idle": Colors.CHANNEL_RIGHT_IDLE},
        5: {"active": Colors.CHANNEL_AUX_ACTIVE, "idle": Colors.CHANNEL_AUX_IDLE},
        6: {"active": Colors.CHANNEL_REVERSE_ACTIVE, "idle": Colors.CHANNEL_REVERSE_IDLE},
    }
    
    def __init__(self, pin, num_pixels=8, brightness=0.3):
        """
        Initialize the NeoPixel strip.
        
        Args:
            pin: The GPIO pin connected to the NeoPixel data line
            num_pixels: Number of pixels in the strip (default 8)
            brightness: Global brightness 0.0-1.0 (default 0.3)
        """
        self.logger = Logger(name="neopixel", level=LogLevel.DEBUG)
        self.logger.debug("Initializing NeoPixel strip...")
        
        self.pixels = neopixel.NeoPixel(
            pin,
            num_pixels,
            brightness=brightness,
            auto_write=False
        )
        
        self.num_pixels = num_pixels
        
        # Initialize all pixels to dim white (standby)
        self.clear()
        
        self.logger.info("NeoPixel strip initialized", count=num_pixels, brightness=brightness)
    
    def clear(self):
        """Turn off all pixels."""
        self.pixels.fill(Colors.OFF)
        self.pixels.show()
    
    def fill(self, color):
        """
        Fill all pixels with a single color.
        
        Args:
            color: RGB tuple (r, g, b)
        """
        self.pixels.fill(color)
        self.pixels.show()
    
    def set_pixel(self, index, color):
        """
        Set a single pixel to a color.
        
        Args:
            index: Pixel index (0-7)
            color: RGB tuple (r, g, b)
        """
        if 0 <= index < self.num_pixels:
            self.pixels[index] = color
            self.pixels.show()
    
    def startup_animation(self):
        """Play a startup animation to indicate the device is booting."""
        self.logger.debug("Playing startup animation")
        
        # Quick sweep in cyan
        for idx in range(self.num_pixels):
            self.pixels.fill(Colors.OFF)
            self.pixels[idx] = Colors.CYAN
            self.pixels.show()
            time.sleep(0.05)
        
        # Flash all green briefly
        self.pixels.fill(Colors.GREEN)
        self.pixels.show()
        time.sleep(0.2)
        
        # Settle to idle state
        self.set_all_idle()
    
    def set_mode_indicator(self, mode):
        """
        Set the mode indicator LED (LED 0) based on current mode.
        
        Args:
            mode: TestMode enum value
        """
        from test_modes import TestMode
        
        mode_colors = {
            TestMode.VEHICLE_TESTER: Colors.MODE_VEHICLE,
            TestMode.TRAILER_TESTER: Colors.MODE_TRAILER,
            TestMode.PASS_THROUGH: Colors.MODE_PASSTHROUGH,
        }
        
        color = mode_colors.get(mode, Colors.WHITE)
        self.pixels[0] = color
        self.pixels.show()
        
        self.logger.debug(f"Mode indicator set to {mode.name}")
    
    def set_channel_active(self, led_index):
        """
        Set a channel LED to its active (bright) color.
        
        Args:
            led_index: LED index (1-6 for channels)
        """
        if led_index in self.CHANNEL_COLORS:
            self.pixels[led_index] = self.CHANNEL_COLORS[led_index]["active"]
            self.pixels.show()
    
    def set_channel_idle(self, led_index):
        """
        Set a channel LED to its idle (dim) color.
        
        Args:
            led_index: LED index (1-6 for channels)
        """
        if led_index in self.CHANNEL_COLORS:
            self.pixels[led_index] = self.CHANNEL_COLORS[led_index]["idle"]
            self.pixels.show()
    
    def set_channel_fault(self, led_index):
        """
        Set a channel LED to fault indication (red).
        
        Args:
            led_index: LED index (1-6 for channels)
        """
        if 1 <= led_index <= 6:
            self.pixels[led_index] = Colors.FAULT
            self.pixels.show()
    
    def set_all_idle(self):
        """Set all channel LEDs to their idle state."""
        # Mode indicator dim
        self.pixels[0] = Colors.WHITE_DIM
        
        # All channels to idle colors
        for led_idx in range(1, 7):
            self.pixels[led_idx] = self.CHANNEL_COLORS[led_idx]["idle"]
        
        # Ground indicator dim green (good ground)
        self.pixels[7] = Colors.GREEN_DIM
        
        self.pixels.show()
    
    def set_ground_status(self, is_good):
        """
        Set the ground status indicator (LED 7).
        
        Args:
            is_good: True if ground is good, False if fault
        """
        self.pixels[7] = Colors.GREEN if is_good else Colors.FAULT
        self.pixels.show()
    
    def blink_all(self, color, count=3, on_time=0.1, off_time=0.1):
        """
        Blink all pixels a specified color.
        
        Args:
            color: RGB tuple to blink
            count: Number of blinks
            on_time: Duration of on state in seconds
            off_time: Duration of off state in seconds
        """
        for _ in range(count):
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(on_time)
            self.pixels.fill(Colors.OFF)
            self.pixels.show()
            time.sleep(off_time)
    
    def update_from_readings(self, readings, threshold=3.0):
        """
        Update all channel LEDs based on voltage readings.
        
        Args:
            readings: Dict mapping channel names to voltage values
            threshold: Voltage threshold for considering a channel active
        """
        for channel_name, led_index in self.CHANNEL_LED_MAP.items():
            if channel_name in readings:
                voltage = readings[channel_name]
                if voltage >= threshold:
                    self.set_channel_active(led_index)
                else:
                    self.set_channel_idle(led_index)
        
        self.pixels.show()
