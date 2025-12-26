# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock displayio module for desktop simulation.

Provides stub implementations of displayio classes for testing
without actual display hardware.

Author: Mike Morris
License: GNU GPL v3
"""


def release_displays():
    """Release any existing display connections."""
    pass


class I2CDisplay:
    """Mock I2C display bus."""
    
    def __init__(self, i2c, device_address=0x3C):
        self.i2c = i2c
        self.device_address = device_address


class Group:
    """Mock display group that holds display elements."""
    
    def __init__(self):
        self._items = []
    
    def append(self, item):
        self._items.append(item)
    
    def remove(self, item):
        self._items.remove(item)
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]


class Bitmap:
    """Mock bitmap for pixel data."""
    
    def __init__(self, width, height, value_count):
        self.width = width
        self.height = height
        self.value_count = value_count
        self._data = [[0] * width for _ in range(height)]
    
    def __setitem__(self, key, value):
        x_coord, y_coord = key
        if 0 <= x_coord < self.width and 0 <= y_coord < self.height:
            self._data[y_coord][x_coord] = value
    
    def __getitem__(self, key):
        x_coord, y_coord = key
        return self._data[y_coord][x_coord]


class Palette:
    """Mock color palette."""
    
    def __init__(self, count):
        self._colors = [0] * count
    
    def __setitem__(self, index, color):
        self._colors[index] = color
    
    def __getitem__(self, index):
        return self._colors[index]


class TileGrid:
    """Mock tile grid for bitmap display."""
    
    def __init__(self, bitmap, pixel_shader, x=0, y=0):
        self.bitmap = bitmap
        self.pixel_shader = pixel_shader
        self.x = x
        self.y = y
