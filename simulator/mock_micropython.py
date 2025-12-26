# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Mock micropython module for desktop simulation.

Author: Mike Morris
License: GNU GPL v3
"""


def const(value):
    """
    Mock const() function.
    
    In MicroPython, const() is used to declare compile-time constants.
    On desktop Python, we just return the value as-is.
    """
    return value
