# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock adafruit_display_text module for desktop simulation.

Author: Mike Morris
License: GNU GPL v3
"""


# Class registry for simulation access (module-level to avoid reference issues)
_label_registry = []


class Label:
    """Mock text label for display."""
    
    def __init__(self, font, text="", color=0xFFFFFF, x=0, y=0, **kwargs):
        self.font = font
        self._text = text
        self.color = color
        self.x = x
        self.y = y
        _label_registry.append(self)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
    
    @classmethod
    def get_all_labels(cls):
        """Get all label instances for display."""
        return _label_registry
    
    @classmethod
    def clear_labels(cls):
        """Clear label registry."""
        global _label_registry
        _label_registry = []


# Also expose as label.Label for compatibility with firmware imports
class label:
    """Mock label module namespace."""
    Label = Label
