# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock neopixel module for desktop simulation.

Simulates the NeoPixel LED strip with terminal-based visualization.

Author: Mike Morris
License: GNU GPL v3
"""


class NeoPixel:
    """
    Mock NeoPixel strip.
    
    Stores pixel colors and provides visualization methods for
    terminal-based simulation display.
    """
    
    # Class-level instance for simulation access
    _instance = None
    
    def __init__(self, pin, num_pixels, brightness=1.0, auto_write=True):
        self.pin = pin
        self.num_pixels = num_pixels
        self._brightness = brightness
        self.auto_write = auto_write
        self._pixels = [(0, 0, 0)] * num_pixels
        
        # Register as the active instance
        NeoPixel._instance = self
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        self._brightness = max(0.0, min(1.0, value))
    
    def __len__(self):
        return self.num_pixels
    
    def __getitem__(self, index):
        return self._pixels[index]
    
    def __setitem__(self, index, color):
        if isinstance(index, slice):
            for idx in range(*index.indices(self.num_pixels)):
                self._pixels[idx] = color
        else:
            self._pixels[index] = color
        
        if self.auto_write:
            self.show()
    
    def fill(self, color):
        """Fill all pixels with a single color."""
        self._pixels = [color] * self.num_pixels
        if self.auto_write:
            self.show()
    
    def show(self):
        """Update the display (no-op in simulation, but signals update)."""
        pass
    
    def get_display_string(self):
        """Get a terminal-friendly display of the pixel states."""
        result = []
        for idx, color in enumerate(self._pixels):
            red, green, blue = color
            # Scale by brightness
            red = int(red * self._brightness)
            green = int(green * self._brightness)
            blue = int(blue * self._brightness)
            
            # Determine dominant color for simple display
            if red == 0 and green == 0 and blue == 0:
                char = "."
                ansi = "\033[90m"  # Dark gray
            elif red > green and red > blue:
                char = "R" if red > 128 else "r"
                ansi = "\033[91m" if red > 128 else "\033[31m"
            elif green > red and green > blue:
                char = "G" if green > 128 else "g"
                ansi = "\033[92m" if green > 128 else "\033[32m"
            elif blue > red and blue > green:
                char = "B" if blue > 128 else "b"
                ansi = "\033[94m" if blue > 128 else "\033[34m"
            elif red == green and red > blue:
                char = "Y" if red > 128 else "y"
                ansi = "\033[93m" if red > 128 else "\033[33m"
            elif red == blue and red > green:
                char = "M" if red > 128 else "m"
                ansi = "\033[95m" if red > 128 else "\033[35m"
            elif green == blue and green > red:
                char = "C" if green > 128 else "c"
                ansi = "\033[96m" if green > 128 else "\033[36m"
            else:
                char = "W" if red > 128 else "w"
                ansi = "\033[97m" if red > 128 else "\033[37m"
            
            result.append(f"{ansi}[{char}]\033[0m")
        
        return " ".join(result)
    
    def get_pixel_colors(self):
        """Get raw pixel colors for external display."""
        return list(self._pixels)
    
    @classmethod
    def get_instance(cls):
        """Get the active NeoPixel instance."""
        return cls._instance
