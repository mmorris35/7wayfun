# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock adafruit_displayio_sh1107 module for desktop simulation.

Author: Mike Morris
License: GNU GPL v3
"""


class SH1107:
    """Mock SH1107 OLED display driver."""
    
    _instance = None
    
    def __init__(self, display_bus, width, height, rotation=0):
        self.display_bus = display_bus
        self.width = width
        self.height = height
        self.rotation = rotation
        self._root_group = None
        
        SH1107._instance = self
    
    @property
    def root_group(self):
        return self._root_group
    
    @root_group.setter
    def root_group(self, group):
        self._root_group = group
    
    @classmethod
    def get_instance(cls):
        """Get the active display instance."""
        return cls._instance
