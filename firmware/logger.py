# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Centralized logging module for CircuitPython.

Provides structured logging with levels, timestamps, and optional
serial output for debugging the trailer tester.

Author: Mike Morris
License: GNU GPL v3
"""

import time
from micropython import const


class LogLevel:
    """Log level constants."""
    DEBUG = const(10)
    INFO = const(20)
    WARNING = const(30)
    ERROR = const(40)
    CRITICAL = const(50)
    
    _names = {
        DEBUG: "DEBUG",
        INFO: "INFO",
        WARNING: "WARN",
        ERROR: "ERROR",
        CRITICAL: "CRIT",
    }
    
    @classmethod
    def name(cls, level):
        """Get the name for a log level."""
        return cls._names.get(level, "UNKNOWN")


class Logger:
    """
    Simple structured logger for CircuitPython.
    
    Usage:
        logger = Logger(name="mymodule", level=LogLevel.DEBUG)
        logger.info("Application started")
        logger.debug("Processing item", item_id=42)
        logger.error("Failed to connect", error=str(e))
    """
    
    # Class-level default settings
    _global_level = LogLevel.INFO
    _start_time = time.monotonic()
    _loggers = {}
    
    def __init__(self, name, level=None):
        """
        Initialize a logger instance.
        
        Args:
            name: Name of the module/component for log prefixing
            level: Minimum log level to output (defaults to global level)
        """
        self.name = name
        self._level = level if level is not None else Logger._global_level
        
        # Register this logger
        Logger._loggers[name] = self
    
    @classmethod
    def set_global_level(cls, level):
        """Set the default log level for all new loggers."""
        cls._global_level = level
    
    @property
    def level(self):
        """Get the current log level."""
        return self._level
    
    @level.setter
    def level(self, value):
        """Set the log level."""
        self._level = value
    
    def _format_message(self, level, message, **kwargs):
        """Format a log message with timestamp and metadata."""
        elapsed = time.monotonic() - Logger._start_time
        level_name = LogLevel.name(level)
        
        # Build the base message
        formatted = f"[{elapsed:8.3f}] {level_name:5} [{self.name}] {message}"
        
        # Append any extra kwargs
        if kwargs:
            extras = " ".join(f"{key}={value}" for key, value in kwargs.items())
            formatted = f"{formatted} | {extras}"
        
        return formatted
    
    def _log(self, level, message, **kwargs):
        """Internal logging method."""
        if level >= self._level:
            formatted = self._format_message(level, message, **kwargs)
            print(formatted)
    
    def debug(self, message, **kwargs):
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message, **kwargs):
        """Log an info message."""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message, **kwargs):
        """Log a warning message."""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message, **kwargs):
        """Log an error message."""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message, **kwargs):
        """Log a critical message."""
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def exception(self, message, error=None, **kwargs):
        """Log an error with exception details."""
        if error:
            kwargs["error"] = str(error)
            kwargs["type"] = type(error).__name__
        self._log(LogLevel.ERROR, message, **kwargs)


def get_logger(name, level=None):
    """
    Get or create a logger by name.
    
    Args:
        name: Logger name
        level: Optional log level override
    
    Returns:
        Logger instance
    """
    if name in Logger._loggers:
        logger = Logger._loggers[name]
        if level is not None:
            logger.level = level
        return logger
    return Logger(name=name, level=level)
