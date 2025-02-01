import os
import json
import pygame
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import board
import digitalio
import adafruit_ssd1306

# --- CONFIG ---
SOUND_FOLDER = "/home/pi/sounds/"
MACRO_FILE = "/home/pi/macros.json"
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
ROWS_VISIBLE = 3  # Number of sounds visible (excluding index row)

# --- GPIO Setup ---
encoder_clk = 17
encoder_dt = 27
encoder_sw = 22
stop_button = 23
set_button = 20
macro_buttons = [5, 6, 13, 19, 26, 21]

GPIO.setmode(GPIO.BCM)
GPIO.setup([encoder_clk, encoder_dt, encoder_sw, stop_button, set_button] + macro_buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Initialize Display (SSD1306 OLED via I2C) ---
i2c = board.I2C()
display = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
font = ImageFont.load_default()

# --- Initialize Audio ---
pygame.mixer.init()

# --- Load Sound Files ---
def get_sound_files():
    return sorted([f for f in os.listdir(SOUND_FOLDER) if f.endswith(".wav")])

sound_files = get_sound_files()
current_index = 0
setting_macro = False  # Flag to track macro setting mode

# --- Load/Save Macros ---
def load_macros():
    if os.path.exists(MACRO_FILE):
        with open(MACRO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_macros():
    with open(MACRO_FILE, "w") as f:
        json.dump(macros, f)

macros = load_macros()

# --- Display Update ---
def update_display():
    global current_index
    display.fill(0)

    image = Image.new("1", (DISPLAY_WIDTH, DISPLAY_HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    # Top Row: "current index / total" at the top right
    index_text = f"{current_index+1}/{len(sound_files)}"
    draw.text((DISPLAY_WIDTH - len(index_text) * 6, 0), index_text, font=font, fill=255)

    # Start at index - 1 (to show the previous sound above the selected one)
    start_index = max(0, current_index - 1)
    end_index = min(start_index + ROWS_VISIBLE, len(sound_files))

    for i in range(start_index, end_index):
        y = (i - start_index + 1) * 16  # Move text down for rows
        text = sound_files[i][:20]  # Trim long filenames

        if i == current_index:  # Highlighted sound
            draw.rectangle((0, y, DISPLAY_WIDTH, y + 15), outline=1, fill=1)
            draw.text((5, y + 3), text, font=font, fill=0)  # Inverted text
        else:
            draw.text((5, y + 3), text, font=font, fill=255)

    display.image(image)
    display.show()

update_display()

# --- Play Sound ---
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# --- Stop Sound ---
def stop_sound(channel):
    pygame.mixer.music.stop()

# --- Handle Macro Buttons ---
def macro_button_pressed(channel):
    global setting_macro
    macro_index = macro_buttons.index(channel) + 1  # Get macro number (1-6)

    if setting_macro:
        # Assign current sound to macro
        if sound_files:
            macros[str(macro_index)] = sound_files[current_index]
            save_macros()
            print(f"Assigned {sound_files[current_index]} to Macro {macro_index}")
        setting_macro = False  # Exit macro setting mode
    else:
        # Play assigned sound if it exists
        if str(macro_index) in macros:
            play_sound(os.path.join(SOUND_FOLDER, macros[str(macro_index)]))
            print(f"Playing Macro {macro_index}: {macros[str(macro_index)]}")

# --- Set Button Handler ---
def set_macro(channel):
    global setting_macro
    setting_macro = True  # Enter macro setting mode
    print("Press a macro button to assign current sound")

# --- Handle Rotary Encoder ---
last_encoder_value = GPIO.input(encoder_clk)

def scroll_sounds():
    global current_index, last_encoder_value
    clk_state = GPIO.input(encoder_clk)
    dt_state = GPIO.input(encoder_dt)

    if clk_state != last_encoder_value:  # Detect rotation
        if dt_state != clk_state:
            current_index = (current_index + 1) % len(sound_files)
        else:
            current_index = (current_index - 1) % len(sound_files)

        update_display()
    last_encoder_value = clk_state

def play_selected_sound(channel):
    if sound_files:
        play_sound(os.path.join(SOUND_FOLDER, sound_files[current_index]))

# --- Attach Event Listeners ---
GPIO.add_event_detect(encoder_sw, GPIO.FALLING, callback=play_selected_sound, bouncetime=200)
GPIO.add_event_detect(stop_button, GPIO.FALLING, callback=stop_sound, bouncetime=200)
GPIO.add_event_detect(set_button, GPIO.FALLING, callback=set_macro, bouncetime=200)

for btn in macro_buttons:
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=macro_button_pressed, bouncetime=200)

# --- Main Loop ---
try:
    while True:
        scroll_sounds()
        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    pygame.mixer.quit()
