import os
import pygame
import RPi.GPIO as GPIO
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from adafruit_ssd1306 import SSD1306_I2C
import board
import busio
from PIL import Image, ImageDraw, ImageFont

# Configuration
SOUND_FOLDER = "./sounds"
MACRO_BUTTONS = {5: None, 6: None, 13: None, 19: None, 26: None, 21: None}
SET_BUTTON = 20
STOP_BUTTON = 23
ENCODER_CLK = 17
ENCODER_DT = 27
ENCODER_SW = 22

# Initialize pygame for sound
pygame.mixer.init()

# Initialize I2C display
i2c = busio.I2C(board.SCL, board.SDA)
display = SSD1306_I2C(128, 64, i2c)
font = ImageFont.load_default()

def list_sounds():
    return sorted([f for f in os.listdir(SOUND_FOLDER) if f.lower().endswith(('mp3', 'wav', 'ogg'))])

SOUNDS = list_sounds()
current_index = 0
assign_mode = False

def play_sound(filename):
    global current_index
    file_path = os.path.join(SOUND_FOLDER, filename)
    if filename.lower().endswith(".mp3"):
        sound = AudioSegment.from_mp3(file_path)
    elif filename.lower().endswith(".wav"):
        sound = AudioSegment.from_wav(file_path)
    elif filename.lower().endswith(".ogg"):
        sound = AudioSegment.from_ogg(file_path)
    else:
        return
    play(sound)

def stop_sound():
    pygame.mixer.stop()

def update_display():
    global current_index
    display.fill(0)
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), f"{current_index+1}/{len(SOUNDS)}", font=font, fill=255)
    for i in range(3):
        idx = current_index + i
        if idx < len(SOUNDS):
            draw.text((0, 10 + i*20), SOUNDS[idx][:16], font=font, fill=255)
    display.image(image)
    display.show()

def encoder_rotated(channel):
    global current_index
    if GPIO.input(ENCODER_DT):
        current_index = (current_index + 1) % len(SOUNDS)
    else:
        current_index = (current_index - 1) % len(SOUNDS)
    update_display()

def encoder_pressed(channel):
    play_sound(SOUNDS[current_index])

def macro_pressed(channel):
    global assign_mode
    if assign_mode:
        MACRO_BUTTONS[channel] = SOUNDS[current_index]
        assign_mode = False
    elif MACRO_BUTTONS[channel]:
        play_sound(MACRO_BUTTONS[channel])

def set_button_pressed(channel):
    global assign_mode
    assign_mode = True

def stop_button_pressed(channel):
    stop_sound()

# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in MACRO_BUTTONS.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=macro_pressed, bouncetime=300)
GPIO.setup(SET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SET_BUTTON, GPIO.FALLING, callback=set_button_pressed, bouncetime=300)
GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(STOP_BUTTON, GPIO.FALLING, callback=stop_button_pressed, bouncetime=300)
GPIO.setup(ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(ENCODER_CLK, GPIO.FALLING, callback=encoder_rotated, bouncetime=50)
GPIO.add_event_detect(ENCODER_SW, GPIO.FALLING, callback=encoder_pressed, bouncetime=300)

update_display()

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
