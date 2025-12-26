# CLAUDE.md - Project Rules for trailer-tester

> This document defines HOW Claude Code should work on trailer-tester.
> Read at the start of every session to maintain consistency.

## Project Overview

**trailer-tester** is embedded firmware for a 7-way trailer wiring tester built with Adafruit CircuitPython hardware. The codebase has two execution environments:

1. **CircuitPython on Feather RP2040** - Production firmware in `firmware/`
2. **Desktop Python simulation** - Development/testing in `simulator/`

## Project Structure

```
trailer-tester/
├── firmware/                    # CircuitPython firmware (runs on device)
│   ├── code.py                 # Main entry point (CircuitPython convention)
│   ├── logger.py               # Centralized logging
│   ├── adc_manager.py          # ADS1115 voltage reading
│   ├── relay_manager.py        # 6-channel relay control
│   ├── neopixel_manager.py     # 8-LED status display
│   ├── display_manager.py      # SH1107 OLED control
│   └── test_modes.py           # Mode definitions
├── simulator/                   # Desktop simulation (Python 3.8+)
│   ├── mock_*.py               # Mock CircuitPython modules
│   ├── sim_state.py            # Simulation state manager
│   ├── test_firmware.py        # Automated test suite
│   └── run_simulator.py        # Interactive terminal UI
├── docs/                        # Documentation
│   ├── HARDWARE_DESIGN.md      # Full hardware specifications
│   └── SHOPPING_LIST.md        # Adafruit part numbers
├── PROJECT_BRIEF.md            # Requirements document
├── DEVELOPMENT_PLAN.md         # Task tracking
└── CLAUDE.md                   # This file
```

## Core Operating Principles

### 1. Single Session Execution
- Complete the ENTIRE subtask in one session
- End every session with a git commit
- If blocked, document why and mark as BLOCKED

### 2. Read Before Acting
Every session must begin with:
1. Read this file (CLAUDE.md)
2. Read DEVELOPMENT_PLAN.md completely
3. Locate the specific subtask ID from the prompt
4. Verify prerequisites are marked `[x]` complete

### 3. Dual Environment Awareness

**Firmware code** (`firmware/`):
- Uses CircuitPython libraries (board, digitalio, neopixel, etc.)
- Runs on Feather RP2040 microcontroller
- Entry point is `code.py` (CircuitPython convention)
- No f-strings in older CircuitPython (use `.format()` or `%`)

**Simulator code** (`simulator/`):
- Uses standard Python 3.8+
- Mocks all CircuitPython hardware modules
- Can use modern Python features

**When modifying firmware**: Always verify it works in simulator first!

## Commands

| Command | Purpose |
|---------|---------|
| `make test` | Run simulator tests |
| `make lint` | Run ruff linter |
| `make format` | Format code with ruff |
| `make sim` | Launch interactive simulator |
| `make clean` | Remove __pycache__ directories |

## Coding Standards

### Python Style
- No single-letter variable names (except `i`, `j` in tight loops)
- Type hints on all functions in simulator code
- Docstrings on all public functions
- Max line length: 100 characters

### CircuitPython Specifics
- Use `from micropython import const` for constants
- Prefer integer math over floats where possible
- Minimize memory allocations in main loop
- Use `time.monotonic()` not `time.time()`

### Logging
All modules must use the centralized logger:
```python
from logger import Logger, LogLevel

logger = Logger(name="mymodule", level=LogLevel.DEBUG)
logger.info("Operation complete", count=42)
```

### Error Handling
- Catch specific exceptions, not bare `except:`
- Log errors with context
- Graceful degradation preferred over crashing

## Testing Requirements

### Running Tests
```bash
# All tests via Makefile
make test

# Direct execution
python3 simulator/test_firmware.py

# Expected output: 7 passed, 0 failed
```

### Test Coverage
- All firmware modules must be testable via simulator
- Minimum 80% coverage target
- Test success, failure, and edge cases

### Before Every Commit
- [ ] `make test` passes (7/7 tests)
- [ ] `make lint` has no errors
- [ ] Code runs in simulator without errors

## Git Workflow

### Branch Naming
- Feature branches: `feature/{phase}.{task}-description`
- Example: `feature/2.1-application`

### Commit Messages
Format: `type(scope): description`

Types:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `test` - Test changes
- `docs` - Documentation

Scopes:
- `firmware` - CircuitPython code
- `simulator` - Desktop simulation
- `docs` - Documentation

Examples:
```bash
git commit -m "feat(firmware): add button debounce logic"
git commit -m "fix(simulator): correct ADC voltage scaling"
git commit -m "docs: add assembly guide"
```

## Completion Protocol

### When a subtask is complete:

1. **Update DEVELOPMENT_PLAN.md** with completion notes:
```markdown
**Completion Notes**:
- **Implementation**: Brief description of what was built
- **Files Created**: 
  - `firmware/newmodule.py` - 120 lines
- **Files Modified**:
  - `firmware/code.py`
- **Tests**: X tests passing
- **Status**: COMPLETE
```

2. **Check all checkboxes** in the subtask (change `[ ]` to `[x]`)

3. **Git commit** with semantic message

4. **Report completion** with summary

## Hardware Reference

### 7-Way Connector Pinout
| Pin | Function | Wire Color | ADC/Relay Index |
|-----|----------|------------|-----------------|
| 2 | Brake | Blue | 0 |
| 3 | Tail | Brown | 1 |
| 4 | Left Turn | Yellow | 2 |
| 5 | Right Turn | Green | 3 |
| 6 | Aux 12V | Red | 4 |
| 7 | Reverse | Purple | 5 |

### GPIO Assignments
| Pin | Function |
|-----|----------|
| D5 | NeoPixel Data |
| D6 | Relay 0 (Brake) |
| D9 | Relay 1 (Tail) |
| D10 | Relay 2 (Left) |
| D11 | Relay 3 (Right) |
| D12 | Relay 4 (Aux) |
| D13 | Relay 5 (Reverse) |
| D24 | Mode Button |
| D25 | Test Button |

### I2C Devices
| Address | Device |
|---------|--------|
| 0x3C | OLED Display (SH1107) |
| 0x48 | ADC #1 (Brake, Tail, Left, Right) |
| 0x49 | ADC #2 (Aux, Reverse) |

## Session Checklists

### Starting a Session
- [ ] Read CLAUDE.md (this file)
- [ ] Read DEVELOPMENT_PLAN.md
- [ ] Identify subtask from prompt
- [ ] Verify prerequisites complete
- [ ] Understand success criteria
- [ ] Ready to code!

### Ending a Session
- [ ] All subtask checkboxes checked
- [ ] `make test` passes
- [ ] `make lint` clean
- [ ] Completion notes written in DEVELOPMENT_PLAN.md
- [ ] Git commit with semantic message
- [ ] Summary reported

## Prohibited Practices

- No `print()` statements (use logger)
- No single-letter variable names
- No bare `except:` clauses
- No hardcoded pin numbers outside managers
- No modifications to mock modules for test-specific behavior (use sim_state instead)

---

**Version**: 1.0
**Last Updated**: 2024
**Project**: trailer-tester
