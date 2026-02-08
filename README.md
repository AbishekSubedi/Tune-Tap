# TuneTap

TuneTap is a **gesture-controlled music interaction system** that allows users to **play and control music using hand gestures**. The project uses a wearable glove equipped with flex sensors and an **Adafruit Feather Bluefruit Sense** microcontroller programmed in **CircuitPython** to translate finger movements into musical actions.

---

## Project Overview

TuneTap was designed to explore **gesture-based human–computer interaction** in the context of music. By detecting finger bends and hand gestures, the system enables users to interact with music naturally—without traditional buttons, keyboards, or screens.

The project demonstrates how wearable sensors and embedded systems can be combined to create expressive, real-time music control.

---

## Features

- Gesture-based music control  
- Wearable glove interface  
- Real-time sensor processing using CircuitPython  
- Flex sensor–based finger detection  
- Expandable for wireless or advanced music features  

---

## Hardware Components

TuneTap is implemented using embedded hardware and sensors programmed with **CircuitPython** to enable real-time, interactive input processing.

### Microcontroller
- **Adafruit Feather Bluefruit Sense (nRF52840)**
  - CircuitPython-compatible
  - BLE-capable
  - Onboard IMU, microphone, and environmental sensors

### Sensors Used
- **Flex Sensors (mounted on glove fingers)**
  - Detect finger bending
  - Used to trigger musical actions (play, pause, change notes, etc.)

- **LSM6DS3TR-C (IMU)**
  - Detects hand movement and orientation (optional gesture extension)

- **Onboard Microphone**
  - Can be used for sound-reactive features (optional)

### Supporting Components
- Wearable glove
- Perfboard
- Jumper wires
- USB power / battery

---
## How It Works

1. The microcontroller continuously reads data from onboard sensors.
2. Sensor values are processed using CircuitPython logic.
3. Tap, motion, or sound events are detected based on predefined thresholds.
4. The system responds in real time by triggering actions.

The modular structure allows easy expansion with additional sensors or interaction logic.

---

## Hardware Setup

```md
![TuneTap Wearable Setup](images/interface.HEIC)
```

---

## Installation & Setup (CircuitPython)

### Prerequisites
- Adafruit Feather Bluefruit Sense  
- CircuitPython installed on the board  
- USB cable  
- Computer with file access  

### Setup Steps

1. Install **CircuitPython** on the Feather Bluefruit Sense from Adafruit.
2. Download required CircuitPython libraries and place them in the `lib/` folder on the device.
3. Copy the project files to the CircuitPython drive:
   - `code.py`
   - Supporting `.py` modules (if any)

```text
CIRCUITPY/
├── code.py
├── lib/
│   ├── adafruit_lsm6ds/
│   ├── adafruit_bmp280.mpy
│   ├── adafruit_sht31d.mpy
│   ├── adafruit_displayio_sh1107.mpy
│   └── other_required_libraries
```
