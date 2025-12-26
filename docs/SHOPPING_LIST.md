# 7-Way Trailer Tester - Adafruit Shopping List

## Quick Order List

Copy these product IDs to add to your Adafruit cart quickly.

### Essential Components (Adafruit)

| Product ID | Description | Qty | Price |
|------------|-------------|-----|-------|
| [4884](https://www.adafruit.com/product/4884) | Feather RP2040 | 1 | $11.95 |
| [4650](https://www.adafruit.com/product/4650) | FeatherWing OLED 128x64 | 1 | $14.95 |
| [1426](https://www.adafruit.com/product/1426) | NeoPixel Stick (8x WS2812B) | 1 | $5.95 |
| [1085](https://www.adafruit.com/product/1085) | ADS1115 16-Bit ADC | 2 | $14.95 ea |
| [5648](https://www.adafruit.com/product/5648) | 4-Channel STEMMA Relay | 2 | $9.95 ea |
| [4399](https://www.adafruit.com/product/4399) | Feather Stacking Headers | 1 | $1.25 |
| [4210](https://www.adafruit.com/product/4210) | STEMMA QT Breadboard Adapter | 2 | $1.50 ea |
| [4209](https://www.adafruit.com/product/4209) | STEMMA QT Cable 100mm | 3 | $0.95 ea |
| [1385](https://www.adafruit.com/product/1385) | Buck Converter 5V 3A | 1 | $4.95 |

**Adafruit Subtotal: ~$95**

### Prototyping Supplies (Adafruit)

| Product ID | Description | Qty | Price |
|------------|-------------|-----|-------|
| [64](https://www.adafruit.com/product/64) | Half-Size Breadboard | 2 | $5.00 ea |
| [153](https://www.adafruit.com/product/153) | Breadboard Jumper Wire Bundle | 1 | $6.95 |
| [2892](https://www.adafruit.com/product/2892) | Through-Hole Resistor Kit | 1 | $7.95 |
| [3299](https://www.adafruit.com/product/3299) | Tactile Button Assortment | 1 | $6.95 |
| [3628](https://www.adafruit.com/product/3628) | Terminal Block 2-pin (5pk) | 1 | $2.50 |
| [4184](https://www.adafruit.com/product/4184) | SPDT Slide Switch | 2 | $0.95 ea |
| [2830](https://www.adafruit.com/product/2830) | USB-C Cable | 1 | $4.95 |

**Prototyping Subtotal: ~$42**

### Wire and Connectors (Adafruit)

| Product ID | Description | Qty | Price |
|------------|-------------|-----|-------|
| [3314](https://www.adafruit.com/product/3314) | Silicone Wire 22AWG (various) | 1 | $9.95 |
| [2880](https://www.adafruit.com/product/2880) | Alligator Clips to Male Header | 1 | $3.95 |

---

## Non-Adafruit Components

### 7-Way Trailer Connectors (Amazon/Hardware Store)

| Item | Description | Qty | Est. Price |
|------|-------------|-----|------------|
| 7-Way Blade Plug (Male) | Connects to vehicle socket | 1 | ~$8 |
| 7-Way Blade Socket (Female) | Connects to trailer plug | 1 | ~$8 |

**Search terms:**
- "7 way trailer plug male blade"
- "7 way trailer connector female RV"

**Recommended brands:** Hopkins, CURT, Reese

### Protection Components (DigiKey/Mouser)

| Part Number | Description | Qty | Notes |
|-------------|-------------|-----|-------|
| 1N4728A | 3.3V Zener Diode | 10 | Overvoltage protection |
| P6KE18A | TVS Diode 18V | 2 | Transient suppression |
| 1N4007 | Rectifier Diode | 10 | Reverse polarity |

**Or buy a diode assortment kit from Amazon (~$8)**

### Fusing (Auto Parts Store)

| Item | Description | Qty |
|------|-------------|-----|
| Inline blade fuse holder | For 12V main input | 1 |
| 10A blade fuses | Standard automotive | 5 |

---

## Complete Order Summary

| Category | Estimated Cost |
|----------|----------------|
| Adafruit Electronics | $95 |
| Adafruit Prototyping | $42 |
| 7-Way Connectors | $16 |
| Protection Components | $10 |
| Fuses/Holders | $5 |
| **Total** | **~$170** |

---

## Adafruit Quick Cart Link

Visit Adafruit and search these product numbers:
4884, 4650, 1426, 1085, 5648, 4399, 4210, 4209, 1385, 64, 153, 2892, 3299, 3628, 4184, 2830, 3314, 2880

---

## Notes

1. **Voltage Divider Resistors**: The resistor kit (2892) includes the 10K and 2.7K resistors needed for the input voltage dividers.

2. **I2C Addressing**: The two ADS1115 boards need different addresses:
   - Board 1: Leave ADDR pin floating or connect to GND (0x48)
   - Board 2: Connect ADDR pin to VDD (0x49)

3. **Alternative ADC Option**: If you want more precision, consider:
   - [1083](https://www.adafruit.com/product/1083) - ADS1015 12-bit ADC ($9.95, cheaper but lower resolution)

4. **Relay Alternative**: If the STEMMA relay boards are out of stock:
   - Use any logic-level (3.3V compatible) relay module
   - Common 8-channel relay boards on Amazon work fine (~$8)

5. **Power Considerations**: The buck converter should be mounted with airflow. For permanent install, consider adding a small heatsink.
