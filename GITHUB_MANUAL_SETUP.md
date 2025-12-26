# GitHub Manual Setup - Required Actions

The GitHub CLI doesn't have sufficient permissions to create labels and milestones programmatically. Follow these manual steps to complete repository setup.

---

## Step 1: Create Labels

Navigate to: https://github.com/mmorris35/7wayfun/labels

Click **"New label"** for each of these:

### Component Labels

| Name | Description | Color |
|------|-------------|-------|
| `firmware` | Firmware/CircuitPython code changes | `#d73a4a` (red) |
| `simulator` | Desktop simulator changes | `#0075ca` (blue) |
| `hardware` | Physical hardware related | `#fbca04` (yellow) |
| `mobile` | Mobile app features | `#1d76db` (dark blue) |

### Process Labels

| Name | Description | Color |
|------|-------------|-------|
| `testing` | Test infrastructure and coverage | `#5319e7` (purple) |
| `future` | Long-term future feature | `#e4e669` (light yellow) |

**Note**: These labels supplement the existing default labels (enhancement, bug, documentation, etc.)

---

## Step 2: Create Milestones

Navigate to: https://github.com/mmorris35/7wayfun/milestones

Click **"New milestone"** for each of these:

### Active Development Milestones

#### v1.0 MVP
- **Title**: `v1.0 MVP`
- **Due date**: January 15, 2025
- **Description**: Core functionality: Vehicle tester, trailer tester, pass-through modes with OLED and NeoPixel displays

#### v1.1 Polish
- **Title**: `v1.1 Polish`
- **Due date**: January 31, 2025
- **Description**: Button debouncing, mode transitions, ADC validation, simulator fixes

### Future Milestones (no due dates)

#### v2.0 Mobile Integration
- **Title**: `v2.0 Mobile Integration`
- **Description**: Bluetooth mobile app, data logging, automatic fault diagnosis

#### v2.5 Hardware Refinements
- **Title**: `v2.5 Hardware Refinements`
- **Description**: Production PCB, enclosure design, audio feedback

#### v3.0 Power & Portability
- **Title**: `v3.0 Power & Portability`
- **Description**: Battery operation, USB-C PD charging, solar charging option

#### v3.5 Multi-Standard
- **Title**: `v3.5 Multi-Standard`
- **Description**: Support for 4-way, 5-way, 6-way, European 13-pin connectors with modular adapters

#### v4.0 Professional
- **Title**: `v4.0 Professional`
- **Description**: Fleet management, advanced diagnostics, oscilloscope mode, certification features

#### Future/Ideas
- **Title**: `Future/Ideas`
- **Description**: Ideas parking lot - features under consideration

---

## Step 3: Label Existing Issues

Once labels are created, apply them to issues:

### Issue #1: Button debouncing
- Labels: `enhancement`, `firmware`
- Milestone: `v1.1 Polish`

### Issue #2: Mode transition cleanup
- Labels: `enhancement`, `firmware`
- Milestone: `v1.1 Polish`

### Issue #3: ADC input validation
- Labels: `enhancement`, `firmware`
- Milestone: `v1.1 Polish`

### Issue #4: Pass-through signal integrity
- Labels: `enhancement`, `firmware`
- Milestone: `v1.1 Polish`

### Issue #5: Interactive simulator
- Labels: `bug`, `simulator`
- Milestone: `v1.1 Polish`

### Issue #6: User documentation
- Labels: `documentation`
- Milestone: `v1.0 MVP`

### Issue #7: Voltage calibration
- Labels: `enhancement`, `hardware`
- Milestone: `v1.0 MVP`

### Issue #8: Bluetooth mobile app
- Labels: `enhancement`, `mobile`, `future`
- Milestone: `v2.0 Mobile Integration`

### Issue #9: SD card logging
- Labels: `enhancement`, `hardware`, `firmware`, `future`
- Milestone: `v2.0 Mobile Integration`

### Issue #10: Automatic fault diagnosis
- Labels: `enhancement`, `firmware`, `future`
- Milestone: `v2.0 Mobile Integration`

### Issue #11: Production PCB
- Labels: `enhancement`, `hardware`, `future`
- Milestone: `v2.5 Hardware Refinements`

### Issue #12: Weatherproof enclosure
- Labels: `enhancement`, `hardware`, `future`
- Milestone: `v2.5 Hardware Refinements`

### Issue #13: Audio feedback
- Labels: `enhancement`, `firmware`, `hardware`, `future`
- Milestone: `v2.5 Hardware Refinements`

### Issue #14: Battery operation
- Labels: `enhancement`, `hardware`, `firmware`, `future`
- Milestone: `v3.0 Power & Portability`

### Issue #15: Solar charging
- Labels: `enhancement`, `hardware`, `future`
- Milestone: `v3.0 Power & Portability`

### Issue #16: Multi-standard connectors
- Labels: `enhancement`, `hardware`, `firmware`, `future`
- Milestone: `v3.5 Multi-Standard`

### Issue #17: Fleet management
- Labels: `enhancement`, `mobile`, `future`
- Milestone: `v4.0 Professional`

### Issue #18: Advanced diagnostics
- Labels: `enhancement`, `firmware`, `hardware`, `future`
- Milestone: `v4.0 Professional`

### Issue #19: DOT certification
- Labels: `enhancement`, `mobile`, `documentation`, `future`
- Milestone: `v4.0 Professional`

### Issue #20: Accessibility/UX ideas
- Labels: `enhancement`, `future`, `help wanted`, `good first issue`
- Milestone: `Future/Ideas`

### Issue #21: Advanced electrical testing
- Labels: `enhancement`, `hardware`, `firmware`, `future`, `help wanted`
- Milestone: `Future/Ideas`

---

## Step 4: Quick Labeling via Web UI

For each issue, click the issue number, then:
1. Click the **gear icon** next to "Labels" on the right sidebar
2. Select appropriate labels from the checkboxes
3. Click the **gear icon** next to "Milestone"
4. Select the appropriate milestone
5. Changes save automatically

---

## Step 5: Verify Setup

Check the following views:

- **[Issues by Milestone](https://github.com/mmorris35/7wayfun/milestones)** - Should show 8 milestones with issue counts
- **[Issues by Label](https://github.com/mmorris35/7wayfun/labels)** - Should show all labels with issue counts
- **[Project Board](https://github.com/mmorris35/7wayfun/issues)** - Filter by milestone or label to organize work

---

## Why Manual Setup?

GitHub CLI (`gh`) returned 404 errors when attempting to create labels and milestones programmatically. Possible causes:
- Repository permissions/authentication scope limitations
- API access restrictions
- GitHub CLI version or configuration issues

Manual setup via web UI is reliable and takes approximately 10-15 minutes.

---

## After Setup

Once labels and milestones are configured, you can:
- Filter issues by milestone to see roadmap progress
- Filter by label to focus on specific areas (firmware, hardware, etc.)
- Use project boards with automation based on labels
- Track milestone completion percentage

---

*Setup checklist created: December 26, 2024*
