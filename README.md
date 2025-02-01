# M4rshe1/rbpi0sb

# Raspberry Pi Zero Soundboard

## Overview
This project is a **custom soundboard** built using a Raspberry Pi Zero. It features:
- **Rotary Encoder** for scrolling & selecting sounds
- **6 Macro Buttons** to quickly play assigned sounds
- **Set Button** to assign sounds to macro buttons
- **OLED Display** to show available sounds
- **Stop Button** to immediately halt playback
- **Speaker Output** for audio playback
- **Easy File Management** (just add/remove sound files from the `sounds` folder)
- **Supports Multiple Formats** (MP3, WAV, OGG, etc.)

## Hardware Requirements
- **Raspberry Pi Zero (or any Pi model)**
- **128x64 OLED Display (SSD1306, I2C)**
- **Rotary Encoder with push button**
- **7 Push Buttons** (6 Macro + 1 Set Button + 1 Stop Button)
- **Speaker or Audio Output (USB or 3.5mm jack)**
- **Resistors & Wires**

## Wiring Table

| **Component**     | **GPIO Pin** | **Physical Pin** | **Notes** |
|------------------|------------|----------------|----------|
| **Rotary CLK**   | GPIO 17    | Pin 11         | Rotary Encoder Clock |
| **Rotary DT**    | GPIO 27    | Pin 13         | Rotary Encoder Data |
| **Rotary SW**    | GPIO 22    | Pin 15         | Rotary Encoder Push |
| **Stop Button**  | GPIO 23    | Pin 16         | Stops sound playback |
| **Set Button**   | GPIO 20    | Pin 38         | Assigns sounds to macro buttons |
| **Macro 1**      | GPIO 5     | Pin 29         | Macro button 1 |
| **Macro 2**      | GPIO 6     | Pin 31         | Macro button 2 |
| **Macro 3**      | GPIO 13    | Pin 33         | Macro button 3 |
| **Macro 4**      | GPIO 19    | Pin 35         | Macro button 4 |
| **Macro 5**      | GPIO 26    | Pin 37         | Macro button 5 |
| **Macro 6**      | GPIO 21    | Pin 40         | Macro button 6 |
| **OLED SDA**     | GPIO 2 (SDA)  | Pin 3         | I2C Data |
| **OLED SCL**     | GPIO 3 (SCL)  | Pin 5         | I2C Clock |
| **GND**          | GND        | Various Pins   | Ground connections |

## Installation

1. **Set up Raspberry Pi:**
    - Install **Raspberry Pi OS Lite**
    - Enable **I2C** for the OLED display

2. **Install dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-pygame ffmpeg i2c-tools
   pip3 install adafruit-circuitpython-ssd1306 pydub
   ```

3. **Create a Sounds Folder:**
   ```bash
   mkdir -p ~/sounds
   ```
   Add **MP3, WAV, OGG, or other supported files** to this folder.

4. **Run the Soundboard:**
   ```bash
   python3 soundboard.py
   ```

## Usage

- **Rotate the encoder** to scroll through sounds.
- **Press the encoder** to play the selected sound.
- **Press the Set button** and then a macro button to assign a sound.
- **Press a macro button** to play an assigned sound.
- **Press the Stop button** to halt playback.

## Future Improvements
- LED indicators for playing/stopped states
- Bluetooth speaker support
- Volume control knob

---

**Enjoy your custom soundboard! 🎵🎛️**

