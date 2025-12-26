# Voltage Calibration Procedure

Procedure for calibrating the ADC voltage readings to ensure ±0.5V accuracy.

---

## When to Calibrate

**Required:**
- After initial assembly
- When replacing ADC boards
- When changing voltage divider resistors
- If readings drift over time

**Recommended:**
- Annually if device is used regularly
- After any repairs to input circuitry

---

## Prerequisites

**Equipment needed:**
- Calibrated digital multimeter (±0.1V accuracy or better)
- Adjustable bench power supply (0-15V, 1A) **OR** automotive battery
- Test leads with alligator clips
- Computer with Python 3 and USB cable

**Firmware access:**
- Copy of firmware source code
- Ability to edit `firmware/adc_manager.py`
- CircuitPython installed on device

**Skills:**
- Basic multimeter usage
- Text file editing
- File transfer to CircuitPython device

---

## Test Setup

### Option A: Bench Power Supply (Recommended)

1. Set power supply to 12.0V
2. Verify voltage with multimeter
3. Connect positive lead to test clip
4. Connect negative lead to ground clip

**Advantages:**
- Precise, stable voltage
- Easy to adjust for different test points
- No battery discharge concerns

### Option B: Automotive Battery

1. Verify battery is fully charged (12.6V - 12.8V resting)
2. Disconnect from vehicle if possible
3. Use quality test leads

**Advantages:**
- Realistic test voltage
- Tests under actual operating conditions

**Disadvantages:**
- Voltage varies with charge state
- Alternator voltage (14.4V) requires running engine

---

## Calibration Procedure

### Step 1: Prepare the Device

1. **Power on the trailer tester**
2. **Select Vehicle Tester mode:**
   - Press Mode button until "VEHICLE_TESTER" appears on OLED
3. **Verify display is updating:**
   - All channels should show 0.0V with no inputs connected

### Step 2: Test Each Channel

For each of the 6 channels, perform this sequence:

1. **Connect test voltage to channel input**
   - Use color-coded test leads matching wire colors
   - Ensure solid connection

2. **Measure actual voltage with multimeter**
   - Connect multimeter directly to input pin
   - Record reading to 0.1V precision
   - Example: 12.04V

3. **Read displayed voltage on tester**
   - Wait for reading to stabilize (1-2 seconds)
   - Record reading from OLED display
   - Example: 12.6V

4. **Calculate error:**
   - Error = Displayed - Actual
   - Example: 12.6V - 12.04V = +0.56V

5. **Disconnect and move to next channel**

### Step 3: Record Measurements

Create a table with your measurements:

| Channel | Pin | Color | Actual (V) | Displayed (V) | Error (V) |
|---------|-----|-------|------------|---------------|-----------|
| Brake | 2 | Blue | 12.04 | 12.6 | +0.56 |
| Tail | 3 | Green | 12.04 | 12.5 | +0.46 |
| Left | 4 | Red | 12.04 | 12.7 | +0.66 |
| Right | 5 | Brown | 12.04 | 12.5 | +0.46 |
| Aux | 6 | Black | 12.04 | 12.6 | +0.56 |
| Reverse | 7 | Yellow | 12.04 | 12.5 | +0.46 |

### Step 4: Calculate Average Error

1. **Sum all errors:** +0.56 + 0.46 + 0.66 + 0.46 + 0.56 + 0.46 = +3.16V
2. **Divide by number of channels:** 3.16V / 6 = +0.527V
3. **Average error:** +0.53V (round to 2 decimals)

### Step 5: Calculate New Scaling Factor

**Current scaling factor:**
- Default value in code: `VOLTAGE_SCALE = 4.7`

**Formula:**
```
new_scale = old_scale * (displayed_average / actual_average)
```

**Example calculation:**
- Actual average: 12.04V
- Displayed average: 12.04 + 0.53 = 12.57V
- New scale: 4.7 * (12.04 / 12.57) = 4.7 * 0.9578 = 4.50

**Adjustment direction:**
- If readings are **too high** → **decrease** VOLTAGE_SCALE
- If readings are **too low** → **increase** VOLTAGE_SCALE

### Step 6: Update Firmware

1. **Open firmware file:**
   ```
   firmware/adc_manager.py
   ```

2. **Locate the VOLTAGE_SCALE constant:**
   ```python
   # Voltage divider scaling factor
   # With R1=10K, R2=2.7K: ratio = (10K + 2.7K) / 2.7K = 4.7
   VOLTAGE_SCALE = 4.7
   ```

3. **Update value:**
   ```python
   # Voltage divider scaling factor
   # Calibrated: [DATE] - Average error was +0.53V
   # With R1=10K, R2=2.7K: ratio = (10K + 2.7K) / 2.7K = 4.7 (calculated)
   VOLTAGE_SCALE = 4.50  # Adjusted from 4.7 based on calibration
   ```

4. **Save file**

5. **Transfer to device:**
   - Copy `adc_manager.py` to CIRCUITPY drive
   - Wait for device to reload
   - Device will reset automatically

### Step 7: Verify Calibration

1. **Reconnect test voltage** to first channel (Brake)
2. **Check displayed value:**
   - Should now match multimeter reading within ±0.3V
   - Example: Multimeter 12.04V, Display 12.1V = 0.06V error ✓

3. **Test all channels:**
   - Repeat measurement on all 6 channels
   - All should be within ±0.3V of actual

4. **If still out of spec:**
   - Check for wiring issues
   - Verify resistor values (10K and 2.7K)
   - Check zener diode orientation
   - Repeat calibration procedure

---

## Noise Floor Measurement

The noise floor is the voltage reading when no input is applied.

**Procedure:**

1. **Disconnect all inputs** (all channels open circuit)
2. **Record readings** for each channel
3. **Acceptable noise:** < 0.5V

**Example:**
| Channel | Noise (V) | Status |
|---------|-----------|--------|
| Brake | 0.1 | ✓ OK |
| Tail | 0.2 | ✓ OK |
| Left | 0.1 | ✓ OK |
| Right | 0.8 | ✗ HIGH |
| Aux | 0.1 | ✓ OK |
| Reverse | 0.2 | ✓ OK |

**If noise is high (>0.5V):**
- Check for loose connections
- Verify zener diodes are installed
- Check for electromagnetic interference
- Ensure proper grounding
- May need to adjust `NOISE_FLOOR` constant in firmware (default 0.3V)

---

## Advanced Calibration

### Per-Channel Calibration

If channels have significantly different errors (>0.3V variation), individual calibration may be needed:

1. **Measure error for each channel** (as in Step 2)
2. **Calculate per-channel scale factors**
3. **Modify firmware** to use channel-specific scaling:

```python
VOLTAGE_SCALES = {
    'brake': 4.50,
    'tail': 4.65,
    'left': 4.40,
    'right': 4.65,
    'aux': 4.50,
    'reverse': 4.65,
}
```

**Note:** This requires firmware modification to use dict instead of single constant.

### Temperature Compensation

If you notice drift with temperature:

1. **Record readings at different temperatures**
   - Cold: 0°C - 10°C
   - Room: 20°C - 25°C
   - Warm: 35°C - 40°C

2. **Calculate temperature coefficient**
3. **Consider adding temperature sensor** and compensation algorithm

**Typical drift:** ±0.1V over 0-40°C range (usually acceptable)

---

## Calibration Record

Document your calibration in `HARDWARE_DESIGN.md` or create a calibration log:

```
CALIBRATION RECORD

Date: December 26, 2024
Technician: [Your Name]
Device S/N: [Serial Number if applicable]

Test Equipment:
- Multimeter: Fluke 87V (Cal due: 06/2025)
- Power Supply: BK Precision 1672 (Cal due: 12/2025)

Test Voltage: 12.04V (measured)

Initial Readings:
- Average error: +0.53V
- Max error: +0.66V (Left channel)
- Min error: +0.46V (Tail, Right, Reverse channels)

Calibration:
- Old VOLTAGE_SCALE: 4.7
- New VOLTAGE_SCALE: 4.50
- Adjustment: -0.20 (-4.3%)

Post-Calibration Verification:
- All channels within ±0.1V of actual
- Noise floor: <0.2V all channels
- Result: PASS

Next calibration due: December 2025
```

---

## Troubleshooting Calibration Issues

### Readings Still Inaccurate After Calibration

**Possible causes:**

1. **Incorrect resistor values:**
   - Verify with multimeter
   - 10K resistor should read 9.5K - 10.5K (±5%)
   - 2.7K resistor should read 2.5K - 2.9K (±5%)

2. **ADC reference voltage incorrect:**
   - Should be 3.3V
   - Measure at ADC VDD pin
   - Check 3.3V regulator on Feather

3. **Math error in calculation:**
   - Double-check formula
   - Verify division direction
   - Common mistake: inverted fraction

### Different Channels Read Differently

**Indicates:**
- Different resistor tolerances per channel
- Possible wiring issue on one channel
- ADC board issue

**Solution:**
- Use per-channel calibration
- Check individual resistors
- Test ADC with known voltage source

### Readings Drift During Use

**Possible causes:**
- Temperature effects
- Poor connections heating up
- Power supply instability

**Solution:**
- Allow warm-up time (5 minutes)
- Check connection quality
- Use voltage regulator for cleaner reference

---

## Success Criteria

Calibration is complete when:

- [ ] All 6 channels measured at known voltage
- [ ] Average error calculated
- [ ] New VOLTAGE_SCALE calculated and applied
- [ ] Post-calibration verification performed
- [ ] All channels read within ±0.5V of actual (±0.3V recommended)
- [ ] Noise floor <0.5V on all channels
- [ ] Calibration documented

---

## Maintenance Calibration Schedule

| Condition | Recommended Interval |
|-----------|---------------------|
| Normal use (monthly) | Annually |
| Heavy use (daily) | Every 6 months |
| Harsh environment | Every 3 months |
| After repair | Immediately |
| After resistor replacement | Immediately |

---

*Calibration Procedure v1.0 - December 2024*
