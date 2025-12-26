# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Relay Manager for 4-channel STEMMA relay boards.

Controls two 4-channel relay boards to switch 12V outputs for
trailer light testing. Provides individual channel control and
safety features like all-off on initialization.

Author: Mike Morris
License: GNU GPL v3
"""

import board
import digitalio
from logger import Logger, LogLevel


class RelayManager:
    """
    Manager for two 4-channel STEMMA relay boards (8 relays total).
    
    The relays are controlled via GPIO pins. Each relay can switch
    up to 10A at 12V, which is sufficient for trailer lighting circuits.
    
    Relay assignments:
        Relay 0 (D6):  Brake (Blue)
        Relay 1 (D9):  Tail (Brown)
        Relay 2 (D10): Left Turn (Yellow)
        Relay 3 (D11): Right Turn (Green)
        Relay 4 (D12): Aux 12V (Red)
        Relay 5 (D13): Reverse (Purple)
        Relay 6: Spare
        Relay 7: Spare
    
    Relays are active-HIGH (GPIO high = relay energized = circuit closed).
    """
    
    # GPIO pin assignments for relay control
    RELAY_PINS = [
        board.D6,   # Relay 0: Brake
        board.D9,   # Relay 1: Tail
        board.D10,  # Relay 2: Left Turn
        board.D11,  # Relay 3: Right Turn
        board.D12,  # Relay 4: Aux
        board.D13,  # Relay 5: Reverse
    ]
    
    # Channel names for logging
    CHANNEL_NAMES = ["brake", "tail", "left", "right", "aux", "reverse"]
    
    def __init__(self):
        """Initialize the relay manager."""
        self.logger = Logger(name="relay", level=LogLevel.DEBUG)
        self.logger.debug("Initializing relay manager...")
        
        # Initialize GPIO pins for relay control
        self.relays = []
        
        for idx, pin in enumerate(self.RELAY_PINS):
            relay_io = digitalio.DigitalInOut(pin)
            relay_io.direction = digitalio.Direction.OUTPUT
            relay_io.value = False  # Start with all relays off
            self.relays.append(relay_io)
            self.logger.debug(f"Relay {idx} ({self.CHANNEL_NAMES[idx]}) initialized on pin {pin}")
        
        # Track relay states
        self.states = [False] * len(self.relays)
        
        self.logger.info("Relay manager initialized", relay_count=len(self.relays))
    
    def set_channel(self, channel_idx, state):
        """
        Set a single relay channel on or off.
        
        Args:
            channel_idx: Relay index (0-5)
            state: True to energize relay (circuit closed), False to open
        """
        if not 0 <= channel_idx < len(self.relays):
            self.logger.error(f"Invalid relay index: {channel_idx}")
            return
        
        self.relays[channel_idx].value = state
        self.states[channel_idx] = state
        
        channel_name = self.CHANNEL_NAMES[channel_idx]
        state_str = "ON" if state else "OFF"
        self.logger.debug(f"Relay {channel_idx} ({channel_name}): {state_str}")
    
    def get_channel(self, channel_idx):
        """
        Get the current state of a relay channel.
        
        Args:
            channel_idx: Relay index (0-5)
        
        Returns:
            True if relay is energized, False otherwise
        """
        if not 0 <= channel_idx < len(self.relays):
            return False
        return self.states[channel_idx]
    
    def toggle_channel(self, channel_idx):
        """
        Toggle a relay channel.
        
        Args:
            channel_idx: Relay index (0-5)
        
        Returns:
            New state of the relay
        """
        if not 0 <= channel_idx < len(self.relays):
            return False
        
        new_state = not self.states[channel_idx]
        self.set_channel(channel_idx, new_state)
        return new_state
    
    def all_off(self):
        """Turn off all relays (safety function)."""
        self.logger.info("All relays OFF")
        for idx in range(len(self.relays)):
            self.relays[idx].value = False
            self.states[idx] = False
    
    def all_on(self):
        """Turn on all relays (use with caution)."""
        self.logger.warning("All relays ON")
        for idx in range(len(self.relays)):
            self.relays[idx].value = True
            self.states[idx] = True
    
    def set_pattern(self, pattern):
        """
        Set multiple relays at once using a pattern.
        
        Args:
            pattern: List of boolean values, one per relay
        """
        for idx, state in enumerate(pattern):
            if idx < len(self.relays):
                self.relays[idx].value = state
                self.states[idx] = state
        
        self.logger.debug(f"Relay pattern set: {pattern}")
    
    def set_by_name(self, channel_name, state):
        """
        Set a relay by channel name.
        
        Args:
            channel_name: One of "brake", "tail", "left", "right", "aux", "reverse"
            state: True to energize, False to open
        """
        try:
            idx = self.CHANNEL_NAMES.index(channel_name.lower())
            self.set_channel(idx, state)
        except ValueError:
            self.logger.error(f"Unknown channel name: {channel_name}")
    
    def get_active_channels(self):
        """
        Get list of currently active channel names.
        
        Returns:
            List of channel names that are currently on
        """
        active = []
        for idx, state in enumerate(self.states):
            if state:
                active.append(self.CHANNEL_NAMES[idx])
        return active
    
    def get_diagnostics(self):
        """
        Get diagnostic information about relay states.
        
        Returns:
            Dict with relay state information
        """
        return {
            "relay_count": len(self.relays),
            "states": dict(zip(self.CHANNEL_NAMES, self.states)),
            "active_channels": self.get_active_channels(),
        }
