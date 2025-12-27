# SPDX-FileCopyrightText: 2024 Mike Morris
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Automatic Fault Diagnosis Engine

Analyzes voltage readings and patterns to detect common trailer wiring
issues and suggest fixes.

Author: Mike Morris
License: GNU GPL v3
"""

from logger import Logger, LogLevel


class FaultPattern:
    """Represents a known fault pattern with diagnosis and fixes."""

    def __init__(self, name, description, confidence, fixes):
        """
        Initialize fault pattern.

        Args:
            name: Short name for the fault
            description: Human-readable description
            confidence: Confidence level (0-100)
            fixes: List of suggested fix steps
        """
        self.name = name
        self.description = description
        self.confidence = confidence
        self.fixes = fixes


class DiagnosticsEngine:
    """
    Automatic fault diagnosis engine.

    Analyzes voltage patterns to detect common wiring faults and
    suggest repair steps.
    """

    # Voltage thresholds
    EXPECTED_VOLTAGE = 12.0
    NORMAL_MIN = 11.0
    WEAK_THRESHOLD = 9.0
    ACTIVE_THRESHOLD = 3.0

    def __init__(self):
        """Initialize diagnostics engine."""
        self.logger = Logger(name="diagnostics", level=LogLevel.DEBUG)
        self.logger.info("Diagnostics engine initialized")

    def analyze_readings(self, readings, mode=None):
        """
        Analyze voltage readings and detect faults.

        Args:
            readings: Dict of channel_name -> voltage
            mode: Current operating mode (optional context)

        Returns:
            List of FaultPattern objects detected, sorted by confidence
        """
        faults = []

        # Check each channel for issues
        # Only analyze channels that are active (above ACTIVE_THRESHOLD)
        # to avoid false positives on channels that are supposed to be off
        for channel, voltage in readings.items():
            # Only check active channels for faults
            if voltage > self.ACTIVE_THRESHOLD:
                # Detect voltage drop
                if self._is_voltage_drop(voltage):
                    faults.append(self._diagnose_voltage_drop(channel, voltage))

                # Detect weak signal
                elif self._is_weak_signal(voltage):
                    faults.append(self._diagnose_weak_signal(channel, voltage))

        # Check for cross-wiring (left/right swapped)
        cross_wire = self._detect_cross_wiring(readings)
        if cross_wire:
            faults.append(cross_wire)

        # Check for ground issues (all channels low)
        ground_fault = self._detect_ground_fault(readings)
        if ground_fault:
            faults.append(ground_fault)

        # Sort by confidence (highest first)
        faults.sort(key=lambda f: f.confidence, reverse=True)

        return faults

    def _is_open_circuit(self, channel, voltage):
        """Check if channel shows open circuit."""
        # Expected to be active but reading near zero
        return voltage < 0.5

    def _is_voltage_drop(self, voltage):
        """Check if voltage drop indicates degraded connection."""
        return self.ACTIVE_THRESHOLD < voltage < self.WEAK_THRESHOLD

    def _is_weak_signal(self, voltage):
        """Check if signal is weak but functional."""
        return self.WEAK_THRESHOLD <= voltage < self.NORMAL_MIN

    def _diagnose_open_circuit(self, channel, voltage):
        """Diagnose open circuit fault."""
        channel_info = self._get_channel_info(channel)

        return FaultPattern(
            name="OPEN_CIRCUIT",
            description="No signal on {} ({}) - reads {:.1f}V (expected 12V)".format(
                channel_info['name'],
                channel_info['color'],
                voltage
            ),
            confidence=95,
            fixes=[
                "Check fuse in vehicle fuse panel",
                "Inspect connector pin {} ({}) for corrosion".format(
                    channel_info['pin'],
                    channel_info['color']
                ),
                "Verify {} circuit bulbs/lights are functional".format(channel),
                "Test wire continuity with multimeter",
                "Check for broken wire in harness",
            ]
        )

    def _diagnose_voltage_drop(self, channel, voltage):
        """Diagnose significant voltage drop."""
        channel_info = self._get_channel_info(channel)

        return FaultPattern(
            name="VOLTAGE_DROP",
            description="{} ({}) shows {:.1f}V - significant voltage drop".format(
                channel_info['name'],
                channel_info['color'],
                voltage
            ),
            confidence=85,
            fixes=[
                "Clean connector pins with electrical contact cleaner",
                "Check for loose connections at pin {}".format(channel_info['pin']),
                "Inspect wire for damage or corrosion",
                "Verify adequate wire gauge (16-18 AWG minimum)",
                "Check ground connection (Pin 1, White wire)",
                "Apply dielectric grease to prevent corrosion",
            ]
        )

    def _diagnose_weak_signal(self, channel, voltage):
        """Diagnose weak but functional signal."""
        channel_info = self._get_channel_info(channel)

        return FaultPattern(
            name="WEAK_SIGNAL",
            description="{} ({}) reads {:.1f}V - below normal (11-12V expected)".format(
                channel_info['name'],
                channel_info['color'],
                voltage
            ),
            confidence=70,
            fixes=[
                "Check battery voltage (should be 12.6V resting)",
                "Clean connector contacts",
                "Verify ground connection quality",
                "Check for high-resistance connections",
                "Inspect wire run for excessive length",
            ]
        )

    def _detect_cross_wiring(self, readings):
        """Detect if left and right turn signals are swapped."""
        left_voltage = readings.get('left', 0)
        right_voltage = readings.get('right', 0)

        # Simple check: both shouldn't be on simultaneously unless hazards
        # This is a simplified detection - real implementation would track over time
        if left_voltage > self.ACTIVE_THRESHOLD and right_voltage > self.ACTIVE_THRESHOLD:
            if abs(left_voltage - right_voltage) < 1.0:  # Similar voltages
                return FaultPattern(
                    name="POSSIBLE_CROSS_WIRE",
                    description="Left and Right turn signals both active - possible cross-wiring or hazards",
                    confidence=60,
                    fixes=[
                        "Verify this is not hazard lights mode",
                        "Check wire colors: Left=Red(4), Right=Brown(5)",
                        "Inspect connector for crossed pins",
                        "Verify trailer wiring matches RV 7-Way standard",
                        "Check for short circuit between left/right wires",
                    ]
                )

        return None

    def _detect_ground_fault(self, readings):
        """Detect if all channels show low voltage (bad ground)."""
        active_channels = [v for v in readings.values() if v > self.ACTIVE_THRESHOLD]

        # If we have active channels but all are weak
        if len(active_channels) >= 3:
            avg_voltage = sum(active_channels) / len(active_channels)

            if avg_voltage < self.NORMAL_MIN:
                return FaultPattern(
                    name="GROUND_FAULT",
                    description="All channels read low ({:.1f}V avg) - likely ground issue".format(
                        avg_voltage
                    ),
                    confidence=90,
                    fixes=[
                        "Inspect ground wire (Pin 1, White) connection",
                        "Clean ground connection at trailer frame",
                        "Verify ground wire is securely attached",
                        "Check for rust/corrosion at ground point",
                        "Install additional ground strap if needed",
                        "Verify ground wire gauge is adequate",
                    ]
                )

        return None

    def _get_channel_info(self, channel):
        """Get display info for a channel."""
        # RV 7-Way Standard mapping
        channel_map = {
            'brake': {'name': 'Brake', 'pin': 2, 'color': 'Blue'},
            'tail': {'name': 'Tail/Running', 'pin': 3, 'color': 'Green'},
            'left': {'name': 'Left Turn', 'pin': 4, 'color': 'Red'},
            'right': {'name': 'Right Turn', 'pin': 5, 'color': 'Brown'},
            'aux': {'name': 'Aux Power', 'pin': 6, 'color': 'Black'},
            'reverse': {'name': 'Reverse', 'pin': 7, 'color': 'Yellow'},
        }

        return channel_map.get(channel, {'name': channel, 'pin': 0, 'color': 'Unknown'})

    def format_diagnosis_report(self, faults):
        """
        Format diagnosis results as human-readable report.

        Args:
            faults: List of FaultPattern objects

        Returns:
            String containing formatted report
        """
        if not faults:
            return "No faults detected - all signals normal"

        report = "FAULT DIAGNOSIS REPORT\n"
        report += "=" * 40 + "\n\n"

        for idx, fault in enumerate(faults, 1):
            report += "{}. {} ({}% confidence)\n".format(
                idx, fault.name, fault.confidence
            )
            report += "   {}\n\n".format(fault.description)
            report += "   Suggested Fixes:\n"

            for fix_idx, fix in enumerate(fault.fixes, 1):
                report += "   {}. {}\n".format(fix_idx, fix)

            report += "\n"

        return report


class DiagnosticHistory:
    """
    Track fault history over time for trend analysis.

    This allows detection of intermittent faults and degradation over time.
    """

    def __init__(self, max_history=100):
        """
        Initialize diagnostic history tracker.

        Args:
            max_history: Maximum number of readings to keep
        """
        self.history = []
        self.max_history = max_history
        self.fault_counts = {}

    def add_reading(self, timestamp, readings, faults):
        """
        Add a reading to history.

        Args:
            timestamp: Time of reading (seconds)
            readings: Voltage readings dict
            faults: List of detected faults
        """
        self.history.append({
            'timestamp': timestamp,
            'readings': readings.copy(),
            'faults': faults.copy()
        })

        # Count fault occurrences
        for fault in faults:
            if fault.name not in self.fault_counts:
                self.fault_counts[fault.name] = 0
            self.fault_counts[fault.name] += 1

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def detect_intermittent_fault(self, fault_name, threshold=0.3):
        """
        Detect if a fault is intermittent (appears and disappears).

        Args:
            fault_name: Name of fault to check
            threshold: Percentage of time fault must appear (0.0-1.0)

        Returns:
            True if fault appears intermittently
        """
        if len(self.history) < 10:
            return False  # Not enough data

        occurrences = self.fault_counts.get(fault_name, 0)
        percentage = occurrences / len(self.history)

        # Intermittent: appears sometimes but not always
        return 0.1 < percentage < 0.9

    def get_trend(self, channel):
        """
        Get voltage trend for a channel.

        Args:
            channel: Channel name

        Returns:
            'improving', 'degrading', 'stable', or None
        """
        if len(self.history) < 5:
            return None

        # Get recent readings
        recent = [h['readings'].get(channel, 0) for h in self.history[-10:]]

        if len(recent) < 5:
            return None

        # Simple linear trend
        first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
        second_half = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)

        diff = second_half - first_half

        if abs(diff) < 0.5:
            return 'stable'
        elif diff > 0:
            return 'improving'
        else:
            return 'degrading'
