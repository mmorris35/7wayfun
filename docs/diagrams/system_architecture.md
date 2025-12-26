# System Architecture Diagram

## High-Level Block Diagram

```mermaid
graph TB
    subgraph Vehicle["Vehicle 7-Way Connector"]
        V1[Pin 2: Brake - Blue]
        V2[Pin 3: Tail - Brown]
        V3[Pin 4: Left - Yellow]
        V4[Pin 5: Right - Green]
        V5[Pin 6: Aux - Red]
        V6[Pin 7: Reverse - Purple]
        VG[Pin 1: Ground - White]
    end

    subgraph Input["Input Stage"]
        VD1[Voltage Divider 1<br/>10K + 2.7K]
        VD2[Voltage Divider 2<br/>10K + 2.7K]
        VD3[Voltage Divider 3<br/>10K + 2.7K]
        VD4[Voltage Divider 4<br/>10K + 2.7K]
        VD5[Voltage Divider 5<br/>10K + 2.7K]
        VD6[Voltage Divider 6<br/>10K + 2.7K]
        ZENER[Zener Protection<br/>3.6V]
    end

    subgraph ADC["ADC Subsystem"]
        ADC1[ADS1115 #1<br/>I2C: 0x48<br/>Channels 0-3]
        ADC2[ADS1115 #2<br/>I2C: 0x49<br/>Channels 0-1]
    end

    subgraph MCU["Feather RP2040"]
        CPU[RP2040<br/>Dual Core Cortex-M0+]
        I2C_BUS[I2C Bus<br/>SDA/SCL]
        GPIO[GPIO Pins<br/>D5-D13, D24-D25]
    end

    subgraph Display["Display Subsystem"]
        OLED[SH1107 OLED<br/>128x64<br/>I2C: 0x3C]
        NEO[NeoPixel Strip<br/>8x WS2812B<br/>PWM on D5]
    end

    subgraph Output["Output Stage"]
        R1[Relay 1: Brake<br/>D6]
        R2[Relay 2: Tail<br/>D9]
        R3[Relay 3: Left<br/>D10]
        R4[Relay 4: Right<br/>D11]
        R5[Relay 5: Aux<br/>D12]
        R6[Relay 6: Reverse<br/>D13]
    end

    subgraph Trailer["Trailer 7-Way Connector"]
        T1[Pin 2: Brake]
        T2[Pin 3: Tail]
        T3[Pin 4: Left]
        T4[Pin 5: Right]
        T5[Pin 6: Aux]
        T6[Pin 7: Reverse]
        TG[Pin 1: Ground]
    end

    subgraph Power["Power Supply"]
        VIN[12V Vehicle Power]
        BUCK[Buck Converter<br/>12V → 5V]
        LDO[LDO Regulator<br/>5V → 3.3V]
    end

    subgraph UI["User Interface"]
        MODE[Mode Button<br/>D24]
        TEST[Test Button<br/>D25]
    end

    V1 --> VD1 --> ZENER
    V2 --> VD2 --> ZENER
    V3 --> VD3 --> ZENER
    V4 --> VD4 --> ZENER
    V5 --> VD5 --> ZENER
    V6 --> VD6 --> ZENER

    VD1 --> ADC1
    VD2 --> ADC1
    VD3 --> ADC1
    VD4 --> ADC1
    VD5 --> ADC2
    VD6 --> ADC2

    ADC1 --> I2C_BUS
    ADC2 --> I2C_BUS
    OLED --> I2C_BUS
    I2C_BUS --> CPU

    CPU --> GPIO
    GPIO --> NEO
    GPIO --> R1 --> T1
    GPIO --> R2 --> T2
    GPIO --> R3 --> T3
    GPIO --> R4 --> T4
    GPIO --> R5 --> T5
    GPIO --> R6 --> T6

    VIN --> BUCK --> LDO
    LDO --> CPU
    LDO --> ADC1
    LDO --> ADC2
    BUCK --> OLED
    BUCK --> NEO
    VIN --> R1
    VIN --> R2
    VIN --> R3
    VIN --> R4
    VIN --> R5
    VIN --> R6

    MODE --> CPU
    TEST --> CPU

    VG -.-> TG

    style Vehicle fill:#e1f5ff
    style Input fill:#fff3cd
    style ADC fill:#d4edda
    style MCU fill:#f8d7da
    style Display fill:#d1ecf1
    style Output fill:#fff3cd
    style Trailer fill:#e1f5ff
    style Power fill:#f5c6cb
    style UI fill:#e2e3e5
```

## Component Details

| Component | Model | Interface | Address/Pin | Purpose |
|-----------|-------|-----------|-------------|---------|
| **MCU** | Feather RP2040 | - | - | Main controller |
| **ADC #1** | ADS1115 | I2C | 0x48 | Channels 0-3: Brake, Tail, Left, Right |
| **ADC #2** | ADS1115 | I2C | 0x49 | Channels 0-1: Aux, Reverse |
| **Display** | SH1107 OLED | I2C | 0x3C | 128x64 pixel display |
| **LEDs** | WS2812B NeoPixel | PWM | D5 | 8-LED status strip |
| **Relay 1** | STEMMA Relay | GPIO | D6 | Brake output |
| **Relay 2** | STEMMA Relay | GPIO | D9 | Tail output |
| **Relay 3** | STEMMA Relay | GPIO | D10 | Left turn output |
| **Relay 4** | STEMMA Relay | GPIO | D11 | Right turn output |
| **Relay 5** | STEMMA Relay | GPIO | D12 | Aux output |
| **Relay 6** | STEMMA Relay | GPIO | D13 | Reverse output |
| **Mode Button** | Tactile Switch | GPIO | D24 | Mode selection |
| **Test Button** | Tactile Switch | GPIO | D25 | Test trigger |

## Signal Flow

### Vehicle Tester Mode
1. Vehicle signals enter through 7-way connector
2. Voltage dividers scale 12V → 3.3V range
3. Zener diodes protect against overvoltage
4. ADS1115 ADCs read voltages (16-bit resolution)
5. I2C bus transmits readings to RP2040
6. Firmware scales back to original voltage (×4.7)
7. OLED displays voltage readings
8. NeoPixels show active/idle status

### Trailer Tester Mode
1. User presses test button
2. RP2040 activates relays sequentially
3. 12V vehicle power switched through relays
4. Signals output to trailer connector
5. NeoPixels show which output is active
6. OLED displays test progress

### Pass-Through Mode
1. Vehicle signals monitored via ADCs
2. Relays can pass signals to trailer (if needed)
3. Real-time monitoring of all channels
4. Both displays show current state
