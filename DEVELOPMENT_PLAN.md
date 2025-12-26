# trailer-tester - Development Plan

## How to Use This Plan

**For Claude Code**: Read this plan, find the subtask ID from the prompt, complete ALL checkboxes, update completion notes, commit.

**For You**: Use this prompt:
```
Please read CLAUDE.md and DEVELOPMENT_PLAN.md completely, then implement subtask [X.Y.Z], following all rules and marking checkboxes as you complete each item.
```

---

## Project Overview

**Project Name**: trailer-tester
**Goal**: Bidirectional 7-way trailer wiring tester using Adafruit CircuitPython hardware
**Target Users**: RV owners, trailer owners, mobile mechanics, DIY enthusiasts
**Timeline**: 2 weeks

**MVP Scope**:
- [x] Vehicle Tester Mode - Read voltages from tow vehicle
- [x] Trailer Tester Mode - Output test signals to trailer
- [x] Pass-Through Mode - Monitor signals in real-time
- [x] NeoPixel LED status display
- [x] 128x64 OLED information display
- [x] Desktop simulator for development

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | CircuitPython 8.x/9.x |
| **MCU** | Adafruit Feather RP2040 |
| **ADC** | ADS1115 16-bit I2C (x2) |
| **Display** | SH1107 128x64 OLED FeatherWing |
| **LEDs** | WS2812B NeoPixel Stick (8x) |
| **Relays** | 4-channel STEMMA relay boards (x2) |
| **Testing** | Python 3.8+ with mock modules |
| **Linting** | ruff |

---

## Progress Tracking

### Phase 0: Foundation
- [x] 0.1.1: Repository Structure
- [x] 0.1.2: Hardware Design Documentation
- [ ] 0.1.3: Development Environment Setup

### Phase 1: Core Firmware Modules
- [x] 1.1.1: Logger Module
- [x] 1.2.1: ADC Manager
- [x] 1.3.1: Relay Manager
- [x] 1.4.1: NeoPixel Manager
- [x] 1.5.1: Display Manager
- [x] 1.6.1: Test Modes Module

### Phase 2: Main Application
- [x] 2.1.1: Main Application Loop
- [ ] 2.1.2: Button Handling Refinement
- [ ] 2.1.3: Mode Transition Logic

### Phase 3: Desktop Simulator
- [x] 3.1.1: Mock Hardware Modules
- [x] 3.1.2: Simulation State Manager
- [x] 3.1.3: Automated Test Suite
- [ ] 3.1.4: Interactive Terminal UI

### Phase 4: Integration & Testing
- [ ] 4.1.1: Hardware Integration Test
- [ ] 4.1.2: Voltage Calibration
- [ ] 4.1.3: End-to-End System Test

### Phase 5: Documentation
- [x] 5.1.1: Hardware Design Doc
- [x] 5.1.2: Shopping List
- [ ] 5.1.3: Assembly Guide
- [ ] 5.1.4: User Manual

**Current**: Phase 3 (Simulator refinement)
**Next**: 3.1.4

---

## Phase 0: Foundation

**Goal**: Repository structure and documentation
**Status**: Mostly complete

### Task 0.1: Project Setup

**Subtask 0.1.1: Repository Structure (COMPLETE)**

**Deliverables**:
- [x] Create directory structure: `firmware/`, `simulator/`, `docs/`, `tests/`
- [x] Create `.gitignore` with Python and CircuitPython ignores
- [x] Create `README.md` with project overview
- [x] Create `LICENSE` with MIT license

**Completion Notes**:
- **Implementation**: Standard repo structure created
- **Files Created**: Directory structure, .gitignore, README.md, LICENSE
- **Status**: COMPLETE

---

**Subtask 0.1.2: Hardware Design Documentation (COMPLETE)**

**Deliverables**:
- [x] Create `docs/HARDWARE_DESIGN.md` with full specifications
- [x] Document voltage divider calculations
- [x] Create GPIO pin assignment table
- [x] Create system architecture diagram
- [x] Create `docs/SHOPPING_LIST.md` with Adafruit part numbers

**Completion Notes**:
- **Implementation**: Comprehensive hardware docs with BOM
- **Files Created**: HARDWARE_DESIGN.md (350+ lines), SHOPPING_LIST.md
- **Status**: COMPLETE

---

**Subtask 0.1.3: Development Environment Setup (Single Session)**

**Prerequisites**:
- [x] 0.1.1: Repository Structure

**Deliverables**:
- [ ] Create `pyproject.toml` with project metadata
- [ ] Add development dependencies (ruff, pytest)
- [ ] Create `.pre-commit-config.yaml` for linting
- [ ] Create `Makefile` with common commands
- [ ] Verify `make test` runs simulator tests

**Files to Create**:
- `pyproject.toml`
- `.pre-commit-config.yaml`
- `Makefile`

**Complete Code**:

Create `pyproject.toml`:
```toml
[project]
name = "trailer-tester"
version = "0.1.0"
description = "7-way trailer wiring controller tester"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
authors = [
    {name = "Mike Morris"}
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["simulator"]
python_files = ["test_*.py"]
```

Create `Makefile`:
```makefile
.PHONY: test lint format clean sim

test:
	python3 simulator/test_firmware.py

lint:
	ruff check firmware/ simulator/

format:
	ruff format firmware/ simulator/

sim:
	python3 simulator/run_simulator.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
```

**Verification**:
```bash
make test
# Expected: All 7 tests pass

make lint
# Expected: No errors (or only warnings)
```

**Success Criteria**:
- [ ] `make test` runs all simulator tests successfully
- [ ] `make lint` completes without errors
- [ ] `make sim` launches interactive simulator (if terminal supports)

---

### Task 0.1 Complete - Squash Merge
- [ ] All subtasks complete
- [ ] Squash merge: `git checkout main && git merge --squash feature/0.1-project-setup`

---

## Phase 1: Core Firmware Modules

**Goal**: Implement all hardware abstraction modules
**Status**: COMPLETE

### Task 1.1: Logger Module (COMPLETE)

**Subtask 1.1.1: Logger Module (COMPLETE)**

**Deliverables**:
- [x] Create `firmware/logger.py` with LogLevel class
- [x] Implement Logger class with debug/info/warning/error methods
- [x] Add timestamp formatting
- [x] Add keyword argument support for structured logging

**Completion Notes**:
- **Files Created**: `firmware/logger.py` - 95 lines
- **Status**: COMPLETE, tested via simulator

---

### Task 1.2-1.6: Hardware Managers (COMPLETE)

All hardware abstraction modules implemented:
- [x] `firmware/adc_manager.py` - ADS1115 voltage reading with scaling
- [x] `firmware/relay_manager.py` - 6-channel relay control
- [x] `firmware/neopixel_manager.py` - 8-LED status display
- [x] `firmware/display_manager.py` - SH1107 OLED control
- [x] `firmware/test_modes.py` - Mode definitions and test sequences

**Completion Notes**:
- **Files Created**: 5 modules, ~350 lines total
- **Status**: COMPLETE, all tested via simulator

---

## Phase 2: Main Application

**Goal**: Integrate modules into main application loop
**Status**: Mostly complete

### Task 2.1: Application Integration

**Subtask 2.1.1: Main Application Loop (COMPLETE)**

**Deliverables**:
- [x] Create `firmware/code.py` as CircuitPython entry point
- [x] Initialize all hardware managers
- [x] Implement main loop with button polling
- [x] Implement mode cycling
- [x] Implement voltage reading in vehicle/pass-through modes

**Completion Notes**:
- **Files Created**: `firmware/code.py` - 180 lines
- **Status**: COMPLETE

---

**Subtask 2.1.2: Button Handling Refinement (Single Session)**

**Prerequisites**:
- [x] 2.1.1: Main Application Loop

**Deliverables**:
- [ ] Add debounce logic to button handling (50ms minimum)
- [ ] Add long-press detection for test button (hold 2s for full test)
- [ ] Add button feedback via NeoPixel flash
- [ ] Update `check_buttons()` method in `code.py`

**Files to Modify**:
- `firmware/code.py`

**Complete Code**:

Add to `TrailerTester` class in `firmware/code.py`:

```python
# Add these constants at class level
DEBOUNCE_MS = 50
LONG_PRESS_MS = 2000

def check_buttons(self):
    """Poll buttons with debounce and long-press detection."""
    import time
    current_time = time.monotonic() * 1000  # Convert to ms
    
    # Mode button - simple press with debounce
    mode_current = self.mode_button.value
    if not mode_current and self.mode_button_last:
        if not hasattr(self, '_mode_press_time'):
            self._mode_press_time = 0
        if current_time - self._mode_press_time > self.DEBOUNCE_MS:
            self._cycle_mode()
            self.neopixels.blink_all((255, 255, 255), count=1, on_time=0.05, off_time=0.0)
            self._mode_press_time = current_time
    self.mode_button_last = mode_current
    
    # Test button - detect press start for long-press timing
    test_current = self.test_button.value
    if not test_current and self.test_button_last:
        # Button just pressed
        self._test_press_start = current_time
    elif not test_current and not self.test_button_last:
        # Button held - check for long press
        if hasattr(self, '_test_press_start'):
            hold_time = current_time - self._test_press_start
            if hold_time > self.LONG_PRESS_MS and not getattr(self, '_long_press_triggered', False):
                self._trigger_full_test()
                self._long_press_triggered = True
    elif test_current and not self.test_button_last:
        # Button released
        if hasattr(self, '_test_press_start'):
            hold_time = current_time - self._test_press_start
            if hold_time < self.LONG_PRESS_MS:
                self._trigger_test()
            self._long_press_triggered = False
    self.test_button_last = test_current

def _trigger_full_test(self):
    """Run complete test sequence (long press action)."""
    self.logger.info("Full test sequence triggered (long press)")
    if self.current_mode == TestMode.TRAILER_TESTER:
        self._run_trailer_test_sequence()
```

**Verification**:
```bash
# Run simulator and test button behavior
python3 simulator/test_firmware.py
```

**Success Criteria**:
- [ ] Rapid button presses are debounced (only one action per press)
- [ ] Short press triggers quick action
- [ ] Long press (2s) triggers full test sequence
- [ ] NeoPixel flashes on button press

---

**Subtask 2.1.3: Mode Transition Logic (Single Session)**

**Prerequisites**:
- [x] 2.1.2: Button Handling Refinement

**Deliverables**:
- [ ] Add mode entry/exit hooks for clean transitions
- [ ] Turn off all relays when leaving trailer mode
- [ ] Reset display when changing modes
- [ ] Add mode indicator persistence on NeoPixel

**Files to Modify**:
- `firmware/code.py`
- `firmware/neopixel_manager.py`

**Success Criteria**:
- [ ] Relays always off in vehicle tester mode
- [ ] Display updates immediately on mode change
- [ ] NeoPixel LED 0 shows correct mode color

---

### Task 2.1 Complete - Squash Merge
- [ ] All subtasks complete
- [ ] All tests pass
- [ ] Squash merge: `git checkout main && git merge --squash feature/2.1-application`

---

## Phase 3: Desktop Simulator

**Goal**: Complete simulator for hardware-free development
**Status**: Core complete, interactive UI in progress

### Task 3.1: Simulator Implementation

**Subtask 3.1.1-3.1.3: Mock Modules (COMPLETE)**

**Deliverables**:
- [x] Create mock modules for all CircuitPython hardware
- [x] Create `sim_state.py` for coordinated state management
- [x] Create `test_firmware.py` with automated tests

**Completion Notes**:
- **Files Created**: 12 mock modules, sim_state.py, test_firmware.py
- **Tests**: 7 passing tests
- **Status**: COMPLETE

---

**Subtask 3.1.4: Interactive Terminal UI (Single Session)**

**Prerequisites**:
- [x] 3.1.3: Automated Test Suite

**Deliverables**:
- [ ] Fix terminal raw mode handling in `run_simulator.py`
- [ ] Add graceful exit on 'q' key
- [ ] Add screen refresh rate limiting (10 FPS)
- [ ] Test on macOS Terminal and iTerm2

**Files to Modify**:
- `simulator/run_simulator.py`

**Success Criteria**:
- [ ] Simulator starts without error on macOS
- [ ] Display refreshes smoothly
- [ ] 'q' exits cleanly
- [ ] Keyboard input responsive

---

### Task 3.1 Complete - Squash Merge
- [ ] All subtasks complete
- [ ] All tests pass
- [ ] Squash merge: `git checkout main && git merge --squash feature/3.1-simulator`

---

## Phase 4: Integration & Testing

**Goal**: Test with actual hardware
**Status**: Pending hardware arrival

### Task 4.1: Hardware Validation

**Subtask 4.1.1: Hardware Integration Test (Single Session)**

**Prerequisites**:
- [x] 3.1.4: Interactive Terminal UI
- [ ] Physical hardware assembled on breadboard

**Deliverables**:
- [ ] Copy firmware to Feather RP2040 CIRCUITPY drive
- [ ] Verify OLED displays startup screen
- [ ] Verify NeoPixels light up with startup animation
- [ ] Verify mode button cycles through modes
- [ ] Document any hardware issues

**Success Criteria**:
- [ ] Device boots to vehicle tester mode
- [ ] All 8 NeoPixels illuminate
- [ ] OLED shows readable text
- [ ] Buttons respond to presses

---

**Subtask 4.1.2: Voltage Calibration (Single Session)**

**Prerequisites**:
- [x] 4.1.1: Hardware Integration Test

**Deliverables**:
- [ ] Connect known voltage source (bench supply or battery)
- [ ] Compare displayed voltage to multimeter reading
- [ ] Adjust `VOLTAGE_SCALE` constant if needed
- [ ] Test all 6 input channels
- [ ] Document final calibration values

**Success Criteria**:
- [ ] Readings within 0.3V of actual voltage
- [ ] All channels respond correctly
- [ ] Noise floor under 0.5V

---

**Subtask 4.1.3: End-to-End System Test (Single Session)**

**Prerequisites**:
- [x] 4.1.2: Voltage Calibration

**Deliverables**:
- [ ] Test vehicle mode with actual tow vehicle
- [ ] Test trailer mode with actual trailer (or test lights)
- [ ] Test pass-through mode with both connected
- [ ] Document any field issues
- [ ] Create test checklist for QA

**Success Criteria**:
- [ ] Vehicle mode correctly detects all signals
- [ ] Trailer mode lights up all trailer circuits
- [ ] Pass-through mode shows real-time signal changes

---

### Task 4.1 Complete - Squash Merge
- [ ] All subtasks complete
- [ ] Squash merge: `git checkout main && git merge --squash feature/4.1-hardware-test`

---

## Phase 5: Documentation

**Goal**: Complete user-facing documentation
**Status**: Design docs complete, user docs pending

### Task 5.1: Documentation

**Subtask 5.1.1-5.1.2: Design Documentation (COMPLETE)**

**Deliverables**:
- [x] `docs/HARDWARE_DESIGN.md` - Full specifications
- [x] `docs/SHOPPING_LIST.md` - Adafruit part numbers

**Status**: COMPLETE

---

**Subtask 5.1.3: Assembly Guide (Single Session)**

**Prerequisites**:
- [x] 4.1.1: Hardware Integration Test

**Deliverables**:
- [ ] Create `docs/ASSEMBLY_GUIDE.md`
- [ ] Add step-by-step breadboard assembly instructions
- [ ] Include wiring diagrams for each subsystem
- [ ] Add photos of completed assembly (if available)
- [ ] Document common assembly mistakes

**Files to Create**:
- `docs/ASSEMBLY_GUIDE.md`

**Success Criteria**:
- [ ] Guide is followable by someone with basic electronics experience
- [ ] All connections explicitly documented
- [ ] Safety warnings included

---

**Subtask 5.1.4: User Manual (Single Session)**

**Prerequisites**:
- [x] 4.1.3: End-to-End System Test

**Deliverables**:
- [ ] Create `docs/USER_MANUAL.md`
- [ ] Document all three operating modes
- [ ] Explain NeoPixel color codes
- [ ] Explain OLED display information
- [ ] Add troubleshooting section

**Files to Create**:
- `docs/USER_MANUAL.md`

**Success Criteria**:
- [ ] End user can operate device without technical background
- [ ] All features documented
- [ ] Troubleshooting covers common issues

---

### Task 5.1 Complete - Squash Merge
- [ ] All subtasks complete
- [ ] Squash merge: `git checkout main && git merge --squash feature/5.1-documentation`

---

## Git Workflow

### Branch Strategy
- **One branch per TASK** (e.g., `feature/2.1-application`)
- Commit after each subtask
- Squash merge to main when task complete

### Commit Messages
- Format: `feat(scope): description`
- Scopes: `firmware`, `simulator`, `docs`, `tests`
- Example: `feat(firmware): add button debounce logic`

### Workflow
```bash
# Start a task
git checkout -b feature/2.1-application

# After each subtask
git add . && git commit -m "feat(firmware): implement button debounce"

# When task complete
git checkout main && git merge --squash feature/2.1-application
git commit -m "feat: complete application integration"
git branch -d feature/2.1-application
```

---

## Ready to Build

Most firmware is implemented. Focus areas:
1. Complete Phase 0 (dev environment setup)
2. Refine button handling (Phase 2)
3. Polish simulator UI (Phase 3)
4. Hardware testing when parts arrive (Phase 4)
5. User documentation (Phase 5)

**Next subtask**: `0.1.3` (Development Environment Setup)

---

*Generated for DevPlan methodology*
